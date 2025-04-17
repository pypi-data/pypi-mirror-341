from abc import abstractmethod
from collections.abc import Sequence
from typing import Optional

import torch
from transformers import BatchEncoding

from lm_pub_quiz.evaluators.model_util import ModelMixin
from lm_pub_quiz.evaluators.util import iter_batches
from lm_pub_quiz.types import ScoringMask


class PLLScoringBaseMixin(ModelMixin):
    """This class is used retrieve PLL scores for tokens or the complete statement."""

    def default_scoring_mask(self, batched_statements: BatchEncoding) -> Sequence[ScoringMask]:
        return [(~mask.bool()).tolist() for mask in batched_statements["special_tokens_mask"]]

    @abstractmethod
    def score_statements(
        self,
        batched_statements: BatchEncoding,
        *,
        scoring_masks: Optional[Sequence[ScoringMask]],
        batch_size: int = 1,
    ) -> list[list[float]]:
        """Compute the PLL score for the tokens (determined by the scoring mask) in a statements.

        This function must be implemented by child-classes for each model-type.
        """


class MaskedLMScoringMixin(PLLScoringBaseMixin):
    def __init__(self, *, pll_metric: str = "within_word_l2r", **kw) -> None:
        if pll_metric not in ("original", "within_word_l2r"):
            msg = f"PLL strategy {pll_metric} not know."
            raise ValueError(msg)

        super().__init__(**kw)
        self.pll_metric = pll_metric

    @property
    def mask_token(self) -> int:
        """Return the mask token id used by the tokenizer."""
        token_id = self.tokenizer.convert_tokens_to_ids(self.tokenizer.mask_token)
        assert isinstance(token_id, int)
        return token_id

    def score_statements(
        self,
        batched_statements: BatchEncoding,
        *,
        scoring_masks: Optional[Sequence[ScoringMask]] = None,
        batch_size: int = 1,
    ) -> list[list[float]]:
        if scoring_masks is None:
            # If no scoring mask is given, all non-special tokens are scored
            scoring_masks = self.default_scoring_mask(batched_statements)

        extended_batch = self.create_masked_batch(batched_statements, scoring_masks)

        token_scores: list[list[float]] = [[] for _ in range(batched_statements["input_ids"].size(0))]

        # Split up the larger batch based on the batch size
        for minibatch in iter_batches(extended_batch.to(self.device), batch_size=batch_size):
            minibatch.to(self.device)

            masked_indices = minibatch.pop("masked_indices")
            statement_indices = minibatch.pop("statement_index")
            batch_labels = minibatch.pop("labels")

            # Forward the batches through the model
            with torch.no_grad():
                minibatch.pop("special_tokens_mask")
                minibatch.pop("length")
                model_output = self.model(**minibatch)

            # Shift so that tokens < n predict n
            batch_logits = model_output.logits
            batch_logits = batch_logits[torch.arange(batch_logits.size(0)), masked_indices].contiguous()

            batch_preds = torch.nn.functional.log_softmax(batch_logits, -1)
            batch_scores = batch_preds[torch.arange(batch_labels.size(0)), batch_labels].to("cpu")

            # Retrieve the score for each of the tokens
            for statement_index, score in zip(statement_indices, batch_scores):
                token_scores[statement_index].append(score.item())

        return token_scores

    def mask_to_indices(self, scoring_masks: Sequence[ScoringMask]) -> list[torch.Tensor]:
        """Transform the scoring mask to a list of indices."""
        mask_indices = []
        # Replace the relevant tokens by the pad token
        for mask in scoring_masks:
            (indices,) = torch.where(torch.tensor(mask))
            mask_indices.append(indices.to(self.device))

        return mask_indices

    def create_masked_batch(self, batch: BatchEncoding, scoring_masks: Sequence[ScoringMask]) -> BatchEncoding:
        """Extend the existing batch and mask the relevant tokens based on the scoring mask."""
        mask_indices = self.mask_to_indices(scoring_masks)

        extended_batch = {
            k: torch.repeat_interleave(v, torch.tensor([i.size(0) for i in mask_indices], device=v.device), dim=0)
            for k, v in batch.items()
        }

        # Prepare tensors holding relevant information
        extended_batch["labels"] = torch.full(
            (extended_batch["input_ids"].size(0),), -1, dtype=torch.long, device=self.device
        )
        extended_batch["masked_indices"] = torch.full(
            (extended_batch["input_ids"].size(0),), -1, dtype=torch.long, device=self.device
        )
        extended_batch["statement_index"] = torch.full(
            (extended_batch["input_ids"].size(0),), -1, dtype=torch.long, device=self.device
        )

        ### Apply the masking strategy ###
        statement_offset = 0  # to keep track which element in large batch to modify

        for statemet_index, token_indices in enumerate(mask_indices):
            # Number of passes induced by this statement
            n = token_indices.size(0)

            # Passes within the extended_batch which belong to the current statement
            extended_batch_indices = torch.arange(statement_offset, statement_offset + n, device=self.device)

            extended_batch["labels"][extended_batch_indices] = extended_batch["input_ids"][
                extended_batch_indices, token_indices
            ]
            extended_batch["masked_indices"][extended_batch_indices] = token_indices

            # Store the statement index for each token such that it can later be assigned more easily
            extended_batch["statement_index"][extended_batch_indices] = statemet_index

            # Mask tokens based on the selected masking-strategy
            if self.pll_metric == "original":
                # Mask each token individually
                extended_batch["input_ids"][extended_batch_indices, token_indices] = self.mask_token

            elif self.pll_metric == "within_word_l2r":
                word_ids = batch.word_ids(statemet_index)

                # Mask each token and the remaineder of the same word
                for i, token_index in enumerate(token_indices):
                    current_word = word_ids[int(token_index.item())]

                    extended_batch["input_ids"][statement_offset + i, token_index] = self.mask_token

                    if current_word is None:
                        continue

                    # Go over all other tokens which are masked
                    for token_to_the_right in token_indices[i + 1 :]:
                        # and mask them if they are part of the same word
                        if word_ids[token_to_the_right] == current_word:
                            extended_batch["input_ids"][statement_offset + i, token_to_the_right] = self.mask_token
                        else:
                            # Assuming a word cannot be nested in another, different word means that all remaining
                            # tokens belong to other words as well
                            break

            else:
                msg = f"PLL strategy {self.pll_metric} not implemented."
                raise NotImplementedError(msg)

            statement_offset += n

        return BatchEncoding(extended_batch)


class CausalLMScoringMixin(PLLScoringBaseMixin):
    def score_statements(
        self,
        batched_statements: BatchEncoding,
        *,
        scoring_masks: Optional[Sequence[ScoringMask]] = None,
        batch_size: int = 1,
    ) -> list[list[float]]:
        scores: list[list[float]] = []

        if scoring_masks is None:
            # If no scoring mask is given, all non-special tokens are scored
            scoring_masks = self.default_scoring_mask(batched_statements)

        for minibatch, masks in zip(
            iter_batches(batched_statements.to(self.device), batch_size=batch_size),  # Iter through the batches
            iter_batches(scoring_masks, batch_size=batch_size),  # and masks at the same time
        ):
            # Forward the batch through the model
            with torch.no_grad():
                minibatch.pop("special_tokens_mask")
                minibatch.pop("length")
                model_output = self.model(**minibatch)

            # Shift so that tokens < n predict n
            batch_logits = model_output.logits[:, :-1]
            batch_labels = minibatch["input_ids"][:, 1:]

            for i, mask in enumerate(masks):
                if mask is None:
                    logits = batch_logits[i, :].contiguous()
                    labels = batch_labels[i, :].contiguous()
                else:
                    logits = batch_logits[i, mask[1:]].contiguous()
                    labels = batch_labels[i, mask[1:]].contiguous()

                preds = torch.nn.functional.log_softmax(logits, -1)

                scores.append(preds[torch.arange(labels.size(0)), labels].to("cpu").tolist())

        return scores

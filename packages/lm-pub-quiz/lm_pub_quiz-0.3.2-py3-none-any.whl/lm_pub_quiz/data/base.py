import json
import logging
import os
import re
import warnings
from abc import ABC, abstractmethod
from collections import defaultdict
from collections.abc import Iterable, Iterator, Mapping, Sequence
from pathlib import Path
from typing import (
    Any,
    Generic,
    Optional,
    TypeVar,
    Union,
    cast,
    overload,
)

import pandas as pd
from typing_extensions import Self

from lm_pub_quiz.types import PathLike

log = logging.getLogger(__name__)


class NoInstanceTableError(Exception):
    pass


InstanceTableFileFormat = Optional[Union[str, tuple[str, ...]]]


class DataBase(ABC):
    """Base class for the representation of relations, relations results, and dataset collections."""

    @classmethod
    @abstractmethod
    def from_path(cls, path: PathLike, *, lazy: bool = True, fmt: InstanceTableFileFormat = None) -> "DataBase":
        """Load data from the given path.

        If `lazy`, only the metadata is loaded and the instances are loaded once they are accessed.
        """
        pass

    @abstractmethod
    def save(self, path: PathLike, fmt: InstanceTableFileFormat = None) -> Optional[Path]:
        """Save the data under the given path."""
        pass

    @property
    @abstractmethod
    def is_lazy(self) -> bool:
        """Return true if lazy loading is active."""
        pass

    @abstractmethod
    def activated(self) -> Self:
        """Return self if lazy loading is active, otherwise return a copy without lazy loading."""
        pass


class RelationBase(DataBase):
    """Base class for the representation of relations and relations results."""

    _instance_table_file_name_suffix: str = ""
    _instance_table_default_format: str = "jsonl"
    _metadata_file_name: str = "metadata_relations.json"

    _supported_instance_table_file_formats: tuple[InstanceTableFileFormat, ...] = ("jsonl", ("parquet", "*"))

    _len: Optional[int] = None

    def __init__(
        self,
        relation_code: str,
        *,
        lazy_options: Optional[dict[str, Any]] = None,
        instance_table: Optional[pd.DataFrame] = None,
        answer_space: Optional[pd.Series] = None,
        relation_info: Optional[dict[str, Any]] = None,
    ):
        self._relation_code = relation_code
        self._lazy_options = lazy_options
        self._instance_table = instance_table
        self._answer_space = answer_space
        self._relation_info = relation_info or {}

    @property
    def relation_code(self) -> str:
        """The identifier of the relation."""
        return self._relation_code

    def copy(self, **kw):
        """Create a copy of the isntance with specified fields replaced by new values."""

        kw = {
            "relation_code": self.relation_code,
            "lazy_options": self._lazy_options.copy() if self._lazy_options is not None else None,
            "instance_table": self._instance_table.copy() if self._instance_table is not None else None,
            "answer_space": self._answer_space.copy() if self._answer_space is not None else None,
            "relation_info": self._relation_info.copy(),
            **kw,
        }
        return self.__class__(kw.pop("relation_code"), **kw)

    def saved(self, path: PathLike, *, fmt: InstanceTableFileFormat = None) -> Self:
        # Save relation and return the lazy-loading relation
        saved_path = self.save(path, fmt=fmt)

        if path is not None:
            lazy_options = {
                "path": saved_path,
                "fmt": fmt,
            }
        else:
            lazy_options = None

        return self.copy(instance_table=None, lazy_options=lazy_options)

    def activated(self) -> Self:
        """Return self or a copy of self with the instance_table loaded (lazy loading disabled)."""

        if not self.is_lazy:
            return self

        return self.copy(instance_table=self.instance_table)

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"{self.__class__.__name__} `{self.relation_code}`"

    def _derive_cardinality(self, instance_table: pd.DataFrame) -> str:
        if instance_table.duplicated("obj_id").any():
            return "multiple instances per answer"
        else:
            return "single instance per answer"

    @overload
    def relation_info(self, /, **kw) -> dict[str, Any]: ...

    @overload
    def relation_info(self, key: str, /) -> Any: ...

    def relation_info(self, key: Optional[str] = None, /, **kw) -> Union[None, Any, dict[str, Any]]:
        """Get or set additional relation information.

        Use `relation.relation_info(<field name>=<new value>)` to set fields in the relation info dictionary.
        If a single field is selected, the respective value is returned. Otherwise the complete dictionary is
        returned.

        Parameters:
            key: The field to retrieve.
            **kw: The fields not modify.

        Returns:
            If a field is selected, the respective value is returned, otherwise, the complete info dictionary is
            returned.
        """
        if key is not None:
            if key == "cardinality" and "cardinality" not in self._relation_info:
                return self._derive_cardinality(self.instance_table)
            else:
                return self._relation_info[key]
        elif len(kw) > 0:
            self._relation_info.update(kw)

        info = self._relation_info.copy()
        if "cardinality" not in info:
            info["cardinality"] = self._derive_cardinality(self.instance_table)
        return info

    @overload
    def get_metadata(self) -> dict[str, Any]: ...

    @overload
    def get_metadata(self, key: str, /) -> Any: ...

    def get_metadata(self, key: Optional[str] = None) -> Union[Any, dict[str, Any]]:
        """Get or set metadata.

        Parameters:
            key: The metadata to retrieve. If not field is specified, the complete dictionary is returned.

        Returns:
            Either the selected field or the complete dictionary.
        """
        if key is not None:
            if self._answer_space is None:
                msg = f"Key '{key}' not in metadata (no answer space in metadata)."
                raise KeyError(msg)
            elif key == "answer_space_labels":
                return self.answer_space.tolist()
            elif key == "answer_space_ids":
                return self.answer_space.index.tolist()
            elif key == "relation_info":
                return self.relation_info()
            else:
                msg = f"Key '{key}' not in metadata."
                raise KeyError(msg)

        elif self._answer_space is not None:
            return {k: self.get_metadata(k) for k in ("answer_space_labels", "answer_space_ids", "relation_info")}
        else:
            return {}

    @staticmethod
    def _generate_obj_ids(n: int, *, id_prefix: str = ""):
        return id_prefix + pd.RangeIndex(n, name="obj_id").astype(str)

    @classmethod
    def answer_space_from_instance_table(cls, instance_table: pd.DataFrame, **kw) -> pd.Series:
        if "obj_label" not in instance_table:
            msg = "Cannot generate answer space: No object information in instance table."
            raise ValueError(msg)

        if "obj_id" in instance_table:
            answer_groups = instance_table.groupby("obj_id", sort=False).obj_label
            unique_ids = answer_groups.nunique().eq(1)

            if not unique_ids.all():
                ids = ", ".join(f"'{v}'" for v in unique_ids[~unique_ids].index)
                log.warning("Some object IDs contain multiple labels: %s", ids)

            return answer_groups.first()

        else:
            answer_labels = instance_table["obj_label"].unique()
            return pd.Series(answer_labels, index=cls._generate_obj_ids(len(answer_labels), **kw), name="obj_label")

    @classmethod
    def answer_space_from_metadata(cls, metadata, **kw) -> Optional[pd.Series]:
        if "answer_space_labels" in metadata and "answer_space_ids" in metadata:
            if "answer_space_labels" in metadata:
                answer_space_labels = metadata.pop("answer_space_labels")
            else:
                answer_space_labels = metadata.pop("answer_space")

            answer_space_ids = metadata.pop("answer_space_ids", None)

            if answer_space_ids is None:
                answer_space_ids = cls._generate_obj_ids(len(answer_space_labels), **kw)

            index = pd.Index(answer_space_ids, name="obj_id")

            answer_space = pd.Series(answer_space_labels, index=index, name="obj_label")

            return answer_space
        elif (
            "answer_space_labels" not in metadata
            and "answer_space_ids" not in metadata
            and "answer_space" not in metadata
        ):
            return None
        else:
            warnings.warn(
                "To define an answer space in the medata data, specify `answer_space_ids` and "
                "`answer_space_labels` (using answer space base on the instance table).",
                stacklevel=1,
            )
            return None

    @property
    def answer_space(self) -> pd.Series:
        """The answer space of the relation."""
        if self._answer_space is None:
            # invoke file loading to get answer space
            _ = self.instance_table

        return cast(pd.Series, self._answer_space)

    @property
    def instance_table(self) -> pd.DataFrame:
        """A `pandas.DataFrame` containing all items in the relation."""
        if self._instance_table is None:
            if self._lazy_options is None:
                msg = (
                    f"Could not load instance table for {self.__class__.__name__} "
                    f"({self.relation_code}): No path given."
                )
                raise NoInstanceTableError(msg)

            instance_table = self.load_instance_table(answer_space=self._answer_space, **self._lazy_options)
            self.relation_info(cardinality=self._derive_cardinality(instance_table))

            if self._answer_space is None:
                # store answer_space
                self._answer_space = self.answer_space_from_instance_table(
                    instance_table, id_prefix=f"{self.relation_code}-"
                )

            # store number of instances
            self._len = len(instance_table)

            return instance_table

        return self._instance_table

    def __len__(self) -> int:
        if self._instance_table is None:
            if self._len is None:
                # invoke file loading to get answer space
                _ = self.instance_table
            return cast(int, self._len)
        else:
            return len(self.instance_table)

    @abstractmethod
    def filter_subset(self, indices: Sequence[int], *, keep_answer_space: bool = False) -> Self:
        pass

    @classmethod
    def load_instance_table(
        cls,
        path: Path,
        *,
        answer_space: Optional[pd.Series] = None,  # noqa: ARG003
        fmt: InstanceTableFileFormat = None,
    ) -> pd.DataFrame:
        if not path.exists():
            msg = f"Could not load instance table for {cls.__name__}: Path `{path}` could not be found."
            raise FileNotFoundError(msg)
        elif not path.is_file():
            msg = f"Could not load instance table for {cls.__name__}: `{path}` is not a file."
            raise RuntimeError(msg)

        if fmt is None:
            fmt = tuple(s[1:] for s in path.suffixes)
        elif isinstance(fmt, str):
            fmt = tuple(fmt.split("."))

        log.debug("Loading instance table (format=.%s) from: %s", ".".join(fmt), path)

        if fmt == ("jsonl",):
            instance_table = pd.read_json(path, lines=True)

        elif fmt[0] == "parquet" and len(fmt) <= 2:  # noqa: PLR2004
            instance_table = pd.read_parquet(path)

        else:
            msg = f"Format .{'.'.join(fmt)} not recognized: Could not load instances at {path}."
            raise ValueError(msg)

        if instance_table.index.name is None:
            instance_table.index.name = "instance"

        return instance_table

    @classmethod
    def save_instance_table(cls, instance_table: pd.DataFrame, path: Path, fmt: InstanceTableFileFormat = None):
        """Save instance table with the format determined by the path suffix.

        Parameters:
           instance_table (pd.DataFrame): The instances to save.
           path (Path): Where to save the instance table. If format is not specified, the suffix is used to determined
                        the format.
           fmt (str): Which to save the instances in.
        """
        if fmt is None:
            fmt = tuple(s[1:] for s in path.suffixes)
        elif isinstance(fmt, str):
            fmt = tuple(fmt.split("."))

        if fmt == ("jsonl",):
            instance_table.to_json(path, orient="records", lines=True)

        elif 0 < len(fmt) <= 2 and fmt[0] == "parquet":  # noqa: PLR2004
            compression: Optional[str]

            if len(fmt) == 1:
                compression = None
            else:
                compression = fmt[1]

            instance_table.to_parquet(path, compression=compression)
        else:
            msg = f"Format .{'.'.join(fmt)} not recognized: Could not save instances at {path}."
            raise ValueError(msg)

    @property
    def is_lazy(self) -> bool:
        return self._instance_table is None and self._lazy_options is not None

    @property
    @abstractmethod
    def has_instance_table(self) -> bool:
        pass

    def save(self, path: PathLike, fmt: InstanceTableFileFormat = None) -> Optional[Path]:
        """Save results to a file and export meta_data"""
        save_path = Path(path)
        save_path.mkdir(parents=True, exist_ok=True)

        log.debug("Saving %s result to: %s", self, save_path)

        ### Metadata file -> .json ###
        if save_path.is_dir():
            metadata_path = save_path / self._metadata_file_name
        else:
            metadata_path = save_path
            save_path = save_path.parent

        if metadata_path.exists():
            with open(metadata_path) as file:
                all_metadata = json.load(file)

                if self.relation_code in all_metadata:
                    log.warning("Overwriting metadata info for relation %s (%s)", self.relation_code, save_path)
        else:
            all_metadata = {}

        ### Store instance table to .jsonl file ###
        if self.has_instance_table:
            instances_path = self.path_for_code(save_path, self.relation_code, fmt=fmt)
            self.save_instance_table(self.instance_table, instances_path, fmt=fmt)
            log.debug("Instance table was saved to: %s", instances_path)

        else:
            instances_path = None

        all_metadata[self.relation_code] = self.get_metadata()

        with open(metadata_path, "w") as file:
            json.dump(all_metadata, file, indent=4, default=str)
            log.debug("Metadata file was saved to: %s", metadata_path)

        return instances_path

    @staticmethod
    def true_stem(path: Path) -> str:
        return path.name.partition(".")[0]

    @classmethod
    def code_from_path(cls, path: Path) -> str:
        if not path.name.endswith(cls._instance_table_file_name_suffix):
            msg = (
                f"Incorrect path for {cls.__name__} instance table "
                f"(expected suffix {cls._instance_table_file_name_suffix}): {path}"
            )
            raise ValueError(msg)
        code = cls.true_stem(path)
        if len(cls._instance_table_file_name_suffix) > 0:
            code = code[: -len(cls._instance_table_file_name_suffix)]
        return code

    @classmethod
    def suffix_from_instance_table_file_format(cls, fmt: InstanceTableFileFormat = None) -> str:
        if fmt is None:
            return cls._instance_table_default_format
        elif isinstance(fmt, str):
            return fmt
        else:
            return ".".join(fmt)

    @classmethod
    def path_for_code(cls, path: Path, relation_code: str, *, fmt: InstanceTableFileFormat = None) -> Path:
        return (
            path
            / f"{relation_code}{cls._instance_table_file_name_suffix}.{cls.suffix_from_instance_table_file_format(fmt)}"
        )

    @overload
    @classmethod
    def search_path(cls, path: Path, relation_code: None = None, fmt: InstanceTableFileFormat = None) -> list[Path]: ...

    @overload
    @classmethod
    def search_path(cls, path: Path, relation_code: str, fmt: InstanceTableFileFormat = None) -> Path: ...

    @classmethod
    def search_path(
        cls, path: Path, relation_code: Optional[str] = None, fmt: InstanceTableFileFormat = None
    ) -> Union[list[Path], Path, None]:
        """Search path for instance files."""

        if relation_code is not None and fmt is not None:
            # Just look for the file
            p = cls.path_for_code(path, relation_code, fmt=fmt)
            if p.exists():
                return p
            else:
                return None

        if relation_code is None:
            code = ".*"
        else:
            code = re.escape(relation_code)

        if fmt is None:
            suffix = "|".join(
                f"({cls.suffix_from_instance_table_file_format(f)})" for f in cls._supported_instance_table_file_formats
            )
        else:
            suffix = cls.suffix_from_instance_table_file_format(fmt)

        pattern = re.compile(f"(?P<relation_code>{code}){cls._instance_table_file_name_suffix}.(?P<suffix>{suffix})")

        matches: dict[str, list[Path]] = defaultdict(list)
        for p in map(Path, os.scandir(path)):
            if p.name == cls._metadata_file_name:
                continue

            match = re.fullmatch(pattern, p.name)

            if match is not None:
                matches[match.group("relation_code")].append(p)

        selected_paths = []
        for code, matching_paths in matches.items():
            if len(matching_paths) > 1:
                log.warning("Found multiple files for relation %: %s", code, ", ".join(p.name for p in matching_paths))
            selected_paths.append(matching_paths[0])

        if relation_code is None:
            return selected_paths
        elif len(selected_paths) == 0:
            return None
        else:
            return selected_paths[0]


RT = TypeVar("RT", bound=RelationBase)


class DatasetBase(DataBase, Generic[RT]):
    """Base class for a collection of relations or relations results."""

    relation_data: list[RT]

    def __len__(self) -> int:
        return len(self.relation_data)

    def __str__(self) -> str:
        relations = ", ".join(self.relation_codes)
        return f"{self.__class__.__name__}({relations})"

    def __repr__(self) -> str:
        return str(self)

    def __getitem__(self, key: Union[int, str]) -> RT:
        if isinstance(key, int):
            return self.relation_data[key]
        else:
            for relation in self:
                if relation.relation_code == key:
                    return relation

            # no match
            msg = f"Relation {key} not found in this {self.__class__.__name__}."
            raise KeyError(msg)

    def __contains__(self, key: str) -> bool:
        for relation in self:
            if relation.relation_code == key:
                return True
        return False

    def __iter__(self) -> Iterator[RT]:
        yield from self.relation_data

    @abstractmethod
    def filter_subset(
        self,
        indices: Mapping[str, Sequence[int]],
        *,
        save_path: Optional[PathLike] = None,
        keep_answer_space: bool = False,
        dataset_name: Optional[str] = None,
    ) -> Self:
        pass

    @property
    def relation_codes(self) -> Iterable[str]:
        return (r.relation_code for r in self)

    @property
    def is_lazy(self) -> bool:
        return any(rel.is_lazy for rel in self)

    def save(self, path: PathLike, fmt: InstanceTableFileFormat = None) -> None:
        for result in self:
            result.save(path, fmt=fmt)

    def joined_instance_table(self) -> pd.DataFrame:
        return pd.concat({relation.relation_code: relation.instance_table for relation in self}, names=["relation"])

    def update_relation_info(self, info: dict[str, dict[str, Any]]):
        for rel in self:
            if rel.relation_code in info:
                rel.relation_info(**info[rel.relation_code])

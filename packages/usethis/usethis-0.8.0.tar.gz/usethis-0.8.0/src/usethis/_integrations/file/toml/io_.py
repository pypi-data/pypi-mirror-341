from __future__ import annotations

import contextlib
import copy
from typing import TYPE_CHECKING, Any

import mergedeep
import tomlkit.api
import tomlkit.items
from pydantic import TypeAdapter
from tomlkit import TOMLDocument
from tomlkit.exceptions import TOMLKitError

from usethis._integrations.file.toml.errors import (
    TOMLDecodeError,
    TOMLNotFoundError,
    TOMLValueAlreadySetError,
    TOMLValueMissingError,
    UnexpectedTOMLIOError,
    UnexpectedTOMLOpenError,
)
from usethis._io import (
    KeyValueFileManager,
    UnexpectedFileIOError,
    UnexpectedFileOpenError,
)

if TYPE_CHECKING:
    from pathlib import Path
    from typing import ClassVar

    from typing_extensions import Self


class TOMLFileManager(KeyValueFileManager):
    """An abstract class for managing TOML files."""

    _content_by_path: ClassVar[dict[Path, TOMLDocument | None]] = {}

    def __enter__(self) -> Self:
        try:
            return super().__enter__()
        except UnexpectedFileOpenError as err:
            raise UnexpectedTOMLOpenError(err) from None

    def read_file(self) -> None:
        try:
            super().read_file()
        except FileNotFoundError as err:
            raise TOMLNotFoundError(err) from None
        except UnexpectedFileIOError as err:
            raise UnexpectedTOMLIOError(err) from None
        except TOMLKitError as err:
            msg = f"Failed to decode '{self.name}': {err}"
            raise TOMLDecodeError(msg) from None

    def _dump_content(self) -> str:
        if self._content is None:
            msg = "Content is None, cannot dump."
            raise ValueError(msg)

        return tomlkit.api.dumps(self._content)

    def _parse_content(self, content: str) -> TOMLDocument:
        return tomlkit.api.parse(content)

    def get(self) -> TOMLDocument:
        return super().get()

    def commit(self, document: TOMLDocument) -> None:
        return super().commit(document)

    @property
    def _content(self) -> TOMLDocument | None:
        return super()._content

    @_content.setter
    def _content(self, value: TOMLDocument | None) -> None:
        self._content_by_path[self.path] = value

    def _validate_lock(self) -> None:
        try:
            super()._validate_lock()
        except UnexpectedFileIOError as err:
            raise UnexpectedTOMLIOError(err) from None

    def __contains__(self, keys: list[str]) -> bool:
        """Check if the TOML file contains a value.

        An non-existent file will return False.
        """
        try:
            try:
                container = self.get()
            except FileNotFoundError:
                return False
            for key in keys:
                TypeAdapter(dict).validate_python(container)
                assert isinstance(container, dict)
                container = container[key]
        except KeyError:
            return False

        return True

    def __getitem__(self, item: list[str]) -> Any:
        keys = item

        d = self.get()
        for key in keys:
            TypeAdapter(dict).validate_python(d)
            assert isinstance(d, dict)
            d = d[key]

        return d

    def set_value(
        self, *, keys: list[str], value: Any, exists_ok: bool = False
    ) -> None:
        """Set a value in the TOML file.

        An empty list of keys corresponds to the root of the document.
        """
        toml_document = copy.copy(self.get())

        if not keys:
            # Root level config - value must be a mapping.
            TypeAdapter(dict).validate_python(toml_document)
            assert isinstance(toml_document, dict)
            TypeAdapter(dict).validate_python(value)
            assert isinstance(value, dict)
            if not toml_document or exists_ok:
                toml_document.update(value)
                self.commit(toml_document)
                return

        d, parent = toml_document, {}
        shared_keys = []
        try:
            # Index our way into each ID key.
            # Eventually, we should land at a final dict, which is the one we are setting.
            for key in keys:
                TypeAdapter(dict).validate_python(d)
                assert isinstance(d, dict)
                d, parent = d[key], d
                shared_keys.append(key)
        except KeyError:
            # The old configuration should be kept for all ID keys except the
            # final/deepest one which shouldn't exist anyway since we checked as much,
            # above. For example, if there is [tool.ruff] then we shouldn't overwrite it
            # with [tool.deptry]; they should coexist. So under the "tool" key, we need
            # to "merge" the two dicts.

            if len(keys) <= 3:
                contents = value
                for key in reversed(keys):
                    contents = {key: contents}
                toml_document = mergedeep.merge(toml_document, contents)  # type: ignore[reportAssignmentType]
                assert isinstance(toml_document, TOMLDocument)
            else:
                # Note that this alternative logic is just to avoid a bug:
                # https://github.com/nathanjmcdougall/usethis-python/issues/507
                TypeAdapter(dict).validate_python(d)
                assert isinstance(d, dict)

                unshared_keys = keys[len(shared_keys) :]

                d[_get_unified_key(unshared_keys)] = value
        else:
            if not exists_ok:
                # The configuration is already present, which is not allowed.
                if keys:
                    msg = f"Configuration value '{'.'.join(keys)}' is already set."
                else:
                    msg = "Configuration value at root level is already set."
                raise TOMLValueAlreadySetError(msg)
            else:
                # The configuration is already present, but we're allowed to overwrite it.
                TypeAdapter(dict).validate_python(parent)
                assert isinstance(parent, dict)
                parent[keys[-1]] = value

        self.commit(toml_document)

    def __delitem__(self, keys: list[str]) -> None:
        """Delete a value in the TOML file.

        An empty list of keys corresponds to the root of the document.

        Trying to delete a key from a document that doesn't exist will pass silently.
        """
        try:
            toml_document = copy.copy(self.get())
        except FileNotFoundError:
            return

        # Exit early if the configuration is not present.
        try:
            d = toml_document
            for key in keys:
                TypeAdapter(dict).validate_python(d)
                assert isinstance(d, dict)
                d = d[key]
        except KeyError:
            # N.B. by convention a del call should raise an error if the key is not found.
            msg = f"Configuration value '{'.'.join(keys)}' is missing."
            raise TOMLValueMissingError(msg) from None

        # Remove the configuration.
        d = toml_document
        for key in keys[:-1]:
            TypeAdapter(dict).validate_python(d)
            assert isinstance(d, dict)
            d = d[key]
        assert isinstance(d, dict)
        if not keys:
            # i.e. the case where we're deleting the root of the document.
            for key in list(d.keys()):
                del d[key]
        else:
            with contextlib.suppress(KeyError):
                # There is a strange behaviour (bug?) in tomlkit where deleting a key
                # has two separate lines:
                # self._value.remove(key)  # noqa: ERA001
                # dict.__delitem__(self, key)  # noqa: ERA001
                # but it's not clear why there's this duplicate and it causes a KeyError
                # in some cases.
                d.remove(keys[-1])

            # Cleanup: any empty sections should be removed.
            for idx in range(len(keys) - 1):
                d, parent = toml_document, {}

                for key in keys[: idx + 1]:
                    d, parent = d[key], d
                    TypeAdapter(dict).validate_python(d)
                    TypeAdapter(dict).validate_python(parent)
                    assert isinstance(d, dict)
                    assert isinstance(parent, dict)
                assert isinstance(d, dict)
                if not d:
                    del parent[keys[idx]]

        self.commit(toml_document)

    def extend_list(self, *, keys: list[str], values: list[Any]) -> None:
        if not keys:
            msg = "At least one ID key must be provided."
            raise ValueError(msg)

        toml_document = copy.copy(self.get())

        try:
            d = toml_document
            for key in keys[:-1]:
                TypeAdapter(dict).validate_python(d)
                assert isinstance(d, dict)
                d = d[key]
            p_parent = d
            TypeAdapter(dict).validate_python(p_parent)
            assert isinstance(p_parent, dict)
            d = p_parent[keys[-1]]
        except KeyError:
            contents = values
            for key in reversed(keys):
                contents = {key: contents}
            assert isinstance(contents, dict)
            pyproject = mergedeep.merge(toml_document, contents)
            assert isinstance(pyproject, TOMLDocument)
        else:
            TypeAdapter(dict).validate_python(p_parent)
            TypeAdapter(list).validate_python(d)
            assert isinstance(p_parent, dict)
            assert isinstance(d, list)
            p_parent[keys[-1]] = d + values

        self.commit(toml_document)

    def remove_from_list(self, *, keys: list[str], values: list[Any]) -> None:
        if not keys:
            msg = "At least one ID key must be provided."
            raise ValueError(msg)

        toml_document = copy.copy(self.get())

        try:
            p = toml_document
            for key in keys[:-1]:
                TypeAdapter(dict).validate_python(p)
                assert isinstance(p, dict)
                p = p[key]

            p_parent = p
            TypeAdapter(dict).validate_python(p_parent)
            assert isinstance(p_parent, dict)
            p = p_parent[keys[-1]]
        except KeyError:
            # The configuration is not present - do not modify
            return

        TypeAdapter(dict).validate_python(p_parent)
        TypeAdapter(list).validate_python(p)
        assert isinstance(p_parent, dict)
        assert isinstance(p, list)

        new_values = [value for value in p if value not in values]
        p_parent[keys[-1]] = new_values

        self.commit(toml_document)


def _get_unified_key(keys: list[str]) -> tomlkit.items.Key:
    single_keys = [tomlkit.items.SingleKey(key) for key in keys]
    if len(single_keys) == 1:
        (unified_key,) = single_keys
    else:
        unified_key = tomlkit.items.DottedKey(single_keys)
    return unified_key

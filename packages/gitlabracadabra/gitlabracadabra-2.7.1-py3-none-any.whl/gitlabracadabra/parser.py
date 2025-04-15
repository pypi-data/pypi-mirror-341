#
# Copyright (C) 2013-2017 Gauvain Pocentek <gauvain@pocentek.net>
# Copyright (C) 2019-2025 Mathieu Parent <math.parent@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import annotations

import re
from typing import TYPE_CHECKING

import yaml

from gitlabracadabra.dictutils import update_dict_with_defaults

if TYPE_CHECKING:
    from io import TextIOWrapper

    from gitlabracadabra.objects.object import GitLabracadabraObject


MAX_RECURSION = 10


class GitlabracadabraParser:
    """YAML parser."""

    def __init__(self, action_file: str, config: dict, recursion: int = 0) -> None:
        self._action_file = action_file
        self._config = config
        self._objects: dict[str, GitLabracadabraObject] | None = None
        self._include = self._config.pop("include", [])
        for included in self._include:
            if recursion >= MAX_RECURSION:
                msg = f"{self._action_file}: nesting too deep in `include`"
                raise ValueError(msg)
            if isinstance(included, str):
                included = {"local": included}
            if not isinstance(included, dict):
                msg = f"{self._action_file}: invalid value for `include`: {included}"
                raise TypeError(msg)
            if list(included.keys()) == ["local"] and isinstance(included["local"], str):
                if ".." in included["local"] or included["local"][0] == "/":
                    msg = "{}: forbidden path for `include`: {}".format(self._action_file, included["local"])
                    raise ValueError(msg)
                included = self.from_yaml_file(included["local"], recursion + 1)
            else:
                msg = f"{self._action_file}: invalid value for `include`: {included}"
                raise ValueError(msg)
            update_dict_with_defaults(self._config, included._config)  # noqa: SLF001

    @classmethod
    def from_yaml(
        cls,
        action_file: str,
        yaml_blob: str | TextIOWrapper,
        recursion: int = 0,
    ) -> GitlabracadabraParser:
        config = yaml.safe_load(yaml_blob)
        return GitlabracadabraParser(action_file, config, recursion)

    @classmethod
    def from_yaml_file(cls, action_file: str, recursion: int = 0) -> GitlabracadabraParser:
        with open(action_file) as yaml_blob:
            return cls.from_yaml(action_file, yaml_blob, recursion)

    """items()

    Handle hidden objects (starting with a dot) and extends.
    """

    def _items(self):
        for k, v in sorted(self._config.items()):
            if k.startswith("."):
                continue
            recursion = 0
            while "extends" in v:
                recursion += 1
                if recursion >= MAX_RECURSION:
                    msg = f"{self._action_file} ({k}): nesting too deep in `extends`"
                    raise ValueError(msg)
                # No need to deepcopy as update_dict_with_defaults() does
                v = v.copy()
                extends = v.pop("extends")
                if isinstance(extends, str):
                    extends = [extends]
                for extends_item in reversed(extends):
                    if isinstance(extends_item, str):
                        extends_item = {extends_item: "deep"}
                    for extends_k, extends_v in extends_item.items():
                        try:
                            parent = self._config[extends_k]
                        except KeyError as exc:
                            msg = f"{self._action_file} (`{extends_k}` from `{k}`): {extends_k} not found"
                            raise ValueError(msg) from exc
                        if extends_v == "deep":
                            update_dict_with_defaults(v, parent)
                        elif extends_v == "replace":
                            result = parent.copy()
                            result.update(v)
                            v = result
                        elif extends_v == "aggregate":
                            update_dict_with_defaults(v, parent, aggregate=True)
                        else:
                            msg = (
                                f"{self._action_file} (`{extends_k}` from `{k}`): Unknown merge strategy `{extends_v}`"
                            )
                            raise ValueError(msg)
            # Drop None values from v
            yield (k, {a: b for a, b in v.items() if b is not None})

    """_type_to_classname()

    Converts object-type to GitLabracadabraObjectType.
    """

    @classmethod
    def _type_to_classname(cls, obj_type: str) -> str:
        splitted = re.split("[-_]", obj_type)
        mapped = (s[0].upper() + s[1:].lower() for s in splitted)
        return "GitLabracadabra" + "".join(mapped)

    """_type_to_module()

    Converts object-type to gitlabracadabra.objects.object_type.
    """

    @classmethod
    def _type_to_module(cls, obj_type: str) -> str:
        return "gitlabracadabra.objects." + obj_type.lower().replace("-", "_")

    """get_class_for()

    Get the class for the given object type.
    """

    @classmethod
    def get_class_for(cls, obj_type: str) -> type[GitLabracadabraObject]:
        obj_classname = cls._type_to_classname(obj_type)
        obj_module = __import__(cls._type_to_module(obj_type), globals(), locals(), [obj_classname])
        return getattr(obj_module, obj_classname)  # type: ignore

    """objects()

    Returns .
    """

    def objects(self) -> dict[str, GitLabracadabraObject]:
        if self._objects is not None:
            return self._objects
        self._objects = {}
        for k, v in self._items():  # type:ignore
            if "type" in v:
                obj_type = v["type"]
                v.pop("type")
            elif k.endswith("/"):
                obj_type = "group"
            else:
                obj_type = "project"
            if k.endswith("/"):
                k = k[:-1]
            obj_class = self.get_class_for(obj_type)
            self._objects[k] = obj_class(self._action_file, k, v)
        return self._objects

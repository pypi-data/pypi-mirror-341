#
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

import logging
from pathlib import PurePosixPath
from re import Match
from typing import TYPE_CHECKING

from gitlabracadabra.containers.registries import ReferenceParts, Registries
from gitlabracadabra.matchers import Matcher
from gitlabracadabra.objects.object import GitLabracadabraObject

if TYPE_CHECKING:
    from typing import Any

    from gitlabracadabra.containers.registry import Registry


logger = logging.getLogger(__name__)

Source = tuple[PurePosixPath, str, Match, str | None]


class ImageMirrorsMixin(GitLabracadabraObject):
    """Object (Project) with image mirrors."""

    def _process_image_mirrors(
        self,
        param_name: str,
        param_value: Any,
        *,
        dry_run: bool = False,
        skip_save: bool = False,
    ) -> None:
        """Process the image_mirrors param.

        Args:
            param_name: "image_mirrors".
            param_value: List of image mirror dicts.
            dry_run: Dry run.
            skip_save: False.
        """
        assert param_name == "image_mirrors"  # noqa: S101
        assert not skip_save  # noqa: S101

        dest_registry, prefix = self._get_destination()

        for image_mirror in param_value:
            if not image_mirror.get("enabled", True):
                continue
            self._mirror(image_mirror, dest_registry, prefix, dry_run=dry_run)

    def _get_destination(self) -> tuple[Registry, PurePosixPath]:
        # https://gitlab.com/gitlab-org/gitlab/-/merge_requests/54090
        try:
            container_registry_image_prefix = self._obj.container_registry_image_prefix
        except AttributeError:
            container_registry_image_prefix = None
        if not isinstance(container_registry_image_prefix, str):
            msg = f"Unexpected type for container_registry_image_prefix: {type(container_registry_image_prefix)}"
            raise TypeError(msg)

        netloc, path = container_registry_image_prefix.split("/", 1)
        registry = Registries().get_registry(netloc, self.connection.registry_session_callback)
        return (registry, PurePosixPath(path))

    def _mirror(
        self,
        image_mirror: dict,
        dest_registry: Registry,
        prefix: PurePosixPath,
        *,
        dry_run: bool,
    ) -> None:
        sources = self._get_sources(image_mirror.get("from"), image_mirror.get("semver"))
        for source in sources:
            dest = self._get_dest(
                source[0],
                source[1],
                source[2],
                image_mirror.get("to"),
            )
            digest_suffix = ""
            if source[3]:
                digest_suffix = f"@{source[3]}"
            source_manifest = Registries().get_manifest(f"{source[0] / source[1]!s}:{source[2][0]}{digest_suffix}")
            source_manifest.forced_digest = source[3] is not None
            dest_manifest = Registries().get_manifest(
                ReferenceParts(
                    dest_registry.hostname,
                    str(prefix / dest[0]),
                    dest[1],
                    None,
                )
            )
            dest_manifest.registry.import_manifest(
                source_manifest,
                dest_manifest.manifest_name,
                tag=dest_manifest.tag,
                platform=None,
                log_prefix=f"[{self._name}] ",
                dry_run=dry_run,
            )

    def _get_sources(self, from_param: Any, semver: str | None) -> list[Source]:
        """Get sources.

        Args:
            from_param: The "from" param.
            semver: Optional "semver" param.

        Returns:
            A list of tuples (base, repository, tag, digest)

        Raises:
            ValueError: Unexpected from param type.
        """
        default_tag = "latest"
        if semver:
            default_tag = "/.*/"
        if isinstance(from_param, str):
            parts = Registries().full_reference_parts(from_param)
            return self._get_sources_from_parts(
                PurePosixPath(parts.hostname),
                [parts.manifest_name],
                [parts.tag or default_tag],
                parts.digest,
                semver,
            )
        if isinstance(from_param, dict):
            base = PurePosixPath(from_param.get("base", ""))
            repositories = from_param.get("repositories", None)
            tags = from_param.get("tags", [default_tag])
            return self._get_sources_from_parts(base, repositories, tags, None, semver)
        msg = f"Unexpected from param type: {type(from_param)}"
        raise ValueError(msg)

    def _get_sources_from_parts(
        self,
        base: PurePosixPath,
        repositories: list[str],
        tags: list[str],
        digest: str | None,
        semver: str | None,
    ) -> list[Source]:
        if not isinstance(repositories, list):
            msg = f"Unexpected from.repositories param type: {type(repositories)}"  # type: ignore[unreachable]
            raise TypeError(msg)
        if not isinstance(tags, list):
            msg = f"Unexpected from.tags param type: {type(tags)}"  # type: ignore[unreachable]
            raise TypeError(msg)
        sources: list[Source] = []
        for repository in repositories:
            matcher = Matcher(
                tags,
                semver,
                log_prefix=f"[{self._name}] ",
            )
            manifest = Registries().get_manifest(str(base / repository))
            for match in matcher.match(manifest.tag_list):
                sources.append((base, repository, match, digest))  # noqa: PERF401
        return sources

    def _get_dest(
        self,
        source_base: PurePosixPath,
        source_repository: str,
        source_tag: Match,
        to_param: Any,
    ) -> tuple[str, str]:
        """Get Destination.

        Args:
            source_base: base as PurePosixPath.
            source_repository: source repository, relative to base.
            source_tag: source tag.
            source_digest: source digest.
            to_param: "to" parameter.

        Returns:
            A tuple (repository, tag)

        Raises:
            ValueError: Unexpected to param type.
        """
        if to_param is None:
            repository = str(source_base / source_repository).split("/", 1).pop()
            return repository, source_tag[0]
        if isinstance(to_param, str):
            tag: str | None
            try:
                to_param, tag = to_param.rsplit(":", 1)
            except ValueError:
                tag = None
            return to_param, tag or source_tag[0]
        if isinstance(to_param, dict):
            return self._get_dest_from_dict(source_base, source_repository, source_tag, to_param)
        msg = f"Unexpected to param type: {type(to_param)}"
        raise ValueError(msg)

    def _get_dest_from_dict(
        self,
        source_base: PurePosixPath,
        source_repository: str,
        source_tag: Match,
        to_param: dict,
    ) -> tuple[str, str]:
        base = PurePosixPath(to_param.get("base", source_base) or "")
        repository = to_param.get("repository", source_repository) or ""
        tag = source_tag.expand(to_param.get("tag") or source_tag[0])
        return str(base / repository), tag

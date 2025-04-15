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

from logging import getLogger
from typing import TYPE_CHECKING
from urllib.parse import quote

from gitlabracadabra.packages.destination import Destination

if TYPE_CHECKING:
    from gitlabracadabra.gitlab.connection import GitlabConnection
    from gitlabracadabra.packages.package_file import PackageFile


HELM = "helm"
PYPI = "pypi"

logger = getLogger(__name__)


class Gitlab(Destination):
    """Gitlab repository."""

    def __init__(
        self,
        *,
        connection: GitlabConnection,
        full_path: str,
        project_id: int,
    ) -> None:
        """Initialize Gitlab repository.

        Args:
            connection: A Gitlab connection.
            full_path: Project full path.
            project_id: Project ID.
        """
        super().__init__(log_prefix=f"[{full_path}] ")
        self._connection = connection
        self._full_path = full_path
        self._project_id = project_id
        self._connection.session_callback(self.session)

    def upload_method(self, package_file: PackageFile) -> str:
        """Get upload HTTP method.

        Args:
            package_file: Source package file.

        Returns:
            The upload method.
        """
        if package_file.package_type in {HELM, PYPI}:
            return "POST"

        return super().upload_method(package_file)

    def head_url(self, package_file: PackageFile) -> str:
        """Get URL to test existence of destination package file with a HEAD request.

        Args:
            package_file: Source package file.

        Returns:
            An URL.

        Raises:
            NotImplementedError: For unsupported package types.
        """
        if package_file.package_type == "raw":
            return "{}/projects/{}/packages/generic/{}/{}/{}".format(
                self._connection.api_url,
                quote(self._full_path, safe=""),
                quote(package_file.package_name, safe=""),  # [A-Za-z0-9\.\_\-\+]+
                quote(package_file.package_version, safe=""),  # (\.?[\w\+-]+\.?)+
                quote(package_file.file_name, safe=""),  # [A-Za-z0-9\.\_\-\+]+
            )
        if package_file.package_type == HELM:
            channel = package_file.metadata.get("channel") or "stable"
            file_name = f"{package_file.package_name}-{package_file.package_version}.tgz"
            return "{}/projects/{}/packages/helm/{}/charts/{}".format(
                self._connection.api_url,
                quote(self._full_path, safe=""),
                quote(channel, safe=""),
                quote(file_name, safe=""),
            )
        if package_file.package_type == PYPI:
            return "{}/projects/{}/packages/pypi/files/{}/{}".format(
                self._connection.api_url,
                self._project_id,
                quote(package_file.metadata.get("sha256", ""), safe=""),
                quote(package_file.file_name, safe=""),
            )

        raise NotImplementedError

    def upload_url(self, package_file: PackageFile) -> str:
        """Get URL to upload to.

        Args:
            package_file: Source package file.

        Returns:
            The upload URL.
        """
        if package_file.package_type == HELM:
            channel = package_file.metadata.get("channel") or "stable"
            return "{}/projects/{}/packages/helm/api/{}/charts".format(
                self._connection.api_url,
                quote(self._full_path, safe=""),
                quote(channel, safe=""),
            )
        if package_file.package_type == PYPI:
            return (
                "{}/projects/{}/packages/pypi?"
                "requires_python={}&"
                "name={}&"
                "version={}&"
                "md5_digest={}&"
                "sha256_digest={}"
            ).format(
                self._connection.api_url,
                self._project_id,
                quote(package_file.metadata.get("requires-python", ""), safe=""),
                quote(package_file.package_name, safe=""),
                quote(package_file.package_version, safe=""),
                quote(package_file.metadata.get("md5", ""), safe=""),
                quote(package_file.metadata.get("sha256", ""), safe=""),
            )

        return super().upload_url(package_file)

    def files_key(self, package_file: PackageFile) -> str | None:
        """Get files key, to upload to. If None, uploaded as body.

        Args:
            package_file: Source package file.

        Returns:
            The files key, or None.
        """
        if package_file.package_type == HELM:
            return "chart"
        if package_file.package_type == PYPI:
            return "content"

        return super().files_key(package_file)

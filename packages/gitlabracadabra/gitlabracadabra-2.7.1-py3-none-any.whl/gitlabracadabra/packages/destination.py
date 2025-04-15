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

from requests import RequestException, codes

from gitlabracadabra import __version__ as gitlabracadabra_version
from gitlabracadabra.packages.stream import Stream
from gitlabracadabra.session import Session

if TYPE_CHECKING:
    from gitlabracadabra.packages.package_file import PackageFile
    from gitlabracadabra.packages.source import Source

logger = getLogger(__name__)


class Destination:
    """Destination package repository."""

    def __init__(
        self,
        *,
        log_prefix: str = "",
    ) -> None:
        """Initialize Destination repository.

        Args:
            log_prefix: Log prefix.
        """
        self._log_prefix = log_prefix
        self.session = Session()
        self.session.headers["User-Agent"] = f"gitlabracadabra/{gitlabracadabra_version}"

    def __del__(self) -> None:
        """Destroy a connection."""
        self.session.close()

    def import_source(self, source: Source, *, dry_run: bool) -> None:
        """Import package files from Source.

        Args:
            source: Source repository.
            dry_run: Dry run.
        """
        try:
            for package_file in source.package_files:
                self.try_import_package_file(source, package_file, dry_run=dry_run)
        except RequestException as err:
            if err.request:
                logger.warning(
                    "%sError retrieving package files list from %s (%s %s): %s",
                    self._log_prefix,
                    str(source),
                    err.request.method,
                    err.request.url,
                    repr(err),
                )
            else:
                logger.warning(
                    "%sError retrieving package files list from %s: %s",
                    self._log_prefix,
                    str(source),
                    repr(err),
                )

    def try_import_package_file(self, source: Source, package_file: PackageFile, *, dry_run: bool) -> None:
        """Try to import one package file, and catch RequestExceptions.

        Args:
            source: Source repository.
            package_file: Source package file.
            dry_run: Dry run.
        """
        try:
            self.import_package_file(source, package_file, dry_run=dry_run)
        except RequestException as err:
            if err.request:
                logger.warning(
                    '%sError uploading %s package file "%s" from "%s" version %s (%s %s): %s',
                    self._log_prefix,
                    package_file.package_type,
                    package_file.file_name,
                    package_file.package_name,
                    package_file.package_version,
                    err.request.method,
                    err.request.url,
                    repr(err),
                )
            else:
                logger.warning(
                    '%sError uploading %s package file "%s" from "%s" version %s: %s',
                    self._log_prefix,
                    package_file.package_type,
                    package_file.file_name,
                    package_file.package_name,
                    package_file.package_version,
                    repr(err),
                )

    def import_package_file(self, source: Source, package_file: PackageFile, *, dry_run: bool) -> None:
        """Import one package file.

        Args:
            source: Source repository.
            package_file: Source package file.
            dry_run: Dry run.
        """
        # Test source exists
        if not self._source_package_file_exists(source, package_file):
            return

        # Test destination exists
        if self._destination_package_file_exists(package_file):
            return

        # Test dry run
        if self._dry_run(package_file, dry_run=dry_run):
            return

        # Upload
        self._upload_package_file(source, package_file)

    def upload_method(
        self,
        package_file: PackageFile,  # noqa: ARG002
    ) -> str:
        """Get upload HTTP method.

        Args:
            package_file: Source package file.

        Returns:
            The upload method.
        """
        return "PUT"

    def head_url(self, package_file: PackageFile) -> str:
        """Get URL to test existence of destination package file with a HEAD request.

        Args:
            package_file: Source package file.

        Raises:
            NotImplementedError: This is an abstract method.
        """
        raise NotImplementedError

    def upload_url(self, package_file: PackageFile) -> str:
        """Get URL to upload to.

        Args:
            package_file: Source package file.

        Returns:
            The upload URL.
        """
        return self.head_url(package_file)

    def files_key(
        self,
        package_file: PackageFile,  # noqa: ARG002
    ) -> str | None:
        """Get files key, to upload to. If None, uploaded as body.

        Args:
            package_file: Source package file.

        Returns:
            The files key, or None.
        """
        return None

    def _source_package_file_exists(self, source: Source, package_file: PackageFile) -> bool:
        source_exists_response = source.session.request(
            "HEAD",
            package_file.url,
        )
        if source_exists_response.status_code == codes["ok"]:
            return True
        if source_exists_response.status_code == codes["not_found"]:
            logger.warning(
                '%sNOT uploading %s package file "%s" from "%s" version %s (%s): source not found',
                self._log_prefix,
                package_file.package_type,
                package_file.file_name,
                package_file.package_name,
                package_file.package_version,
                package_file.url,
            )
            return False
        logger.warning(
            '%sNOT uploading %s package file "%s" from "%s" version %s (%s): received %i %s with HEAD method on source',
            self._log_prefix,
            package_file.package_type,
            package_file.file_name,
            package_file.package_name,
            package_file.package_version,
            package_file.url,
            source_exists_response.status_code,
            source_exists_response.reason,
        )
        return False

    def _destination_package_file_exists(self, package_file: PackageFile) -> bool:
        head_url = self.head_url(package_file)
        destination_exists_response = self.session.request(
            "HEAD",
            head_url,
        )
        if destination_exists_response.status_code == codes["ok"]:
            return True
        if destination_exists_response.status_code == codes["not_found"]:
            return False
        logger.warning(
            '%sUnexpected HTTP status for %s package file "%s" from "%s" version %s (%s): received %i %s with HEAD method on destination',
            self._log_prefix,
            package_file.package_type,
            package_file.file_name,
            package_file.package_name,
            package_file.package_version,
            head_url,
            destination_exists_response.status_code,
            destination_exists_response.reason,
        )
        return False

    def _dry_run(self, package_file: PackageFile, *, dry_run: bool) -> bool:
        if dry_run:
            logger.info(
                '%sNOT uploading %s package file "%s" from "%s" version %s (%s): Dry run',
                self._log_prefix,
                package_file.package_type,
                package_file.file_name,
                package_file.package_name,
                package_file.package_version,
                package_file.url,
            )
        return dry_run

    def _upload_package_file(self, source: Source, package_file: PackageFile) -> None:
        upload_method = self.upload_method(package_file)
        upload_url = self.upload_url(package_file)
        files_key = self.files_key(package_file)

        logger.info(
            '%sUploading %s package file "%s" from "%s" version %s (%s)',
            self._log_prefix,
            package_file.package_type,
            package_file.file_name,
            package_file.package_name,
            package_file.package_version,
            package_file.url,
        )
        download_response = source.session.request(
            "GET",
            package_file.url,
            stream=True,
            headers={
                "Accept-Encoding": "*",
            },
        )

        if files_key:
            upload_response = self.session.request(
                upload_method,
                upload_url,
                files={files_key: Stream(download_response)},  # type: ignore
            )
        else:
            upload_response = self.session.request(
                upload_method,
                upload_url,
                data=Stream(download_response),
            )
        if upload_response.status_code not in {codes["created"], codes["accepted"]}:
            logger.warning(
                '%sError uploading %s package file "%s" from "%s" version %s (%s): %s',
                self._log_prefix,
                package_file.package_type,
                package_file.file_name,
                package_file.package_name,
                package_file.package_version,
                upload_url,
                upload_response.content,
            )

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

from typing import TYPE_CHECKING

from gitlabracadabra.containers.authenticated_session import AuthenticatedSession
from gitlabracadabra.containers.const import DOCKER_HOSTNAME, DOCKER_REGISTRY

if TYPE_CHECKING:
    from collections.abc import Callable

    from requests import Response
    from requests.auth import AuthBase

    from gitlabracadabra.containers.authenticated_session import Data, Params
    from gitlabracadabra.containers.scope import Scope


class RegistrySession:
    """Container registry HTTP methods."""

    def __init__(
        self,
        hostname: str,
        session_callback: Callable[[AuthenticatedSession], None] | None = None,
    ) -> None:
        """Instantiate a registry connection.

        Args:
            hostname: fqdn of a registry.
            session_callback: Callback applied to requests Session.
        """
        self._session = AuthenticatedSession()
        self._hostname = hostname
        if hostname == DOCKER_HOSTNAME:
            self._session.connection_hostname = DOCKER_REGISTRY
        else:
            self._session.connection_hostname = hostname
        if session_callback is not None:
            session_callback(self._session)
        # Cache where blobs are present
        # dict key is digest, value is a list of manifest names
        # Used in WithBlobs
        self._blobs: dict[str, list[str]] = {}
        self._sizes: dict[str, int] = {}

    def __del__(self) -> None:
        """Destroy a registry connection."""
        self._session.close()

    @property
    def hostname(self) -> str:
        """Get hostname.

        Returns:
            The registry hostname.
        """
        return self._hostname

    def request(
        self,
        method: str,
        url: str,
        *,
        scopes: set[Scope] | None = None,
        params: Params = None,
        data: Data | None = None,
        headers: dict[str, str] | None = None,
        content_type: str | None = None,
        accept: tuple[str, ...] | None = None,
        auth: AuthBase | None = None,
        stream: bool | None = None,
        raise_for_status: bool = True,
    ) -> Response:
        """Send an HTTP request.

        Args:
            method: HTTP method.
            url: Either a path or a full url.
            scopes: An optional set of scopes.
            params: query string params.
            data: Request body stream.
            headers: Request headers.
            content_type: Uploaded MIME type.
            accept: An optional list of accepted mime-types.
            auth: HTTPBasicAuth.
            stream: Stream the response.
            raise_for_status: Raises `requests.HTTPError`, if one occurred.

        Returns:
            A Response.
        """
        headers = headers.copy() if headers else {}
        if accept:
            headers["Accept"] = ", ".join(accept)
        if content_type:
            headers["Content-Type"] = content_type

        self._session.connect(scopes)
        response = self._session.authenticated_request(
            method,
            url,
            params=params,
            data=data,
            headers=headers,
            auth=auth,
            stream=stream,
        )
        if raise_for_status:
            response.raise_for_status()
        return response

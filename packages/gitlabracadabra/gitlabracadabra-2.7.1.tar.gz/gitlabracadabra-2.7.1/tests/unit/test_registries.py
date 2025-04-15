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

from typing import NamedTuple

from gitlabracadabra.containers.const import DOCKER_HOSTNAME, DOCKER_REGISTRY
from gitlabracadabra.containers.registries import Registries
from gitlabracadabra.tests.case import TestCase


class FixtureData(NamedTuple):
    input_name: str
    hostname: str
    manifest_name: str
    tag: str
    reference_tag: str | None
    digest: str | None
    full_reference: str
    short_reference: str


LATEST = "latest"
TEST_DATA = (
    FixtureData(
        "my/repo",
        DOCKER_HOSTNAME,
        "my/repo",
        LATEST,
        None,
        None,
        "docker.io/my/repo",
        "my/repo",
    ),
    FixtureData(
        "debian",
        DOCKER_HOSTNAME,
        "library/debian",
        LATEST,
        None,
        None,
        "docker.io/library/debian",
        "debian",
    ),
    FixtureData(
        "localhost/foo/bar:v1.0",
        "localhost",
        "foo/bar",
        "v1.0",
        "v1.0",
        None,
        "localhost/foo/bar:v1.0",
        "localhost/foo/bar:v1.0",
    ),
    FixtureData(
        "example.org/foo/baz:v2.3.4",
        "example.org",
        "foo/baz",
        "v2.3.4",
        "v2.3.4",
        None,
        "example.org/foo/baz:v2.3.4",
        "example.org/foo/baz:v2.3.4",
    ),
    FixtureData(
        "registry:5000/foo/bar:latest",
        "registry:5000",
        "foo/bar",
        LATEST,
        LATEST,
        None,
        "registry:5000/foo/bar:latest",
        "registry:5000/foo/bar",
    ),
    FixtureData(
        "busybox:latest@sha256:74e4a68dfba6f40b01787a3876cc1be0fb1d9025c3567cf8367c659f2187234f",
        DOCKER_HOSTNAME,
        "library/busybox",
        LATEST,
        LATEST,
        "sha256:74e4a68dfba6f40b01787a3876cc1be0fb1d9025c3567cf8367c659f2187234f",
        "docker.io/library/busybox:latest@sha256:74e4a68dfba6f40b01787a3876cc1be0fb1d9025c3567cf8367c659f2187234f",
        "busybox@sha256:74e4a68dfba6f40b01787a3876cc1be0fb1d9025c3567cf8367c659f2187234f",
    ),
)


class TestRegistries(TestCase):
    def test_singleton(self) -> None:
        registries1 = Registries()
        registries2 = Registries()
        assert id(registries1) == id(registries2)

    def test_get_registry(self) -> None:
        registries = Registries()
        docker_registry = registries.get_registry(DOCKER_REGISTRY)
        assert docker_registry.hostname == DOCKER_HOSTNAME
        docker_registry2 = registries.get_registry(DOCKER_HOSTNAME)
        assert docker_registry2.hostname == DOCKER_HOSTNAME
        docker_registry3 = registries.get_registry("example.org")
        assert docker_registry3.hostname == "example.org"

    def test_get_manifest(self) -> None:
        registries = Registries()
        for test_data in TEST_DATA:
            with self.subTest(input_name=test_data.input_name):
                manifest = registries.get_manifest(test_data.input_name)
                assert manifest.registry.hostname == test_data.hostname
                assert manifest.manifest_name == test_data.manifest_name
                assert manifest.tag == test_data.tag
                assert manifest._digest == test_data.digest

    def test_short_reference(self) -> None:
        for test_data in TEST_DATA:
            with self.subTest(input_name=test_data.input_name):
                reference = Registries.short_reference(test_data.input_name)
                assert reference == test_data.short_reference

    def test_full_reference(self) -> None:
        for test_data in TEST_DATA:
            with self.subTest(input_name=test_data.input_name):
                reference = Registries.full_reference(test_data.input_name)
                assert reference == test_data.full_reference

    def test_full_reference_parts(self) -> None:
        for test_data in TEST_DATA:
            with self.subTest(input_name=test_data.input_name):
                manifest = Registries.full_reference_parts(test_data.input_name)
                assert manifest.hostname == test_data.hostname
                assert manifest.manifest_name == test_data.manifest_name
                assert manifest.tag == test_data.reference_tag
                assert manifest.digest == test_data.digest

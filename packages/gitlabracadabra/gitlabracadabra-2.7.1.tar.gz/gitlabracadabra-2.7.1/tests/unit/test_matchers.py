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

from typing import Any, NamedTuple
from unittest.mock import MagicMock

from gitlabracadabra.matchers import Matcher
from gitlabracadabra.tests.case import TestCaseWithManager


class FixtureData(NamedTuple):
    patterns: str | list[str]
    as_callable: bool
    result: list[str]
    called: bool | None


class FixtureDataSemVer(NamedTuple):
    patterns: list[str]
    semver: str
    result: list[str]
    called: bool


INPUT_DATA = ("item", "item_suffix", "prefix_item", "another")

TEST_DATA = (
    # String patterns
    FixtureData("item", as_callable=False, result=["item"], called=None),
    FixtureData("item", as_callable=True, result=["item"], called=False),
    FixtureData(["item", "extra"], as_callable=False, result=["item"], called=None),
    FixtureData(["item", "extra"], as_callable=True, result=["item", "extra"], called=False),
    # Regex patterns
    FixtureData("/item/", as_callable=False, result=["item"], called=None),
    FixtureData("/item/", as_callable=True, result=["item"], called=True),
    FixtureData(["/item/", "/extra/"], as_callable=False, result=["item"], called=None),
    FixtureData(["/item/", "/extra/"], as_callable=True, result=["item"], called=True),
    # Mixed patterns
    FixtureData(["another", "/item.*/"], as_callable=False, result=["item", "item_suffix", "another"], called=None),
    FixtureData(["another", "/item.*/"], as_callable=True, result=["item", "item_suffix", "another"], called=True),
    FixtureData(["another", "/.*item/"], as_callable=False, result=["item", "prefix_item", "another"], called=None),
    FixtureData(["another", "/.*item/"], as_callable=True, result=["item", "prefix_item", "another"], called=True),
    # Flags
    FixtureData("/Item/", as_callable=False, result=[], called=None),
    FixtureData("/Item/i", as_callable=False, result=["item"], called=None),
)


INPUT_DATA_SEMVER = ("v1.20.4", "v1.20.5", "v1.20.6", "v1.21.0")

TEST_DATA_SEMVER = (
    FixtureDataSemVer(["/v.*/"], ">=1.20.5", ["v1.20.5", "v1.20.6", "v1.21.0"], called=True),
    FixtureDataSemVer(["/v.*/", "v1.0"], ">=1.20.5", ["v1.20.5", "v1.20.6", "v1.21.0"], called=True),
    FixtureDataSemVer(["v1.0", "v2.0"], ">=1.20.5", ["v1.0", "v2.0"], called=False),
)


class TestMatcher(TestCaseWithManager):
    """Test Matcher class."""

    def test_match(self):
        """Test Matcher.match method."""
        for test_data in TEST_DATA:
            with self.subTest(patterns=test_data.patterns, as_callable=test_data.as_callable):
                if test_data.as_callable:
                    input_data = MagicMock()
                    input_data.return_value = list(INPUT_DATA)
                else:
                    input_data = list(INPUT_DATA)
                matches = Matcher(test_data.patterns, None).match(input_data)
                self._assert_match_equal(matches, test_data.result)
                self._assert_call(input_data, as_callable=test_data.as_callable, called=test_data.called)

    def test_match_limit(self):
        """Test Matcher.match method, without semver and with limit."""
        matches = Matcher(
            ["1.0.1", "v2.0.2", "invalid", "3.0.1", "4.2.1"],
            None,
            limit=3,
            log_prefix="LP:",
        ).match(MagicMock())
        self._assert_match_equal(matches, ["4.2.1", "3.0.1", "v2.0.2"])

    def test_match_semver(self):
        """Test Matcher.match method, with semver."""
        for test_data in TEST_DATA_SEMVER:
            with self.subTest(patterns=test_data.patterns):
                input_data = MagicMock()
                input_data.return_value = list(INPUT_DATA_SEMVER)
                matches = Matcher(test_data.patterns, test_data.semver).match(input_data)
                self._assert_match_equal(matches, test_data.result)
                self._assert_call(input_data, as_callable=True, called=test_data.called)

    def test_match_semver_limit(self):
        """Test Matcher.match method, with semver and with limit."""
        matches = Matcher(
            ["/.*/"],
            ">=3",
            limit=3,
            log_prefix="LP:",
        ).match(["1.0.1", "v2.0.2", "invalid", "3.0.1", "4.2.1"])
        self._assert_match_equal(matches, ["4.2.1", "3.0.1"])

    def _assert_match_equal(self, actual: list[str], expected: list[str]) -> None:
        assert len(actual) == len(expected)
        for index, match in enumerate(actual):
            assert match[0] == expected[index]

    def _assert_call(self, input_data: Any, *, as_callable: bool, called: bool) -> None:
        if as_callable and called:
            input_data.assert_called_once_with()
        elif as_callable:
            assert len(input_data.mock_calls) == 0
        else:
            assert called is None

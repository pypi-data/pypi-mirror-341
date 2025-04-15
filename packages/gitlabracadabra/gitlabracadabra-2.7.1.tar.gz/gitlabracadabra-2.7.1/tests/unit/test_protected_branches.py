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

from unittest.mock import call

from gitlabracadabra.objects.project import GitLabracadabraProject
from gitlabracadabra.tests import my_vcr, patch
from gitlabracadabra.tests.case import TestCaseWithManager


class TestProtectedBranches(TestCaseWithManager):
    """Test ProtectedBranchesMixin."""

    @my_vcr.use_cassette
    def test_protected_branches_ce(self, cass):
        """Test new protected branch.

        Args:
            cass: VCR cassette.
        """
        project = GitLabracadabraProject(
            "memory",
            "test/protected-branches",
            {
                "create_object": True,
                "initialize_with_readme": True,
                "protected_branches": {
                    "main": {"push_access_level": "developer", "merge_access_level": "noone"},
                    "develop": {"push_access_level": "noone", "merge_access_level": "developer"},
                },
            },
        )
        with patch("gitlabracadabra.mixins.protected_branches.logger", autospec=True) as logger:
            assert project.errors() == []
            project.process()
            assert cass.all_played
            logger.assert_has_calls([])

    @my_vcr.use_cassette
    def test_protected_branches_delete(self, cass):
        """Test deleting unknown protected branch.

        Args:
            cass: VCR cassette.
        """
        project = GitLabracadabraProject(
            "memory",
            "test/protected-branches2",
            {
                "protected_branches": {},
                "unknown_protected_branches": "delete",
            },
        )
        with patch("gitlabracadabra.mixins.protected_branches.logger", autospec=True) as logger:
            assert project.errors() == []
            project.process()
            assert cass.all_played
            logger.info.assert_called_once_with(
                "[%s] Deleting unknown protected branch: %s",
                "test/protected-branches2",
                "main",
            )

    @my_vcr.use_cassette
    def test_protected_branches_ee(self, cass):
        """Test protected branch EE.

        Args:
            cass: VCR cassette.
        """
        project = GitLabracadabraProject(
            "memory",
            "gitlabracadabra/test-group/protected-branches",
            {
                "protected_branches": {
                    "main": {
                        "allowed_to_merge": [
                            {"role": "maintainer"},
                            {"user": "kubitus-bot"},
                            # {'group': 'some-group'},
                        ],
                        "allowed_to_push": [
                            {"role": "noone"},
                            {"user": "kubitus-bot"},
                            # {'group': 'some-group'},
                            # {'deploy_key': 'My Key'},
                        ],
                        "allow_force_push": True,
                        "code_owner_approval_required": True,
                    },
                    "develop": {
                        "allowed_to_merge": [
                            {"role": "developer"},
                            {"user": "kubitus-bot"},
                            # {'group': 'some-group'},
                        ],
                        "allowed_to_push": [
                            {"role": "developer"},
                            {"user": "kubitus-bot"},
                            # {'group': 'some-group'},
                            {"deploy_key": "My Key"},
                        ],
                        "allow_force_push": True,
                        "code_owner_approval_required": True,
                    },
                },
            },
        )
        with patch("gitlabracadabra.mixins.protected_branches.logger", autospec=True) as logger:
            assert project.errors() == []
            project.process()
            assert cass.all_played
            logger.assert_has_calls(
                [
                    call.info(
                        "[%s] Creating protected branch %s: %s",
                        "gitlabracadabra/test-group/protected-branches",
                        "develop",
                        (
                            '{"allow_force_push": true, '
                            '"allowed_to_merge": [{"access_level": 30}, {"user_id": 9280824}], '
                            '"allowed_to_push": [{"access_level": 30}, {"deploy_key_id": 15407951},'
                            ' {"user_id": 9280824}], '
                            '"code_owner_approval_required": true, '
                            '"name": "develop"}'
                        ),
                    ),
                    call.info(
                        "[%s] Changing protected branch %s: %s -> %s",
                        "gitlabracadabra/test-group/protected-branches",
                        "main",
                        (
                            '{"allow_force_push": false, '
                            '"allowed_to_merge": [{"access_level": 40}], '
                            '"allowed_to_push": [{"access_level": 40}], '
                            '"allowed_to_unprotect": [], '
                            '"code_owner_approval_required": false, '
                            '"name": "main"}'
                        ),
                        (
                            '{"allow_force_push": true, '
                            '"allowed_to_merge": [{"access_level": 40}, {"user_id": 9280824}], '
                            '"allowed_to_push": [{"access_level": 0}, {"user_id": 9280824}], '
                            '"allowed_to_unprotect": [], '
                            '"code_owner_approval_required": true, '
                            '"name": "main"}'
                        ),
                    ),
                ]
            )

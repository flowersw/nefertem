#!/usr/bin/env python3
# Nefertem
# Copyright(C) 2018 Fridolin Pokorny
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Wrappers for running analyzers."""

import logging
import os

from thoth.analyzer import run_command
import git

from .config import config
from .exceptions import NoTestsFound

_LOGGER = logging.getLogger(__name__)
_COMMAND_TIMEOUT = int(os.getenv('NEFERTEM_COMMAND_TIMEOUT', 60*30))  # Give commands 30 mins to finish by default.


def clone_if_remote_repo(project_path: str, destination: str = None, branch: str = None):
    """Clone a repository containing sources into CWD if project_path is a remote repository."""
    destination = destination or '.'
    branch = branch or 'master'

    if project_path.startswith(('https://', 'http://', 'git@')):
        # We can clone only the last state (depth=1).
        git.Repo.clone_from(project_path, destination, branch=branch, depth=1)
        return destination, True

    return project_path, False


def run_coala(project_path: str, *, no_color: bool = False, apply_patches: bool = False, json: bool = True):
    """Run configured Coala bears on the codebase."""
    _LOGGER.debug("Running coala bears...")
    cmd = f'coala --config {config.coala_config_path} --non-interactive '

    if no_color:
        cmd += '--no-color '
    if json:
        cmd += '--json '
    if apply_patches:
        cmd += '--apply-patches '

    result = run_command(cmd + project_path, timeout=_COMMAND_TIMEOUT, raise_on_error=False)
    return result.to_dict()


def run_pylint(project_path: str):
    """Run PyLint on the codebase."""
    _LOGGER.debug("Running pylint...")
    cmd = f'pylint --rcfile={config.pylint_config_path} '
    result = run_command(cmd + project_path, timeout=_COMMAND_TIMEOUT, raise_on_error=False)
    return result.to_dict()


def run_pytest(project_path: str, *, timeout: int = 20):
    """Execute testsuite for the given project."""
    _LOGGER.debug("Running pytest on the test-suite...")
    if not os.path.isdir(os.path.join(project_path, 'tests')):
        raise NoTestsFound("No tests found in the project codebase")

    cmd = f'pytest --capture=no --cov={project_path} --verbose --verbose --showlocals --timeout={timeout} '
    result = run_command(cmd + project_path, timeout=_COMMAND_TIMEOUT, raise_on_error=False)

    return result.to_dict()


def run_pycodestyle(project_path: str, *, exclude_tests: bool = True):
    """Check Python's docstrings style."""
    _LOGGER.debug("Running pycodestyle...")
    cmd = 'pydocstyle '

    if exclude_tests:
        cmd += '--match="(?!test_).*\.py" '

    result = run_command(cmd + project_path, timeout=_COMMAND_TIMEOUT, raise_on_error=False)
    return result.to_dict()

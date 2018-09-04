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

"""CLI for Nefertem - checks for Python code issues."""

import logging
import os
import json
import sys

import click
import daiquiri

from thoth.analyzer import print_command_result

from nefertem import __version__ as nefertem_version
from nefertem import __name__ as nefertem_name
from nefertem.analzers import run_coala, run_pycodestyle, run_pylint, run_pytest, clone_if_remote_repo

daiquiri.setup(level=logging.INFO)

_LOGGER = logging.getLogger(__name__)


def _print_version(ctx, _, value):
    """Print version and exit."""
    if not value or ctx.resilient_parsing:
        return
    click.echo(nefertem_version)
    ctx.exit()


def _print_results(click_ctx, result):
    """Print results obtained by analyzers."""
    if bool(int(os.getenv('NEFERTEM_JSON_OUTPUT', 0))):
        print_command_result(
            click_ctx,
            result,
            analyzer=nefertem_name,
            analyzer_version=nefertem_version,
            pretty=True
        )
    else:
        json.dump(result, sys.stdout)


@click.group()
@click.pass_context
@click.option('--version', is_flag=True, is_eager=True, callback=_print_version, expose_value=False,
              help="Print version and exit.")
@click.option('-v', '--verbose', is_flag=True, envvar='NEFERTEM_VERBOSE',
              help="Be verbose about what's going on.")
def cli(ctx, verbose: bool = False):
    """Analyze Python source code in a simple tool."""
    if ctx:
        ctx.auto_envvar_prefix = 'NEFERTEM'

    if verbose:
        _LOGGER.setLevel(logging.DEBUG)
        _LOGGER.debug("Debug mode turned on")
        _LOGGER.debug("Nefertem version: %r", nefertem_version)


@cli.command('run-all')
@click.pass_context
@click.argument('project', metavar='project', envvar='NEFERTEM_PROJECT')
def run_all(click_ctx, project):
    """Run all static analyzers and execute the test-suite on the given codebase."""
    # This will run all analyzers with their default configuration.
    project_path, _ = clone_if_remote_repo(project, branch='master')
    result = {
        'pydocstyle': run_pycodestyle(project_path),
        'pytest': run_pytest(project_path),
        'pylint': run_pylint(project_path),
        'coala': run_coala(project_path)
    }
    _print_results(click_ctx, result)


@cli.command('pylint')
@click.pass_context
@click.argument('project', metavar='project', envvar='NEFERTEM_PROJECT')
def pylint(click_ctx, project):
    """Run PyLint on the given codebase."""
    project_path, _ = clone_if_remote_repo(project, branch='master')
    result = run_pylint(project_path)
    _print_results(click_ctx, result)


@cli.command('coala')
@click.pass_context
@click.argument('project', metavar='project', envvar='NEFERTEM_PROJECT')
@click.option('--no-color', is_flag=True, help="Do not use colorized output.")
@click.option('--apply-patches', is_flag=True, help="Apply fixes where possible.")
@click.option('--json', is_flag=True, help="Print output as a JSON.")
def coala(click_ctx, project, **options):
    """Run Coala bears on the given codebase."""
    project_path, _ = clone_if_remote_repo(project, branch='master')
    result = run_coala(project_path, **options)
    _print_results(click_ctx, result)


@cli.command('pytest')
@click.pass_context
@click.argument('project', metavar='project', envvar='NEFERTEM_PROJECT')
def pytest(click_ctx, project, **options):
    """Execute testsuite for the given codebase."""
    project_path, _ = clone_if_remote_repo(project, branch='master')
    result = run_pytest(project, **options)
    _print_results(click_ctx, result)


@cli.command('pydocstyle')
@click.pass_context
@click.argument('project', metavar='project', envvar='NEFERTEM_PROJECT')
def pydocstyle(click_ctx, project, **options):
    """Check formatting of Python's docstrings."""
    project_path, _ = clone_if_remote_repo(project, branch='master')
    result = run_pycodestyle(project, **options)
    _print_results(click_ctx, result)


if __name__ == '__main__':
    cli()

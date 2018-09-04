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

"""Nefertem's configuration abstraction."""

import logging
import os

_LOGGER = logging.getLogger(__name__)


class _Config:
    """Configuration of config files used across analyzers."""

    _CONFIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config')

    _DEFAULT_PYLINT_CONFIG_PATH = os.path.join(_CONFIG_DIR, 'pylintrc')
    _DEFAULT_COALA_CONFIG_PATH = os.path.join(_CONFIG_DIR, 'coafile')

    __slots__ = ['pylint_config_path', 'coala_config_path']

    def __init__(self, *, pylint_config_path: str = None, coala_config_path: str = None):
        self.pylint_config_path = pylint_config_path or self._DEFAULT_PYLINT_CONFIG_PATH
        self.coala_config_path = coala_config_path or self._DEFAULT_COALA_CONFIG_PATH


config = _Config()

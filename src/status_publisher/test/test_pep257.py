# Copyright 2026 ROS 2 System Status Monitor contributors
#
# SPDX-License-Identifier: MIT

import pytest
from ament_pep257.main import main


@pytest.mark.linter
@pytest.mark.pep257
def test_pep257():
    rc = main(argv=['.', 'test'])
    assert rc == 0, 'Found docstring style errors'


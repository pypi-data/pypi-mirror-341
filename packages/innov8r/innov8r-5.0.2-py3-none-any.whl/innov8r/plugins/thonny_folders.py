# -*- coding: utf-8 -*-
"""Adds commands for opening certain Thonny folders"""

from innov8r import THONNY_USER_DIR, get_workbench
from innov8r.languages import tr
from innov8r.ui_utils import open_path_in_system_file_manager


def load_plugin() -> None:
    def cmd_open_data_dir():
        open_path_in_system_file_manager(THONNY_USER_DIR)

    def cmd_open_program_dir():
        open_path_in_system_file_manager(get_workbench().get_package_dir())

    get_workbench().add_command(
        "open_program_dir",
        "tools",
        tr("Open Innovator program folder..."),
        cmd_open_program_dir,
        group=110,
    )
    get_workbench().add_command(
        "open_data_dir", "tools", tr("Open Innovator data folder..."), cmd_open_data_dir, group=110
    )

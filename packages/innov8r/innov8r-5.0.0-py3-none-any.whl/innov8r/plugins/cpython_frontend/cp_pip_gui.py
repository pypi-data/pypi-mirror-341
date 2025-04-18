import os
from abc import ABC

import innov8r
from innov8r import get_runner, is_private_python
from innov8r.common import normpath_with_actual_case
from innov8r.languages import tr
from innov8r.plugins.cpython_frontend.cp_front import LocalCPythonProxy
from innov8r.plugins.pip_gui import BackendPipDialog


class CPythonPipDialog(BackendPipDialog, ABC):
    def _is_read_only(self):
        # readonly if not in a virtual environment
        # and user site packages is disabled
        return (
            self._use_user_install()
            and not get_runner().get_backend_proxy().get_user_site_packages()
        ) or self._backend_proxy.is_externally_managed()

    def _get_target_directory(self):
        if self._use_user_install():
            usp = self._backend_proxy.get_user_site_packages()
            if isinstance(self._backend_proxy, LocalCPythonProxy):
                os.makedirs(usp, exist_ok=True)
                return normpath_with_actual_case(usp)
            else:
                return usp
        else:
            sp = self._backend_proxy.get_site_packages()
            if sp is None:
                return None
            return normpath_with_actual_case(sp)

    def _use_user_install(self):
        return not (
            self._targets_virtual_environment()
            or innov8r.is_portable()
            and is_private_python(self._backend_proxy.get_target_executable())
        )

    def _targets_virtual_environment(self):
        return get_runner().using_venv()

    def _show_read_only_instructions(self):
        if self._backend_proxy.is_externally_managed():
            self._append_info_text(tr("Browse the packages") + "\n\n", ("caption",))
            self.info_text.direct_insert(
                "end",
                tr(
                    "The packages of this interpreter can be managed via your system package manager."
                )
                + "\n\n",
            )
            self.info_text.direct_insert(
                "end",
                tr("For pip-installing a package, you need to use a virtual environment.") + "\n\n",
            )


class LocalCPythonPipDialog(CPythonPipDialog):
    def _installer_runs_locally(self):
        return True

    def _get_interpreter_description(self):
        return get_runner().get_backend_proxy().get_target_executable()

    def _normalize_target_path(self, path: str) -> str:
        return normpath_with_actual_case(path)

    def _append_location_to_info_path(self, path):
        self.info_text.direct_insert("end", normpath_with_actual_case(path), ("url",))

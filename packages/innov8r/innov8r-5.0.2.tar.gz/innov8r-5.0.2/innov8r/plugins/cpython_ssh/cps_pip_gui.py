from innov8r import get_runner
from innov8r.plugins.cpython_frontend.cp_pip_gui import CPythonPipDialog
from innov8r.plugins.cpython_ssh import SshCPythonProxy


class SshCPythonPipDialog(CPythonPipDialog):
    def _installer_runs_locally(self):
        return False

    def _get_interpreter_description(self):
        return self._backend_proxy.get_full_label()

from innov8r.languages import tr
from innov8r.plugins.circuitpython.cirpy_front import CircuitPythonConfigPage, CircuitPythonProxy
from innov8r.plugins.micropython import add_micropython_backend


def load_plugin():
    add_micropython_backend(
        "CircuitPython",
        CircuitPythonProxy,
        tr("CircuitPython (generic)"),
        CircuitPythonConfigPage,
        sort_key="50",
    )

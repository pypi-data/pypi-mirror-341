import os.path
import sys
from logging import getLogger
from typing import List, Optional

import innov8r
from innov8r.plugins.micropython.bare_metal_backend import (
    BareMetalMicroPythonBackend,
    launch_bare_metal_backend,
)

logger = getLogger("innov8r.plugins.prime_inventor.prime_inventor_back")


class PrimeInventorMicroPythonBackend(BareMetalMicroPythonBackend):
    def _get_sys_path_for_analysis(self) -> Optional[List[str]]:
        return [
            os.path.join(os.path.dirname(__file__), "api_stubs"),
        ] + super()._get_sys_path_for_analysis()


if __name__ == "__main__":
    launch_bare_metal_backend(PrimeInventorMicroPythonBackend)

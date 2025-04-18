from logging import getLogger
from typing import Optional

from innov8r import get_workbench, ui_utils
from innov8r.plugins.micropython import add_micropython_backend
from innov8r.plugins.micropython.mp_common import RAW_PASTE_SUBMIT_MODE
from innov8r.plugins.micropython.mp_front import get_uart_adapter_vids_pids
from innov8r.plugins.micropython.uf2dialog import Uf2FlashingDialog
from innov8r.plugins.rp2040 import RP2040BackendConfigPage, RP2040BackendProxy
from innov8r.ui_utils import show_dialog

logger = getLogger(__name__)


class RaspberryPiPicoBackendProxy(RP2040BackendProxy):
    @classmethod
    def should_consider_unknown_devices(cls):
        return False

    @classmethod
    def get_known_usb_vids_pids(cls):
        # https://github.com/raspberrypi/usb-pid
        return {(0x2E8A, 0x0005)}

    @classmethod
    def get_node_label(self):
        return "Raspberry Pi Pico"


class RaspberryPiPicoBackendConfigPage(RP2040BackendConfigPage):
    pass


def load_plugin():
    add_micropython_backend(
        "RPiPico",
        RaspberryPiPicoBackendProxy,
        "MicroPython (Raspberry Pi Pico)",
        RaspberryPiPicoBackendConfigPage,
        bare_metal=True,
        sort_key="32",
        validate_time=False,
        sync_time=True,
        submit_mode=RAW_PASTE_SUBMIT_MODE,
        write_block_size=64,
    )

    # Don't consider Pico in generic backends
    # The main reason is to reduce the number of items in the backend switcher menu
    import innov8r.plugins.circuitpython
    import innov8r.plugins.esp
    import innov8r.plugins.micropython

    innov8r.plugins.circuitpython.cirpy_front.VIDS_PIDS_TO_AVOID.update(
        RaspberryPiPicoBackendProxy.get_known_usb_vids_pids()
    )
    innov8r.plugins.micropython.mp_front.VIDS_PIDS_TO_AVOID_IN_GENERIC_BACKEND.update(
        RaspberryPiPicoBackendProxy.get_known_usb_vids_pids()
    )
    innov8r.plugins.esp.VIDS_PIDS_TO_AVOID_IN_ESP_BACKENDS.update(
        RaspberryPiPicoBackendProxy.get_known_usb_vids_pids()
    )

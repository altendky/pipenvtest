import epyqlib.device
import epyqlib.devicetree
import epyqlib.nv
import pytest
import pytest_twisted

import gridtied.tests.hil.common


parameters = gridtied.tests.hil.common.load_parameters_fixture()

pytestmark = pytest.mark.usefixtures(
    'parameters',
)

# Only mark the test as pytest_twisted.inlineCallbacks if you actually
# `yield` in the body.  Otherwise you will get errors.


@pytest_twisted.inlineCallbacks
def test_hash(device):
    software_hash = device.nvs.signal_from_names(
        'SoftwareHash',
        'SoftwareHash',
    )

    hash, _meta = yield device.nvs.protocol.read(
        nv_signal=software_hash,
        meta=epyqlib.nv.MetaEnum.value,
    )
    hash = int(hash)

    assert hex(hash) != 0


@pytest_twisted.inlineCallbacks
def test_run(device):
    clear_faults = ('ProcessToInverter', 'CommandModeControl', 'FaultClear')
    state = ('StatusBits', 'State')
    enable = ('ProcessToInverter', 'CommandModeControl', 'Enable')
    real_power_command = ('ProcessToInverter', 'CommandPower', 'RealPower')
    measured_real_power = ('StatusMeasuredPower', 'RealPower_measured')

    yield device.set_access_level()

    for value in True, False:
        device.set_signal(
            path=clear_faults,
            value=value,
        )
        yield epyqlib.utils.twisted.sleep(0.3)

    assert device.get_signal(state) != 'Fault'
    yield epyqlib.utils.twisted.sleep(2)
    assert device.get_signal(state) == 'Ready'

    device.set_signal(enable, True)
    yield epyqlib.utils.twisted.sleep(5)
    assert device.get_signal(state) == 'Following'

    power = 100
    device.set_signal(real_power_command, power)
    yield epyqlib.utils.twisted.sleep(2)
    error = (
        device.get_signal(measured_real_power) / power
    ) - 1
    assert abs(error) < 0.05

import can.interface
import ccstudiodss.api
import epyqlib.busproxy
import epyqlib.device
import epyqlib.devicetree
import epyqlib.hildevice
import epyqlib.tests.common
import pytest
import pytest_twisted


@pytest.fixture(scope='session', autouse=True)
def load_binary(pytestconfig):
    binary = pytestconfig.getoption('embedded_binary')

    if binary is not None:
        ccxml = pytestconfig.getoption('ccxml')

        with ccstudiodss.api.Session(ccxml=ccxml) as session:
            session.load(binary=binary)


@pytest.fixture(scope='module')
def factory_device(qapp, pytestconfig):
    project_root = pytestconfig.getoption('project_root')
    path = project_root/'interface'/'distributed_generation_factory.epc'

    available_buses = epyqlib.devicetree.available_buses()
    selected_bus = available_buses[pytestconfig.getoption('can_adapter')]

    real_bus = can.interface.Bus(
        bustype=selected_bus['interface'],
        channel=selected_bus['channel'],
        bitrate=500_000,
    )

    bus_proxy = epyqlib.busproxy.BusProxy(
        bus=real_bus,
        auto_disconnect=False,
    )

    device = epyqlib.hildevice.Device(definition_path=path)

    device.load()
    device.set_bus(bus=bus_proxy)

    return device


@pytest.fixture(scope='function')
def device(factory_device):
    factory_device.bus.transmit = True
    factory_device.cyclic_send_signal(
        path=('ProcessToInverter', 'CommandModeControl', 'Enable'),
        period=0.1,
    )

    try:
        yield factory_device
    finally:
        pytest_twisted.blockon(
            factory_device.set_access_level(level=0),
        )
        factory_device.bus.transmit = False
        factory_device.cancel_all_cyclic_sends()

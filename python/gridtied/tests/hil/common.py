import pathlib

import epyqlib.pm.valuesetmodel
import pytest
import pytest_twisted


def load_parameters_fixture(*paths, scope='module'):
    paths = (
        pathlib.Path(path)
        for path in paths
    )

    @pytest.fixture(scope=scope)
    def load_parameters(factory_device, pytestconfig):
        device = factory_device
        project_root = pytestconfig.getoption('project_root')

        for path in paths:
            if not path.is_absolute():
                path = project_root / path

            value_set = epyqlib.pm.valuesetmodel.loadp(path)

            device.nvs.from_value_set(value_set)

        pytest_twisted.blockon(
            device.set_access_level(),
        )

        pytest_twisted.blockon(
            device.nvs.write_all_to_device(background=True),
        )

        pytest_twisted.blockon(
            device.set_access_level(level=0),
        )

    return load_parameters

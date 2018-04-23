import pathlib


def pytest_addoption(parser):
    group = parser.getgroup('grid-tied')

    group.addoption('--embedded-binary', default=None)
    group.addoption('--can-adapter', type=int, default=0)
    group.addoption(
        '--project-root',
        type=pathlib.Path,
        default=pathlib.Path.cwd(),
    )

import pytest
from _pytest.scope import Scope
from teardown import Teardown


@pytest.fixture(scope=Scope.Session.value)
def teardown():
    _teardown = Teardown()
    yield _teardown
    _teardown.execute(Scope.Session)


@pytest.fixture(scope=Scope.Package.value)
def _teardown_package(teardown):
    yield teardown
    teardown.execute(Scope.Package)


@pytest.fixture(scope=Scope.Module.value)
def _teardown_module(_teardown_package):
    yield _teardown_package
    _teardown_package.execute(Scope.Module)


@pytest.fixture(scope=Scope.Class.value)
def _teardown_class(_teardown_module):
    yield _teardown_module
    _teardown_module.execute(Scope.Class)


@pytest.fixture(scope=Scope.Function.value, autouse=True)
def _teardown_function(_teardown_class):
    yield _teardown_class
    _teardown_class.execute(Scope.Function)

import json
from pathlib import Path
from typing import Dict, Tuple

try:
    import docker
    from docker.errors import NotFound
except ImportError:
    pass
import pytest

from keycloak.realm import KeycloakRealm

# store history of failures per test class name and per index in parametrize
# (if parametrize used)
_test_failed_incremental: Dict[str, Dict[Tuple[int, ...], str]] = {}


def pytest_runtest_makereport(item, call):
    if "incremental" in item.keywords:
        # incremental marker is used
        if call.excinfo is not None:
            # the test has failed
            # retrieve the class name of the test
            cls_name = str(item.cls)
            # retrieve the index of the test
            # (if parametrize is used in combination with incremental)
            parametrize_index = (
                tuple(item.callspec.indices.values())
                if hasattr(item, "callspec")
                else ()
            )
            # retrieve the name of the test function
            test_name = item.originalname or item.name
            # store in _test_failed_incremental the original name of the failed test
            _test_failed_incremental.setdefault(cls_name, {}).setdefault(
                parametrize_index, test_name
            )


def pytest_runtest_setup(item):
    if "incremental" in item.keywords:
        # retrieve the class name of the test
        cls_name = str(item.cls)
        # check if a previous test has failed for this class
        if cls_name in _test_failed_incremental:
            # retrieve the index of the test
            # (if parametrize is used in combination with incremental)
            parametrize_index = (
                tuple(item.callspec.indices.values())
                if hasattr(item, "callspec")
                else ()
            )
            # retrieve the name of the first test function to fail for
            # this class name and index
            test_name = _test_failed_incremental[cls_name].get(parametrize_index, None)
            # if name found, test has failed for the combination of
            # class name & test name
            if test_name is not None:
                pytest.xfail("previous test failed ({})".format(test_name))


DATA_DIR = Path(__file__).parent / "data"


@pytest.fixture(scope="session")
def realm(pytestconfig) -> KeycloakRealm:

    server_port = pytestconfig.getoption("server_port", "8080")
    server_url = f"http://localhost:{server_port}"

    keycloak_user = pytestconfig.getoption("keycloak_user", "admin")
    keycloak_password = pytestconfig.getoption("keycloak_password", "admin")
    keycloak_image = pytestconfig.getoption(
        "keycloak_image", "jboss/keycloak:4.8.3.Final"
    )
    keycloak_container_name = pytestconfig.getoption("keycloak_container_name", "kc")
    realm_name = pytestconfig.getoption("realm_name", "test_realm")

    docker_client = docker.from_env()
    try:
        keycloak_container = docker_client.containers.get(keycloak_container_name)
    except NotFound:
        keycloak_container = docker_client.containers.run(
            keycloak_image,
            (
                "-b 0.0.0.0 "
                "-Dkeycloak.migration.action=import "
                "-Dkeycloak.migration.provider=dir "
                "-Dkeycloak.migration.dir=/tmp/ "
                "-Dkeycloak.migration.strategy=IGNORE_EXISTING"
            ),
            name=keycloak_container_name,
            remove=True,
            detach=True,
            volumes={str(DATA_DIR / "realms"): {"bind": "/tmp", "mode": "ro"}},
            ports={8080: 8080},
            environment={
                "KEYCLOAK_USER": keycloak_user,
                "KEYCLOAK_PASSWORD": keycloak_password,
                "KEYCLOAK_LOGLEVEL": "INFO",
            },
        )

        logs = keycloak_container.logs(stream=True)

        # Wait until the container is ready
        for line in logs:
            if "Admin console listening on http://127.0.0.1" in str(line):
                break

    yield KeycloakRealm(server_url=server_url, realm_name=realm_name)

    keycloak_container.kill()


@pytest.fixture(scope="session")
def openid_connect(realm: KeycloakRealm, client_details: Dict):
    return realm.open_id_connect(
        client_id=client_details["clientId"], client_secret=client_details["secret"]
    )


@pytest.fixture(scope="session")
def realm_details():
    return json.load((DATA_DIR / "realms" / "test_realm-realm.json").open("r"))


@pytest.fixture(scope="session")
def client_details(realm_details):
    for client in realm_details["clients"]:
        if client["clientId"] == "test_client":
            return client

    return None

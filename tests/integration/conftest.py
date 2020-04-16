import json
from pathlib import Path
from typing import Dict

import docker
import pytest

from keycloak.realm import KeycloakRealm

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
    realm_name = pytestconfig.getoption("realm_name", "test_realm")

    if True:

        docker_client = docker.from_env()
        keycloak_container = docker_client.containers.run(
            keycloak_image,
            (
                "-b 0.0.0.0 "
                "-Dkeycloak.migration.action=import "
                "-Dkeycloak.migration.provider=dir "
                "-Dkeycloak.migration.dir=/tmp/ "
                "-Dkeycloak.migration.strategy=IGNORE_EXISTING"
            ),
            name="kc",
            remove=True,
            detach=True,
            volumes={str(DATA_DIR / "realms"): {"bind": "/tmp", "mode": "ro"}},
            ports={8080: 8080},
            environment={
                "KEYCLOAK_USER": keycloak_user,
                "KEYCLOAK_PASSWORD": keycloak_password,
            },
        )

        logs = keycloak_container.logs(stream=True)

        # Wait until the container is ready
        for line in logs:
            if "Admin console listening on http://127.0.0.1" in str(line):
                break

    yield KeycloakRealm(server_url=server_url, realm_name=realm_name)

    keycloak_container.kill()


@pytest.fixture()
def openid_connect(realm: KeycloakRealm, client_details: Dict):
    return realm.open_id_connect(
        client_id=client_details["clientId"], client_secret=client_details["secret"]
    )


@pytest.fixture
def realm_details():
    return json.load((DATA_DIR / "realms" / "test_realm-realm.json").open("r"))


@pytest.fixture
def client_details(realm_details):
    for client in realm_details["clients"]:
        if client["clientId"] == "test_client":
            return client

    return None

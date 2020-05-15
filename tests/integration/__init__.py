import pytest

docker = pytest.importorskip("docker", reason="Docker not available")

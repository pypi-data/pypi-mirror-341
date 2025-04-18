import json
import os
import subprocess

from grpc import ssl_channel_credentials
import ray
import requests
import yt.wrapper as yt

from tests.yt_instances import YtInstance


def test_ray_cli(ray_instance: str, test_data_path: str) -> None:
    status_process = subprocess.run(
        ["tractoray", "status", "--workdir", str(ray_instance), "--format", "json"],
        capture_output=True,
        text=True,
    )
    assert status_process.returncode == 0

    parsed_status = json.loads(status_process.stdout)
    submit_process = subprocess.run(
        [
            "ray",
            "job",
            "submit",
            "--working-dir",
            str(test_data_path),
            "--",
            "python3",
            "script.py",
        ],
        env={
            **os.environ,
            **parsed_status["cli"]["env"],
        },
        capture_output=True,
        text=True,
    )
    assert submit_process.returncode == 0
    for i in range(10):
        assert f"Task {i} has been completed on host" in submit_process.stdout
    assert " succeeded", status_process.stdout


def test_ray_dashboard(yt_instance: YtInstance, ray_instance: str) -> None:
    client = yt_instance.get_client()

    status_process = subprocess.run(
        ["tractoray", "status", "--workdir", str(ray_instance), "--format", "json"],
        capture_output=True,
        text=True,
    )
    assert status_process.returncode == 0

    parsed_status = json.loads(status_process.stdout)
    response = requests.get(
        parsed_status["dashboard_url"],
        headers={"Authorization": f"OAuth {yt.http_helpers.get_token(client=client)}"},
    )
    assert response.status_code == 200, response.text


def test_ray_client(ray_instance: str) -> None:
    status_process = subprocess.run(
        ["tractoray", "status", "--workdir", str(ray_instance), "--format", "json"],
        capture_output=True,
        text=True,
    )
    assert status_process.returncode == 0

    parsed_status = json.loads(status_process.stdout)
    ray_params = {
        "address": parsed_status["client"]["address"],
        "_metadata": parsed_status["client"]["metadata"],
    }
    if certs := os.environ.get("REQUESTS_CA_BUNDLE"):
        with open(certs, "rb") as f:
            trusted_certs = f.read()
        ray_params["_credentials"] = ssl_channel_credentials(
            root_certificates=trusted_certs,
        )
    ray.init(**ray_params)
    assert len(ray.nodes()) == 2
    ray.shutdown()


def test_ray_cluster_status_not_found(yt_path: str) -> None:
    status_process = subprocess.run(
        ["tractoray", "status", "--workdir", yt_path],
        capture_output=True,
        text=True,
    )
    assert status_process.returncode == 0
    assert "Ray cluster not found" in status_process.stdout

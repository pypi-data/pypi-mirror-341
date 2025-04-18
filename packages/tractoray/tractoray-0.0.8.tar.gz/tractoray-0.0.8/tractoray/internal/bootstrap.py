from dataclasses import dataclass
import logging
import os

import yt.wrapper as yt

from tractoray.internal.coordinator import (
    HeadCoordinatorFactory,
    WorkerCoordinatorFactory,
)
from tractoray.internal.ray import (
    HeadNode,
    WorkerNode,
)
from tractoray.ytpath import YtPath


_LOGGER = logging.getLogger(__name__)


@dataclass
class BootstrapperHead:
    _yt_client: yt.YtClient
    _workdir: YtPath
    _cpu_limit: int
    _node_count: int

    _node_index: int
    _operation_id: str
    _job_id: str

    _head_port: int
    _dashboard_port: int
    _dashboard_agent_listen_port: int
    _public_dashboard_port: int
    _client_port: int
    _runtime_env_agent_port: int

    def run(self) -> None:
        hostname = _get_hostname(
            yt_client=self._yt_client,
            job_id=self._job_id,
            operation_id=self._operation_id,
        )
        _fix_hosts(hostname=hostname)

        HeadCoordinatorFactory(
            _self_endpoint=hostname,
            _node_index=self._node_index,
            _node_count=self._node_count,
            _coordinator_path=_make_coordinator_path(self._workdir),
            _yt_client=self._yt_client,
            _operation_id=self._operation_id,
            _wait_barrier=True,
            _head_port=self._head_port,
            _public_dashboard_port=self._public_dashboard_port,
            _client_port=self._client_port,
        ).make()

        head_node = HeadNode(
            _self_endpoint=hostname,
            _cpu_limit=self._cpu_limit,
            _head_port=self._head_port,
            _dashboard_port=self._dashboard_port,
            _dashboard_agent_listen_port=self._dashboard_agent_listen_port,
            _client_port=self._client_port,
            _runtime_env_agent_port=self._runtime_env_agent_port,
            _yt_client=self._yt_client,
            _public_dashboard_port=self._public_dashboard_port,
        )
        head_node.run()


@dataclass
class BootstrapperNode:
    _yt_client: yt.YtClient
    _workdir: YtPath
    _cpu_limit: int
    _node_count: int

    _node_index: int
    _operation_id: str
    _job_id: str

    _runtime_env_agent_port: int

    def run(self) -> None:
        hostname = _get_hostname(
            yt_client=self._yt_client,
            job_id=self._job_id,
            operation_id=self._operation_id,
        )
        _fix_hosts(hostname=hostname)

        runtime_env_agent_port = int(os.environ["YT_PORT_0"])

        coordinator = WorkerCoordinatorFactory(
            _self_endpoint=hostname,
            _node_index=self._node_index,
            _node_count=self._node_count,
            _coordinator_path=_make_coordinator_path(self._workdir),
            _yt_client=self._yt_client,
            _operation_id=self._operation_id,
            _wait_barrier=True,
        ).make()

        WorkerNode(
            _cpu_limit=self._cpu_limit,
            _head_endpoint=coordinator.head_endpoint,
            _head_port=coordinator.head_port,
            _self_endpoint=hostname,
            _runtime_env_agent_port=runtime_env_agent_port,
        ).run()


def _make_coordinator_path(workdir: YtPath) -> YtPath:
    return YtPath(f"{workdir}/coordinator")


def _get_hostname(operation_id: str, job_id: str, yt_client: yt.YtClient) -> str:
    return str(
        yt_client.get_job(operation_id=operation_id, job_id=job_id)["address"]
    ).split(":")[0]


def _fix_hosts(hostname: str) -> None:
    with open("/etc/hosts", "a") as f:
        f.write(f"\n127.0.0.1\t{hostname}\n")

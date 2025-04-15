# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .activate.activate_builder import ActivateBuilder
    from .cluster_info.cluster_info_builder import ClusterInfoBuilder
    from .dbrestorestatus.dbrestorestatus_builder import DbrestorestatusBuilder
    from .delete_local_data_center.delete_local_data_center_builder import (
        DeleteLocalDataCenterBuilder,
    )
    from .delete_remote_data_center.delete_remote_data_center_builder import (
        DeleteRemoteDataCenterBuilder,
    )
    from .deregister.deregister_builder import DeregisterBuilder
    from .details.details_builder import DetailsBuilder
    from .drstatus.drstatus_builder import DrstatusBuilder
    from .history.history_builder import HistoryBuilder
    from .local_latest_history.local_latest_history_builder import LocalLatestHistoryBuilder
    from .localdc.localdc_builder import LocaldcBuilder
    from .password.password_builder import PasswordBuilder
    from .pause.pause_builder import PauseBuilder
    from .pause_local_arbitrator.pause_local_arbitrator_builder import PauseLocalArbitratorBuilder
    from .pause_local_dc.pause_local_dc_builder import PauseLocalDcBuilder
    from .pause_local_replication.pause_local_replication_builder import (
        PauseLocalReplicationBuilder,
    )
    from .pausereplication.pausereplication_builder import PausereplicationBuilder
    from .register.register_builder import RegisterBuilder
    from .remote_dc_state.remote_dc_state_builder import RemoteDcStateBuilder
    from .remotedc.remotedc_builder import RemotedcBuilder
    from .schedule.schedule_builder import ScheduleBuilder
    from .status.status_builder import StatusBuilder
    from .unpause.unpause_builder import UnpauseBuilder
    from .unpause_local_arbitrator.unpause_local_arbitrator_builder import (
        UnpauseLocalArbitratorBuilder,
    )
    from .unpause_local_dc.unpause_local_dc_builder import UnpauseLocalDcBuilder
    from .unpause_local_replication.unpause_local_replication_builder import (
        UnpauseLocalReplicationBuilder,
    )
    from .unpausereplication.unpausereplication_builder import UnpausereplicationBuilder
    from .update_dr_config_on_arbitrator.update_dr_config_on_arbitrator_builder import (
        UpdateDrConfigOnArbitratorBuilder,
    )
    from .usernames.usernames_builder import UsernamesBuilder


class DisasterrecoveryBuilder:
    """
    Builds and executes requests for operations under /disasterrecovery
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def activate(self) -> ActivateBuilder:
        """
        The activate property
        """
        from .activate.activate_builder import ActivateBuilder

        return ActivateBuilder(self._request_adapter)

    @property
    def cluster_info(self) -> ClusterInfoBuilder:
        """
        The clusterInfo property
        """
        from .cluster_info.cluster_info_builder import ClusterInfoBuilder

        return ClusterInfoBuilder(self._request_adapter)

    @property
    def dbrestorestatus(self) -> DbrestorestatusBuilder:
        """
        The dbrestorestatus property
        """
        from .dbrestorestatus.dbrestorestatus_builder import DbrestorestatusBuilder

        return DbrestorestatusBuilder(self._request_adapter)

    @property
    def delete_local_data_center(self) -> DeleteLocalDataCenterBuilder:
        """
        The deleteLocalDataCenter property
        """
        from .delete_local_data_center.delete_local_data_center_builder import (
            DeleteLocalDataCenterBuilder,
        )

        return DeleteLocalDataCenterBuilder(self._request_adapter)

    @property
    def delete_remote_data_center(self) -> DeleteRemoteDataCenterBuilder:
        """
        The deleteRemoteDataCenter property
        """
        from .delete_remote_data_center.delete_remote_data_center_builder import (
            DeleteRemoteDataCenterBuilder,
        )

        return DeleteRemoteDataCenterBuilder(self._request_adapter)

    @property
    def deregister(self) -> DeregisterBuilder:
        """
        The deregister property
        """
        from .deregister.deregister_builder import DeregisterBuilder

        return DeregisterBuilder(self._request_adapter)

    @property
    def details(self) -> DetailsBuilder:
        """
        The details property
        """
        from .details.details_builder import DetailsBuilder

        return DetailsBuilder(self._request_adapter)

    @property
    def drstatus(self) -> DrstatusBuilder:
        """
        The drstatus property
        """
        from .drstatus.drstatus_builder import DrstatusBuilder

        return DrstatusBuilder(self._request_adapter)

    @property
    def history(self) -> HistoryBuilder:
        """
        The history property
        """
        from .history.history_builder import HistoryBuilder

        return HistoryBuilder(self._request_adapter)

    @property
    def local_latest_history(self) -> LocalLatestHistoryBuilder:
        """
        The localLatestHistory property
        """
        from .local_latest_history.local_latest_history_builder import LocalLatestHistoryBuilder

        return LocalLatestHistoryBuilder(self._request_adapter)

    @property
    def localdc(self) -> LocaldcBuilder:
        """
        The localdc property
        """
        from .localdc.localdc_builder import LocaldcBuilder

        return LocaldcBuilder(self._request_adapter)

    @property
    def password(self) -> PasswordBuilder:
        """
        The password property
        """
        from .password.password_builder import PasswordBuilder

        return PasswordBuilder(self._request_adapter)

    @property
    def pause(self) -> PauseBuilder:
        """
        The pause property
        """
        from .pause.pause_builder import PauseBuilder

        return PauseBuilder(self._request_adapter)

    @property
    def pause_local_arbitrator(self) -> PauseLocalArbitratorBuilder:
        """
        The pauseLocalArbitrator property
        """
        from .pause_local_arbitrator.pause_local_arbitrator_builder import (
            PauseLocalArbitratorBuilder,
        )

        return PauseLocalArbitratorBuilder(self._request_adapter)

    @property
    def pause_local_dc(self) -> PauseLocalDcBuilder:
        """
        The pauseLocalDC property
        """
        from .pause_local_dc.pause_local_dc_builder import PauseLocalDcBuilder

        return PauseLocalDcBuilder(self._request_adapter)

    @property
    def pause_local_replication(self) -> PauseLocalReplicationBuilder:
        """
        The pauseLocalReplication property
        """
        from .pause_local_replication.pause_local_replication_builder import (
            PauseLocalReplicationBuilder,
        )

        return PauseLocalReplicationBuilder(self._request_adapter)

    @property
    def pausereplication(self) -> PausereplicationBuilder:
        """
        The pausereplication property
        """
        from .pausereplication.pausereplication_builder import PausereplicationBuilder

        return PausereplicationBuilder(self._request_adapter)

    @property
    def register(self) -> RegisterBuilder:
        """
        The register property
        """
        from .register.register_builder import RegisterBuilder

        return RegisterBuilder(self._request_adapter)

    @property
    def remote_dc_state(self) -> RemoteDcStateBuilder:
        """
        The remoteDcState property
        """
        from .remote_dc_state.remote_dc_state_builder import RemoteDcStateBuilder

        return RemoteDcStateBuilder(self._request_adapter)

    @property
    def remotedc(self) -> RemotedcBuilder:
        """
        The remotedc property
        """
        from .remotedc.remotedc_builder import RemotedcBuilder

        return RemotedcBuilder(self._request_adapter)

    @property
    def schedule(self) -> ScheduleBuilder:
        """
        The schedule property
        """
        from .schedule.schedule_builder import ScheduleBuilder

        return ScheduleBuilder(self._request_adapter)

    @property
    def status(self) -> StatusBuilder:
        """
        The status property
        """
        from .status.status_builder import StatusBuilder

        return StatusBuilder(self._request_adapter)

    @property
    def unpause(self) -> UnpauseBuilder:
        """
        The unpause property
        """
        from .unpause.unpause_builder import UnpauseBuilder

        return UnpauseBuilder(self._request_adapter)

    @property
    def unpause_local_arbitrator(self) -> UnpauseLocalArbitratorBuilder:
        """
        The unpauseLocalArbitrator property
        """
        from .unpause_local_arbitrator.unpause_local_arbitrator_builder import (
            UnpauseLocalArbitratorBuilder,
        )

        return UnpauseLocalArbitratorBuilder(self._request_adapter)

    @property
    def unpause_local_dc(self) -> UnpauseLocalDcBuilder:
        """
        The unpauseLocalDC property
        """
        from .unpause_local_dc.unpause_local_dc_builder import UnpauseLocalDcBuilder

        return UnpauseLocalDcBuilder(self._request_adapter)

    @property
    def unpause_local_replication(self) -> UnpauseLocalReplicationBuilder:
        """
        The unpauseLocalReplication property
        """
        from .unpause_local_replication.unpause_local_replication_builder import (
            UnpauseLocalReplicationBuilder,
        )

        return UnpauseLocalReplicationBuilder(self._request_adapter)

    @property
    def unpausereplication(self) -> UnpausereplicationBuilder:
        """
        The unpausereplication property
        """
        from .unpausereplication.unpausereplication_builder import UnpausereplicationBuilder

        return UnpausereplicationBuilder(self._request_adapter)

    @property
    def update_dr_config_on_arbitrator(self) -> UpdateDrConfigOnArbitratorBuilder:
        """
        The updateDRConfigOnArbitrator property
        """
        from .update_dr_config_on_arbitrator.update_dr_config_on_arbitrator_builder import (
            UpdateDrConfigOnArbitratorBuilder,
        )

        return UpdateDrConfigOnArbitratorBuilder(self._request_adapter)

    @property
    def usernames(self) -> UsernamesBuilder:
        """
        The usernames property
        """
        from .usernames.usernames_builder import UsernamesBuilder

        return UsernamesBuilder(self._request_adapter)

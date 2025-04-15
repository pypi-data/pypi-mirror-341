# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .certdetails.certdetails_builder import CertdetailsBuilder
    from .controller.controller_builder import ControllerBuilder
    from .csr.csr_builder import CsrBuilder
    from .device.device_builder import DeviceBuilder
    from .forcesync.forcesync_builder import ForcesyncBuilder
    from .generate.generate_builder import GenerateBuilder
    from .install.install_builder import InstallBuilder
    from .jks.jks_builder import JksBuilder
    from .list.list_builder import ListBuilder
    from .mthub.mthub_builder import MthubBuilder
    from .record.record_builder import RecordBuilder
    from .reset.reset_builder import ResetBuilder
    from .revoke.revoke_builder import RevokeBuilder
    from .rootcertchains.rootcertchains_builder import RootcertchainsBuilder
    from .rootcertificate.rootcertificate_builder import RootcertificateBuilder
    from .rsakeylengthdefault.rsakeylengthdefault_builder import RsakeylengthdefaultBuilder
    from .save.save_builder import SaveBuilder
    from .stats.stats_builder import StatsBuilder
    from .syncvbond.syncvbond_builder import SyncvbondBuilder
    from .tokengeneratedlist.tokengeneratedlist_builder import TokengeneratedlistBuilder
    from .vedge.vedge_builder import VedgeBuilder
    from .view.view_builder import ViewBuilder
    from .vmanage.vmanage_builder import VmanageBuilder
    from .vsmart.vsmart_builder import VsmartBuilder


class CertificateBuilder:
    """
    Builds and executes requests for operations under /certificate
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def delete(
        self,
        uuid: str,
        replace_controller: Optional[bool] = None,
        device_id: Optional[str] = None,
        **kw,
    ) -> str:
        """
        invalid device
        DELETE /dataservice/certificate/{uuid}

        :param uuid: Uuid
        :param replace_controller: Replace controller
        :param device_id: Device id
        :returns: str
        """
        params = {
            "uuid": uuid,
            "replaceController": replace_controller,
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "DELETE", "/dataservice/certificate/{uuid}", return_type=str, params=params, **kw
        )

    @property
    def certdetails(self) -> CertdetailsBuilder:
        """
        The certdetails property
        """
        from .certdetails.certdetails_builder import CertdetailsBuilder

        return CertdetailsBuilder(self._request_adapter)

    @property
    def controller(self) -> ControllerBuilder:
        """
        The controller property
        """
        from .controller.controller_builder import ControllerBuilder

        return ControllerBuilder(self._request_adapter)

    @property
    def csr(self) -> CsrBuilder:
        """
        The csr property
        """
        from .csr.csr_builder import CsrBuilder

        return CsrBuilder(self._request_adapter)

    @property
    def device(self) -> DeviceBuilder:
        """
        The device property
        """
        from .device.device_builder import DeviceBuilder

        return DeviceBuilder(self._request_adapter)

    @property
    def forcesync(self) -> ForcesyncBuilder:
        """
        The forcesync property
        """
        from .forcesync.forcesync_builder import ForcesyncBuilder

        return ForcesyncBuilder(self._request_adapter)

    @property
    def generate(self) -> GenerateBuilder:
        """
        The generate property
        """
        from .generate.generate_builder import GenerateBuilder

        return GenerateBuilder(self._request_adapter)

    @property
    def install(self) -> InstallBuilder:
        """
        The install property
        """
        from .install.install_builder import InstallBuilder

        return InstallBuilder(self._request_adapter)

    @property
    def jks(self) -> JksBuilder:
        """
        The jks property
        """
        from .jks.jks_builder import JksBuilder

        return JksBuilder(self._request_adapter)

    @property
    def list(self) -> ListBuilder:
        """
        The list property
        """
        from .list.list_builder import ListBuilder

        return ListBuilder(self._request_adapter)

    @property
    def mthub(self) -> MthubBuilder:
        """
        The mthub property
        """
        from .mthub.mthub_builder import MthubBuilder

        return MthubBuilder(self._request_adapter)

    @property
    def record(self) -> RecordBuilder:
        """
        The record property
        """
        from .record.record_builder import RecordBuilder

        return RecordBuilder(self._request_adapter)

    @property
    def reset(self) -> ResetBuilder:
        """
        The reset property
        """
        from .reset.reset_builder import ResetBuilder

        return ResetBuilder(self._request_adapter)

    @property
    def revoke(self) -> RevokeBuilder:
        """
        The revoke property
        """
        from .revoke.revoke_builder import RevokeBuilder

        return RevokeBuilder(self._request_adapter)

    @property
    def rootcertchains(self) -> RootcertchainsBuilder:
        """
        The rootcertchains property
        """
        from .rootcertchains.rootcertchains_builder import RootcertchainsBuilder

        return RootcertchainsBuilder(self._request_adapter)

    @property
    def rootcertificate(self) -> RootcertificateBuilder:
        """
        The rootcertificate property
        """
        from .rootcertificate.rootcertificate_builder import RootcertificateBuilder

        return RootcertificateBuilder(self._request_adapter)

    @property
    def rsakeylengthdefault(self) -> RsakeylengthdefaultBuilder:
        """
        The rsakeylengthdefault property
        """
        from .rsakeylengthdefault.rsakeylengthdefault_builder import RsakeylengthdefaultBuilder

        return RsakeylengthdefaultBuilder(self._request_adapter)

    @property
    def save(self) -> SaveBuilder:
        """
        The save property
        """
        from .save.save_builder import SaveBuilder

        return SaveBuilder(self._request_adapter)

    @property
    def stats(self) -> StatsBuilder:
        """
        The stats property
        """
        from .stats.stats_builder import StatsBuilder

        return StatsBuilder(self._request_adapter)

    @property
    def syncvbond(self) -> SyncvbondBuilder:
        """
        The syncvbond property
        """
        from .syncvbond.syncvbond_builder import SyncvbondBuilder

        return SyncvbondBuilder(self._request_adapter)

    @property
    def tokengeneratedlist(self) -> TokengeneratedlistBuilder:
        """
        The tokengeneratedlist property
        """
        from .tokengeneratedlist.tokengeneratedlist_builder import TokengeneratedlistBuilder

        return TokengeneratedlistBuilder(self._request_adapter)

    @property
    def vedge(self) -> VedgeBuilder:
        """
        The vedge property
        """
        from .vedge.vedge_builder import VedgeBuilder

        return VedgeBuilder(self._request_adapter)

    @property
    def view(self) -> ViewBuilder:
        """
        The view property
        """
        from .view.view_builder import ViewBuilder

        return ViewBuilder(self._request_adapter)

    @property
    def vmanage(self) -> VmanageBuilder:
        """
        The vmanage property
        """
        from .vmanage.vmanage_builder import VmanageBuilder

        return VmanageBuilder(self._request_adapter)

    @property
    def vsmart(self) -> VsmartBuilder:
        """
        The vsmart property
        """
        from .vsmart.vsmart_builder import VsmartBuilder

        return VsmartBuilder(self._request_adapter)

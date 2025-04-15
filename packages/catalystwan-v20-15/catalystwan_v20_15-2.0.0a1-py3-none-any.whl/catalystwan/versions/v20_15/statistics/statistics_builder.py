# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .aggregation.aggregation_builder import AggregationBuilder
    from .app_agg.app_agg_builder import AppAggBuilder
    from .apphosting.apphosting_builder import ApphostingBuilder
    from .apphostinginterface.apphostinginterface_builder import ApphostinginterfaceBuilder
    from .approute.approute_builder import ApprouteBuilder
    from .art.art_builder import ArtBuilder
    from .bfd.bfd_builder import BfdBuilder
    from .bridgeinterface.bridgeinterface_builder import BridgeinterfaceBuilder
    from .bridgemac.bridgemac_builder import BridgemacBuilder
    from .cflowd.cflowd_builder import CflowdBuilder
    from .cloudx.cloudx_builder import CloudxBuilder
    from .collect.collect_builder import CollectBuilder
    from .collection.collection_builder import CollectionBuilder
    from .csv.csv_builder import CsvBuilder
    from .demomode.demomode_builder import DemomodeBuilder
    from .device.device_builder import DeviceBuilder
    from .devicehealth.devicehealth_builder import DevicehealthBuilder
    from .doccount.doccount_builder import DoccountBuilder
    from .download.download_builder import DownloadBuilder
    from .dpi.dpi_builder import DpiBuilder
    from .eiolte.eiolte_builder import EiolteBuilder
    from .endpoint_tracker.endpoint_tracker_builder import EndpointTrackerBuilder
    from .fields.fields_builder import FieldsBuilder
    from .flowlog.flowlog_builder import FlowlogBuilder
    from .fwall.fwall_builder import FwallBuilder
    from .interface.interface_builder import InterfaceBuilder
    from .ipsalert.ipsalert_builder import IpsalertBuilder
    from .nwa.nwa_builder import NwaBuilder
    from .on_demand.on_demand_builder import OnDemandBuilder
    from .page.page_builder import PageBuilder
    from .perfmon.perfmon_builder import PerfmonBuilder
    from .process.process_builder import ProcessBuilder
    from .qos.qos_builder import QosBuilder
    from .query.query_builder import QueryBuilder
    from .sdra.sdra_builder import SdraBuilder
    from .settings.settings_builder import SettingsBuilder
    from .sitehealth.sitehealth_builder import SitehealthBuilder
    from .speedtest.speedtest_builder import SpeedtestBuilder
    from .sul.sul_builder import SulBuilder
    from .system.system_builder import SystemBuilder
    from .tunnelhealth.tunnelhealth_builder import TunnelhealthBuilder
    from .umbrella.umbrella_builder import UmbrellaBuilder
    from .urlf.urlf_builder import UrlfBuilder
    from .vnfstatistics.vnfstatistics_builder import VnfstatisticsBuilder
    from .wlanclientinfo.wlanclientinfo_builder import WlanclientinfoBuilder


class StatisticsBuilder:
    """
    Builds and executes requests for operations under /statistics
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[Any]:
        """
        Get statistics types
        GET /dataservice/statistics

        :returns: List[Any]
        """
        return self._request_adapter.request(
            "GET", "/dataservice/statistics", return_type=List[Any], **kw
        )

    def post(
        self,
        payload: Any,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = None,
        **kw,
    ) -> Any:
        """
        Get stats raw data
        POST /dataservice/statistics

        :param page: page number
        :param page_size: page size
        :param sort_by: sort by
        :param sort_order: sort order
        :param payload: Stats query string
        :returns: Any
        """
        params = {
            "page": page,
            "pageSize": page_size,
            "sortBy": sort_by,
            "sortOrder": sort_order,
        }
        return self._request_adapter.request(
            "POST", "/dataservice/statistics", params=params, payload=payload, **kw
        )

    @property
    def aggregation(self) -> AggregationBuilder:
        """
        The aggregation property
        """
        from .aggregation.aggregation_builder import AggregationBuilder

        return AggregationBuilder(self._request_adapter)

    @property
    def app_agg(self) -> AppAggBuilder:
        """
        The app-agg property
        """
        from .app_agg.app_agg_builder import AppAggBuilder

        return AppAggBuilder(self._request_adapter)

    @property
    def apphosting(self) -> ApphostingBuilder:
        """
        The apphosting property
        """
        from .apphosting.apphosting_builder import ApphostingBuilder

        return ApphostingBuilder(self._request_adapter)

    @property
    def apphostinginterface(self) -> ApphostinginterfaceBuilder:
        """
        The apphostinginterface property
        """
        from .apphostinginterface.apphostinginterface_builder import ApphostinginterfaceBuilder

        return ApphostinginterfaceBuilder(self._request_adapter)

    @property
    def approute(self) -> ApprouteBuilder:
        """
        The approute property
        """
        from .approute.approute_builder import ApprouteBuilder

        return ApprouteBuilder(self._request_adapter)

    @property
    def art(self) -> ArtBuilder:
        """
        The art property
        """
        from .art.art_builder import ArtBuilder

        return ArtBuilder(self._request_adapter)

    @property
    def bfd(self) -> BfdBuilder:
        """
        The bfd property
        """
        from .bfd.bfd_builder import BfdBuilder

        return BfdBuilder(self._request_adapter)

    @property
    def bridgeinterface(self) -> BridgeinterfaceBuilder:
        """
        The bridgeinterface property
        """
        from .bridgeinterface.bridgeinterface_builder import BridgeinterfaceBuilder

        return BridgeinterfaceBuilder(self._request_adapter)

    @property
    def bridgemac(self) -> BridgemacBuilder:
        """
        The bridgemac property
        """
        from .bridgemac.bridgemac_builder import BridgemacBuilder

        return BridgemacBuilder(self._request_adapter)

    @property
    def cflowd(self) -> CflowdBuilder:
        """
        The cflowd property
        """
        from .cflowd.cflowd_builder import CflowdBuilder

        return CflowdBuilder(self._request_adapter)

    @property
    def cloudx(self) -> CloudxBuilder:
        """
        The cloudx property
        """
        from .cloudx.cloudx_builder import CloudxBuilder

        return CloudxBuilder(self._request_adapter)

    @property
    def collect(self) -> CollectBuilder:
        """
        The collect property
        """
        from .collect.collect_builder import CollectBuilder

        return CollectBuilder(self._request_adapter)

    @property
    def collection(self) -> CollectionBuilder:
        """
        The collection property
        """
        from .collection.collection_builder import CollectionBuilder

        return CollectionBuilder(self._request_adapter)

    @property
    def csv(self) -> CsvBuilder:
        """
        The csv property
        """
        from .csv.csv_builder import CsvBuilder

        return CsvBuilder(self._request_adapter)

    @property
    def demomode(self) -> DemomodeBuilder:
        """
        The demomode property
        """
        from .demomode.demomode_builder import DemomodeBuilder

        return DemomodeBuilder(self._request_adapter)

    @property
    def device(self) -> DeviceBuilder:
        """
        The device property
        """
        from .device.device_builder import DeviceBuilder

        return DeviceBuilder(self._request_adapter)

    @property
    def devicehealth(self) -> DevicehealthBuilder:
        """
        The devicehealth property
        """
        from .devicehealth.devicehealth_builder import DevicehealthBuilder

        return DevicehealthBuilder(self._request_adapter)

    @property
    def doccount(self) -> DoccountBuilder:
        """
        The doccount property
        """
        from .doccount.doccount_builder import DoccountBuilder

        return DoccountBuilder(self._request_adapter)

    @property
    def download(self) -> DownloadBuilder:
        """
        The download property
        """
        from .download.download_builder import DownloadBuilder

        return DownloadBuilder(self._request_adapter)

    @property
    def dpi(self) -> DpiBuilder:
        """
        The dpi property
        """
        from .dpi.dpi_builder import DpiBuilder

        return DpiBuilder(self._request_adapter)

    @property
    def eiolte(self) -> EiolteBuilder:
        """
        The eiolte property
        """
        from .eiolte.eiolte_builder import EiolteBuilder

        return EiolteBuilder(self._request_adapter)

    @property
    def endpoint_tracker(self) -> EndpointTrackerBuilder:
        """
        The endpointTracker property
        """
        from .endpoint_tracker.endpoint_tracker_builder import EndpointTrackerBuilder

        return EndpointTrackerBuilder(self._request_adapter)

    @property
    def fields(self) -> FieldsBuilder:
        """
        The fields property
        """
        from .fields.fields_builder import FieldsBuilder

        return FieldsBuilder(self._request_adapter)

    @property
    def flowlog(self) -> FlowlogBuilder:
        """
        The flowlog property
        """
        from .flowlog.flowlog_builder import FlowlogBuilder

        return FlowlogBuilder(self._request_adapter)

    @property
    def fwall(self) -> FwallBuilder:
        """
        The fwall property
        """
        from .fwall.fwall_builder import FwallBuilder

        return FwallBuilder(self._request_adapter)

    @property
    def interface(self) -> InterfaceBuilder:
        """
        The interface property
        """
        from .interface.interface_builder import InterfaceBuilder

        return InterfaceBuilder(self._request_adapter)

    @property
    def ipsalert(self) -> IpsalertBuilder:
        """
        The ipsalert property
        """
        from .ipsalert.ipsalert_builder import IpsalertBuilder

        return IpsalertBuilder(self._request_adapter)

    @property
    def nwa(self) -> NwaBuilder:
        """
        The nwa property
        """
        from .nwa.nwa_builder import NwaBuilder

        return NwaBuilder(self._request_adapter)

    @property
    def on_demand(self) -> OnDemandBuilder:
        """
        The on-demand property
        """
        from .on_demand.on_demand_builder import OnDemandBuilder

        return OnDemandBuilder(self._request_adapter)

    @property
    def page(self) -> PageBuilder:
        """
        The page property
        """
        from .page.page_builder import PageBuilder

        return PageBuilder(self._request_adapter)

    @property
    def perfmon(self) -> PerfmonBuilder:
        """
        The perfmon property
        """
        from .perfmon.perfmon_builder import PerfmonBuilder

        return PerfmonBuilder(self._request_adapter)

    @property
    def process(self) -> ProcessBuilder:
        """
        The process property
        """
        from .process.process_builder import ProcessBuilder

        return ProcessBuilder(self._request_adapter)

    @property
    def qos(self) -> QosBuilder:
        """
        The qos property
        """
        from .qos.qos_builder import QosBuilder

        return QosBuilder(self._request_adapter)

    @property
    def query(self) -> QueryBuilder:
        """
        The query property
        """
        from .query.query_builder import QueryBuilder

        return QueryBuilder(self._request_adapter)

    @property
    def sdra(self) -> SdraBuilder:
        """
        The sdra property
        """
        from .sdra.sdra_builder import SdraBuilder

        return SdraBuilder(self._request_adapter)

    @property
    def settings(self) -> SettingsBuilder:
        """
        The settings property
        """
        from .settings.settings_builder import SettingsBuilder

        return SettingsBuilder(self._request_adapter)

    @property
    def sitehealth(self) -> SitehealthBuilder:
        """
        The sitehealth property
        """
        from .sitehealth.sitehealth_builder import SitehealthBuilder

        return SitehealthBuilder(self._request_adapter)

    @property
    def speedtest(self) -> SpeedtestBuilder:
        """
        The speedtest property
        """
        from .speedtest.speedtest_builder import SpeedtestBuilder

        return SpeedtestBuilder(self._request_adapter)

    @property
    def sul(self) -> SulBuilder:
        """
        The sul property
        """
        from .sul.sul_builder import SulBuilder

        return SulBuilder(self._request_adapter)

    @property
    def system(self) -> SystemBuilder:
        """
        The system property
        """
        from .system.system_builder import SystemBuilder

        return SystemBuilder(self._request_adapter)

    @property
    def tunnelhealth(self) -> TunnelhealthBuilder:
        """
        The tunnelhealth property
        """
        from .tunnelhealth.tunnelhealth_builder import TunnelhealthBuilder

        return TunnelhealthBuilder(self._request_adapter)

    @property
    def umbrella(self) -> UmbrellaBuilder:
        """
        The umbrella property
        """
        from .umbrella.umbrella_builder import UmbrellaBuilder

        return UmbrellaBuilder(self._request_adapter)

    @property
    def urlf(self) -> UrlfBuilder:
        """
        The urlf property
        """
        from .urlf.urlf_builder import UrlfBuilder

        return UrlfBuilder(self._request_adapter)

    @property
    def vnfstatistics(self) -> VnfstatisticsBuilder:
        """
        The vnfstatistics property
        """
        from .vnfstatistics.vnfstatistics_builder import VnfstatisticsBuilder

        return VnfstatisticsBuilder(self._request_adapter)

    @property
    def wlanclientinfo(self) -> WlanclientinfoBuilder:
        """
        The wlanclientinfo property
        """
        from .wlanclientinfo.wlanclientinfo_builder import WlanclientinfoBuilder

        return WlanclientinfoBuilder(self._request_adapter)

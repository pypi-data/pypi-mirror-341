# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .active_flow_with_query.active_flow_with_query_builder import ActiveFlowWithQueryBuilder
    from .agg_flow.agg_flow_builder import AggFlowBuilder
    from .app_qos_data.app_qos_data_builder import AppQosDataBuilder
    from .app_qos_state.app_qos_state_builder import AppQosStateBuilder
    from .concurrent_data.concurrent_data_builder import ConcurrentDataBuilder
    from .concurrent_domain_data.concurrent_domain_data_builder import ConcurrentDomainDataBuilder
    from .current_timestamp.current_timestamp_builder import CurrentTimestampBuilder
    from .device.device_builder import DeviceBuilder
    from .device_info_by_site.device_info_by_site_builder import DeviceInfoBySiteBuilder
    from .domain_metric.domain_metric_builder import DomainMetricBuilder
    from .event_app_hop_list.event_app_hop_list_builder import EventAppHopListBuilder
    from .event_app_score_bandwidth.event_app_score_bandwidth_builder import (
        EventAppScoreBandwidthBuilder,
    )
    from .event_flow_from_app_hop.event_flow_from_app_hop_builder import EventFlowFromAppHopBuilder
    from .event_readout.event_readout_builder import EventReadoutBuilder
    from .event_readout_by_site.event_readout_by_site_builder import EventReadoutBySiteBuilder
    from .event_readout_by_traces.event_readout_by_traces_builder import EventReadoutByTracesBuilder
    from .export_trace.export_trace_builder import ExportTraceBuilder
    from .finalized_data.finalized_data_builder import FinalizedDataBuilder
    from .finalized_domain_data.finalized_domain_data_builder import FinalizedDomainDataBuilder
    from .flow_detail.flow_detail_builder import FlowDetailBuilder
    from .flow_metric.flow_metric_builder import FlowMetricBuilder
    from .get_monitor_state.get_monitor_state_builder import GetMonitorStateBuilder
    from .import_trace.import_trace_builder import ImportTraceBuilder
    from .monitor.monitor_builder import MonitorBuilder
    from .nwpi_dscp.nwpi_dscp_builder import NwpiDscpBuilder
    from .nwpi_nbar_app_group.nwpi_nbar_app_group_builder import NwpiNbarAppGroupBuilder
    from .nwpi_protocol.nwpi_protocol_builder import NwpiProtocolBuilder
    from .nwpi_setting_view.nwpi_setting_view_builder import NwpiSettingViewBuilder
    from .packet_features.packet_features_builder import PacketFeaturesBuilder
    from .preloadinfo.preloadinfo_builder import PreloadinfoBuilder
    from .query.query_builder import QueryBuilder
    from .routing_detail.routing_detail_builder import RoutingDetailBuilder
    from .tasks.tasks_builder import TasksBuilder
    from .trace.trace_builder import TraceBuilder
    from .trace_cft_record.trace_cft_record_builder import TraceCftRecordBuilder
    from .trace_fin_flow_count.trace_fin_flow_count_builder import TraceFinFlowCountBuilder
    from .trace_fin_flow_time_range.trace_fin_flow_time_range_builder import (
        TraceFinFlowTimeRangeBuilder,
    )
    from .trace_fin_flow_with_query.trace_fin_flow_with_query_builder import (
        TraceFinFlowWithQueryBuilder,
    )
    from .trace_flow.trace_flow_builder import TraceFlowBuilder
    from .trace_history.trace_history_builder import TraceHistoryBuilder
    from .trace_info_by_base_key.trace_info_by_base_key_builder import TraceInfoByBaseKeyBuilder
    from .trace_readout_filter.trace_readout_filter_builder import TraceReadoutFilterBuilder
    from .upsert_setting.upsert_setting_builder import UpsertSettingBuilder


class NwpiBuilder:
    """
    Builds and executes requests for operations under /stream/device/nwpi
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def active_flow_with_query(self) -> ActiveFlowWithQueryBuilder:
        """
        The activeFlowWithQuery property
        """
        from .active_flow_with_query.active_flow_with_query_builder import (
            ActiveFlowWithQueryBuilder,
        )

        return ActiveFlowWithQueryBuilder(self._request_adapter)

    @property
    def agg_flow(self) -> AggFlowBuilder:
        """
        The aggFlow property
        """
        from .agg_flow.agg_flow_builder import AggFlowBuilder

        return AggFlowBuilder(self._request_adapter)

    @property
    def app_qos_data(self) -> AppQosDataBuilder:
        """
        The appQosData property
        """
        from .app_qos_data.app_qos_data_builder import AppQosDataBuilder

        return AppQosDataBuilder(self._request_adapter)

    @property
    def app_qos_state(self) -> AppQosStateBuilder:
        """
        The appQosState property
        """
        from .app_qos_state.app_qos_state_builder import AppQosStateBuilder

        return AppQosStateBuilder(self._request_adapter)

    @property
    def concurrent_data(self) -> ConcurrentDataBuilder:
        """
        The concurrentData property
        """
        from .concurrent_data.concurrent_data_builder import ConcurrentDataBuilder

        return ConcurrentDataBuilder(self._request_adapter)

    @property
    def concurrent_domain_data(self) -> ConcurrentDomainDataBuilder:
        """
        The concurrentDomainData property
        """
        from .concurrent_domain_data.concurrent_domain_data_builder import (
            ConcurrentDomainDataBuilder,
        )

        return ConcurrentDomainDataBuilder(self._request_adapter)

    @property
    def current_timestamp(self) -> CurrentTimestampBuilder:
        """
        The currentTimestamp property
        """
        from .current_timestamp.current_timestamp_builder import CurrentTimestampBuilder

        return CurrentTimestampBuilder(self._request_adapter)

    @property
    def device(self) -> DeviceBuilder:
        """
        The device property
        """
        from .device.device_builder import DeviceBuilder

        return DeviceBuilder(self._request_adapter)

    @property
    def device_info_by_site(self) -> DeviceInfoBySiteBuilder:
        """
        The deviceInfoBySite property
        """
        from .device_info_by_site.device_info_by_site_builder import DeviceInfoBySiteBuilder

        return DeviceInfoBySiteBuilder(self._request_adapter)

    @property
    def domain_metric(self) -> DomainMetricBuilder:
        """
        The domainMetric property
        """
        from .domain_metric.domain_metric_builder import DomainMetricBuilder

        return DomainMetricBuilder(self._request_adapter)

    @property
    def event_app_hop_list(self) -> EventAppHopListBuilder:
        """
        The eventAppHopList property
        """
        from .event_app_hop_list.event_app_hop_list_builder import EventAppHopListBuilder

        return EventAppHopListBuilder(self._request_adapter)

    @property
    def event_app_score_bandwidth(self) -> EventAppScoreBandwidthBuilder:
        """
        The eventAppScoreBandwidth property
        """
        from .event_app_score_bandwidth.event_app_score_bandwidth_builder import (
            EventAppScoreBandwidthBuilder,
        )

        return EventAppScoreBandwidthBuilder(self._request_adapter)

    @property
    def event_flow_from_app_hop(self) -> EventFlowFromAppHopBuilder:
        """
        The eventFlowFromAppHop property
        """
        from .event_flow_from_app_hop.event_flow_from_app_hop_builder import (
            EventFlowFromAppHopBuilder,
        )

        return EventFlowFromAppHopBuilder(self._request_adapter)

    @property
    def event_readout(self) -> EventReadoutBuilder:
        """
        The eventReadout property
        """
        from .event_readout.event_readout_builder import EventReadoutBuilder

        return EventReadoutBuilder(self._request_adapter)

    @property
    def event_readout_by_site(self) -> EventReadoutBySiteBuilder:
        """
        The eventReadoutBySite property
        """
        from .event_readout_by_site.event_readout_by_site_builder import EventReadoutBySiteBuilder

        return EventReadoutBySiteBuilder(self._request_adapter)

    @property
    def event_readout_by_traces(self) -> EventReadoutByTracesBuilder:
        """
        The eventReadoutByTraces property
        """
        from .event_readout_by_traces.event_readout_by_traces_builder import (
            EventReadoutByTracesBuilder,
        )

        return EventReadoutByTracesBuilder(self._request_adapter)

    @property
    def export_trace(self) -> ExportTraceBuilder:
        """
        The exportTrace property
        """
        from .export_trace.export_trace_builder import ExportTraceBuilder

        return ExportTraceBuilder(self._request_adapter)

    @property
    def finalized_data(self) -> FinalizedDataBuilder:
        """
        The finalizedData property
        """
        from .finalized_data.finalized_data_builder import FinalizedDataBuilder

        return FinalizedDataBuilder(self._request_adapter)

    @property
    def finalized_domain_data(self) -> FinalizedDomainDataBuilder:
        """
        The finalizedDomainData property
        """
        from .finalized_domain_data.finalized_domain_data_builder import FinalizedDomainDataBuilder

        return FinalizedDomainDataBuilder(self._request_adapter)

    @property
    def flow_detail(self) -> FlowDetailBuilder:
        """
        The flowDetail property
        """
        from .flow_detail.flow_detail_builder import FlowDetailBuilder

        return FlowDetailBuilder(self._request_adapter)

    @property
    def flow_metric(self) -> FlowMetricBuilder:
        """
        The flowMetric property
        """
        from .flow_metric.flow_metric_builder import FlowMetricBuilder

        return FlowMetricBuilder(self._request_adapter)

    @property
    def get_monitor_state(self) -> GetMonitorStateBuilder:
        """
        The getMonitorState property
        """
        from .get_monitor_state.get_monitor_state_builder import GetMonitorStateBuilder

        return GetMonitorStateBuilder(self._request_adapter)

    @property
    def import_trace(self) -> ImportTraceBuilder:
        """
        The importTrace property
        """
        from .import_trace.import_trace_builder import ImportTraceBuilder

        return ImportTraceBuilder(self._request_adapter)

    @property
    def monitor(self) -> MonitorBuilder:
        """
        The monitor property
        """
        from .monitor.monitor_builder import MonitorBuilder

        return MonitorBuilder(self._request_adapter)

    @property
    def nwpi_dscp(self) -> NwpiDscpBuilder:
        """
        The nwpiDSCP property
        """
        from .nwpi_dscp.nwpi_dscp_builder import NwpiDscpBuilder

        return NwpiDscpBuilder(self._request_adapter)

    @property
    def nwpi_nbar_app_group(self) -> NwpiNbarAppGroupBuilder:
        """
        The nwpiNbarAppGroup property
        """
        from .nwpi_nbar_app_group.nwpi_nbar_app_group_builder import NwpiNbarAppGroupBuilder

        return NwpiNbarAppGroupBuilder(self._request_adapter)

    @property
    def nwpi_protocol(self) -> NwpiProtocolBuilder:
        """
        The nwpiProtocol property
        """
        from .nwpi_protocol.nwpi_protocol_builder import NwpiProtocolBuilder

        return NwpiProtocolBuilder(self._request_adapter)

    @property
    def nwpi_setting_view(self) -> NwpiSettingViewBuilder:
        """
        The nwpiSettingView property
        """
        from .nwpi_setting_view.nwpi_setting_view_builder import NwpiSettingViewBuilder

        return NwpiSettingViewBuilder(self._request_adapter)

    @property
    def packet_features(self) -> PacketFeaturesBuilder:
        """
        The packetFeatures property
        """
        from .packet_features.packet_features_builder import PacketFeaturesBuilder

        return PacketFeaturesBuilder(self._request_adapter)

    @property
    def preloadinfo(self) -> PreloadinfoBuilder:
        """
        The preloadinfo property
        """
        from .preloadinfo.preloadinfo_builder import PreloadinfoBuilder

        return PreloadinfoBuilder(self._request_adapter)

    @property
    def query(self) -> QueryBuilder:
        """
        The query property
        """
        from .query.query_builder import QueryBuilder

        return QueryBuilder(self._request_adapter)

    @property
    def routing_detail(self) -> RoutingDetailBuilder:
        """
        The routingDetail property
        """
        from .routing_detail.routing_detail_builder import RoutingDetailBuilder

        return RoutingDetailBuilder(self._request_adapter)

    @property
    def tasks(self) -> TasksBuilder:
        """
        The tasks property
        """
        from .tasks.tasks_builder import TasksBuilder

        return TasksBuilder(self._request_adapter)

    @property
    def trace(self) -> TraceBuilder:
        """
        The trace property
        """
        from .trace.trace_builder import TraceBuilder

        return TraceBuilder(self._request_adapter)

    @property
    def trace_cft_record(self) -> TraceCftRecordBuilder:
        """
        The traceCftRecord property
        """
        from .trace_cft_record.trace_cft_record_builder import TraceCftRecordBuilder

        return TraceCftRecordBuilder(self._request_adapter)

    @property
    def trace_fin_flow_count(self) -> TraceFinFlowCountBuilder:
        """
        The traceFinFlowCount property
        """
        from .trace_fin_flow_count.trace_fin_flow_count_builder import TraceFinFlowCountBuilder

        return TraceFinFlowCountBuilder(self._request_adapter)

    @property
    def trace_fin_flow_time_range(self) -> TraceFinFlowTimeRangeBuilder:
        """
        The traceFinFlowTimeRange property
        """
        from .trace_fin_flow_time_range.trace_fin_flow_time_range_builder import (
            TraceFinFlowTimeRangeBuilder,
        )

        return TraceFinFlowTimeRangeBuilder(self._request_adapter)

    @property
    def trace_fin_flow_with_query(self) -> TraceFinFlowWithQueryBuilder:
        """
        The traceFinFlowWithQuery property
        """
        from .trace_fin_flow_with_query.trace_fin_flow_with_query_builder import (
            TraceFinFlowWithQueryBuilder,
        )

        return TraceFinFlowWithQueryBuilder(self._request_adapter)

    @property
    def trace_flow(self) -> TraceFlowBuilder:
        """
        The traceFlow property
        """
        from .trace_flow.trace_flow_builder import TraceFlowBuilder

        return TraceFlowBuilder(self._request_adapter)

    @property
    def trace_history(self) -> TraceHistoryBuilder:
        """
        The traceHistory property
        """
        from .trace_history.trace_history_builder import TraceHistoryBuilder

        return TraceHistoryBuilder(self._request_adapter)

    @property
    def trace_info_by_base_key(self) -> TraceInfoByBaseKeyBuilder:
        """
        The traceInfoByBaseKey property
        """
        from .trace_info_by_base_key.trace_info_by_base_key_builder import TraceInfoByBaseKeyBuilder

        return TraceInfoByBaseKeyBuilder(self._request_adapter)

    @property
    def trace_readout_filter(self) -> TraceReadoutFilterBuilder:
        """
        The traceReadoutFilter property
        """
        from .trace_readout_filter.trace_readout_filter_builder import TraceReadoutFilterBuilder

        return TraceReadoutFilterBuilder(self._request_adapter)

    @property
    def upsert_setting(self) -> UpsertSettingBuilder:
        """
        The upsertSetting property
        """
        from .upsert_setting.upsert_setting_builder import UpsertSettingBuilder

        return UpsertSettingBuilder(self._request_adapter)

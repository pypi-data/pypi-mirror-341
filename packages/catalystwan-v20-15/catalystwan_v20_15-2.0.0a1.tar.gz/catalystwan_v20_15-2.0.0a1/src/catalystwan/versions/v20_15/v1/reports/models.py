# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, Dict, List, Literal, Optional, Union

ReportStatus = Literal["completed", "failed", "in_progress", "not_scheduled", "scheduled"]

ActiveStatus = Literal["active", "cancelled"]

FileType = Literal["csv", "pdf"]

ScheduleType = Literal[
    "on_demand", "reoccur_daily", "reoccur_monthly", "reoccur_onetime", "reoccur_weekly"
]

TemplateType = Literal[
    "app_usage",
    "executive_summary",
    "firewall_enforcement",
    "internet_browsing",
    "ips_events_collected",
    "link_availability",
    "link_sla",
    "link_utilization",
    "malware_files_collected",
    "site_availability",
]

TimeRange = Literal["one_day", "one_month", "one_week"]


@dataclass
class ReportSummaryInfo:
    """
    Report summary information
    """

    business_hours: str = _field(metadata={"alias": "businessHours"})
    file_type: str = _field(metadata={"alias": "fileType"})
    # If the report template has running task records or not
    has_task: bool = _field(metadata={"alias": "hasTask"})
    # Report next running timestamp
    next_run_time: int = _field(metadata={"alias": "nextRunTime"})
    # vManage which scheduled report generating tasks
    on_vmanage: str = _field(metadata={"alias": "onVmanage"})
    # The report UUID for report template
    report_id: str = _field(metadata={"alias": "reportId"})
    # The report template name
    report_name: str = _field(metadata={"alias": "reportName"})
    # Report schedule status(not_scheduled/scheduled/in_progress/completed/failed))
    report_status: ReportStatus = _field(
        metadata={"alias": "reportStatus"}
    )  # pytype: disable=annotation-type-mismatch
    # Report schedule information
    schedule: str
    # The number of scheduled tasks for report template
    task_num: int = _field(metadata={"alias": "taskNum"})
    template_type: str = _field(metadata={"alias": "templateType"})
    # Report time frame(7 Days/30 Days)
    time_frame: str = _field(metadata={"alias": "timeFrame"})
    # Email address list to receive the report files
    email_recipient: Optional[List[str]] = _field(
        default=None, metadata={"alias": "emailRecipient"}
    )


@dataclass
class ReportSummaryResponse:
    """
    Query all reports summary information response
    """

    # Report List
    reports: List[ReportSummaryInfo]
    header: Optional[Dict[str, Any]] = _field(default=None)


@dataclass
class ReportBusinessHours:
    """
    Report business hours for data generating
    """

    end_time: str = _field(metadata={"alias": "endTime"})
    start_time: str = _field(metadata={"alias": "startTime"})


@dataclass
class ScheduleConfig1:
    """
    On-demand schedule
    """

    # Schedule type
    schedule_type: ScheduleType = _field(
        metadata={"alias": "scheduleType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class ScheduleConfig2:
    # Schedule type
    schedule_type: ScheduleType = _field(
        metadata={"alias": "scheduleType"}
    )  # pytype: disable=annotation-type-mismatch
    # startTime string format is yyyy-MM-dd HH:mm:ss,UTC timezone
    start_time: str = _field(metadata={"alias": "startTime"})


@dataclass
class ScheduleConfig3:
    # Schedule type
    schedule_type: ScheduleType = _field(
        metadata={"alias": "scheduleType"}
    )  # pytype: disable=annotation-type-mismatch
    # startTime string format is HH:mm:ss
    start_time: str = _field(metadata={"alias": "startTime"})


@dataclass
class ScheduleConfig4:
    # The day number of a week, mapping is as 1 - Sun, 2 - Mon, 3 - Tus, 4 - Wed, 5 - Thu, 6 - Fri, 7 - Sat
    day_of_week: int = _field(metadata={"alias": "dayOfWeek"})
    # Schedule type
    schedule_type: ScheduleType = _field(
        metadata={"alias": "scheduleType"}
    )  # pytype: disable=annotation-type-mismatch
    # startTime string format is HH:mm:ss
    start_time: str = _field(metadata={"alias": "startTime"})


@dataclass
class ScheduleConfig5:
    # Schedule type
    schedule_type: ScheduleType = _field(
        metadata={"alias": "scheduleType"}
    )  # pytype: disable=annotation-type-mismatch
    # startTime string format is (yyyy-MM-dd HH:mm:ss), time zone is UTC
    start_time: str = _field(metadata={"alias": "startTime"})


@dataclass
class ExecutiveSummaryReport:
    """
    Executive summary report template
    """

    # Email address list to receive the report files
    email_recipient: List[str] = _field(metadata={"alias": "emailRecipient"})
    # Report Name
    report_name: str = _field(metadata={"alias": "reportName"})
    # schedule config
    schedule_config: Union[
        ScheduleConfig1, ScheduleConfig2, ScheduleConfig3, ScheduleConfig4, ScheduleConfig5
    ] = _field(metadata={"alias": "scheduleConfig"})
    # Time range for report(one_week/one_month)
    time_range: TimeRange = _field(
        metadata={"alias": "timeRange"}
    )  # pytype: disable=annotation-type-mismatch
    # Report business hours for data generating
    business_hours: Optional[ReportBusinessHours] = _field(
        default=None, metadata={"alias": "businessHours"}
    )
    file_type: Optional[FileType] = _field(default=None, metadata={"alias": "fileType"})
    # Filtering by Site ID list is optional, if no site Id is included, all site ID will be used for report generating.
    site_ids: Optional[List[int]] = _field(default=None, metadata={"alias": "siteIds"})
    template_type: Optional[TemplateType] = _field(default=None, metadata={"alias": "templateType"})


@dataclass
class ReportInfo:
    """
    Report Template detail info
    """

    # Report active status(active,cancelled)
    active_status: ActiveStatus = _field(
        metadata={"alias": "activeStatus"}
    )  # pytype: disable=annotation-type-mismatch
    # user name for who created the report template.
    created_by: str = _field(metadata={"alias": "createdBy"})
    # If the report template has running task records or not
    has_task: bool = _field(metadata={"alias": "hasTask"})
    # Report template last update timestamp
    last_update_time: int = _field(metadata={"alias": "lastUpdateTime"})
    # Report next running timestamp
    next_run_time: int = _field(metadata={"alias": "nextRunTime"})
    # vManage which scheduled report generating tasks
    on_vmanage: str = _field(metadata={"alias": "onVmanage"})
    # Executive summary report template
    report_config: ExecutiveSummaryReport = _field(metadata={"alias": "reportConfig"})
    # The report UUID for report template
    report_id: str = _field(metadata={"alias": "reportId"})
    # Report schedule status(not_scheduled/scheduled/in_progress/completed/failed))
    report_status: ReportStatus = _field(
        metadata={"alias": "reportStatus"}
    )  # pytype: disable=annotation-type-mismatch
    debug_info: Optional[str] = _field(default=None, metadata={"alias": "debugInfo"})
    file_type: Optional[FileType] = _field(default=None, metadata={"alias": "fileType"})
    need_run_immediately: Optional[bool] = _field(
        default=None, metadata={"alias": "needRunImmediately"}
    )
    task_num: Optional[int] = _field(default=None, metadata={"alias": "taskNum"})
    template_type: Optional[TemplateType] = _field(default=None, metadata={"alias": "templateType"})


@dataclass
class UpdateReportTemplateResponse:
    # Report ID
    report_id: str = _field(metadata={"alias": "reportId"})

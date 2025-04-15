# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, Dict, List, Literal, Optional

TaskStatus = Literal["failure", "in_progress", "success"]


@dataclass
class ReportTaskProcessStepInfo:
    """
    The detail status for each step of report generating task
    """

    # Report file is generated or not
    file_generated: bool = _field(metadata={"alias": "fileGenerated"})
    # Report data query success or not
    report_data_query: bool = _field(metadata={"alias": "reportDataQuery"})
    # Email sent or not, if sending report via email is enabled
    email_sent: Optional[bool] = _field(default=None, metadata={"alias": "emailSent"})
    # Report file is all replicated or not when vManage is a cluster deployment
    file_replicated: Optional[bool] = _field(default=None, metadata={"alias": "fileReplicated"})


@dataclass
class ReportTaskUiInfo:
    """
    Report Task list for specific report ID
    """

    # Report Template UUID
    report_id: str = _field(metadata={"alias": "reportId"})
    # Report name for task
    report_name: str = _field(metadata={"alias": "reportName"})
    # Report schedule information
    schedule: str
    # Report task start timestamp
    start_time: int = _field(metadata={"alias": "startTime"})
    # Task UUID
    task_id: str = _field(metadata={"alias": "taskId"})
    # Report Task status
    task_status: TaskStatus = _field(
        metadata={"alias": "taskStatus"}
    )  # pytype: disable=annotation-type-mismatch
    # The detail status for each step of report generating task
    task_step_detail: ReportTaskProcessStepInfo = _field(metadata={"alias": "taskStepDetail"})
    # Report time frame (7 Days or 30 Days)
    time_frame: str = _field(metadata={"alias": "timeFrame"})
    # Email address to receive the report files
    email_recipient: Optional[List[str]] = _field(
        default=None, metadata={"alias": "emailRecipient"}
    )
    # Report task end timestamp
    end_time: Optional[int] = _field(default=None, metadata={"alias": "endTime"})
    # Report file type
    file_type: Optional[str] = _field(default=None, metadata={"alias": "fileType"})
    # In Cluster deployment, the follower vManage IP address which needs to replicate the report file from source vManage which generated the report file.
    follower_vmanages: Optional[List[str]] = _field(
        default=None, metadata={"alias": "followerVmanages"}
    )
    # IP address of the source vManage which is scheduled to generate report file. Default value is "localhost" for single node vManage deployment.
    on_vmanage: Optional[str] = _field(default=None, metadata={"alias": "onVmanage"})
    # Report file download URL
    report_download_url: Optional[str] = _field(
        default=None, metadata={"alias": "reportDownloadUrl"}
    )


@dataclass
class ReportTaskQueryResponse:
    """
    Report task query response
    """

    # Report Task list for specific report ID
    task_list: List[ReportTaskUiInfo] = _field(metadata={"alias": "taskList"})
    header: Optional[Dict[str, Any]] = _field(default=None)


@dataclass
class TaskIdResponse:
    # Task ID
    task_id: str = _field(metadata={"alias": "taskId"})

# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DownloadListPostRequest


class FilelistBuilder:
    """
    Builds and executes requests for operations under /statistics/download/{processType}/filelist
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, process_type: str, payload: DownloadListPostRequest, **kw):
        """
        Downloading list of stats file
        POST /dataservice/statistics/download/{processType}/filelist

        :param process_type: Possible types are: remoteprocessing, dr
        :param payload: Payload
        :returns: None
        """
        params = {
            "processType": process_type,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/statistics/download/{processType}/filelist",
            params=params,
            payload=payload,
            **kw,
        )

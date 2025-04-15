# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import QueryFieldsResponsePayloadInner


class FieldsBuilder:
    """
    Builds and executes requests for operations under /stream/device/nwpi/query/fields
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[QueryFieldsResponsePayloadInner]:
        """
        Get query fields
        GET /dataservice/stream/device/nwpi/query/fields

        :returns: List[QueryFieldsResponsePayloadInner]
        """
        logging.warning("Operation: %s is deprecated", "getStatQueryFields_27")
        return self._request_adapter.request(
            "GET",
            "/dataservice/stream/device/nwpi/query/fields",
            return_type=List[QueryFieldsResponsePayloadInner],
            **kw,
        )

# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .dscpmapping.dscpmapping_builder import DscpmappingBuilder
    from .events.events_builder import EventsBuilder
    from .prefixmapping.prefixmapping_builder import PrefixmappingBuilder
    from .sequences.sequences_builder import SequencesBuilder


class PolicyBuilder:
    """
    Builds and executes requests for operations under /partner/aci/policy
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Get ACI definitions
        GET /dataservice/partner/aci/policy

        :returns: Any
        """
        return self._request_adapter.request("GET", "/dataservice/partner/aci/policy", **kw)

    @property
    def dscpmapping(self) -> DscpmappingBuilder:
        """
        The dscpmapping property
        """
        from .dscpmapping.dscpmapping_builder import DscpmappingBuilder

        return DscpmappingBuilder(self._request_adapter)

    @property
    def events(self) -> EventsBuilder:
        """
        The events property
        """
        from .events.events_builder import EventsBuilder

        return EventsBuilder(self._request_adapter)

    @property
    def prefixmapping(self) -> PrefixmappingBuilder:
        """
        The prefixmapping property
        """
        from .prefixmapping.prefixmapping_builder import PrefixmappingBuilder

        return PrefixmappingBuilder(self._request_adapter)

    @property
    def sequences(self) -> SequencesBuilder:
        """
        The sequences property
        """
        from .sequences.sequences_builder import SequencesBuilder

        return SequencesBuilder(self._request_adapter)

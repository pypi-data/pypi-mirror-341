# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field


@dataclass
class ApplyRecommendationRes:
    not_valid_recommendation_ids: str = _field(metadata={"alias": "notValidRecommendationIds"})
    not_valid_sites: str = _field(metadata={"alias": "notValidSites"})
    process_id: str = _field(metadata={"alias": "processId"})
    wani_policy_id: str = _field(metadata={"alias": "waniPolicyId"})

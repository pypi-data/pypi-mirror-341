from typing import TypedDict
from uuid import UUID

from ed_domain.queues.ed_optimization.location_model import LocationModel


class BusinessModel(TypedDict):
    id: UUID
    business_name: str
    owner_first_name: str
    owner_last_name: str
    phone_number: str
    email: str
    location: LocationModel

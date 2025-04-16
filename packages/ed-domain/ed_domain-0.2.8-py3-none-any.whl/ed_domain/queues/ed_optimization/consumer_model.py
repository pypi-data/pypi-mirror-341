from typing import NotRequired, TypedDict
from uuid import UUID

from ed_domain.queues.ed_optimization.location_model import LocationModel


class ConsumerModel(TypedDict):
    id: UUID
    first_name: str
    last_name: str
    phone_number: str
    email: NotRequired[str]
    location: LocationModel

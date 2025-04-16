from datetime import datetime
from typing import Literal, TypedDict
from uuid import UUID

from ed_domain.core.entities.order import OrderStatus, Parcel
from ed_domain.queues.ed_optimization.business_model import BusinessModel
from ed_domain.queues.ed_optimization.consumer_model import ConsumerModel


class OrderModel(TypedDict):
    id: UUID
    consumer: ConsumerModel
    business: BusinessModel
    latest_time_of_delivery: datetime
    parcel: Parcel
    order_status: Literal[OrderStatus.PENDING]

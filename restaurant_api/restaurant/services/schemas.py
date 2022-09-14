from typing import TypedDict


class OrderItem(TypedDict):
    name: str
    quantity: int
    unit_price: int


class OrderClient(TypedDict):
    name: str
    phone: int


class OrderData(TypedDict):
    id: int
    price: int
    items: list[OrderItem]
    address: str
    client: OrderClient
    point_id: int

from dataclasses import dataclass


@dataclass
class Truck:
    id: int
    capacity: float
    coordinates: tuple[float, float]

from dataclasses import dataclass


@dataclass
class Request:
    id: int
    coordinates: tuple[float, float]
    volume_object: float

def round_to_nearest(price: float, step: float) -> float:
    """
    Fiyatı en yakın adıma yuvarlar.
    Örn: round_to_nearest(0.01983, 0.002) -> 0.02
    """
    return round(round(price / step) * step, 6)

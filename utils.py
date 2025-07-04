from math import floor
from frect import FRect
from pygame import Vector2

def sign(x: int | float):
    return [-1,1][x >= 0]

def clamp(x: int | float, a: int | float, b: int | float):
    return min(max(a, x), b)

def frange(a: float, b: float, step: float):
    assert(a<b)
    result = []
    while a < b:
        result.append(a)
        a += step
    return result

def floorvec(v: Vector2) -> Vector2:
    return Vector2(floor(v[0]), floor(v[1]))

def tuplevec(x: tuple[float | int, float | int]) -> Vector2:
    assert(len(x) >= 2)
    return Vector2(x[0], x[1])

def tuplefrect(x: tuple[float | int, float | int, float | int, float | int]) -> FRect:
    assert(len(x) >= 4)
    return FRect(x[0], x[1], x[2], x[3])

def is_colliding(a: FRect, b: FRect) -> bool:
    x_axis = (a.x < b.x + b.w) and (a.x + a.w > b.x)
    y_axis = (a.y < b.y + b.h) and (a.y + a.h > b.y)
    return x_axis and y_axis

def get_broadphase(position: Vector2, size: Vector2, velocity: Vector2) -> FRect:
    result = FRect(0.0, 0.0, 0.0, 0.0)
    
    if velocity.x >= 0:
        result.x = position.x
        result.w = size.x + velocity.x
    else:
        result.x = position.x + velocity.x
        result.w = size.x - velocity.x

    if velocity.y >= 0:
        result.y = position.y
        result.h = size.y + velocity.y
    else:
        result.y = position.y + velocity.y
        result.h = size.y - velocity.y
    
    return result
from multipledispatch import dispatch
import random

@dispatch()
def random():
    return random(0.0, 1.0)

@dispatch(float)
def random(max: float):
    return random(0.0, max)

@dispatch(float, float)
def random(min: float, max: float):
    return random.random() * (max - min) + min;
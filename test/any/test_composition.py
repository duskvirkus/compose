from compose import *

def test_default_compose():
    comp = Composition()

    assert comp.width == 100
    assert comp.height == 100
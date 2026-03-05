from Point import Point

def eq_test():
    p = Point(5,6,"p")
    P = Point(5,6,"p2")
    q = Point(10,0,"Q")
    s = Point(0,0,"s")
    S = Point(0,0,"s2")
    d = Point(5,-6,"d")
    f = Point(-11,-25, "f")
    F = Point(-11,-25, "f2")


    # Test with a p with positive coordinates
    assert p.__eq__(p) == True
    assert p.__eq__(P) == True
    assert p.__eq__(d) == False
    assert p.__eq__(q) == False
    assert p.__eq__(s) == False

    # Test with s (0,0)
    assert s.__eq__(s) == True
    assert s.__eq__(S) == True
    assert s.__eq__(q) == False
    assert s.__eq__(f) == False

    # Test with f with negative coordinates
    assert f.__eq__(f) == True
    assert f.__eq__(F) == True
    assert f.__eq__(d) == False
    assert f.__eq__(s) == False

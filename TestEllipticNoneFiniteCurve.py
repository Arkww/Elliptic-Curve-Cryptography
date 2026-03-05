import EllipticNoneFiniteCurve as ecnf

''' We performed the tests using this site: https://andrea.corbellini.name/ecc/interactive/modk-mul.html'''
def test_addition():
    # Test addition of two normal points
    curve = ecnf.EllipticNoneFiniteCurve(a=-7, b=10)
    curve.add_point((1, 2))
    curve.add_point((3, 4))
    result_point = curve.addition(curve.points[1], curve.points[2])
    curve.add_point(result_point)
    assert result_point == (-3, 2)

    curve = ecnf.EllipticNoneFiniteCurve(a=8, b=25)
    curve.add_point((0, 5))
    curve.add_point((-1, 4))
    result_point = curve.addition(curve.points[1], curve.points[2])
    curve.add_point(result_point)
    assert result_point == (2, -7)


    curve = ecnf.EllipticNoneFiniteCurve(a=11, b=25)
    curve.add_point((0, 5))
    curve.add_point((8, 25))
    result_point = curve.addition(curve.points[1], curve.points[2])
    curve.add_point(result_point)
    assert result_point == (-1.75, -0.625)

    curve = ecnf.EllipticNoneFiniteCurve(a=50, b=25)
    curve.add_point((5, 20))
    curve.add_point((20, 95))
    result_point = curve.addition(curve.points[1], curve.points[2])
    curve.add_point(result_point)
    assert result_point == (0, 5)

    # Test addition with point at infinity
    curve = ecnf.EllipticNoneFiniteCurve(a=50, b=25)
    curve.add_point((5, 20))
    curve.add_point((None, None))
    result_point = curve.addition(curve.points[0], curve.points[1])
    curve.add_point(result_point)
    assert result_point == (5, 20)

    # Test addition with two equal points
    curve = ecnf.EllipticNoneFiniteCurve(a=24, b=25)
    curve.add_point((8, 27))
    result_point = curve.addition(curve.points[1], curve.points[1])
    curve.add_point(result_point)
    assert result_point == (0, 5)


    '''
    # Test addition with a point and its inverse
    curve = ecnf.EllipticNoneFiniteCurve(a=24, b=25)
    P = Point(8, 27, "P")
    Q = Point(8, -27, "Q")
    result_point = curve.addition(P, Q)
    assert result_point is None
    '''

def test_scalar_mult():

  # Test scalar multiplication with a normal point
  curve = ecnf.EllipticNoneFiniteCurve(a=-7, b=10)
  curve.add_point((1, 2))
  result_point = curve.scalar_mult(3, curve.points[1])
  curve.add_point(result_point)
  assert result_point == (9, -26)

  curve = ecnf.EllipticNoneFiniteCurve(a=20, b=31)
  curve.add_point((5, 16))
  result_point = curve.scalar_mult(13, curve.points[1])
  curve.add_point(result_point)
  assert (round(result_point[0], 3), round(result_point[1], 3)) == (47.950, -333.517)

  curve = ecnf.EllipticNoneFiniteCurve(a=45, b=98)
  curve.add_point((2, 14))
  result_point = curve.scalar_mult(15, curve.points[1])
  curve.add_point(result_point)
  assert (round(result_point[0], 3), round(result_point[1], 3)) == (5.187, -21.701)

  # Test scalar multiplication with point at infinity
  curve = ecnf.EllipticNoneFiniteCurve(a=-7, b=10)
  result_point = curve.scalar_mult(3, None)
  assert result_point is None


  # Test scalar multiplication with a point and a zero scalar
  curve = ecnf.EllipticNoneFiniteCurve(a=-7, b=10)
  curve.add_point((1, 2))
  result_point = curve.scalar_mult(0, curve.points[1])
  assert result_point is None


  # Test scalar multiplication with a point and a negative scalar
  curve = ecnf.EllipticNoneFiniteCurve(a=6, b=15)
  curve.add_point((7, 20))
  result_point = curve.scalar_mult(-3, curve.points[1])
  assert (round(result_point[0], 3), round(result_point[1], 3)) == (-1.603, -1.122)

def test_get_y_value():
  curve = ecnf.EllipticNoneFiniteCurve(a=-7, b=10)

  # Test with a negative x
  result = curve.get_y_values(-3)
  assert abs(result[0] - 2.0) <= 10**(-5)
  assert abs(result[1] + 2.0) <= 10**(-5)

  # Test with a positive x
  result = curve.get_y_values(13)
  assert abs(result[0] - 46.0) <= 10**(-5)
  assert abs(result[1] + 46.0) <= 10**(-5)

  # Test with x = 0
  result = curve.get_y_values(0)
  assert abs(result[0] - 3.16228) <= 10**(-5)
  assert abs(result[1] + 3.16228) <= 10**(-5)

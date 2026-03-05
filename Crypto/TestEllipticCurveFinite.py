import EllipticFiniteCurve as ecf
from Point import Point


''' We performed the tests using this site: https://andrea.corbellini.name/ecc/interactive/modk-mul.html'''
def test_addition():
    # Test addition of two normal points
    curve = ecf.EllipticFiniteCurve(a=-7, b=10, p=97)
    curve.add_point((1, 2))
    curve.add_point((3, 4))
    result_point = curve.addition(curve.points[1], curve.points[2])
    curve.add_point(result_point)
    assert result_point == (94, 2)

    curve = ecf.EllipticFiniteCurve(a=2, b=25, p=23)
    curve.add_point((12, 11))
    curve.add_point((21, 17))
    result_point = curve.addition(curve.points[1], curve.points[2])
    curve.add_point(result_point)
    assert result_point == (16, 17)

    curve = ecf.EllipticFiniteCurve(a=82, b=65, p=311)
    curve.add_point((86, 5))
    curve.add_point((25, 18))
    result_point = curve.addition(curve.points[1], curve.points[2])
    curve.add_point(result_point)
    assert result_point == (15, 194)


    # Test addition with point at infinity
    curve = ecf.EllipticFiniteCurve(a=-7, b=10, p=97)
    curve.add_point((3, 4))
    result_point = curve.addition(None, curve.points[1])
    assert result_point == (3, 4)

    # Test addition with two equal points
    curve = ecf.EllipticFiniteCurve(a=-7, b=10, p=97)
    curve.add_point((1, 2))
    result_point = curve.addition(curve.points[1], curve.points[1])
    assert result_point == (96, 93)

    # Test addition with a point and its inverse
    curve = ecf.EllipticFiniteCurve(a=-7, b=10, p=97)
    P = Point(1, 2, "P")
    Q = Point(1, 95, "Q")
    result_point = curve.addition(P, Q)
    assert result_point is None


def test_mult_scalaire():

  # Test scalar multiplication with a normal point
  curve = ecf.EllipticFiniteCurve(a=-7, b=10, p=97)
  curve.add_point((1, 2))
  result_point = curve.mult_scalaire(3, curve.points[1])
  curve.add_point(result_point)
  assert result_point == (9, 71)

  curve = ecf.EllipticFiniteCurve(a=15, b=65, p=127)
  curve.add_point((14, 15))
  result_point = curve.mult_scalaire(10, curve.points[1])
  curve.add_point(result_point)
  assert result_point == (83, 33)

  # time: 1.73 seconds
  curve = ecf.EllipticFiniteCurve(a=46, b=12, p=1999)
  curve.add_point((124, 36))
  result_point = curve.mult_scalaire(29, curve.points[1])
  curve.add_point(result_point)
  assert result_point == (30, 1547)

  curve = ecf.EllipticFiniteCurve(a=34, b=13, p=59)
  curve.add_point((46, 18))
  result_point = curve.mult_scalaire(20, curve.points[1])
  curve.add_point(result_point)
  assert result_point == (31, 1)

  # Test scalar multiplication with point at infinity
  curve = ecf.EllipticFiniteCurve(a=-7, b=10, p=97)
  result_point = curve.mult_scalaire(3, None)
  assert result_point is None

  # Test scalar multiplication with a point and a zero scalar
  curve = ecf.EllipticFiniteCurve(a=-7, b=10, p=97)
  curve.add_point((1, 2))
  result_point = curve.mult_scalaire(0, curve.points[1])
  assert result_point is None

  # Test scalar multiplication with a point and a negative scalar
  curve = ecf.EllipticFiniteCurve(a=-10, b=15, p=61)
  curve.add_point((36, 16))
  result_point = curve.mult_scalaire(-3, curve.points[1])
  assert result_point == (8, 9)

def test_get_y_value():
  curve = ecf.EllipticFiniteCurve(a=-7, b=10, p=97)

  # Test with a positive x
  result = curve.get_y_values(11)
  assert abs(result[0] - 87.0) <= 10**(-5)
  assert abs(result[1] - 10.0) <= 10**(-5)

  # Test with the minimum x
  result = curve.get_y_values(1)
  assert abs(result[0] - 95.0) <= 10**(-5)
  assert abs(result[1] - 2.0) <= 10**(-5)

def is_quadratic_residueTest():
  curve = ecf.EllipticFiniteCurve(a=50, b=0, p=97)

  # Test 1**2 mod p
  assert curve.is_quadratic_residue(1)
  # Test 95**2 mod p
  assert curve.is_quadratic_residue(4)
  # Test 90**2 mod p
  assert curve.is_quadratic_residue(49)

  # Test with p
  assert not(curve.is_quadratic_residue(97))

  # Test 0**2 mod p which is not a quadratic residue
  assert not(curve.is_quadratic_residue(0))

test_addition()

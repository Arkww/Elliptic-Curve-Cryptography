from EllipticNoneFiniteCurve import EllipticNoneFiniteCurve
from Crypto import EllipticFiniteCurve
from Point import Point
import unittest
import sys
import os

sys.path.append(os.path.abspath("Crypto/"))
from EllipticFiniteCurve import EllipticFiniteCurve

def point_is_abelian(Curve):
        '''
        Displays the result of all abelian group rules
        '''
        print("------Start test------")
        # Check if the list contains at least 1 point
        if(len(Curve.points) >= 1):
            print("List of points:",Curve.points)

            print("--Commutativity--")
            print(commutativity(Curve))

            print("--Associativity--")
            print(associativity(Curve))

            print("--Closure--")
            print(closing(Curve))

            print("--Neutral Element--")
            print(neutral_element(Curve))

            print("--Inverse--")
            print(reverse(Curve))
        else: return ValueError("Empty list of points")

def commutativity(Curve):
        '''
        Checks if the elements are commutative. That is,
        swapping the positions of two factors does not affect
        the result.
        '''
        i = 0
        commutativity_check = True
        # Iterate through the entire list of points
        while(i<len(Curve.points)-1 and commutativity_check == True):
            a = Curve.points[i]
            j = i
            # For all points in the list, add the other points while avoiding redundant calculations
            while(j < len(Curve.points) and commutativity_check == True):
                b = Curve.points[j]
                # Handle the None result case
                if(Curve.addition(a,b) != None and Curve.addition(b,a) != None):
                    try:
                        # Check the respective x and y values
                        unittest.TestCase().assertAlmostEqual(Curve.addition(a,b)[0], Curve.addition(b,a)[0], delta=1e-5)
                        unittest.TestCase().assertAlmostEqual(Curve.addition(a,b)[1], Curve.addition(b,a)[1], delta=1e-5)
                    except AssertionError:
                        commutativity_check = False

                else: commutativity_check = Curve.addition(a,b) == Curve.addition(b,a)
                j += 1
            i += 1
        return commutativity_check

def associativity(Curve):
        '''
        Checks if, regardless of the order of calculation,
        the result is not affected
        '''
        # Check if the list contains at least 1 point
        i = 0
        associativity_check = True
        # Iterate through all elements of the point list efficiently to avoid redundant calculations
        # as long as no problem has been identified
        while(i<len(Curve.points) and associativity_check == True):
            a = Curve.points[i]
            j = i
            while(j<len(Curve.points) and associativity_check == True):
                b = Curve.points[j]
                k = j
                while(k<len(Curve.points) and associativity_check == True):
                    c = Curve.points[k]
                    bc = Curve.addition(b,c)
                    ab = Curve.addition(a,b)
                    # Check if the computed point is not None to create a point with the found results
                    if bc != None:
                        bc = Point(bc[0], bc[1], "bc")
                    if ab != None:
                        ab = Point(ab[0], ab[1], "ab")
                    # Handle the None result case
                    if(Curve.addition(a,bc) != None and Curve.addition(ab,c) != None):
                        try:
                            # Check the respective x and y values
                            unittest.TestCase().assertAlmostEqual(Curve.addition(a,bc)[0], Curve.addition(ab,c)[0], delta=1e-5)
                            unittest.TestCase().assertAlmostEqual(Curve.addition(a,bc)[1], Curve.addition(ab,c)[1], delta=1e-5)
                        except AssertionError:
                            associativity_check = False
                    else:
                        associativity_check = Curve.addition(a,bc) == Curve.addition(ab,c)
                    k += 1
                j += 1
            i += 1
        return associativity_check

def closing(Curve):
        '''
        Checks if the result of any operation on two points of the curve
        in the set also exists on the curve
        '''
        i = 0
        closure_check = True
        # Iterate through all elements of the point list efficiently to avoid redundant calculations
        while(i<len(Curve.points) and closure_check == True):
            a = Curve.points[i]
            j = i
            while(j < len(Curve.points) and closure_check == True):
                b = Curve.points[j]
                # Check if the result of the calculation of a and b is on the curve
                if(not(Curve.is_on_curve(Curve.addition(a,b)))):
                    closure_check = False
                j += 1
            i += 1
        return closure_check

def neutral_element(Curve):
    '''
    Checks if the set contains the neutral element: the point at infinity.
    And verifies by calculation that it behaves as a neutral element
    for all other elements.
    '''
    # Check if the point at infinity is in the set
    if(None in Curve.points):
        neutral_element_check = True
        i = 0
        # Iterate through all points in the list
        while(i < len(Curve.points) and neutral_element_check == True):
            # Verify that the calculation of the neutral element and an element returns said element
            a = Curve.points[i]
            if(Curve.addition(a,None) != None):
                try:
                    # Check the respective x and y values
                    unittest.TestCase().assertAlmostEqual(Curve.addition(a,None)[0], a.x, delta=1e-5)
                    unittest.TestCase().assertAlmostEqual(Curve.addition(a,None)[1], a.y, delta=1e-5)
                except AssertionError:
                    neutral_element_check = False
            else: neutral_element_check = Curve.addition(a,None) == None
            i += 1
        return neutral_element_check
    else: return False

def reverse(Curve):
    '''
    Checks if all points of the curve in the set have an inverse
    also on the curve
    '''
    reverse_element_check = True
    i = 0
    # Iterate through all elements of the set as long as no point is without an inverse
    while(i < len(Curve.points) and reverse_element_check == True):
        a = Curve.points[i]
        # The neutral element has neither real coordinates nor an inverse, so we skip it
        if(a != None):
            # Check if the inverse element of point a is on the curve
            if(not(Curve.is_on_curve((a.x, -a.y)))):
                reverse_element_check = False
        i += 1
    return reverse_element_check


# Define a new elliptic curve y^2 = x^3 + 2x + 3
curveS = EllipticNoneFiniteCurve(2, 4)
curveS.generate_one_point_on_curve()
curveS.generate_one_point_on_curve()
curveS.add_point(curveS.addition(curveS.points[0], curveS.points[1]))
curveS.add_point((curveS.points[3].x, -curveS.points[3].y))
curveS.plot_curve(points=curveS.points, x_range=(-10, 10))

# Abelian test
point_is_abelian(curveS)

#curveS.plot_curve(points=curveS.points, x_range=(-10, 10))

curveS = EllipticFiniteCurve(-7,10,97)
curveS.generate_one_point_on_curve()
curveS.generate_one_point_on_curve()
operation = curveS.addition(curveS.points[0], curveS.points[1])
curveS.add_point((operation[0],operation[1]))
curveS.add_point((curveS.points[3].x, -curveS.points[3].y))
curveS.plot_curve(points=curveS.points, x_range=(-10, 10))

point_is_abelian(curveS)

from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
import random as rd
from Curve import Curve
from Point import Point
from utils import double_and_add

# Class representing an infinite elliptic curve over R²

class EllipticNoneFiniteCurve(Curve):

    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.points = [None]
        super().__init__(a, b)

        if ((4 * a**3) + (27 * b **2)) == 0 :
            raise ValueError("The curve is singular")


    def get_y_values(self, x):
        """Returns the Y value for a point X on the elliptic curve"""
        val = x**3 + self.a * x + self.b
        if val < 0:
            return None
        return sqrt(val), -sqrt(val)



    def addition(self, p , q) :
        """Addition of two points on the curve"""

          # If one of the two points is Omega (point at infinity), return the other point
        if p is None and q is None:
            return None
        if p is None:
            return (q.x, q.y)
        if q is None:
            return (p.x, p.y)


        if isinstance(p, Point) and isinstance(q, Point):
            x1, y1 = p.x, p.y
            x2, y2 = q.x, q.y
        else :
            x1, y1 = p
            x2, y2 = q

        # Case P = -Q -> returns Omega (point at infinity)
        if x1 == x2 and y1 == -y2:
            return None

        if x1 != x2 or y1 != y2 :
            if x1 - x2 == 0 :
                raise ValueError("Division by 0")
            m = (y1 - y2) / (x1 - x2)
            xR = m**2 - x1 - x2
            yR = m*(x1 - xR) - y1
            return (xR,yR)
        else :
            if 2*y1 == 0 :
                raise ValueError("Division by 0 y")
            m = (3*x1**2 + self.a) / (2*y1)
            xR = m**2 - 2*x1
            yR = m * (x1 - xR) - y1
            return (xR,yR)



    def scalar_mult(self, n, P):
        '''
        Adds P to itself n times (scalar multiplication)
        '''
        if n == 0 or P == None:
            return None
        # Differentiate calculation for positive and negative n and instantiate a copy of point P
        if n < 0:
            n = -n
            newP = (P.x,-P.y)
        else:
            newP = (P.x, P.y)

        # Pointer to know which bit we are on, e.g.: if pointer = 4 then we are on bit 3
        pointer = 1

        rslt = (None,None)
        # Decompose n into powers of two
        list_powers_of_two = double_and_add(n)

        # Since newP is already instantiated, if 1 is in the list of powers of two we add it to the result
        # For convenience, we remove elements from list_powers_of_two once the result is accounted for
        if 1 in list_powers_of_two:
                list_powers_of_two.remove(1)
                rslt = newP
        # While the list is not empty, continue advancing through the bits
        while len(list_powers_of_two) > 0:
            # Advance by 1 bit
            pointer *= 2
            coord = self.addition(newP,newP)
            newP = coord
            self.add_point(newP)

            # If the current bit is in the list, add the result of this addition to the result
            if pointer in list_powers_of_two:
                list_powers_of_two.remove(pointer)
                if(rslt == (None,None)):
                    rslt = newP
                else:
                    coord = self.addition(rslt, newP)
                    rslt = coord
        self.add_point(rslt)
        return rslt




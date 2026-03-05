import numpy as np
import matplotlib.pyplot as plt
import random
import os
import sys
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Curve import Curve
from utils import is_prime_fermat, tonelli_shanks, double_and_add, gcd, factorize
from Point import Point
import math
from sympy import sqrt, mod_inverse, symbols

# Class representing an elliptic curve defined over a finite field

class EllipticFiniteCurve(Curve):

    def __init__(self, a, b, p):
        if not is_prime_fermat(p):
            raise ValueError("p must be a prime number.")

        super().__init__(a, b, p)

        # Should be computed with Schoof's algorithm!
        time1 = time.time()
        self.order = self.find_order()
        time2 = time.time()
        print("Order computation time: " + str(time2 - time1))
        print("Order: " + str(self.order))

        if (4 * self.a**3 + 27 * self.b**2) % p == 0:
            raise ValueError("The curve is singular.")



    def is_quadratic_residue(self, n):
        """ Checks if n is a quadratic residue mod p """
        return pow(n, (self.p - 1) // 2, self.p) == 1

    def get_y_values(self, x):
        """ Finds y values such that y^2 = x^3 + ax + b [p] """
        val = (x**3 + self.a * x + self.b) % self.p
        y = tonelli_shanks(val, self.p)
        if y is not None:
            return y % self.p
        return None


    def addition(self, p, q):
        """Addition of two points on an elliptic curve defined over a finite field"""

        if p is None and q is None:
            return None
        if p is None:  # If P is the point at infinity, return Q
            return (q.x % self.p, q.y % self.p)
        if q is None:  # If Q is the point at infinity, return P
            return (p.x % self.p, p.y % self.p)

        if isinstance(p, Point) and isinstance(q, Point):
            x1, y1 = p.x, p.y
            x2, y2 = q.x, q.y
        else :
            x1, y1 = p
            x2, y2 = q

        # Case where P = -Q (same x but opposite y) -> result = point at infinity
        if x1 == x2 and (y1 + y2) % self.p == 0:
            return None

        # Case where P == Q (adding a point to itself)
        if p.x == q.x and p.y == q.y:
            if y1 % self.p == 0:
                return None  # Point at infinity
            m = ((3 * x1**2 + self.a) * pow(2 * y1, self.p - 2, self.p)) % self.p

        else:  # General case (P != Q)
            if x1 == x2:
                return None  # Point at infinity
            m = ((y1 - y2) * pow(x1 - x2,-1, self.p)) % self.p

        # Compute new coordinates
        xR = (m**2 - x1 - x2) % self.p
        yR = (m * (x1 - xR) - y1) % self.p

        return (xR, yR)


    def mult_scalaire(self, n, P):

            if n == 0 or P == None:
                return None
            if n < 0:
                n = -n
                newP = (P.x % self.p, -P.y % self.p)
            else:
                newP = (P.x % self.p, P.y % self.p)
            pointer = 1
            rslt = (None, None)
            list_powers_of_two = double_and_add(n)

            if list_powers_of_two.count(1) == 1:
                list_powers_of_two.remove(1)
                rslt = newP

            while len(list_powers_of_two) > 0:
                pointer *= 2
                coord = self.addition(newP, newP)
                if (coord == None) :
                    self.add_point(rslt)
                    return rslt
                else :
                    newP = (coord[0] % self.p, coord[1] % self.p)
                    self.add_point(newP)


                if list_powers_of_two.count(pointer) == 1:
                    list_powers_of_two.remove(pointer)
                    if rslt == (None, None):
                        rslt = newP
                    else:
                        coord = self.addition(rslt, newP)
                        if (coord == None) :
                            return rslt
                        else:
                            rslt = (coord[0] % self.p, coord[1] % self.p)
            self.add_point(rslt)
            return rslt

    def generate_cyclic_subgroup(self, P):
            if P == None:
                return None

            newP = (P.x % self.p, P.y % self.p)
            result = [(P.x,P.y)]


            while True:
                newP = self.addition(newP, (P.x,P.y))
                if newP == None or newP == P:
                    break
                result.append(newP)


            result.append(None)
            if self.order % len(result) != 0 :
                raise ValueError("The order of the cyclic subgroup must be a divisor of the curve order")
            return result

    def generate_subgroup_order(self) :
        """Selects a prime factor of the curve order to generate a cyclic subgroup."""
        factors = factorize(self.order)  # Factorization of the order
        return max(factors)  # Take the largest prime factor

    def generate_subgroup_start_point(self) :
        """Generates a point to find a starting cyclic subgroup"""
        n = self.generate_subgroup_order()
        h = self.order // n

        G = None
        while (G == None) :
            P = self.generate_and_return_one_point_on_curve()
            G = self.mult_scalaire(h,P)
        return G

    def find_order(self) :
        lower_bound = math.ceil(self.p + 1 - 2 * math.sqrt(self.p))
        upper_bound = math.floor(self.p + 1 + 2 * math.sqrt(self.p))
        points = self.count_points()
        for N in range(lower_bound, upper_bound + 1):
            if self.order_check(N,points):
                return N
        return None


    def count_points(self):
        """ Counts the points on the curve """
        count = 1  # Includes the point at infinity
        for x in range(self.p):
            for y in range(self.p):
                if self.is_on_curve((x, y)):
                    count += 1
        return count

    def order_check(self, N, points):
        """ Checks if a given N is the order of the curve """
        return points == N

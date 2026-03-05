import hashlib
import base58
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Curve import Curve
from utils import is_prime_fermat, tonelli_shanks, double_and_add, gcd, factorize
from Point import Point
import math

# Class representing an elliptic curve defined over a finite field

class SECP256k1(Curve):

    def __init__(self):


        super().__init__(a=0, b=7, p=0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f)

        # Generator point coordinates
        self.Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
        self.Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
        self.add_point((self.Gx,self.Gy))
        # Order of secp256k1
        self.ordre = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
        # Order of the cyclic subgroup generated (h = 1 so it is the same as the curve order)
        self.n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
        self.G = Point(self.Gx,self.Gy, 'G')



    def get_y_values(self, x):
        """ Finds y values such that y^2 = x^3 + ax + b [p] """
        val = (x**3 + self.a * x + self.b) % self.p
        y = tonelli_shanks(val, self.p)
        if y is not None:
            return y, (-y) % self.p
        return None


    def addition(self, p, q):
        """Addition of two points on an elliptic curve defined over a finite field"""

        if p is None:  # If P is the point at infinity, return Q
            return q
        if q is None:  # If Q is the point at infinity, return P
            return p

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
        if p == q:
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
            pointer = 1
            newP = (P.x % self.p, P.y % self.p)
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
            return rslt

    def generate_cyclic_subgroup(self):
            if P == None:
                return None

            G = (self.Gx, self.Gy)
            result = [G]


            while True:
                G = self.addition(G, (self.Gx,self.Gy))
                if G == None or G == (self.Gx,self.Gy):
                    break
                result.append(newP)


            result.append(None)
            if self.ordre % len(result) != 0 :
                raise ValueError("The order of the cyclic subgroup must be a divisor of the curve order")
            return result

import random
import math
# Class containing utility functions

def factorize(n):
    """Returns the prime factors of n as a list"""
    factors = []

    # Check divisibility by 2
    while n % 2 == 0:
        factors.append(2)
        n //= 2

    # Check odd numbers up to sqrt(n)
    for i in range(3, math.isqrt(n) + 1, 2):
        while n % i == 0:
            factors.append(i)
            n //= i

    # If n is still a prime number > 2
    if n > 1:
        factors.append(n)

    return factors

def gcd(a, b):
    """Computes the gcd of a and b"""
    if b == 0:
        return a
    return gcd(b, a % b)

def double_and_add(n):
    """ Decomposition into powers of 2 for the double-and-add algorithm """
    fragmentation = []
    power_of_two = 1
    while power_of_two * 2 <= n:
        power_of_two *= 2
    while n >= 0.99:
        if n >= power_of_two:
            fragmentation.append(power_of_two)
            n -= power_of_two
        power_of_two //= 2
    print(fragmentation)
    return fragmentation


def is_prime_fermat(p, k=5):
    """ Fermat primality test """
    if p < 2:
        return False
    if p in (2, 3):
        return True
    if p % 2 == 0:
        return False

    for _ in range(k):
        a = random.randint(2, p - 2)
        if pow(a, p - 1, p) != 1:
            return False
    return True


def tonelli_shanks(n, p):
    """Tonelli-Shanks algorithm to find x such that x^2 = n (mod p).
       Returns a solution x or None if there is none."""
    # Trivial case
    if n == 0:
        return 0
    # Check if n is a quadratic residue
    if pow(int(n), (p - 1) // 2, p) != 1:
        return None

    # If p = 3 mod 4, we have a direct solution
    if p % 4 == 3:
        return pow(int(n), (p + 1) // 4, p)

    # Write p-1 as Q * 2^S with Q odd
    S = 0
    Q = p - 1
    while Q % 2 == 0:
        S += 1
        Q //= 2

    # Find a z that is a quadratic non-residue modulo p
    z = 2
    while pow(int(z), (p - 1) // 2, p) != p - 1:
        z += 1

    M = S
    c = pow(int(z), Q, p)
    t = pow(int(n), Q, p)
    R = pow(int(n), (Q + 1) // 2, p)

    while t != 1:
        # Find the smallest i such that t^(2^i) = 1 (mod p)
        i = 0
        temp = t
        while temp != 1 and i < M:
            temp = pow(temp, 2, p)
            i += 1
        if i == M:
            return None  # no solution

        # Compute b = c^(2^(M-i-1))
        b = pow(c, 2 ** (M - i - 1), p)
        M = i
        c = pow(b, 2, p)
        t = (t * c) % p
        R = (R * b) % p

    return R

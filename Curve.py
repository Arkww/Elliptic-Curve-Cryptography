from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
import random as rd
from Point import Point

# Class representing an elliptic curve (finite or infinite)


class Curve:
    def __init__(self, a, b, p=None):
        if p:
            self.a = a % p
        else: self.a = a
        self.b = b
        self.points = [None]  
        self.p = p  
        self.is_finite = p is not None

   
    def is_on_curve(self, p):
        """Takes a point p as parameter and returns True if it is on the curve"""
        if p == None:
            return True
        x, y = p[0], p[1]
        if self.is_finite:
            return abs((y**2) % self.p - ((x**3 + self.a * x + self.b) % self.p)) <= 10**(-5)
        else:
            return abs((y**2) - (x**3 + self.a * x + self.b)) <= 10**(-5)

    def add_point(self, coord) :
        """Adds a point to the curve"""
        if(coord == None) :
            self.points.append(None)
        else :
            if(self.is_finite):
                self.points.append(Point(coord[0] % self.p, abs(coord[1] % self.p),len(self.points) +1))
            else:self.points.append(Point(coord[0], coord[1],len(self.points) +1))
        point = self.points[-1]
        print(f"Point added: {point}")

    def generate_two_points_on_curve(self):
        """Generates two random points on the curve, depending on the curve type (finite or infinite)"""
        if self.is_finite:
            # Generate a first random point on the curve (for a finite curve)
            while True:
                x1 = rd.randint(0, self.p - 1)  # Choose a random x in the finite field
                y1_values = self.get_y_values(x1)
                if y1_values is not None:
                    y1 = rd.choice(y1_values)  # Choose a y value
                    p = (x1, y1)
                    if self.is_on_curve(p):
                        break

            # Generate a second random point on the curve (for a finite curve)
            while True:
                x2 = rd.randint(0, self.p - 1)  # Choose a random x in the finite field
                y2_values = self.get_y_values(x2)
                if y2_values is not None:
                    y2 = rd.choice(y2_values)  # Choose a y value
                    q = (x2, y2)
                    if self.is_on_curve(q):
                        break

            self.add_point(p)
            self.add_point(q)
        
        else:
            # Generate a first random point on the curve (for an infinite curve)
            while True:
                x1 = rd.uniform(-5, 5)
                y1_values = self.get_y_values(x1)
                if y1_values is not None:
                    y1 = rd.choice(y1_values)
                    p = (x1, y1)
                    if self.is_on_curve(p):
                        break

            # Generate a second random point on the curve (for an infinite curve)
            while True:
                x2 = rd.uniform(-5, 5)
                y2_values = self.get_y_values(x2)
                if y2_values is not None:
                    y2 = rd.choice(y2_values)
                    q = (x2, y2)
                    if self.is_on_curve(q):
                        break

            self.add_point(p)
            self.add_point(q)

    def generate_one_point_on_curve(self):
        """Generates a random point on the curve, depending on the curve type (finite or infinite)"""
        if self.is_finite:
            # Generate a random point on the curve (for a finite curve)
            while True:
                x1 = rd.randint(0, self.p - 1)  # Choose a random x in the finite field
                y1_values = self.get_y_values(x1)
                if y1_values is not None:
                    if(type(y1_values) is tuple):
                        y1 = rd.choice(y1_values)  # Choose a y value
                    else:
                        print(y1_values) 
                        y1 = y1_values
                    p = (x1, y1)
                    if self.is_on_curve(p):
                        break

            self.add_point(p)
        
        else:
            # Generate a random point on the curve (for an infinite curve)
            while True:
                x1 = rd.uniform(-5, 5)
                y1_values = self.get_y_values(x1)
                if y1_values is not None:
                    y1 = rd.choice(y1_values)
                    p = (x1, y1)
                    if self.is_on_curve(p):
                        break


            self.add_point(p)


    def generate_and_return_one_point_on_curve(self):
        """Returns the coordinates of a point on the curve without adding it to the curve"""
        if self.is_finite:
            # Generate a random point on the curve (for a finite curve)
            while True:
                x1 = rd.randint(0, self.p - 1)  # Choose a random x in the finite field
                y1_values = self.get_y_values(x1)
                if y1_values is not None:
                    y1 = rd.choice(y1_values)  # Choose a y value
                    p = (x1, y1)
                    if self.is_on_curve(p):
                        break
            return Point(x1, y1, len(self.points) -1)
        
        else:
            # Generate a random point on the curve (for an infinite curve)
            while True:
                x1 = rd.uniform(-5, 5)
                y1_values = self.get_y_values(x1)
                if y1_values is not None:
                    y1 = rd.choice(y1_values)
                    p = (x1, y1)
                    if self.is_on_curve(p):
                        break
            return Point(x1, y1, len(self.points) -1)



    def plot_curve(self, points=None, x_range=(-5, 5)):
        """Plot the elliptic curve and the points on it."""
        plt.figure(figsize=(8, 6))

        # For finite curves, use modular arithmetic
        if self.is_finite:
            # Generate x values in the finite field [0, p-1]
            x = np.arange(0, self.p)
            valid_x = []
            valid_y = []
            for xi in x:
                y_vals = self.get_y_values(xi)
                if y_vals is not None:
                    if(type(y_vals) is tuple):
                        for yi in y_vals:
                            valid_x.append(xi)
                            valid_y.append(yi)
                    else: 
                        valid_x.append(xi)
                        valid_y.append(y_vals)

            plt.scatter(valid_x, valid_y, color="blue")

        else:
            # For infinite curves, generate x values in continuous range (-5, 5)
            x = np.linspace(x_range[0], x_range[1], 400)
            y_squared = x**3 + self.a * x + self.b

            # Filter out invalid x values (where y^2 < 0)
            valid_x = x[y_squared >= 0]
            valid_y = np.sqrt(y_squared[y_squared >= 0])

            # Plot the elliptic curve
            plt.plot(valid_x, valid_y, color="blue")
            plt.plot(valid_x, -valid_y, color="blue")  # Plot the negative y values

        # Plot the points on the curve
        if points:
            for P in points:
                if P is not None:
                    plt.scatter(P.x, P.y, color="red", zorder=3)
                    plt.text(P.x, P.y, f"  {P.name}({round(P.x, 2)}, {round(P.y, 2)})", fontsize=10, verticalalignment='bottom')

        # Additional plot settings
        plt.axhline(0, color="black", linewidth=0.5)
        plt.axvline(0, color="black", linewidth=0.5)
        plt.grid(True, linestyle="--", linewidth=0.5)
        plt.legend()
        plt.title(f"Elliptic Curve: y² = x³ + {self.a}x + {self.b}")
        plt.show()


    
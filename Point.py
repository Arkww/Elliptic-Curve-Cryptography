class Point() :
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name

    def __str__(self):
        return f"Point(name={self.name}, x={self.x}, y={self.y})"
    
    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

    def __repr__(self):
        return f"Point(name={self.name}, x={self.x}, y={self.y})"
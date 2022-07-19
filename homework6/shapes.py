import math


class Shape:  # class Shape(object)
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def square(self):
        return 0


class Circle(Shape):

    def __init__(self, x, y, radius):
        super().__init__(x, y)
        self.radius = radius

    def __contains__(self, item):
        return math.sqrt(math.pow((self.x-item.x), 2) + math.pow((self.y-item.y), 2)) <= self.radius

    def square(self):
        return math.pi * self.radius ** 2


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Rectangle(Shape):

    def __init__(self, x, y, height, width):
        super().__init__(x, y)
        self.height = height
        self.width = width

    def square(self):
        return self.width * self.height


class Parallelogram(Rectangle):

    def __init__(self, x, y, height, width, angle):
        super().__init__(x, y, height, width)
        self.angle = angle

    def print_angle(self):
        print(self.angle)

    def square(self):
        return (self.width * self.height) * math.sin(math.radians(self.angle))

    def __str__(self):
        result = super().__str__()
        return result + f'\nParallelogram: {self.width}, {self.height}, {self.angle}'

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class Triangle(Shape):
    def __init__(self, x, y, height, width, angle):
        super().__init__(x, y)
        self.height = height
        self.width = width
        self.angle = angle

    def square(self):
        return (self.width * self.height) * 0.5 * math.sin(math.radians(self.angle))


class Scene:
    def __init__(self):
        self._figures = []

    def add_figure(self, figure):
        self._figures.append(figure)

    def total_square(self):
        return sum(f.square() for f in self._figures)

    def __str__(self):
        pass


if __name__ == '__main__':
    p = Parallelogram(1, 2, 20, 30, 45)
    print(p.square())
    t = Triangle(0, 0, 10, 10, 90)
    print(t.square())
    scene = Scene()
    scene.add_figure(p)
    scene.add_figure(t)
    print(scene.total_square())
    circle = Circle(10, 10, 6.8)
    point1 = Point(4, 7)
    point2 = Point(10, 10)
    point3 = Point(140, 72)
    print(point1 in circle)
    print(point2 in circle)
    print(point3 in circle)
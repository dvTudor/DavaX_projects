# - Define an abstract class ‘Shape’ with an abstract method ‘area()’.
# - Create two child classes: ‘Rectangle’ and ‘Circle’, each implementing its own version of ‘area()’.
# - Each class should be initialized with appropriate attributes (e.g. width/height or radius).
# - Add a docstring to each class describing what it represents and how it calculates the area.
# - In the main part of the program, print the docstring of each shape class to verify the documentation.
# - Create a list of shape objects and print their info using a loop.
# - Count how many rectangles and circles are in the list.

from abc import ABC, abstractmethod

class Shape(ABC):

    @abstractmethod
    def area(self):
        pass

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def dimension(self):
        pass

class Rectangle(Shape):
    """Rectangle class with height and width dimensions.
    Computes the area by multiplying its dimensions."""
    def __init__(self, height, width):
        self.height = height
        self.width = width

    def area(self):
        return self.height * self.width

    @property
    def name(self):
        return "Rectangle"

    @property
    def dimension(self):
        return self.height, self.width

class Circle(Shape):
    """Circle class with radius dimension.
    Computes the area using pi multiplied by the radius squared."""
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14159 * (self.radius ** 2)

    @property
    def name(self):
        return "Circle"

    @property
    def dimension(self):
        return self.radius

print(Rectangle.__doc__)
print(Circle.__doc__)

shapes = [Rectangle(2,3), Circle(5), Circle(1), Rectangle(5, 6)]

rectangle_count = 0
circle_count = 0

for i, shape in enumerate(shapes):
    print(f"Shape {i+1} -> {shape.name} with dimension {shape.dimension} and area: {shape.area()}")
    if shape.name == "Circle":
        circle_count += 1
    elif shape.name == "Rectangle":
        rectangle_count += 1

print(f"There are {rectangle_count} rectangles and {circle_count} circles.")
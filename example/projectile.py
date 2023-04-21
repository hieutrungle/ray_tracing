import os
import sys

package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, package_path)

import ray_tracing
from ray_tracing.elements.tuples import Point, Vector, Color
from ray_tracing.elements.canvas import Canvas


class Projectile:
    """
    A projectile has a position and a velocity
    """

    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def tick(self, environment):
        self.position = self.position + self.velocity
        self.velocity = self.velocity + environment.gravity + environment.wind

    def __repr__(self) -> str:
        return f"Projectile({self.position}, {self.velocity})"


class Environment:
    """
    An environment has gravity and wind
    """

    def __init__(self, gravity, wind):
        self.gravity = gravity
        self.wind = wind


def main():
    canvas = Canvas(900, 550)
    start = Point(102.312, 60.3123, 0)
    velocity = Vector(1, 1.8, 0).normalize() * 11.25
    p = Projectile(start, velocity)

    gravity = Vector(0, -0.1, 0)
    wind = Vector(-0.01, 0, 0)
    env = Environment(gravity, wind)

    red = Color(1, 0, 0)
    while p.position.y() > 0:
        x = int(p.position.x())
        y = canvas.height - int(p.position.y())
        canvas.write_pixel(x, y, red)
        p.tick(env)

    canvas.save_to_file("./projectile.ppm")


if __name__ == "__main__":
    main()

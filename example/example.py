import os
import sys

package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, package_path)

import ray_tracing
from ray_tracing.elements.tuples import Point, Vector


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


if __name__ == "__main__":
    p = Projectile(Point(0, 1, 0), Vector(1, 1, 0).normalize())
    env = Environment(Vector(0, -0.1, 0), Vector(-0.01, 0, 0))
    print(p)
    for i in range(10):
        p.tick(env)
        print(p)

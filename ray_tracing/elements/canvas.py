"""
Canvas class
"""
import os
import sys

package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, package_path)

from ray_tracing.elements.tuples import Color
from ray_tracing.utils import operations


class Canvas:
    """Canvas class"""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixels = [[Color(0, 0, 0) for _ in range(width)] for _ in range(height)]

    def write_pixel(self, x, y, color):
        """Write a pixel to the canvas"""
        self.pixels[y][x] = color

    def pixel_at(self, x, y):
        """Get the color of a pixel"""
        return self.pixels[y][x]

    def to_ppm(self):
        """Convert the canvas to PPM format"""
        header = f"""P3\n{self.width} {self.height}\n255\n"""
        body = ""
        for row in self.pixels:
            row_string = ""
            for pixel in row:
                for i, value in enumerate(pixel.tuple):
                    if i == 3:
                        break

                    value = int(value * 256)
                    value = operations.clamp(value, 0, 255)
                    row_string += f"{value} "
                    if len(row_string) > 70 - 3:
                        row_string = row_string[:-1]
                        body += row_string + "\n"
                        row_string = ""
            row_string = row_string[:-1]
            body += row_string + "\n"

        return header + body

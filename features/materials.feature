Feature: Materials

    Background:
        Given material m ← material()
        And point position ← point(0, 0, 0)

    Scenario: The default material
        Given material m ← material()
        Then material m.color = color(1, 1, 1)
        And material m.ambient = 0.1
        And material m.diffuse = 0.9
        And material m.specular = 0.9
        And material m.shininess = 200.0


    Scenario: Lighting with the eye between the light and the surface
        Given vector eyev ← vector(0, 0, -1)
        And vector normalv ← vector(0, 0, -1)
        And light intensity ← color(1, 1, 1)
        And light light_position ← point(0, 0, -10)
        And light light ← point_light(light_position, intensity)
        When material lighting result ← lighting(m, light, position, eyev, normalv)
        Then material lighting result = color(1.9, 1.9, 1.9)

    Scenario: Lighting with the eye between light and surface, eye offset 45°
        Given vector eyev ← vector(0, 0.7071067811865476, -0.7071067811865476)
        And vector normalv ← vector(0, 0, -1)
        And light intensity ← color(1, 1, 1)
        And light light_position ← point(0, 0, -10)
        And light light ← point_light(light_position, intensity)
        When material lighting result ← lighting(m, light, position, eyev, normalv)
        Then material lighting result = color(1.0, 1.0, 1.0)

    Scenario: Lighting with eye opposite surface, light offset 45°
        Given vector eyev ← vector(0, 0, -1)
        And vector normalv ← vector(0, 0, -1)
        And light intensity ← color(1, 1, 1)
        And light light_position ← point(0, 10, -10)
        And light light ← point_light(light_position, intensity)
        When material lighting result ← lighting(m, light, position, eyev, normalv)
        Then material lighting result = color(0.7364, 0.7364, 0.7364)

    Scenario: Lighting with eye in the path of the reflection vector
        Given vector eyev ← vector(0, -0.7071067811865476, -0.7071067811865476)
        And vector normalv ← vector(0, 0, -1)
        And light intensity ← color(1, 1, 1)
        And light light_position ← point(0, 10, -10)
        And light light ← point_light(light_position, intensity)
        When material lighting result ← lighting(m, light, position, eyev, normalv)
        Then material lighting result = color(1.6364, 1.6364, 1.6364)

    Scenario: Lighting with the light behind the surface
        Given vector eyev ← vector(0, 0, -1)
        And vector normalv ← vector(0, 0, -1)
        And light intensity ← color(1, 1, 1)
        And light light_position ← point(0, 0, -10)
        And light light ← point_light(light_position, intensity)
        When material lighting result ← lighting(m, light, position, eyev, normalv)
        Then material lighting result = color(0.1, 0.1, 0.1)
Feature: World

    Scenario: Creating a world
        Given world w ← world()
        Then world w contains no objects
        And world w has no light source

    Scenario: The default world
        Given point position ← point(-10, 10, -10)
        And color intensity ← color(1, 1, 1)
        And light light ← point_light(position, intensity)

        And sphere s1 ← sphere() with:
            | material.color    | (0.8, 1.0, 0.6) |
            | material.diffuse  | 0.7             |
            | material.specular | 0.2             |
        And sphere s2 ← sphere() with:
            | transform | scaling(0.5, 0.5, 0.5) |
        When world w ← default_world()
        Then world w.light = light
        And world w contains s1
        And world w contains s2
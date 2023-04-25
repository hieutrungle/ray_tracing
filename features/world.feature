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

    Scenario: Intersect a world with a ray
        Given world w ← default_world()
        And ray r ← ray(point(0, 0, -5), vector(0, 0, 1))
        When world xs ← intersect_world(w, r)
        Then intersections xs.count = 4
        And intersections xs[0].t = 4
        And intersections xs[1].t = 4.5
        And intersections xs[2].t = 5.5
        And intersections xs[3].t = 6
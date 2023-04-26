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

    # shading tests
    Scenario: Shading an intersection
        Given world w ← default_world()
        And ray r ← ray(point(0, 0, -5), vector(0, 0, 1))
        And world shape ← the first object in w
        And intersection i ← intersection(4, shape)
        When computation comps ← prepare_computations(i, r)
        And world c ← shade_hit(w, comps)
        Then color c = color(0.38066, 0.47583, 0.285495)
    Scenario: Shading an intersection from the inside
        Given world w ← default_world()
        And world w.light ← point_light(point(0, 0.25, 0), color(1, 1, 1))
        And ray r ← ray(point(0, 0, 0), vector(0, 0, 1))
        And world shape ← the second object in w
        And intersection i ← intersection(0.5, shape)
        When computation comps ← prepare_computations(i, r)
        And world c ← shade_hit(w, comps)
        Then color c = color(0.90498, 0.90498, 0.90498)

    # world-ray intersections output color
    Scenario: The color when a ray misses
        Given world w ← default_world()
        And ray r ← ray(point(0, 0, -5), vector(0, 1, 0))
        When world c ← color_at(w, r)
        Then color c = color(0, 0, 0)
    Scenario: The color when a ray hits
        Given world w ← default_world()
        And ray r ← ray(point(0, 0, -5), vector(0, 0, 1))
        When world c ← color_at(w, r)
        Then color c = color(0.38066, 0.47583, 0.285495)
    Scenario: The color with an intersection behind the ray
        Given world w ← default_world()
        And world outer ← the first object in w
        And world outer.material.ambient ← 1
        And world inner ← the second object in w
        And world inner.material.ambient ← 1
        And ray r ← ray(point(0, 0, 0.75), vector(0, 0, -1))
        When world c ← color_at(w, r)
        Then world c = inner.material.color
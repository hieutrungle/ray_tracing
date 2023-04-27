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

    # shadows
    Scenario: There is no shadow when nothing is collinear with point and light
        Given world w ← default_world()
        And point p ← point(0, 10, 0)
        Then world is_shadowed(w, p) is false
    Scenario: The shadow when an object is between the point and the light
        Given world w ← default_world()
        And point p ← point(10, -10, 10)
        Then world is_shadowed(w, p) is true
    Scenario: There is no shadow when an object is behind the light
        Given world w ← default_world()
        And point p ← point(-20, 20, -20)
        Then world is_shadowed(w, p) is false
    Scenario: There is no shadow when an object is behind the point
        Given world w ← default_world()
        And point p ← point(-2, 2, -2)
        Then world is_shadowed(w, p) is false

    # render shadows
    Scenario: shade_hit() is given an intersection in shadow
        Given world w ← world()
        And world w.light ← point_light(point(0, 0, -10), color(1, 1, 1))
        And sphere s1 ← sphere()
        And world s1 is added to w
        And sphere s2 ← sphere() with:
            | transform | translation(0, 0, 10) |
        And world s2 is added to w
        And ray r ← ray(point(0, 0, 5), vector(0, 0, 1))
        And intersection i ← intersection(4, s2)
        When computation comps ← prepare_computations(i, r)
        And world c ← shade_hit(w, comps)
        Then color c = color(0.1, 0.1, 0.1)


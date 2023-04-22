Feature: Spheres

    Scenario: A ray intersects a sphere at two points
        Given ray r ← ray(point(0, 0, -5), vector(0, 0, 1))
        And sphere s ← sphere()
        When intersect xs ← intersect(s, r)
        Then intersect xs.count = 2
        And intersect xs[0].t = 4.0
        And intersect xs[1].t = 6.0
    Scenario: A ray intersects a sphere at a tangent
        Given ray r ← ray(point(0, 1, -5), vector(0, 0, 1))
        And sphere s ← sphere()
        When intersect xs ← intersect(s, r)
        Then intersect xs.count = 2
        And intersect xs[0].t = 5.0
        And intersect xs[1].t = 5.0
    Scenario: A ray misses a sphere
        Given ray r ← ray(point(0, 2, -5), vector(0, 0, 1))
        And sphere s ← sphere()
        When intersect xs ← intersect(s, r)
        Then intersect xs.count = 0
    Scenario: A ray originates inside a sphere
        Given ray r ← ray(point(0, 0, 0), vector(0, 0, 1))
        And sphere s ← sphere()
        When intersect xs ← intersect(s, r)
        Then intersect xs.count = 2
        And intersect xs[0].t = -1.0
        And intersect xs[1].t = 1.0
    Scenario: A sphere is behind a ray
        Given ray r ← ray(point(0, 0, 5), vector(0, 0, 1))
        And sphere s ← sphere()
        When intersect xs ← intersect(s, r)
        Then intersect xs.count = 2
        And intersect xs[0].t = -6.0
        And intersect xs[1].t = -4.0

    Scenario: Intersect sets the object on the intersection
        Given ray r ← ray(point(0, 0, -5), vector(0, 0, 1))
        And sphere s ← sphere()
        When intersect xs ← intersect(s, r)
        Then intersect xs.count = 2
        And intersect xs[0].object = s
        And intersect xs[1].object = s
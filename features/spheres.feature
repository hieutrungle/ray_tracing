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


    Scenario: A sphere's default transformation
        Given sphere s ← sphere()
        Then sphere s.transform = identity_matrix
    Scenario: Changing a sphere's transformation
        Given sphere s ← sphere()
        And t ← translation(2, 3, 4)
        When set_transform(s, t)
        Then sphere s.transform = t

    Scenario: Intersecting a scaled sphere with a ray
        Given ray r ← ray(point(0, 0, -5), vector(0, 0, 1))
        And sphere s ← sphere()
        And m ← scaling(2, 2, 2)
        When set_transform(s, m)
        And intersect xs ← intersect(s, r)
        Then intersect xs.count = 2
        And intersect xs[0].t = 3
        And intersect xs[1].t = 7
    Scenario: Intersecting a translated sphere with a ray
        Given ray r ← ray(point(0, 0, -5), vector(0, 0, 1))
        And sphere s ← sphere()
        And m ← translation(5, 0, 0)
        When set_transform(s, m)
        And intersect xs ← intersect(s, r)
        Then intersect xs.count = 0
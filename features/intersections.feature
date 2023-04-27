Feature: Intersections

    Scenario: An intersection encapsulates t and object
        Given sphere s ← sphere()
        When intersection i ← intersection(3.5, s)
        Then intersection i.t = 3.5
        And intersection i.shape = s
    Scenario: Aggregating intersections
        Given sphere s ← sphere()
        And intersection i1 ← intersection(1, s)
        And intersection i2 ← intersection(2, s)
        When intersections xs ← 2 intersections(i1, i2)
        Then intersections xs.count = 2
        And intersections xs[0].t = 1
        And intersections xs[1].t = 2

    Scenario: The hit, when all intersections have positive t
        Given sphere s ← sphere()
        And intersection i1 ← intersection(1, s)
        And intersection i2 ← intersection(2, s)
        And intersections xs ← 2 intersections(i2, i1)
        When intersection i ← hit(xs)
        Then intersection i = i1
    Scenario: The hit, when some intersections have negative t
        Given sphere s ← sphere()
        And intersection i1 ← intersection(-1, s)
        And intersection i2 ← intersection(1, s)
        And intersections xs ← 2 intersections(i2, i1)
        When intersection i ← hit(xs)
        Then intersection i = i2
    Scenario: The hit, when all intersections have negative t
        Given sphere s ← sphere()
        And intersection i1 ← intersection(-2, s)
        And intersection i2 ← intersection(-1, s)
        And intersections xs ← 2 intersections(i2, i1)
        When intersection i ← hit(xs)
        Then intersection i is nothing
    Scenario: The hit is always the lowest nonnegative intersection
        Given sphere s ← sphere()
        And intersection i1 ← intersection(5, s)
        And intersection i2 ← intersection(7, s)
        And intersection i3 ← intersection(-3, s)
        And intersection i4 ← intersection(2, s)
        And intersections xs ← 4 intersections(i1, i2, i3, i4)
        When intersection i ← hit(xs)
        Then intersection i = i4

    Scenario: Precomputing the state of an intersection
        Given ray r ← ray(point(0, 0, -5), vector(0, 0, 1))
        And sphere shape ← sphere()
        And intersection i ← intersection(4, shape)
        When computation comps ← prepare_computations(i, r)
        Then computation comps.t = i.t
        And computation comps.object = i.object
        And computation comps.point = point(0, 0, -1)
        And computation comps.eyev = vector(0, 0, -1)
        And computation comps.normalv = vector(0, 0, -1)
    Scenario: The hit, when an intersection occurs on the outside
        Given ray r ← ray(point(0, 0, -5), vector(0, 0, 1))
        And sphere shape ← sphere()
        And intersection i ← intersection(4, shape)
        When computation comps ← prepare_computations(i, r)
        Then computation comps.inside = false
    Scenario: The hit, when an intersection occurs on the inside
        Given ray r ← ray(point(0, 0, 0), vector(0, 0, 1))
        And sphere shape ← sphere()
        And intersection i ← intersection(1, shape)
        When computation comps ← prepare_computations(i, r)
        Then computation comps.point = point(0, 0, 1)
        And computation comps.eyev = vector(0, 0, -1)
        And computation comps.inside = true
        # normal would have been (0, 0, 1), but is inverted!
        And computation comps.normalv = vector(0, 0, -1)

    Scenario: The hit should offset the point
        Given ray r ← ray(point(0, 0, -5), vector(0, 0, 1))
        And sphere shape ← sphere() with:
            | transform | translation(0, 0, 1) |
        And intersection i ← intersection(5, shape)
        When computation comps ← prepare_computations(i, r)
        Then computation comps.over_point.z < -EPSILON/2
        And computation comps.point.z > comps.over_point.z
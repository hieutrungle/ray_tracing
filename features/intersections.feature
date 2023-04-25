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
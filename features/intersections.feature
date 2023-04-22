Feature: Intersections

    Scenario: An intersection encapsulates t and object
        Given sphere s ← sphere()
        When intersection i ← intersection(3.5, s)
        Then intersection i.t = 3.5
        And intersection i.shape_object = s
    Scenario: Aggregating intersections
        Given sphere s ← sphere()
        And intersection i1 ← intersection(1, s)
        And intersection i2 ← intersection(2, s)
        When intersections xs ← intersections(i1, i2)
        Then intersections xs.count = 2
        And intersections xs[0].t = 1
        And intersections xs[1].t = 2
Feature: Rays

    Scenario: Creating and querying a ray
        Given origin ← point(1, 2, 3)
        And direction ← vector(4, 5, 6)
        When ray r ← ray(origin, direction)
        Then ray r.origin = origin
        And ray r.direction = direction

    Scenario: Computing a point from a distance
        Given ray r ← ray(point(2, 3, 4), vector(1, 0, 0))
        Then ray position(r, 0) = point(2, 3, 4)
        And ray position(r, 1) = point(3, 3, 4)
        And ray position(r, -1) = point(1, 3, 4)
        And ray position(r, 2.5) = point(4.5, 3, 4)




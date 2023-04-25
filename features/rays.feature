Feature: Rays

    Scenario: Creating and querying a ray
        Given point origin ← point(1, 2, 3)
        And vector direction ← vector(4, 5, 6)
        When ray r ← ray(origin, direction)
        Then ray r.origin = origin
        And ray r.direction = direction

    Scenario: Computing a point from a distance
        Given ray r ← ray(point(2, 3, 4), vector(1, 0, 0))
        Then ray position(r, 0) = point(2, 3, 4)
        And ray position(r, 1) = point(3, 3, 4)
        And ray position(r, -1) = point(1, 3, 4)
        And ray position(r, 2.5) = point(4.5, 3, 4)

    Scenario: Translating a ray
        Given ray r ← ray(point(1, 2, 3), vector(0, 1, 0))
        And transformation m ← translation(3, 4, 5)
        When ray r2 ← transform(r, m)
        Then ray r2.origin = point(4, 6, 8)
        And ray r2.direction = vector(0, 1, 0)
    Scenario: Scaling a ray
        Given ray r ← ray(point(1, 2, 3), vector(0, 1, 0))
        And transformation m ← scaling(2, 3, 4)
        When ray r2 ← transform(r, m)
        Then ray r2.origin = point(2, 6, 12)
        And ray r2.direction = vector(0, 3, 0)

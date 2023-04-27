Feature: Spheres

    # plane
    Scenario: The normal of a plane is constant everywhere
        Given plane p ← plane()
        When plane n1 ← local_normal_at(p, point(0, 0, 0))
        And plane n2 ← local_normal_at(p, point(10, 0, -10))
        And plane n3 ← local_normal_at(p, point(-5, 0, 150))
        Then normal n1 = vector(0, 1, 0)
        And normal n2 = vector(0, 1, 0)
        And normal n3 = vector(0, 1, 0)

    Scenario: Intersect with a ray parallel to the plane
        Given plane p ← plane()
        And ray r ← ray(point(0, 10, 0), vector(0, 0, 1))
        When plane xs ← local_intersect(p, r)
        Then plane xs is empty
    Scenario: Intersect with a coplanar ray
        Given plane p ← plane()
        And ray r ← ray(point(0, 0, 0), vector(0, 0, 1))
        When plane xs ← local_intersect(p, r)
        Then plane xs is empty
    Scenario: A ray intersecting a plane from above
        Given plane p ← plane()
        And ray r ← ray(point(0, 1, 0), vector(0, -1, 0))
        When plane xs ← local_intersect(p, r)
        Then plane xs.count = 1
        And plane xs[0].t = 1
        And plane xs[0].object = p
    Scenario: A ray intersecting a plane from below
        Given plane p ← plane()
        And ray r ← ray(point(0, -1, 0), vector(0, 1, 0))
        When plane xs ← local_intersect(p, r)
        Then plane xs.count = 1
        And plane xs[0].t = 1
        And plane xs[0].object = p
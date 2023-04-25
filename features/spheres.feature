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
        And transformation t ← translation(2, 3, 4)
        When set_transform(s, t)
        Then sphere s.transform = t

    Scenario: Intersecting a scaled sphere with a ray
        Given ray r ← ray(point(0, 0, -5), vector(0, 0, 1))
        And sphere s ← sphere()
        And transformation m ← scaling(2, 2, 2)
        When set_transform(s, m)
        And intersect xs ← intersect(s, r)
        Then intersect xs.count = 2
        And intersect xs[0].t = 3
        And intersect xs[1].t = 7
    Scenario: Intersecting a translated sphere with a ray
        Given ray r ← ray(point(0, 0, -5), vector(0, 0, 1))
        And sphere s ← sphere()
        And transformation m ← translation(5, 0, 0)
        When set_transform(s, m)
        And intersect xs ← intersect(s, r)
        Then intersect xs.count = 0

    Scenario: The normal on a sphere at a point on the x axis
        Given sphere s ← sphere()
        When normal n ← normal_at(s, point(1, 0, 0))
        Then normal n = vector(1, 0, 0)
    Scenario: The normal on a sphere at a point on the y axis
        Given sphere s ← sphere()
        When normal n ← normal_at(s, point(0, 1, 0))
        Then normal n = vector(0, 1, 0)
    Scenario: The normal on a sphere at a point on the z axis
        Given sphere s ← sphere()
        When normal n ← normal_at(s, point(0, 0, 1))
        Then normal n = vector(0, 0, 1)
    Scenario: The normal on a sphere at a nonaxial point
        Given sphere s ← sphere()
        When normal n ← normal_at(s, point(0.5773502691896257, 0.5773502691896257, 0.5773502691896257))
        Then normal n = vector(0.5773502691896257, 0.5773502691896257, 0.5773502691896257)
    Scenario: The normal is a normalized vector
        Given sphere s ← sphere()
        When normal n ← normal_at(s, point(0.5773502691896257, 0.5773502691896257, 0.5773502691896257))
        Then normal n = normalize(n)
    Scenario: Computing the normal on a translated sphere
        Given sphere s ← sphere()
        And sphere m ← translation(0, 1, 0)
        And sphere set_transform(s, m)
        When normal n ← normal_at(s, point(0, 1.70711, -0.70711))
        Then normal n = vector(0, 0.70711, -0.70711)
    Scenario: Computing the normal on a transformed sphere
        Given sphere s ← sphere()
        And sphere m ← scaling(1, 0.5, 1) * rotation_z(0.6283185307179586)
        And sphere set_transform(s, m)
        When normal n ← normal_at(s, point(0, 0.7071067811865476, -0.7071067811865476))
        Then normal n = vector(0, 0.97014, -0.24254)

    @reflection
    Scenario: A sphere has a default material
        Given sphere s ← sphere()
        When material m ← s.material
        Then material m = material()
    @reflection
    Scenario: A sphere may be assigned a material
        Given sphere s ← sphere()
        And material m ← material()
        And material m.ambient ← 1
        When sphere s.material ← m
        Then sphere s.material = m
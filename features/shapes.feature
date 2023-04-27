Feature: Shape

    Scenario: The default transformation
        Given shape s ← test_shape()
        Then shape s.transform = identity_matrix
    Scenario: Assigning a transformation
        Given shape s ← test_shape()
        When shape set_transform(s, translation(2, 3, 4))
        Then shape s.transform = translation(2, 3, 4)
    Scenario: The default material
        Given shape s ← test_shape()
        When shape m ← s.material
        Then material m = material()
    Scenario: Assigning a material
        Given shape s ← test_shape()
        And material m ← material()
        And material m.ambient ← 1
        When shape s.material ← m
        Then shape s.material = m
    Scenario: Intersecting a scaled shape with a ray
        Given ray r ← ray(point(0, 0, -5), vector(0, 0, 1))
        And shape s ← test_shape()
        When shape set_transform(s, scaling(2, 2, 2))
        And intersect xs ← intersect(s, r)
        Then shape s.saved_ray.origin = point(0, 0, -2.5)
        And shape s.saved_ray.direction = vector(0, 0, 0.5)
    Scenario: Intersecting a translated shape with a ray
        Given ray r ← ray(point(0, 0, -5), vector(0, 0, 1))
        And shape s ← test_shape()
        When shape set_transform(s, translation(5, 0, 0))
        And intersect xs ← intersect(s, r)
        Then shape s.saved_ray.origin = point(-5, 0, -5)
        And shape s.saved_ray.direction = vector(0, 0, 1)
    Scenario: Computing the normal on a translated shape
        Given shape s ← test_shape()
        When shape set_transform(s, translation(0, 1, 0))
        And normal n ← normal_at(s, point(0, 1.70711, -0.70711))
        Then normal n = vector(0, 0.70711, -0.70711)
    Scenario: Computing the normal on a transformed shape
        Given shape s ← test_shape()
        And shape m ← scaling(1, 0.5, 1) * rotation_z(0.6283185307179586)
        When shape set_transform(s, m)
        And normal n ← normal_at(s, point(0, 0.7071067811865476, -0.7071067811865476))
        Then normal n = vector(0, 0.97014, -0.24254)
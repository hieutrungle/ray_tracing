Feature: Transformation

    Scenario: Multiplying by a translation matrix
        Given transformation transform ← translation(5, -3, 2)
        And point p ← point(-3, 4, 5)
        Then transformation transform * p = point(2, 1, 7)
    Scenario: Multiplying by the inverse of a translation matrix
        Given transformation transform ← translation(5, -3, 2)
        And transformation inv ← inverse(transform)
        And point p ← point(-3, 4, 5)
        Then transformation inv * p = point(-8, 7, 3)
    Scenario: Translation does not affect vectors
        Given transformation transform ← translation(5, -3, 2)
        And vector v ← vector(-3, 4, 5)
        Then transformation transform * v = v

    Scenario: A scaling matrix applied to a point
        Given transformation transform ← scaling(2, 3, 4)
        And point p ← point(-4, 6, 8)
        Then transformation transform * p = point(-8, 18, 32)
    Scenario: A scaling matrix applied to a vector
        Given transformation transform ← scaling(2, 3, 4)
        And vector v ← vector(-4, 6, 8)
        Then transformation transform * v = vector(-8, 18, 32)
    Scenario: Multiplying by the inverse of a scaling matrix
        Given transformation transform ← scaling(2, 3, 4)
        And transformation inv ← inverse(transform)
        And vector v ← vector(-4, 6, 8)
        Then transformation inv * v = vector(-2, 2, 2)
    Scenario: Reflection is scaling by a negative value
        Given transformation transform ← scaling(-1, 1, 1)
        And point p ← point(2, 3, 4)
        Then transformation transform * p = point(-2, 3, 4)

    Scenario: Rotating a point around the x axis
        Given p ← point(0, 1, 0)
        And transformation half_quarter ← rotation_x(0.7853981633974483)
        And transformation full_quarter ← rotation_x(1.5707963267948966)
        Then transformation half_quarter * p = point(0, 0.7071067811865476, 0.7071067811865476)
        And transformation full_quarter * p = point(0, 0, 1)
    Scenario: The inverse of an x-rotation rotates in the opposite direction
        Given p ← point(0, 1, 0)
        And transformation half_quarter ← rotation_x(0.7853981633974483)
        And transformation inv ← inverse(half_quarter)
        Then transformation inv * p = point(0, 0.7071067811865476, -0.7071067811865476)
    Scenario: Rotating a point around the y axis
        Given p ← point(0, 0, 1)
        And transformation half_quarter ← rotation_y(0.7853981633974483)
        And transformation full_quarter ← rotation_y(1.5707963267948966)
        Then transformation half_quarter * p = point(0.7071067811865476, 0, 0.7071067811865476)
        And transformation full_quarter * p = point(1, 0, 0)
    Scenario: Rotating a point around the z axis
        Given p ← point(0, 1, 0)
        And transformation half_quarter ← rotation_z(0.7853981633974483)
        And transformation full_quarter ← rotation_z(1.5707963267948966)
        Then transformation half_quarter * p = point(-0.7071067811865476, 0.7071067811865476, 0)
        And transformation full_quarter * p = point(-1, 0, 0)

    Scenario: A shearing transformation moves x in proportion to y
        Given transformation transform ← shearing(1, 0, 0, 0, 0, 0)
        And p ← point(2, 3, 4)
        Then transformation transform * p = point(5, 3, 4)
    Scenario: A shearing transformation moves x in proportion to z
        Given transformation transform ← shearing(0, 1, 0, 0, 0, 0)
        And p ← point(2, 3, 4)
        Then transformation transform * p = point(6, 3, 4)
    Scenario: A shearing transformation moves y in proportion to x
        Given transformation transform ← shearing(0, 0, 1, 0, 0, 0)
        And p ← point(2, 3, 4)
        Then transformation transform * p = point(2, 5, 4)
    Scenario: A shearing transformation moves y in proportion to z
        Given transformation transform ← shearing(0, 0, 0, 1, 0, 0)
        And p ← point(2, 3, 4)
        Then transformation transform * p = point(2, 7, 4)
    Scenario: A shearing transformation moves z in proportion to x
        Given transformation transform ← shearing(0, 0, 0, 0, 1, 0)
        And p ← point(2, 3, 4)
        Then transformation transform * p = point(2, 3, 6)
    Scenario: A shearing transformation moves z in proportion to y
        Given transformation transform ← shearing(0, 0, 0, 0, 0, 1)
        And p ← point(2, 3, 4)
        Then transformation transform * p = point(2, 3, 7)

    Scenario: Individual transformations are applied in sequence
        Given p ← point(1, 0, 1)
        And transformation A ← rotation_x(1.5707963267948966)
        And transformation B ← scaling(5, 5, 5)
        And transformation C ← translation(10, 5, 7)
        # apply rotation first
        When point p2 ← A * p
        Then point p2 = point(1, -1, 0)
        # then apply scaling
        When point p3 ← B * p2
        Then point p3 = point(5, -5, 0)
        # then apply translation
        When point p4 ← C * p3
        Then point p4 = point(15, 0, 7)
    Scenario: Chained transformations must be applied in reverse order
        Given p ← point(1, 0, 1)
        And transformation A ← rotation_x(1.5707963267948966)
        And transformation B ← scaling(5, 5, 5)
        And transformation C ← translation(10, 5, 7)
        When transformation T ← C * B * A
        Then transformation T * p = point(15, 0, 7)
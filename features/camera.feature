Feature: Matrices and Determinants

    Scenario: Constructing a camera
        Given camera hsize ← 160
        And camera vsize ← 120
        And camera field_of_view ← 1.5707963267948966
        When camera c ← camera(hsize, vsize, field_of_view)
        Then camera c.hsize = 160
        And camera c.vsize = 120
        And camera c.field_of_view = 1.5707963267948966
        And camera c.transform = identity_matrix

    Scenario: The pixel size for a horizontal canvas
        Given camera c ← camera(200, 125, 1.5707963267948966)
        Then camera c.pixel_size = 0.01
    Scenario: The pixel size for a vertical canvas
        Given camera c ← camera(125, 200, 1.5707963267948966)
        Then camera c.pixel_size = 0.01

    Scenario: Constructing a ray through the center of the canvas
        Given camera c ← camera(201, 101, 1.5707963267948966)
        When camera r ← ray_for_pixel(c, 100, 50)
        Then ray r.origin = point(0, 0, 0)
        And ray r.direction = vector(0, 0, -1)
    Scenario: Constructing a ray through a corner of the canvas
        Given camera c ← camera(201, 101, 1.5707963267948966)
        When camera r ← ray_for_pixel(c, 0, 0)
        Then ray r.origin = point(0, 0, 0)
        And ray r.direction = vector(0.66519, 0.33259, -0.66851)
    Scenario: Constructing a ray when the camera is transformed
        Given camera c ← camera(201, 101, 1.5707963267948966)
        When camera c.transform ← rotation_y(0.7853981633974483) * translation(0, -2, 5)
        And camera r ← ray_for_pixel(c, 100, 50)
        Then ray r.origin = point(0, 2, -5)
        And ray r.direction = vector(0.7071067811865476, 0, -0.7071067811865476)

    Scenario: Rendering a world with a camera
        Given world w ← default_world()
        And camera c ← camera(11, 11, 1.5707963267948966)
        And point from ← point(0, 0, -5)
        And point to ← point(0, 0, 0)
        And vector up ← vector(0, 1, 0)
        And camera c.transform ← view_transform(from, to, up)
        When camera image ← render(c, w)
        Then pixel_at(image, 5, 5) = color(0.38066119308103435, 0.47582649135129296, 0.28549589481077575)
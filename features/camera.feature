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
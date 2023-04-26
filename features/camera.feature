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
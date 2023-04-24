Feature: Lights

    Scenario: A point light has a position and intensity
        Given light intensity ← color(1, 1, 1)
        And light position ← point(0, 0, 0)
        When light light ← point_light(position, intensity)
        Then light light.position = position
        And light light.intensity = intensity
Feature: Materials

    Scenario: The default material
        Given material m ← material()
        Then material m.color = color(1, 1, 1)
        And material m.ambient = 0.1
        And material m.diffuse = 0.9
        And material m.specular = 0.9
        And material m.shininess = 200.0
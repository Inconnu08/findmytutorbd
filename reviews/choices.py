# Making tuples of the universities, departments, score, and grade choices.
# These will be the choices in the models.

TEN_YEARS_DEGREES = (
    ('O Levels', 'O Levels'),
    ('SSC', 'SSC'),
    ('None', 'None'),
)

TWELVE_YEARS_DEGREES = (
    ('A Levels', 'A Levels'),
    ('HSC', 'HSC'),
    ('None', 'None'),
)

UNIVERSITIES = (
    ('North South University', 'North South University'),
    ('BRAC University', 'BRAC University'),
    ('Independent University Bangladesh', 'Independent University Bangladesh'),
)

DEPARTMENTS = (
    ('Business & Economics', 'Business & Economics'),
    ('Engineering & Physical Sciences', 'Engineering & Physical Sciences'),
    ('Humanities & Social Sciences', 'Humanities & Social Sciences'),
    ('Health & Life Sciences', 'Health & Life Sciences'),
)

SCORE_CHOICES = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
)

GRADE_CHOICES = (
    ('A', 'A'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B', 'B'),
    ('B-', 'B-'),
    ('C+', 'C+'),
    ('C', 'C'),
    ('C-', 'C-'),
    ('D+', 'D+'),
    ('D', 'D'),
    ('F', 'F'),
    ('N/A', 'Not Applicable'),
)

grade_dict_str_key = {
    'A': 11,
    'A-': 10,
    'B+': 9,
    'B': 8,
    'B-': 7,
    'C+': 6,
    'C': 5,
    'C-': 4,
    'D+': 3,
    'D': 2,
    'F': 1,
    'N/A': 0,
}

grade_dict_int_key = {
    11: 'A',
    10: 'A-',
    9: 'B+',
    8: 'B',
    7: 'B-',
    6: 'C+',
    5: 'C',
    4: 'C-',
    3: 'D+',
    2: 'D',
    1: 'F',
    0: 'N/A',

}

import pytest
from unittest.mock import Mock
from source.school import Student, Teacher, Classroom, TooManyStudents

# Assuming the classes are imported from your source module
# from source import Classroom, Teacher, Student


# -------------------------------------------------------------------
# FIXTURES
# -------------------------------------------------------------------
@pytest.fixture
def potions_teacher():
    return Teacher("Severus Snape")


@pytest.fixture
def gryffindor_students():
    return [
        Student("Harry Potter"),
        Student("Hermione Granger"),
        Student("Ron Weasley"),
    ]


@pytest.fixture
def potions_class(potions_teacher, gryffindor_students):
    """Creates a basic Potions classroom with Snape and 3 students."""
    return Classroom(
        teacher=potions_teacher,
        students=gryffindor_students,
        course_title="Potions 101",
    )


# -------------------------------------------------------------------
# TESTS USING FIXTURES & MOCKS
# -------------------------------------------------------------------
def test_classroom_initialization(potions_class, potions_teacher):
    assert potions_class.teacher.name == "Severus Snape"
    assert len(potions_class.students) == 3
    assert potions_class.course_title == "Potions 101"


def test_change_teacher(potions_class):
    new_teacher = Teacher("Horace Slughorn")
    potions_class.change_teacher(new_teacher)

    assert potions_class.teacher.name == "Horace Slughorn"


def test_remove_student(potions_class):
    potions_class.remove_students("Ron Weasley")

    remaining_names = [student.name for student in potions_class.students]
    assert "Ron Weasley" not in remaining_names
    assert len(potions_class.students) == 2


def test_add_student_with_mock(potions_class):
    # Using a Mock object for a new student instead of a full Student instance
    mock_student = Mock()
    mock_student.name = "Neville Longbottom"

    potions_class.add_student(mock_student)

    assert len(potions_class.students) == 4
    assert potions_class.students[-1].name == "Neville Longbottom"


# -------------------------------------------------------------------
# TESTS USING PARAMETRIZE
# -------------------------------------------------------------------
@pytest.mark.parametrize(
    "new_student_name, expected_count",
    [
        ("Draco Malfoy", 4),
        ("Luna Lovegood", 4),
        ("Cedric Diggory", 4),
    ],
)
def test_add_various_students(potions_class, new_student_name, expected_count):
    new_student = Student(new_student_name)
    potions_class.add_student(new_student)

    assert len(potions_class.students) == expected_count
    assert potions_class.students[-1].name == new_student_name


# -------------------------------------------------------------------
# TESTS USING PYTEST.RAISES
# -------------------------------------------------------------------
def test_add_student_capacity_limit_raises_exception():
    teacher = Teacher("Minerva McGonagall")
    # Start with 11 students (len <= 10 condition will trigger the raise)
    initial_students = [Student(f"Student {i}") for i in range(11)]
    transfiguration_class = Classroom(
        teacher=teacher, students=initial_students, course_title="Transfiguration"
    )

    extra_student = Student("Draco Malfoy")

    # Raising a raw string raises a TypeError in modern Python
    with pytest.raises(TypeError):
        transfiguration_class.add_student(extra_student)

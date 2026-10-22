from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,   # JSON keys in camelCase
        validate_by_name=True,      # still accept snake_case field names (data.py)
        validate_by_alias=True,     # and the camelCase aliases (request bodies)
    )


class Course(CamelModel):
    id: str
    title: str
    description: str
    credits: int
    is_elective: bool = False   # in JSON: isElective
    likes: int = 0


class EnrollmentIn(CamelModel):
    course_id: str
    student_name: str = Field(min_length=2)


class Enrollment(EnrollmentIn):
    id: int

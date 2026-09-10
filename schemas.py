from pydantic import BaseModel, ConfigDict, Field

class PlannerOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sub_questions: list[str] = Field(
        min_length=2,
        max_length=5,
        description="2 to 5 focused sub-questions that together cover the research query",
    )
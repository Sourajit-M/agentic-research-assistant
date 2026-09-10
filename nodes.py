import json
from groq import Groq
import config
from state import GraphState
from schemas import PlannerOutput

client = Groq(api_key=config.GROQ_API_KEY)

PLANNER_SYSTEM_PROMPT = """You are a research planning assistant.
Given a research query, break it into 2-5 focused sub-questions that,
together, would let someone write a well-rounded report answering the
original query. Sub-questions should be:
- Non-overlapping (each covers a distinct angle)
- Specific enough to search for directly
- Ordered from foundational to more nuanced

Do not answer the sub-questions. Only produce the list.
"""

def planner_node(state: GraphState) -> dict:
    completion = client.chat.completions.create(
        model=config.MODEL_NAME,
        messages=[
            {"role": "system", "content": PLANNER_SYSTEM_PROMPT},
            {"role": "user", "content": state["query"]},
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "planner_output",
                "schema": PlannerOutput.model_json_schema(),
                "strict": True,
            },
        },
    )

    raw = completion.choices[0].message.content
    parsed = PlannerOutput.model_validate(json.loads(raw))

    return {"sub_questions": parsed.sub_questions}
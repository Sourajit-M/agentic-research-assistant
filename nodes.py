from groq import Groq
import config
from state import GraphState

client = Groq(api_key=config.GROQ_API_KEY)

def echo_node(state: GraphState) -> dict:
    response = client.chat.completions.create(
        model=config.MODEL_NAME,
        messages=[{"role": "user", "content": state["query"]}],
    )
    return {"response": response.choices[0].message.content}
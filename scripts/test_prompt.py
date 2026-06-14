import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from configs.settings import settings
from prompts.system_v0 import SYSTEM_PROMPT_V0, FEW_SHOT_EXAMPLES
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

llm = settings.build_llm()

test_input = (
    "ELA detector result: confidence=0.85, "
    "high residual concentrated in the lower-right quadrant.\n"
    "Noise detector result: confidence=0.72, "
    "noise inconsistency detected in the same region.\n"
    "Please analyze and output JSON."
)

messages = [SystemMessage(content=SYSTEM_PROMPT_V0)]
for ex in FEW_SHOT_EXAMPLES:
    if ex["role"] == "user":
        messages.append(HumanMessage(content=ex["content"]))
    elif ex["role"] == "assistant":
        messages.append(AIMessage(content=ex["content"]))
messages.append(HumanMessage(content=test_input))

response = llm.invoke(messages)
print(response.content)
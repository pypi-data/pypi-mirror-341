import dspy

from autoflow.models.llms import LLM


def get_dspy_lm_by_llm(llm: LLM) -> dspy.LM:
    return dspy.LM(
        model=llm.model,
        max_tokens=llm.max_tokens,
        **llm.additional_kwargs,
    )

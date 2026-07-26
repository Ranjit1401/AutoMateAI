"""Single shared LLM client. Raises a clear error at call time (not import
time) if GROQ_API_KEY is missing, so the rest of the app can still boot
and serve non-LLM routes without it configured."""
from functools import lru_cache

from langchain_groq import ChatGroq

from app.core.config import settings


@lru_cache
def get_llm() -> ChatGroq:
    if not settings.GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is not configured. Set it in backend/.env.")
    return ChatGroq(api_key=settings.GROQ_API_KEY, model=settings.MODEL_NAME, temperature=0)


class _LazyLLM:
    """Defers instantiation until first attribute access, so importing this
    module never fails even without an API key configured."""

    def __getattr__(self, item):
        return getattr(get_llm(), item)

    def with_structured_output(self, *args, **kwargs):
        return get_llm().with_structured_output(*args, **kwargs)

    def invoke(self, *args, **kwargs):
        return get_llm().invoke(*args, **kwargs)


llm = _LazyLLM()

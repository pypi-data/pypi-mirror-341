"""Integrate Tracedy Tracing into your LLM applications with the Tracedy Python SDK using the `@observe()` decorator.

*Simple example (decorator + openai integration)*

```python
from tracedy.decorators import observe
from tracedy.openai import openai # OpenAI integration

@observe()
def story():
    return openai.chat.completions.create(
        model="gpt-3.5-turbo",
        max_tokens=100,
        messages=[
          {"role": "system", "content": "You are a great storyteller."},
          {"role": "user", "content": "Once upon a time in a galaxy far, far away..."}
        ],
    ).choices[0].message.content

@observe()
def main():
    return story()

main()
```

See [docs](https://tracedy.com/docs/sdk/python/decorators) for more information.
"""

from .tracedy_decorator import tracedy_context, observe, TracedyDecorator

__all__ = ["tracedy_context", "observe", "TracedyDecorator"]

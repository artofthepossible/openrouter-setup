# The Model Is Just a String: Right-Sizing AI in a Throwaway Sandbox

*A follow-up to [The AI Model Sizing Problem Nobody Owns](https://medium.com/@abishaiep/the-ai-model-sizing-problem-nobody-owns-and-how-it-gets-solved-e36db7cc5060).*

A few months ago I wrote about the AI model sizing problem nobody owns — the FinOps-shaped hole at the heart of every enterprise rolling out AI. Developers default to the biggest model "just in case," token budgets bleed, and observability is too immature to tell you whether a lighter model would have done the job. I closed by noting that the tools exist; broad enterprise adoption is another story entirely.

This is a quick update from the "tools exist" side of that gap, because the gap is closing fast — and it closed for me in a way worth sharing.

## The setup

I spun up a fresh sandbox using `sbx` (Anthropic's sandboxing tool for Claude Code), gave it nothing but a Python venv and a directory, and pointed an agent at OpenRouter. Thirty minutes later I had a runnable demo that:

1. Calls `openai/gpt-4o-mini` for a basic completion.
2. Swaps to `anthropic/claude-3.5-haiku` — same code, one string changed — for the same prompt.
3. Streams from `openai/gpt-4o-mini` token by token.

The whole script is ~60 lines of Python using the standard OpenAI SDK. The only "OpenRouter-ness" is the base URL:

```python
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)
```

After that, the model is a string. `openai/gpt-4o-mini`. `anthropic/claude-3.5-haiku`. `google/gemini-2.5-flash`. The provider, the price tier, the latency profile — all addressable behind one literal.

That's the routing layer the original article was pointing at, and it works today.

## Why this matters to the sizing problem

The first article argued that AI right-sizing moves through three phases: **identify the problem, build the discipline and tools, scale adoption**. The OpenRouter + sandbox combination is where phases two and three finally meet.

- **Identify**: still on you. You need a candidate task and a working sense of what "good enough" looks like.
- **Build discipline**: the substrate is now trivial. A model bake-off is a `for` loop over a list of strings. Cost, latency, and quality become a matrix you can measure in an afternoon, not a quarter-long architecture exercise.
- **Scale adoption**: this is where the sandbox part matters. Engineers won't experiment if experimentation risks their dev environment, their secrets, or their main repo. `sbx` gives you a disposable workspace with its own filesystem, its own network policy, and its own API keys. The friction of "let me just try Haiku instead of Sonnet on this" drops to near zero.

The original complaint wasn't that nobody *could* swap models. It was that the **organizational ergonomics** of doing so were so bad that the rational engineer defaulted to over-modeling. OpenRouter removes the integration tax. A sandboxed agent removes the blast-radius tax. Together they flip the rational default.

## What I'd build next

Two concrete things, both small enough for a weekend:

- **A quality harness, not just a price list.** A YAML of `(prompt, expected-shape, accepted-models)` and a script that runs each model, scores output against a rubric (or against a frontier-model judge), and writes a markdown leaderboard. This is the missing observability piece the original article flagged — the "ground truth and quality scoring" KPI gap. It's not hard. It's just not built.
- **A routing policy file in the repo.** `routes.yaml`: classification → Haiku, summarization → Gemini Flash, reasoning-heavy → Sonnet, fallback → GPT-4o-mini. Check it in. Let it evolve like a Terraform file. Model selection becomes reviewable, diffable, and **owned by someone** — which is precisely what "nobody owns it" was complaining about.

## The thing I didn't expect

The most useful piece wasn't OpenRouter, or the SDK, or even the model swap. It was the sandbox.

The sizing problem persists partly because nobody wants to break their environment to save 80% on inference. A throwaway sandbox makes the experiment cheap in the dimension that actually matters to engineers — *risk to their own workstation*, not dollars on a corporate card. That's the unlock the FinOps analogy didn't predict.

The tools exist. Adoption is still another story. But the cost of writing the next paragraph of that story just dropped by an order of magnitude.

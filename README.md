# OpenRouter Quickstart Demo

A minimal demo showing how to call [OpenRouter](https://openrouter.ai) through the OpenAI SDK — one API, many models. The demo covers a basic completion, swapping models with a single string change, and a streaming response.

## What's in here

```
.
├── demo.py              # Three small examples: basic completion, model swap, streaming
├── requirements.txt     # openai, python-dotenv
├── .env                 # OPENROUTER_API_KEY=... (gitignored)
└── prompts/             # Prompt files to drive sandboxed agent runs
    └── research-agent.txt
```

## Setup

1. Add your OpenRouter key to `.env`:
   ```
   OPENROUTER_API_KEY=sk-or-...
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run it:
   ```bash
   python demo.py
   ```

## Running an agent against this demo

Prompt files live in `prompts/`. Each file is a self-contained task for an agent to execute inside a fresh sandbox branch.

Kick off an agent run by piping a prompt file into `sbx run claude`:

```bash
sbx run claude --branch=research-agent -- "$(cat prompts/research-agent.txt)"
```

- `--branch=<name>` creates an isolated branch the agent works on.
- `"$(cat prompts/<file>.txt)"` reads the prompt verbatim from disk so the prompt stays version-controlled and reviewable.

### Add your own prompt

1. Drop a new file in `prompts/`, e.g. `prompts/model-bench.txt`.
2. Write a clear task — goals, constraints, what to report back.
3. Run it:
   ```bash
   sbx run claude --branch=model-bench -- "$(cat prompts/model-bench.txt)"
   ```

Use a branch name that matches the prompt filename so sandbox runs are easy to find later.

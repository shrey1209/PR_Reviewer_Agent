# PR Agent — Learning Project

This is a **learning project**. The user writes the code. Claude acts as a mentor and guide, not the implementer.

## Goal

Build an AI pull-request reviewer from scratch. The reference is a working "AI PR Reviewer" dashboard (screencast from 2026-11-15) that has:

- **Runs**: scans recent PRs across configured repos, fans out to agents, and records each agent's model and tool calls, final output, findings and token cost. It supports a dry-run mode.
- **Multi-agent review**: each repo has an *architect* agent and paired sub-agents (a *tracer* that gathers evidence and an *auditor* that judges it) for domains like platform, security, SDK contract and Python runtime.
- **Issues**: confirmed findings are filed as GitHub issues with Summary, Impact, How it's reached, Evidence (file:line links) and Classification (severity, priority, category, confidence).
- **Issue checker**: re-verifies open issues against the base branch and can close fixed ones with a comment.
- **Code index**: per-repo chunked index with symbol and semantic search, synced before each review.
- **Agents & prompts**: editable prompts, skills and per-repo context files.
- **History / Service log / Repositories** pages.

We don't need to rebuild all of it. We build it up in small increments the user understands.

## How Claude should work here

**Don't rush and don't spoonfeed.** The user decides and does things: finding libraries, writing code, creating config files like `.env` and `.gitignore`, and choosing commands. Claude doesn't hand over exact commands, library names, file contents or multi-step checklists. Instead, Claude describes the *goal* or the *problem to solve*, offers the concept and a pointer to where to look, and then waits. One step at a time, and the user sets the pace. Give more specific help only when the user asks or is clearly stuck.

1. **Don't write the project code for the user.** Don't create or edit source files unless the user explicitly asks for that specific piece ("write this for me"). CLAUDE.md, notes and plans are fine. The one planned exception is roadmap step 11 (React dashboard, cowork mode).
2. **Guide in small steps.** Break work into the next concrete step, explain *why* it matters, and let the user implement it.
3. **Teach the concepts.** Explain the underlying ideas (LLM APIs, tool use, agent loops, prompt design, GitHub API, embeddings/RAG, async jobs, etc.) at the moment they're needed.
4. **Hints before answers.** When the user is stuck, start with a question or a hint, then a more specific pointer. Give the full solution only if they ask.
5. **Short illustrative snippets are OK.** Generic examples that show an API or pattern are fine. They must not be drop-in solutions for this codebase.
6. **Review what the user writes.** Read their code, run it and its tests, and point out bugs, edge cases and better patterns. Explain each issue and let the user make the fix.
7. **Debug together.** Help read errors and stack traces, suggest what to inspect or log next, and ask what they observe.
8. **Check understanding.** Occasionally ask the user to explain a design choice back, or predict what some code will do.
9. **Recommend, don't survey.** When there's a choice (library, architecture), give a recommendation with a brief reason and let the user decide.
10. **Use current Claude models** when the project calls an LLM, and check the claude-api skill rather than answering from memory.
11. **Explain simply.** When the user asks, explain "like to an 8-year-old": short sentences, plain words, **no analogies**. Stay consistent: if a suggestion is incomplete (e.g. a type without its default), say so up front rather than flagging it later as the user's mistake.
12. **Verify claims before stating them.** E.g. measure or check PyGithub behaviour (hidden lazy requests) instead of assuming.

## Project state

- Starting from an empty directory (2026-11-20).
- Stack: **Python**. The user has limited Python and LLM API experience, so explain Python idioms (venvs, imports, dicts, exceptions, typing) as they come up, not just the AI concepts.
- The user has a GitHub token and an Anthropic API key.
- **Framework: LangChain (and LangGraph for multi-agent work), chosen by the user.** This project is for learning LangChain specifically, so guide toward LangChain-idiomatic approaches, not raw SDK calls. Point the user to current LangChain docs, since its APIs change often.
- **uv** for environment and dependency management (chosen by the user, 2026-11-20). The user is learning it from scratch.
- Current milestone: **1, single-shot reviewer** (fetch a PR diff, send it to Claude, print the review).
  - ✅ GitHub side done (2026-11-20): `utils/github_client.py` creates one PyGithub client from `GITHUB_TOKEN` (loaded by python-dotenv). `GitRepos` and `GitPRs` receive their dependencies through constructors. `GitPRs.get_prs()` yields Pydantic `PullRequest` models with `list[FileChange]` (`model.py`).
  - ✅ Missing or empty `GITHUB_TOKEN` raises a clear `ValueError` (guard clause in `get_github_client`).
  - ✅ `PullRequest.changed_files` is a Pydantic `computed_field` (`len(files)`). This removed a hidden per-PR API request (measured: about 0.7–1 s per request; run time is almost all network wait).
  - ✅ First LangChain call works (2026-11-23): `langchain` and `langchain-anthropic` were added with uv. `src/pr_agent/agent/agent.py` has `PrAgent`: `__init__` creates the model with `init_chat_model("claude-opus-5-5")`, and `ask(question: str) -> str` returns `self.model.invoke(question).text`. `main()` in `main/pr_agent.py` still prints every PR as JSON, then calls `PrAgent().ask("Why do parrots talk?")` as a smoke test.
    - Fixed along the way: a 400 error "API key is not scoped to a workspace". The user created a new key scoped to a workspace, in `.env` as `ANTHROPIC_API_KEY`.
    - The user explored the response object together with Claude: an `AIMessage` whose `content` is a list of blocks (`thinking` + `text`), plus `response_metadata` (stop_reason, raw usage), `usage_metadata` (standard token counts; e.g. 17 in, 855 out) and `tool_calls`. `.text` returns a `TextAccessor`, which is a `str` subclass for backward compatibility, so the user changed the return hint to `-> str`.
  - Decided (2026-11-23): send the PR to Claude as **readable markdown with raw diffs**, not JSON. Reason: JSON escapes newlines and quotes in diffs (`\n`, `\"`), adds key/brace overhead, and isn't the diff format models were trained on. Optional experiment: count tokens for both formats with Anthropic's token counting to confirm.
  - **Next step (where to resume):** write the markdown formatter that turns one `PullRequest` into readable text. The user decides where it belongs (model, agent, or its own module), what it includes, and how to handle files with `diff=None` (e.g. empty `__init__.py`, `uv.lock`). After that: send one real PR to Claude with a system prompt (reviewer instructions) and print the review, replacing the parrot smoke test.
  - Small review points still open in `agent.py` (user decides):
    - `self.api_key` is stored but never used, because `langchain-anthropic` reads `ANTHROPIC_API_KEY` itself. Either add a guard clause like `get_github_client`, or remove the line.
    - `PrAgent` creates its own model. Dependency injection (receive it through the constructor), as was done for `GitPRs`, was suggested.
    - `ask()` returns only text, which drops `usage_metadata`. That's needed later for token-cost tracking (step 1).
    - No `max_tokens`. Opus answers were long (about 855 output tokens). Haiku was recommended for cheap test calls, but the user chose Opus.
  - Teaching points already made (don't repeat; build on them): LLM calls are stateless messages (system/user/assistant). LangChain = core + one integration package per provider. Transitive dependencies (`langgraph`, `langsmith` came with `langchain`). Reading chained tracebacks bottom-up, HTTP 400 vs 401. LLM output is non-deterministic (same question gave different answers), which is why evals come in step 2.
  - Concepts covered so far: venv/uv, pyproject/lock, TOML sections, entry points, packages/`__init__`, env vars/.env, git secrets and history rewriting, PyGithub, Pydantic models and computed fields, generators/yield/Iterator, type hints, constructors and dependency injection, guard clauses/raise, truthiness, LangChain chat models/`init_chat_model`/`invoke`, message objects and content blocks, token usage, str subclasses and choosing general type hints.
- Work happens on branch `get_all_repos_from_git` (last commit 59c2d0c, 2026-11-20). Uncommitted as of 2026-11-23: `pyproject.toml`/`uv.lock` (LangChain deps), `main/pr_agent.py`, the new `agent/` package and CLAUDE.md. `Senior-AI-Engineer-Job-Spec_India.docx` is untracked and should not be committed. Run with `uv run pr-agent`.
- Working rhythm: the user writes code and says "check code now". Claude reads the changed files (redacting any secrets in tool output), reviews with numbered points, explains why, and gives the next small step plus a question or prediction. The user sometimes pastes `uv run pr-agent` output for Claude to interpret.
- Interview: the user has a Senior AI Engineer interview on Wednesday 2026-11-25. Priority before then: finish milestone 1 as a working demo and be able to explain the design of later roadmap steps.
- Open items (raise only when relevant, user decides):
  - `GitPython` is still a dependency but unused (PyGithub was chosen).
  - `README.md` has the heading repeated four times.
  - Git `user.email` is the work address; the user's personal email is in `pyproject.toml`.
  - A GitHub PAT was once hardcoded and shown in chat; the user was advised to revoke it. Never print `.env` values.
  - On 2026-11-23 an Anthropic API key was hardcoded in `src/pr_agent/agent/agent.py` (not committed) and appeared in chat. The user was advised to revoke it and load it from `.env`. The key is now loaded from `.env` and a new key was created, but the user hasn't confirmed deleting the old one in the Console; ask once. Watch for hardcoded secrets in every review.
  - The project lives in OneDrive, so `.venv` may get synced.
- Update this section as milestones are reached, so later sessions know where we are.

## Roadmap

Agreed order (2026-11-20, revised 2026-11-23 to cover a Senior AI Engineer job spec: RAG, evals, observability, AI security and reliability, testing, CI/CD, cloud deployment, React and ML pipelines; .NET and Java were left out on purpose). Each step builds on the previous one. Quality work (tests, tracing, evals) comes early so that every later step is measured.

0. **Basics, right after milestone 1.** Linter/formatter, pytest, logging, `.env.example`.
1. **Single-shot review (LangChain).** Your code fetches the PR and puts its data in the prompt. Claude reviews it and the result is printed. Decide whether to send the PR as JSON or as readable text with real diffs. Add tracing and token-cost tracking from the first LLM call (LangSmith), and retries/timeouts on the call. *(current)*
2. **Structured output and first evals.** Claude returns findings as Pydantic models (the "Finding" model: what, where, severity, evidence). Handle malformed model output. Build a small eval set (PRs with known bugs) and a script that scores the reviewer, then use it to measure every later prompt or design change.
3. **Tools in LangChain, with security.** Write one or two tools directly (e.g. read a full file, read one file's diff) so the user understands the agent loop. The design rule: fixed steps (which PRs, core PR data) stay in code, and the LLM calls tools only for extra context. Security: the PR diff is untrusted input (prompt injection), tools are read-only, and the agent may only call allowed tools.
4. **Own MCP server.** Move those tools into an MCP server built with the official MCP Python SDK. It's a thin layer over the existing `GitRepos`/`GitPRs` code. Connect LangChain to it through LangChain's MCP adapter, and also connect Claude Code. Concepts: tools/resources/prompts, transports (stdio vs HTTP).
5. **Compare with GitHub's official MCP server.** Look at tool count and context cost, control over outputs, and setup.
6. **RAG code index.** Per-repo chunked index with symbol and semantic search (chunking, embeddings, vector store), synced before each review. It comes before multi-agent because the tracer uses it to gather evidence.
7. **Multi-agent review (LangGraph).** Tracer and auditor pairs plus an architect, as in the demo. Compare it with the single agent on the eval set: is the extra cost and complexity worth it?
8. **Persistence and dry runs.** Store Review/Run models, skip PRs already reviewed at the same commit, and add dry vs live mode.
9. **Service.** FastAPI with GitHub webhooks, Docker, and CI/CD that runs lint, tests and evals.
10. **Cloud deployment.** Deploy to one cloud (Azure recommended, since the job spec lists it first) and add monitoring in production.
11. **React dashboard, in cowork mode.** Exception to rule 1: here Claude writes the code and the user directs and reviews it. This practises the AI-first workflow the job spec asks for, on the part that isn't the learning focus.
12. **Publishing issues and an issue checker.**
13. **Feedback loop and a small ML pipeline.** Record which findings get fixed and which get closed as false positives. Train a simple classifier that ranks or filters new findings (data, features, training, evaluation, versioning).
14. **Later / optional:** performance work (GitHub search API for open PRs, concurrency with ThreadPoolExecutor, repo config instead of every owned repo).

# Agents

This folder contains the agent and workflow layer for the AI Registration Agent Platform.

## Current Components

```text
agents
├── prompts
│   └── registration_agent_system.md
├── workflow
│   ├── graph.py
│   ├── nodes.py
│   └── state.py
└── run_workflow.py
```

## Workflow

The current LangGraph workflow is a deterministic skeleton:

```text
collect_documents
  -> extract_fields
  -> validate_documents
  -> calculate_risk
  -> decide
```

## Design Rule

LLMs can assist, summarize, and reason.

Final approval decisions must remain controlled by deterministic backend logic and reviewer workflows.

## Run Locally

```bash
cd agents
pip install -r requirements.txt
python run_workflow.py
```

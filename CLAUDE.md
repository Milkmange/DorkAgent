# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DorkAgent is a LLM-powered automated Google Dorking tool for security research, bug bounty hunting, and penetration testing reconnaissance. It uses the CrewAI framework to coordinate AI agents that discover potential security vulnerabilities and exposed sensitive information in target domains through passive reconnaissance only.

## Commands

### Running the Tool
```bash
# Interactive mode (menu-driven interface)
python dorkagent.py

# Note: CLI mode (dorkagent-cli.py) mentioned in README is not yet implemented
```

### Package Installation
```bash
# Python 3.11.9 recommended
pip install python-dotenv crewai crewai-tools langchain-openai termcolor prompt-toolkit pyfiglet schedule
```

### Environment Setup
Create `.env` file with required API keys:
```bash
SERPER_API_KEY=        # Required - https://serper.dev/
OPENAI_API_KEY=        # Optional - set if using OpenAI
ANTHROPIC_API_KEY=     # Optional - set if using Anthropic
GEMINI_API_KEY=        # Optional - set if using Gemini (recommended for free usage)
```

## High-Level Architecture

### Core Flow Architecture
The application follows a sequential workflow pattern coordinated by CrewAI:

1. **Initialization Phase**
   - `select_llm_type()`: User selects LLM provider (returns string type only)
   - `ensure_api_keys()`: Validates and prompts for missing API keys, creates `.env` if needed
   - `create_llm()`: Instantiates LLM object after keys are verified

2. **Configuration Phase**
   - Target domain input (single or from file)
   - Search depth selection (1-3 levels of subdomain wildcards)
   - Optional notification integration setup

3. **Execution Phase**
   - **Task 1**: `searcher` agent executes 30 Google Dork queries via SerperDevTool
   - **Task 2**: `bughunter` agent analyzes URLs for vulnerabilities via ScrapeWebsiteTool
   - **Task 3**: `writer` agent generates structured markdown security report

### Critical Implementation Details

**LLM Initialization Sequence** (lines 820-836):
- Must follow exact order: select type → verify keys → create instance
- `ensure_api_keys()` handles `.env` creation and key prompting
- LLM objects are created AFTER key verification to avoid initialization errors

**Agent Configuration** (`agents()` function, lines 324-371):
- All agents use `respect_context_window=True` to handle large result sets
- `allow_delegation=False` prevents agent chaining
- Max iterations set to 3 to avoid infinite loops

**Google Dork Query Structure** (`task()` function, lines 373-807):
- 30 hardcoded queries split into attack vectors (1-15) and info disclosure (16-30)
- Extensive exclusion criteria to filter false positives (lines 406-437)
- JSON-structured output format for consistent parsing

**Depth Adjustment Logic** (`adjust_depth()`, lines 267-283):
- Level 1: `domain.com`
- Level 2: `*.domain.com`
- Level 3: `*.*.domain.com`
- Wildcard domains sanitized in filenames (`*` → `wildcard`)

### Key Integration Points

**CrewAI Configuration** (lines 859-868):
- `max_rpm=15`: Rate limiting for API providers
- `respect_context_window=True`: Prevents token overflow
- Output saved to `./log/YYMMDD/` directory structure

**SerperDevTool Customization**:
- Default 10 results per query (modifiable in site-packages)
- Time range filter: `tbs: "qdr:m"` for past month
- Google search API via serper.dev service

**Model Configurations**:
- GPT-4.1 Mini: `gpt-4.1-mini-2025-04-14`
- Claude 3.5 Haiku: `anthropic/claude-3-5-haiku-20241022`
- Gemini 2.5 Flash: `gemini/gemini-2.5-flash`

## Important Operational Constraints

- **Passive reconnaissance only**: No active exploitation or testing performed
- **False positive filtering**: Extensive exclusion of documentation, demos, examples
- **Rate limiting**: 15 requests/minute to avoid API throttling
- **Context management**: Automatic handling of large result sets that exceed token limits
- **Report categorization**: Findings classified as Critical/High/Medium/Low/Info severity
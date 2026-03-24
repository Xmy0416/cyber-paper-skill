# Cyber Paper Skill

AI agent skill for automatically fetching and organizing arXiv papers on AI safety and security conferences.

## Features

- **Full Paper Capture**: Fetch ALL papers from top 4 security conferences (NDSS, USENIX Security, CCS, IEEE S&P) via arXiv
- **AI Safety Filter**: Filter AI safety papers by keywords for other sources
- **Daily Summaries**: Generate daily paper digests in structured markdown format
- **PDF Management**: Download PDFs into organized subfolders with automatic year-based folder creation
- **Deduplication**: Use soft links for duplicate content to save storage

## Supported Conferences

- **NDSS** - Network and Distributed System Security Symposium
- **USENIX Security**
- **CCS** - ACM Conference on Computer and Communications Security
- **IEEE S&P** - Symposium on Security and Privacy (Oakland)

## Installation

```bash
npx skills add Xmy0416/cyber-paper-skill
```

## Usage

### Daily Fetch (Previous Day)
```
Fetch papers from yesterday
```

### Custom Date Range
```
Fetch papers since 2026-03-01
Fetch papers from the last week
Fetch papers for 2025
```

### Specific Conference Only
```
Fetch only NDSS papers
Fetch only USENIX Security papers
```

## Storage Structure

```
paper/
├── 00-Inbox/              # Daily summaries (e.g., 2026-03-19.md)
├── ai-safety/             # AI safety papers (generic)
├── NDSS_YYYY/             # NDSS papers (auto-create year folder)
├── CCS_YYYY/
├── USENIX_Security_YYYY/
├── IEEE_SP_YYYY/
└── scripts/               # Helper scripts
```

## Output Format

Each daily summary includes:
- Paper title and link
- PDF save path
- Publication date
- Keywords
- Summary (Problem, Method, Results)

## Keywords Filtered

For non-conference sources, filters papers by:
- OpenClaw, opencode, skills, agent, mcp
- llm, gpt, claude, gemini
- prompt injection, sandbox escape, tool calling
- alignment, safety, security, trust
- autonomous, reinforcement learning, tool use

## Author

[Xmy0416](https://github.com/Xmy0416)

## License

MIT

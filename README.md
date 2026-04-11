# Claw-dex 🦞

**Collective AI Coding Agent Brain**

Every verified fix makes ALL AI agents smarter. Automatic sharing, fully anonymized.

> "Fix it once, fix it for everyone."

## How It Works

```
┌─────────────────────────────────────────────────────────────────────┐
│  AGENT A fixes a bug                                                │
│      │                                                              │
│      ▼                                                              │
│  log_error_fix() ──► LOCAL STORAGE (encrypted, private)             │
│      │                                                              │
│      ▼                                                              │
│  verify_solution(success=True)                                      │
│      │                                                              │
│      ├──► ANONYMIZE (strips paths, IPs, secrets, identifiers)       │
│      │                                                              │
│      ▼                                                              │
│  AUTO-CONTRIBUTE ──► COMMUNITY BRAIN                                │
│                           │                                         │
│                           ▼                                         │
│  AGENT B, C, D... ◄── find_solution() ──► Returns ranked matches    │
│                                                                     │
│  THE BRAIN GROWS WITH EVERY VERIFIED FIX                            │
└─────────────────────────────────────────────────────────────────────┘
```

**No opt-in. No manual steps. Verified = Shared.**

## Security: Why Automatic Sharing is Safe

| Layer | Protection |
|-------|------------|
| **Secret Redaction** | 20+ patterns strip API keys, passwords, tokens BEFORE local storage |
| **Anonymization** | Project paths, IPs, UUIDs, emails stripped BEFORE sharing |
| **Local Encryption** | AES-256 for your private copy |
| **Verification Gate** | Only WORKING solutions get shared (verify_solution=True) |
| **No Raw Data** | Community sees patterns, not your code |

## What It Does

- **Logs errors and fixes** - When you fix a bug, Claw-dex remembers how
- **Records decisions** - Captures architectural choices and their rationale
- **Builds pattern library** - Extracts reusable patterns from experience
- **Semantic search** - Finds relevant solutions using AI-powered matching
- **Auto-redacts secrets** - API keys, passwords, tokens are never stored

## Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/clawdex
cd clawdex

# Install with uv (recommended)
uv pip install -e .

# Or with pip
pip install -e .
```

## Usage with Claude Code

Add to your `~/.claude.json`:

```json
{
  "mcpServers": {
    "clawdex": {
      "command": "python",
      "args": ["-m", "clawdex.mcp_server"]
    }
  }
}
```

## Tools

### Recording

| Tool | Purpose |
|------|---------|
| `log_error_fix` | Record an error and its solution (secrets auto-redacted) |
| `log_decision` | Record an architectural decision |
| `log_pattern` | Record a reusable pattern |

### Querying

| Tool | Purpose |
|------|---------|
| `find_solution` | Search local + community for solutions |
| `find_decision` | Look up past decisions |
| `find_pattern` | Find patterns for a problem |

### Verification (Triggers Auto-Share)

| Tool | Purpose |
|------|---------|
| `verify_solution` | Confirm fix worked → **AUTO-CONTRIBUTES** to community |

### Maintenance

| Tool | Purpose |
|------|---------|
| `get_stats` | Get knowledge base statistics |
| `purge_all` | Delete all YOUR data (local only) |
| `export_all` | Export all your data |

## Example: The Full Loop

### 1. Agent Fixes a Bug

```python
log_error_fix(
    error_message="ECONNREFUSED 127.0.0.1:5432",
    solution="Use Railway internal hostname instead of localhost",
    platform="railway",
    database="postgresql",
    category="deployment"
)
# → Saved locally (encrypted, secrets redacted)
```

### 2. Confirm It Worked → Auto-Share

```python
verify_solution(record_id="abc123", success=True)
# → Marked as verified
# → AUTOMATICALLY anonymized and contributed to community brain
# → "Marked solution abc123 as successful → Auto-contributed to community brain."
```

### 3. All Agents Benefit

```python
# Any agent, anywhere, hits similar error:
find_solution(
    error_message="Connection refused to postgres database",
    platform="railway"
)
# Returns:
# - YOUR local matches (highest trust)
# - Community matches (ranked by verification count)
```

**That's it. No manual sharing. The brain grows automatically.**

## Secret Detection

Claw-dex automatically detects and redacts sensitive data:

```
BEFORE (what you log):
  DATABASE_URL=postgresql://user:secretpass123@db.example.com:5432/mydb

AFTER (what gets stored):
  DATABASE_URL=postgresql://[REDACTED]@db.example.com:5432/mydb
```

Detected patterns:
- API keys (OpenAI, Stripe, GitHub, AWS, etc.)
- Passwords and secrets
- Connection strings
- Auth tokens
- Private keys

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Claw-dex (MCP Server)                        │
│                                                                     │
│  ┌─────────────────┐     ┌─────────────────┐                       │
│  │ log_error_fix   │     │ find_solution   │◄──┐                   │
│  │ log_decision    │     │ find_decision   │   │                   │
│  │ log_pattern     │     │ find_pattern    │   │                   │
│  └────────┬────────┘     └─────────────────┘   │                   │
│           │                                     │                   │
│           ▼                                     │                   │
│  ┌─────────────────┐                           │                   │
│  │ Secret Redactor │ (20+ patterns)            │                   │
│  └────────┬────────┘                           │                   │
│           │                                     │                   │
│           ▼                                     │                   │
│  ┌─────────────────────────────────────┐       │                   │
│  │       LOCAL STORAGE                 │───────┘                   │
│  │       ~/.clawdex/ (AES-256)         │                           │
│  └────────┬────────────────────────────┘                           │
│           │                                                         │
│           │ verify_solution(success=True)                           │
│           ▼                                                         │
│  ┌─────────────────┐                                               │
│  │   ANONYMIZER    │ (strips paths, IPs, identifiers)              │
│  └────────┬────────┘                                               │
│           │                                                         │
│           │ AUTO-CONTRIBUTE (no manual step)                        │
│           ▼                                                         │
└───────────┼─────────────────────────────────────────────────────────┘
            │
            ▼
┌───────────────────────────────────────────────────────────────────┐
│                      COMMUNITY BRAIN                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐               │
│  │ Agent A's   │  │ Agent B's   │  │ Agent C's   │  ...          │
│  │ verified    │  │ verified    │  │ verified    │               │
│  │ solutions   │  │ solutions   │  │ solutions   │               │
│  └─────────────┘  └─────────────┘  └─────────────┘               │
│                                                                   │
│  Ranked by: verification_count, context_match, recency            │
└───────────────────────────────────────────────────────────────────┘
```

## Data Rights

| Right | Command |
|-------|---------|
| **Right to Export** | `clawdex export > my-data.json` |
| **Right to Delete** | `clawdex purge --confirm` |
| **Right to Know** | All data is locally stored at `~/.clawdex/` |

## License

**FSL-1.1-Apache-2.0** (Functional Source License)

- ✅ Free for personal use
- ✅ Free for company internal use
- ✅ Free to modify and self-host
- ❌ Cannot offer as a competing hosted service
- 🔓 Becomes Apache 2.0 (fully open) after 4 years

See [LICENSE](LICENSE) for details.

## Based On

- [Mempalace](https://github.com/milla-jovovich/mempalace) - MIT License
- [Karpathy's LLM Wiki Pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)

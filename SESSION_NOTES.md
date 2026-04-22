# vault404 - Session Notes

## 2026-04-22 - Frontend Live with API Integration

### Summary
Built and deployed vault404.dev frontend. Connected dashboard to live Supabase API data. Fixed demo video and docs tabs.

### Changes
- `web/index.html`: Added useLiveStats() and useLiveFeed() hooks for live API data
- `web/index.html`: Dashboard now fetches from Supabase community_solutions table
- `web/index.html`: Demo changed from iframe to link (security restriction fix)
- `web/index.html`: Docs reduced from 25 non-functional tabs to 4 working sections
- `web/vercel.json`: X-Frame-Options headers configured
- `web/.vercel/project.json`: Correct Vercel project linking

### Commits
- `0f77391` feat: connect dashboard to live Supabase API data
- `1893c2e` fix: replace demo iframe with link to avoid security restrictions
- `12f1840` fix: make docs tabs functional and fix demo iframe
- `54d0f81` feat: add vault404.dev static frontend

### Deployment
- Frontend: https://vault404.dev (Vercel)
- DNS: GoDaddy → Vercel (76.76.21.21)
- SSL: Issued via `vercel certs issue vault404.dev`

### Stats
- vault404: 448 total records
- Local: 191 (35 fixes, 11 decisions, 22 patterns)
- Community Brain: 257 (135 fixes, 13 decisions, 22 patterns)

### Testing Needed
- [ ] Verify dashboard shows live stats at vault404.dev
- [ ] Confirm feed displays recent vulnerability patterns
- [ ] Test demo video opens in new tab

### Next Steps
- Launch prep: README update, blog post, Reddit/X/HN submissions
- Frontend polish: leaderboard, severity badges, social proof

---

## 2026-04-21 - Vulnerability Intelligence Pivot Complete

### Summary
Completed the vault404 pivot to AI vulnerability intelligence platform. Added vulnerability API endpoints, MCP tools, seeded 104 vulnerability patterns locally, and synced 87 patterns to the Community Brain (Supabase).

### Changes
- `src/vault404/api/routes.py`: Added 5 vulnerability endpoints (/vulns/report, /feed, /search, /verify, /stats)
- `src/vault404/api/models.py`: Added Pydantic models for vulnerability requests/responses
- `src/vault404/tools/vulnerability.py`: NEW - 3 MCP tools (report_vulnerability, find_similar_vuln, verify_vuln_fix)
- `src/vault404/security/redactor.py`: Added VulnerabilityAnonymizer for pattern anonymization
- `src/vault404/storage/schemas.py`: Added VulnerabilityReport model
- `src/vault404/storage/local_storage.py`: Added vulnerability storage methods
- `src/vault404/mcp_server.py`: Registered 3 new vulnerability MCP tools

### Commits
- `4dd7e87` feat: add vulnerability intelligence platform features
- `bf528e5` docs: update TODO with 104 seeded vulnerabilities
- `98fc640` feat: add /vulns/seed endpoint for initial data seeding
- `8cb5c0a` fix: sync vulnerabilities to Community Brain (Supabase) instead of Railway API

### Deployment
- API redeployed to Railway with vulnerability endpoints
- Community Brain (Supabase): 87 vulnerability patterns synced

### Stats
- Local: 104 vulnerability patterns
- Community Brain: 87 vulnerability patterns
- Coverage: 19 vuln types, 11 languages, 10 frameworks
- Severity: 38 Critical, 38 High, 11 Medium

### Architecture Decision
- Vulnerabilities sync to **Community Brain (Supabase)** not Railway API
- Railway API is for external consumers; Community Brain is shared knowledge repository

### Next Steps
- Build vault404.dev frontend dashboard
- Update README with security-first positioning
- Open GitHub issues on affected repos

---

## 2026-04-16 (Session 2)

### Summary
Added live community stats badges to GitHub README. Badges show real-time fixes count, contributor count, and brain size using Shields.io dynamic endpoint format.

### Changes
- `src/vault404/api/routes.py`: Added `/api/v1/badge/{metric}` endpoint returning Shields.io JSON
- `src/vault404/sync/community.py`: Added unique contributor counting to get_stats()
- `README.md`: Added live badges for fixes (99), contributors (1), brain size
- `tests/test_mcp_tools.py`: Fixed test assertions for updated stats structure

### Commits
- `2a1f7ee` feat: add live community stats badges to README

### Deployment
- API redeployed to Railway (v0.1.3)
- Badge endpoints live at `https://web-production-7e0e3.up.railway.app/api/v1/badge/{fixes|contributors|brain}`

### Current Stats (Real Numbers)
- 99 fixes (seeded)
- 1 contributor (seed script)
- Numbers will grow organically as people use vault404

---

## 2026-04-16 (Session 1)

### Summary
Fixed `agent_brain_stats` MCP tool to show both local and community brain stats. Previously it only showed local storage (1 record), missing the 99 patterns in the remote Supabase community brain.

### Changes
- `src/vault404/sync/community.py`: Added `get_stats()` method to CommunityBrain class
- `src/vault404/tools/maintenance.py`: Updated `get_stats()` to combine local + community stats

### Commits
- `2c16ade` feat: show combined local + community brain stats

### What's Next
- Restart Claude Code to reload MCP server with updated stats
- Project is ON HOLD - letting database grow organically

### Notes
- User mentioned reverting tomorrow - unclear why, code is working correctly
- Combined stats now show: "vault404: 100 total | Local: 1 | Community: 99"

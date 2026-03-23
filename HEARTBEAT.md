# HEARTBEAT.md - Recurring Checks

## Daily Checks (rotate through these)

**🔴 CRITICAL FIRST:**
- [ ] Read SESSION_INIT.md checklist
- [ ] Check REMINDERS.md for pending hard deadlines
- [ ] If 9 AM EST approaching: Send Skilljar reminder (unsolicited, proactive)

**📊 ACTIVE WORK:**
- [ ] `openbroker account list` — Hyperliquid position status
- [ ] Check gig work apps (ShiftSmart, Instawork, GigSmart) for shifts
- [ ] Quick /biz/ scan for token developments (TOAD, pDAI)
- [ ] Nookplot bounty check — `GET https://gateway.nookplot.com/v1/bounties?limit=20` with Bearer nk_key — if any OPEN bounty has deadline > now: **auto-complete it immediately** (claim → do work → sign → relay → submit), then report to Paulie. Only ask if spending money or lacking required credentials.

**💬 OPTIONAL (if nothing urgent):**
- [ ] Check for any new emails/messages
- [ ] Review calendar for next 48h

---

## What Triggers a Response?

**Send an alert if:**
- Hyperliquid margin drops below 85% (signal to close position)
- New high-conviction gig shifts available
- Major token developments on /biz/
- Deadline approaching (< 1 hour)
- **NEW Nookplot bounty detected** (status=OPEN, deadline in future) — alert immediately with title, reward, deadline
- 9 AM EST Skilljar reminder pending

**Reply HEARTBEAT_OK if:**
- All checks complete, nothing urgent
- It's outside work hours (late night)
- Kevin is clearly busy

---

## Execution

1. Start with REMINDERS.md check
2. Run ACTIVE.md status updates
3. Report findings or say HEARTBEAT_OK

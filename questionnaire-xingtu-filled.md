# XingTu + Amulet — Filled Questionnaire with Known Answers & Actionables

## Based on The Founder's Playbook (Anthropic, 2026)
### Compiled from: pitch-package, user-portraits, viral-strategy, leads-strategy, competitive-analysis, xingtu-ai/app, bazi-research prototypes
### Date: June 20, 2026

---

## PART 1: Is the problem REAL?

### 1.1 Who exactly has this problem?

| Question | Answer | Source |
|----------|--------|--------|
| Who needs a Chinese name? | **5 documented personas:** (1) Western esoteric seekers - Sarah, 28 LA — wants depth beyond Western astrology. (2) Chinese diaspora millennials - Wei, 31 SG — needs English ZWDS for cross-cultural biz. (3) Chinese nationals - Li Wei, 34 Shanghai — wants faster/better than traditional masters. (4) B2B HR directors - Chen Ming, 42 SZ — wants psychometric ZWDS for hiring. (5) B2B dating app PMs - Rachel, 29 SF — wants compatibility API. | `xingtu-user-portrait.md` ✅ |
| Who wants daily BaZi fortune? | Assumed overlap with name gen users, but **NOT validated** through interviews. Only inferred from persona analysis. | Need customer discovery ❌ |
| Which segments will PAY? | **B2C:** Pro ($7) / Ultra ($19) one-time. **B2B:** API $0.10/chart, white-label $200/mo. Assumes 3-5% conversion. Fin model built for $30k seed → $229k Year 1 revenue. | `pitch-package.md` ✅ but NOT validated ❌ |

**Status: [V] Hypothesis documented. [ ] Validated with real users.**

### 1.2 How real is the problem?

| Question | Answer | Source |
|----------|--------|--------|
| Monthly search volume? | **Not checked.** Need keyword research: "Chinese name generator", "BaZi fortune", "ZWDS calculator", "Chinese astrology app". | ❌ Actionable |
| Existing solutions? | **11 competitors analyzed.** Gaps identified: 0 AI-native, 0 subscription model, 0 English-market ZWDS interpreter. | `competitive-analysis.html` ✅ |
| Why users dissatisfied? | **Deduced from persona research** (literal translations like "Greedy Wolf" confuse users, no narrative flow, cultural barrier). But **no actual app store reviews scraped**. | ❌ Actionable |
| Competitor breakdown | 4 categories: (1) Chart calculators (ziweicharts, wenming) — free, clunky, no AI. (2) Chinese apps (ZWDS on WeChat) — China-only, Chinese UI. (3) Western esoteric (Co-Star, The Pattern) — not ZWDS. (4) Bazi-only (Chinese Zodiac apps, Alipay Bazi) — limited. Gap: English ZWDS with AI interpretation = empty niche. | ✅ |

**Status: [V] Competitive analysis solid. [ ] Need keyword volume data. [ ] Need app store review mining.**

### 1.3 What do users do NOW?

| Behavior | Evidence | Source |
|----------|----------|--------|
| Free online generators? | Yes — ziweicharts.com, wenming.com, alipay mini-programs. All free, all clunky, no AI. | ✅ |
| Offline BaZi masters? | Yes — Chinese diaspora pays $50-150 SGD for in-person readings. Slow, expensive, language barrier. | ✅ persona research |
| Ignore the need? | Most English users simply never encounter ZWDS. Market is empty (11 competitor gaps). | ✅ competitive analysis |
| Western astrology apps? | Co-Star has 20M+ users. The Pattern has 10M+. These prove paid astrology ARPU. | ✅ |

**Key stat from competitive research:** English ZWDS Shorts get 32-520 views. Chinese ZWDS Shorts get 42K-92K views. **100-2000x gap** = untapped English demand.

### 1.4 Amulet hypothesis

| Question | Status | Action |
|----------|--------|--------|
| Is there online demand for Chinese amulets? | ❌ **Not researched.** Need to check: Etsy amulet sales, Taoist talisman shops, Alibaba/Feng Shui item trends. | **Research task** |
| Who is the amulet buyer? | **Hypothesis:** Same user who gets a Chinese name would buy a physical amulet with that name. But may be different segment (e.g., spiritual collectors vs name-seekers). | **Needs validation** |
| Willingness to pay? | **Hypothesis:** $15-30 for a blessed amulet with custom name. Based on: Etsy custom talisman range ($12-35), Feng Shui item pricing. | **Needs market test** |

**AMULET IS THE BIGGEST UNKNOWN.** The entire monetization model depends on it but **zero research done.**

---

## PART 2: Is the solution RIGHT?

### 2.1 Feature parity

| Feature | XingTu | Competitors | Gap |
|---------|--------|-------------|-----|
| Name generator EN>CN | ✅ v6 prototype done. DB: 75 EN>CN + 20 CN>EN names | ? | Need 200+ names |
| BaZi prediction | ✅ Engine: 4 pillars, elements, 12 animals, luck cycle | Only raw chart dumps | Better UX ✅ |
| Amulet tied to name | ❌ Not started | ? | **MVP blocker** |
| Behavior tracker | ❌ Not started | ? | **MVP blocker** |
| Works offline | ✅ Flutter app, built-in engine | Most need internet | Advantage ✅ |
| Monetization | ❌ Not implemented | Free or one-time | Needs stripe |

**Critical insight:** The pivot from ZWDS AI (complex, LLM-dependent) to Name Generator + BaZi (local engine, no API costs) fundamentally changes the unit economics. The old fin model assumed $0.03-0.05/chart LLM cost. The simplified engine costs **$0/chart**. This is a massive advantage but the old financial model no longer applies.

### 2.2 Three critical assumptions

**Assumption 1: Users will BUY an amulet based on their generated name**
- What we know: Viral strategy assumes shareable name card → curiosity → purchase. But no evidence name-visual → physical product conversion works.
- **If false:** Only ad-revenue model. Need $5-15 CPM. With 150k MAU and 2-3 pages/session, ad revenue = $500-1500/mo. Not enough.
- **Actionable:** Test MVP with mock amulet page. Measure click-through without real payment. If <5% click "view amulet", pivot monetization.

**Assumption 2: Free generator → traffic → conversion**
- What we know: Viral content strategy is fully built (12 content themes, week-1 calendar, 4 audience segments, 5 conversion steps). Name card viral loop designed.
- **If false:** No organic growth → paid acquisition. TG Stories CPA estimated $2-5 per install. $30k seed = 6k-15k paid users.
- **Actionable:** Launch a 2-week content test. Post 1 TikTok/Shorts/day for 14 days on "English name + Chinese astrology" angle. Track to @XingTuBot. Measures baseline viral coefficient before ANY product build.

**Assumption 3: BaZi creates retention**
- What we know: Daily fortune recurring mechanic is **not built**. Current prototype is one-shot: enter DOB → get chart → done.
- **If false:** User comes once, zero LTV. Amulet only works on first visit.
- **Actionable:** Add daily BaZi fortune push (Telegram bot can send). This is the retention engine. Must be in MVP scope.

---

## PART 3: Enough signal to build?

### 3.1 What we HAVE

| Asset | Ready | Notes |
|-------|-------|-------|
| HTML prototype (v6) with Wheel of Fate + BaZi chart | ✅ | Mobile-first, dark theme, 4 selector dials |
| Flutter app (Android + Web) | ✅ Build passes | Name engine + fortune engine working |
| BaZi engine (pillars, elements, animals, luck cycle) | ✅ | Python + Dart implementations |
| Name generator DB | ⚠️ 75 EN>CN + 20 CN>EN | Need expand to 200+ |
| Pitch package (exec summary, fin model, risks, deck) | ✅ | ZWDS-focused, needs update for Name Gen pivot |
| User portraits (5 personas) | ✅ Detailed | Sarah (29 LA), Wei (31 SG), Li Wei (34 SH), + B2B personas |
| Viral strategy (12 content themes, week-1 calendar, 4 segments, viral loop) | ✅ | Full playbook ready to execute |
| Content plan (YouTube/TikTok/Shorts) | ✅ | Platform-specific content calendars |
| Lead generation strategy (7 channels) | ✅ | TG, TikTok, Reddit, YouTube, WeChat, Xiaohongshu, Douyin |
| Competitive analysis (11 competitors, 6 gaps) | ✅ | Empty English ZWDS niche confirmed |
| Financial model | ⚠️ | Built for ZWDS AI (LLM costs). Needs recalc for Name Gen (zero engine cost, but amulet COGS) |
| Amulet e-commerce flow | ❌ | Not started. No supplier, no cart, no payment |
| Behavior tracker | ❌ | No analytics, no events, no retention measurement |
| Customer discovery interviews | ❌ | ZERO. Biggest gap. |
| Scope definition document | ❌ | No MVP scope doc. Everything ad-hoc. |
| Measurement framework | ❌ | No retention targets, no conversion baselines |
| CLAUDE.md / ADR for codebase | ❌ | No architectural context files |

### 3.2 Exit Check

| Criterion | Status | Evidence needed |
|-----------|--------|-----------------|
| Problem is real? | ✅ Strong hypothesis | Chinese names + BaZi = real interest. **But unvalidated.** |
| We know EXACT user? | ⚠️ Good personas | 5 detailed personas exist. But **not confirmed** through interviews. |
| Solution addresses real problem? | ❌ Not verified | Name generator exists. Amulet is assumption. |
| Enough signal for building? | ❌ NO | Zero customer discovery. Zero user tests. |

**MAIN GAP: Zero customer discovery. No confirmation the problem is real for specific people.**

---

## PART 4: What to build first (MVP scope)

### 4.1 MVP v1.0 — Must have (in priority order)

| # | Feature | Status | Effort | Depends on |
|---|---------|--------|--------|------------|
| 1 | **Name generator EN>CN + CN>EN** | Prototype exists | 3-5 days | Expand DB to 200+ |
| 2 | **BaZi fortune chart** | Engine exists | 2-3 days | Integrate into Flutter |
| 3 | **Wheel of Fate animation** | ✅ Done (v6 HTML) | 1 day | Port to Flutter |
| 4 | **Amulet flow** (catalog > cart > payment) | ❌ Not started | 5-8 days | Supplier → Stripe |
| 5 | **Behavior tracker** (events, analytics) | ❌ Not started | 2-3 days | PostHog or custom |
| 6 | **Multi-language** (EN/RU/ZH) | Basic skeleton | 3-5 days | Add ZH content |
| 7 | **Share image** (viral card) | Strategy designed | 2-3 days | Design + Flutter canvas |

**Total MVP effort:** ~18-28 days for a solo dev.

### 4.2 NOT in MVP

- Login wall (conversion killer at this stage)
- Prediction history (nice-to-have)
- AI interpretation (complex, expensive, not needed with BaZi engine)
- Social feed / community

### 4.3 What's MISSING before launch

| Task | Status | Actionable |
|------|--------|-----------|
| Security review | ❌ | Run Claude Code security scan. 1 day. |
| Privacy policy | ❌ | Generate from template. 2 hours. |
| Stripe / payment integration | ❌ | Need legal entity first. Depends on: **business registration**. |
| Analytics (PostHog / Amplitude) | ❌ | PostHog free tier. 1 day setup. **Do before any launch.** |
| Amulet supplier | ❌ | Research: Alibaba feng shui items, Etsy sellers, custom talisman craftsmen. **Critical path.** |
| Pre-launch landing page | ❌ | Simple single-page email capture. Build and run content test first to validate demand. |
| Beta testers (5-10) | ❌ | Recruit from TG diaspora groups. **Can start TODAY.** |
| CLAUDE.md / ADR | ❌ | Write during MVP build. |

---

## PART 5: Amulet monetization funnel

### 5.1 Conversion funnel

```
Visit (100%)
  → Generate name (hyp: 60%)
    → Interest in amulet (hyp: 10%)
      → View amulet catalog (hyp: ?)
        → Add to cart (hyp: ?)
          → Payment (hyp: 2-5% of name gen)
            → Delivery (hyp: $5-10 cost)
```

**Problem: ALL percentages are hypothetical.** No data. No prototype.

### 5.2 Business model

| Parameter | Known / Hypothesis | Status |
|-----------|-------------------|--------|
| Traffic source | Content viral loop (TikTok, Reddit, TG) | Strategy ready ✅ |
| Traffic CPM | $5-15 (TG Stories) | Estimated only ❌ |
| Name gen conversion | 60% (hyp) | Needs prototype data |
| Amulet view conversion | 10% (hyp) | Needs prototype data |
| Purchase conversion | 2-5% (hyp) | Needs MVP data |
| Avg amulet price | $15-30 (hyp) | Needs market research |
| Cost per amulet | $5-10 (hyp) | **Depends on supplier** |
| **Old fin model** | $229k Year 1, 99.5% margin | **Outdated** — assumed ZWDS AI SaaS, not amulet COGS |
| **Current reality** | Amulet COGS + Stripe fees + shipping | **Unknown margin** |

**ACTIONABLE: Rebuild financial model for amulet model.** Need supplier quotes → COGS → margin → unit economics. Then decide if the numbers work.

If amulet margin = $10 (sell $25, cost $10, fees $5) and conversion = 3%, then:
- 10,000 name gens → 300 amulets → $3,000 revenue → $1,500 margin
- 100,000 name gens → 3,000 amulets → $30,000 revenue → $15,000 margin
- Target: 3,000 amulets/mo = $15k mo margin = break-even on $30k seed in 4-6 months

### 5.3 What the tracker must measure

| Event | Priority | Why |
|-------|----------|-----|
| Name generated | P0 | Core conversion metric |
| "Get Amulet" clicked | P0 | Amulet interest signal |
| Amulet detail viewed | P0 | Product interest |
| Add to cart | P0 | Purchase intent |
| Checkout started | P0 | Funnel depth |
| Payment completed | P0 | Revenue |
| Day 1 return | P1 | Retention signal |
| Day 7 return | P1 | Retention |
| Day 30 return | P1 | Retention |
| Share card generated | P1 | Virality metric |
| Second prediction | P1 | Re-engagement |

**ACTIONABLE: Set up PostHog NOW.** Cost: $0 (free tier). Time: 1-2 hours. Even if no app built yet, instrument the HTML prototype to collect behavioral data during the content test phase.

---

## PART 6: ROADMAP — With known & unknown gates

### Phase 1 — Hypothesis validation (NOW, 1-2 weeks)

| Action | Status | Gate |
|--------|--------|------|
| **Start content test:** 1 TikTok/Shorts/day × 14 days | ❌ Not started | Tests viral coefficient. If no traction, rethink. |
| **Recruit 5-10 beta testers** from TG diaspora groups | ❌ Not started | Must happen before any build continues |
| **Conduct 5-10 discovery interviews** | ❌ Not started | **Gate for ALL subsequent phases.** If interviews contradict personas, pivot. |
| Keyword research: search volumes for name gen + BaZi | ❌ Actionable | 1 hour with Google Keyword Planner |
| Mine app store reviews of competitors | ❌ Actionable | 2-3 hours. Extract actual pain points. |
| Research amulet suppliers on Alibaba/Etsy | ❌ Actionable | 2-3 hours. Get COGS estimates. |
| **Rebuild financial model** for amulet model | ❌ Actionable | After supplier research + conversion estimates |

**GATE: Phase 1 must yield AT LEAST:**
- 3+ interviews confirming name gen interest
- 1 supplier identified with COGS estimate
- Content test showing baseline engagement
- Go/No-go decision on amulet viability

### Phase 2 — MVP Scope + Build (2-3 weeks)

| Action | Depends on |
|--------|------------|
| Write MVP scope doc | Phase 1 interviews + amulet research |
| Build amulet flow (catalog > cart > Stripe) | **Stripe account = legal entity needed** |
| Implement behavior tracker (PostHog) | None — can start NOW |
| Expand name DB to 200+ entries | None — 1-2 days work |
| Add daily BaZi fortune push (TG bot) | None — retention foundation |
| Flutter app: port v6 prototype | None — port is 3-5 days |
| Security scan (Claude Code Security) | Before any deploy |

**BLOCKER: Payment needs legal entity.** Without it, cannot process Stripe payments. Alternative: use Telegram Stars (no legal entity needed for payouts, but capped at $50k/year). Research TG Stars integration.

### Phase 3 — Beta Launch (1 week)

| Action | Depends on |
|--------|------------|
| 5-10 beta testers from Phase 1 | Phase 1 recruitment ✅ |
| MVP deployed to TestFlight / APK | Phase 2 build |
| Measurement dashboard live | Phase 2 tracker |
| Feedback loop (weekly synthesis) | Beta user engagement |
| Iterate on critical bugs | Beta feedback |

### Phase 4 — Full Launch (2-4 weeks after PMF signal)

| Action | Depends on |
|--------|------------|
| Android APK → Play Store | Phase 3 PMF evidence |
| Web → custom domain | Phase 3 |
| Content marketing push (YouTube shorts) | Phase 1 content test results |
| Paid acquisition test (TG Stories) | Phase 3 conversion data to calc LTV:CAC |
| Amulet production + logistics | Phase 1 supplier research |

---

## SUMMARY: Decision tree

```
START HERE → Run Phase 1 (content test + interviews + supplier research)
                │
                ├── Interviews show NO interest in name gen + BaZi
                │   └── PIVOT: Test amulet-only model? Or abandon project?
                │
                ├── Amulet COGS too high / supplier unavailable
                │   └── PIVOT: Subscription model (daily fortune $3/mo)
                │
                ├── Content test shows zero engagement
                │   └── PIVOT: Paid acquisition test with $500 budget
                │
                └── Phase 1 confirms hypothesis → Proceed to Phase 2
                        │
                        ├── Legal entity needed for Stripe
                        │   └── Gate: Register business OR use TG Stars
                        │
                        └── Build MVP → Beta → Launch
```

### What you can do RIGHT NOW (this week):

1. **Start PostHog** — free, cloud-hosted, 1-2 hours. Even if app isn't live, you'll need it.
2. **Post 1 TikTok on "weird English names + Chinese astrology"** — test the hook with $0 budget. See if people care.
3. **Join 3 TG diaspora groups** — introduce yourself, offer free name checks. Start building your beta list.
4. **Email 3 Etsy amulet sellers** — ask about custom name talisman pricing and lead time.
5. **Google "Chinese name generator" + "BaZi"** — first 3 results show you your real competition and what keywords they rank for.

---

**File:** `/Users/valera/workspace/bazi-research/questionnaire-xingtu-filled.md`
**Status:** All known answers compiled from existing docs. Actionables highlighted.
**Missing data:** Customer discovery interviews, amulet supplier, keyword volumes.

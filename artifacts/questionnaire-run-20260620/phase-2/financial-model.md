# Financial Model: XingTu Amulet-Based Monetization

**Date:** June 21, 2026
**Source Data:** Agent 2 Supplier Research (`agent-2-supplier.md`)
**Assumptions:** All scenarios assume no LLM inference costs (local engine), hosting $15/mo, marketing $0 (baseline viral).

---

## 1. Unit Economics — 3 Amulet Tiers

| Tier | Materials | Sell Price | COGS | Per-Unit Margin | Gross Margin % |
|------|-----------|:----------:|:----:|:---------------:|:--------------:|
| **Budget** | Stainless steel pendant + chain + simple pouch | $15.00 | $2.00 | **$13.00** | 86.7% |
| **Mid** | Gold-plated pendant + chain + velvet pouch + meaning card | $25.00 | $5.00 | **$20.00** | 80.0% |
| **Premium** | Natural jade/obsidian pendant + cord + gift box + branded card | $45.00 | $15.00 | **$30.00** | 66.7% |

**COGS basis** (from Agent 2 supplier research):
- **Budget suppliers:** xxjmetal ($0.10–$4.00 pendants), hiphoon (~$0.10 obsidian) + chain $0.30–$1.00 + pouch $0.30
- **Mid suppliers:** chenglan2014 ($1.89–$4.52 gold plated) + pouch $0.80 + card $0.20
- **Premium suppliers:** jiwanjade ($10–$30 jade) + box $1–$3 + card $0.20

### Blended Average (for funnel calculations)

Assuming sales mix of **40% Budget / 40% Mid / 20% Premium**:

| Metric | Value |
|--------|:-----:|
| Blended ASP | 0.4×$15 + 0.4×$25 + 0.2×$45 = **$25.00** |
| Blended COGS | 0.4×$2 + 0.4×$5 + 0.2×$15 = **$5.80** |
| Blended Gross Margin (pre-fees) | **$19.20** (76.8%) |

---

## 2. Conversion Funnel — 3 Scenarios

| Stage | Pessimistic | Moderate | Optimistic |
|-------|:-----------:|:--------:|:----------:|
| **Monthly traffic (visitors)** | 5,000 | 15,000 | 50,000 |
| Name generator conversion | 50% | 60% | 70% |
| → Generated names | **2,500** | **9,000** | **35,000** |
| Amulet product page view rate | 5% | 10% | 15% |
| → Amulet page views | **125** | **900** | **5,250** |
| Purchase conversion rate | 2% | 3% | 5% |
| → **Monthly orders** | **2.5** | **27** | **262.5** |

### Monthly Per-Order Breakdown (blended averages)

| Item | Per Order (Blended) |
|------|:-------------------:|
| Revenue | $25.00 |
| COGS | $5.80 |
| Stripe fee (2.9% + $0.30) | $1.025 |
| Gross profit (pre-shipping) | **$18.175** |

> **Note on shipping:** If using supplier direct-ship from China (~$4–$6/unit), add $5/order to COGS which would reduce blended margin to **$13.175/order**. D2C model with bulk import + 3PL fulfillment would achieve the COGS shown above (shipping baked into bulk sea freight at ~$1.50/unit). The model below assumes bulk import (COGS as stated).

---

## 3. Monthly P&L — 12-Month Projection

### Pessimistic Scenario (2.5 orders/mo, flat)

| Month | Orders | Revenue | COGS | Stripe Fees | Gross Profit | Hosting | Mktg | **Net** |
|:----:|:-----:|:-------:|:----:|:-----------:|:------------:|:-------:|:----:|:------:|
| 1 | 2 | $50.00 | $11.60 | $2.05 | $36.35 | $15 | $0 | **$21.35** |
| 2 | 3 | $75.00 | $17.40 | $3.08 | $54.53 | $15 | $0 | **$39.53** |
| 3 | 2 | $50.00 | $11.60 | $2.05 | $36.35 | $15 | $0 | **$21.35** |
| 4 | 3 | $75.00 | $17.40 | $3.08 | $54.53 | $15 | $0 | **$39.53** |
| 5 | 2 | $50.00 | $11.60 | $2.05 | $36.35 | $15 | $0 | **$21.35** |
| 6 | 3 | $75.00 | $17.40 | $3.08 | $54.53 | $15 | $0 | **$39.53** |
| 7 | 2 | $50.00 | $11.60 | $2.05 | $36.35 | $15 | $0 | **$21.35** |
| 8 | 3 | $75.00 | $17.40 | $3.08 | $54.53 | $15 | $0 | **$39.53** |
| 9 | 2 | $50.00 | $11.60 | $2.05 | $36.35 | $15 | $0 | **$21.35** |
| 10 | 3 | $75.00 | $17.40 | $3.08 | $54.53 | $15 | $0 | **$39.53** |
| 11 | 2 | $50.00 | $11.60 | $2.05 | $36.35 | $15 | $0 | **$21.35** |
| 12 | 3 | $75.00 | $17.40 | $3.08 | $54.53 | $15 | $0 | **$39.53** |
| **Year 1** | **30** | **$750.00** | **$174.00** | **$30.75** | **$545.25** | **$180** | **$0** | **$365.25** |

### Moderate Scenario (27 orders/mo, flat)

| Month | Orders | Revenue | COGS | Stripe Fees | Gross Profit | Hosting | Mktg | **Net** |
|:----:|:-----:|:-------:|:----:|:-----------:|:------------:|:-------:|:----:|:------:|
| 1 | 27 | $675.00 | $156.60 | $27.68 | $490.73 | $15 | $0 | **$475.73** |
| 2 | 27 | $675.00 | $156.60 | $27.68 | $490.73 | $15 | $0 | **$475.73** |
| 3 | 27 | $675.00 | $156.60 | $27.68 | $490.73 | $15 | $0 | **$475.73** |
| 4 | 27 | $675.00 | $156.60 | $27.68 | $490.73 | $15 | $0 | **$475.73** |
| 5 | 27 | $675.00 | $156.60 | $27.68 | $490.73 | $15 | $0 | **$475.73** |
| 6 | 27 | $675.00 | $156.60 | $27.68 | $490.73 | $15 | $0 | **$475.73** |
| 7 | 27 | $675.00 | $156.60 | $27.68 | $490.73 | $15 | $0 | **$475.73** |
| 8 | 27 | $675.00 | $156.60 | $27.68 | $490.73 | $15 | $0 | **$475.73** |
| 9 | 27 | $675.00 | $156.60 | $27.68 | $490.73 | $15 | $0 | **$475.73** |
| 10 | 27 | $675.00 | $156.60 | $27.68 | $490.73 | $15 | $0 | **$475.73** |
| 11 | 27 | $675.00 | $156.60 | $27.68 | $490.73 | $15 | $0 | **$475.73** |
| 12 | 27 | $675.00 | $156.60 | $27.68 | $490.73 | $15 | $0 | **$475.73** |
| **Year 1** | **324** | **$8,100.00** | **$1,879.20** | **$332.10** | **$5,888.70** | **$180** | **$0** | **$5,708.70** |

### Optimistic Scenario (262.5 orders/mo, flat)

| Month | Orders | Revenue | COGS | Stripe Fees | Gross Profit | Hosting | Mktg | **Net** |
|:----:|:-----:|:-------:|:----:|:-----------:|:------------:|:-------:|:----:|:------:|
| 1 | 263 | $6,562.50 | $1,522.50 | $269.06 | $4,770.94 | $15 | $0 | **$4,755.94** |
| 2 | 263 | $6,562.50 | $1,522.50 | $269.06 | $4,770.94 | $15 | $0 | **$4,755.94** |
| 3 | 263 | $6,562.50 | $1,522.50 | $269.06 | $4,770.94 | $15 | $0 | **$4,755.94** |
| 4 | 263 | $6,562.50 | $1,522.50 | $269.06 | $4,770.94 | $15 | $0 | **$4,755.94** |
| 5 | 263 | $6,562.50 | $1,522.50 | $269.06 | $4,770.94 | $15 | $0 | **$4,755.94** |
| 6 | 263 | $6,562.50 | $1,522.50 | $269.06 | $4,770.94 | $15 | $0 | **$4,755.94** |
| 7 | 263 | $6,562.50 | $1,522.50 | $269.06 | $4,770.94 | $15 | $0 | **$4,755.94** |
| 8 | 263 | $6,562.50 | $1,522.50 | $269.06 | $4,770.94 | $15 | $0 | **$4,755.94** |
| 9 | 263 | $6,562.50 | $1,522.50 | $269.06 | $4,770.94 | $15 | $0 | **$4,755.94** |
| 10 | 263 | $6,562.50 | $1,522.50 | $269.06 | $4,770.94 | $15 | $0 | **$4,755.94** |
| 11 | 263 | $6,562.50 | $1,522.50 | $269.06 | $4,770.94 | $15 | $0 | **$4,755.94** |
| 12 | 263 | $6,562.50 | $1,522.50 | $269.06 | $4,770.94 | $15 | $0 | **$4,755.94** |
| **Year 1** | **3,150** | **$78,750.00** | **$18,270.00** | **$3,228.75** | **$57,251.25** | **$180** | **$0** | **$57,071.25** |

---

## 4. Break-Even Analysis ($30k Seed Investment)

### Scenario: Seed Burn Rate

Seed capital: **$30,000** — assumed used for:
- Product development (BaZi engine, app): $10k–$15k (one-time)
- First inventory batch (~500 units): ~$2,700 (per Agent 2 estimate)
- Packaging, branding, samples: ~$2,000
- Legal, domain, misc: ~$2,000
- Working capital / buffer: ~$13,300

The $30k is not "burned monthly" — it's a one-time investment. Break-even measures months to recoup that investment from net profit.

| Scenario | Monthly Net | Months to Break-Even (30k) | Time |
|----------|:----------:|:--------------------------:|:----:|
| **Pessimistic** | $30.44 | **~985 months** | **Never (82 years)** |
| **Pessimistic + $500/mo mktg** | -$484.56 | Never profitable | Never |
| **Moderate** | $475.73 | **~63 months** | **5.25 years** |
| **Moderate + $500/mo mktg** | -$24.27 | Never profitable | Never |
| **Optimistic** | $4,755.94 | **~6.3 months** | **6.3 months** |
| **Optimistic + $500/mo mktg** | $4,255.94 | **~7.0 months** | **7 months** |

### Break-Even Sensitivity Table (Moderate + Optimistic)

| If Monthly Net Is... | Months to Break-Even ($30k) |
|:--------------------:|:---------------------------:|
| $500 | 60.0 |
| $1,000 | 30.0 |
| $2,000 | 15.0 |
| $3,000 | 10.0 |
| $4,000 | 7.5 |
| $5,000 | 6.0 |
| $7,500 | 4.0 |

---

## 5. Scenario Comparison Summary

| Metric | Pessimistic | Moderate | Optimistic |
|--------|:-----------:|:--------:|:----------:|
| Monthly traffic | 5,000 | 15,000 | 50,000 |
| Monthly orders | ~2.5 | ~27 | ~263 |
| Monthly revenue | $62.50 | $675 | $6,562.50 |
| Monthly net profit | **$30.44** | **$475.73** | **$4,755.94** |
| Year 1 revenue | $750 | $8,100 | $78,750 |
| Year 1 net profit | **$365.25** | **$5,708.70** | **$57,071.25** |
| Break-even on $30k | **Never** | **5.25 yr** | **6.3 mo** |
| Net margin % | 48.7% | 70.5% | 72.5% |

---

## 6. Operating Cost Breakdown

| Cost Item | Monthly | Annual | Notes |
|-----------|:-------:|:------:|-------|
| **Hosting (VPS/cloud)** | $15 | $180 | Local inference, no GPU needed |
| **LLM inference** | $0 | $0 | Running on local hardware (already owned) |
| **Domain + email** | $2 | $24 | ~$12/yr domain + email routing |
| **Stripe payment processing** | ~2.9% + $0.30/order | Varies | Included in P&L above |
| **Marketing (baseline)** | $0 | $0 | Viral/organic via name-generator SEO |
| **Marketing (optional)** | $500 | $6,000 | Social ads, influencer seeding |
| **Shipping (if not in COGS)** | $5/order | Varies | Dropshipping add-on; bulk import avoids this |
| **Total fixed costs (baseline)** | **~$17/mo** | **~$204/yr** | Hosting + domain |

---

## 7. Key Takeaways

1. **Moderate scenario is viable but slow** — $476/mo net is not a business, it's a side project. Break-even on $30k takes 5+ years.

2. **Optimistic scenario justifies the investment** — $4,756/mo net yields 6.3-month break-even and >$57k/year profit. Requires 50k monthly visitors and solid conversion (5% purchase rate on amulet page views).

3. **Pessimistic scenario is fatal** — even with zero marketing cost, ~$30/mo doesn't cover the time investment. The venture must clear at least 5k amulet page views/month (Moderate) to be viable.

4. **Marketing spend is dangerous at Moderate scale** — $500/mo marketing at Moderate levels wipes out all profit. Marketing only makes sense at Optimistic traffic levels.

5. **The key lever is traffic to the name generator** — every percentage point improvement in traffic → name gen → amulet view → purchase compounds directly to the bottom line. SEO/content marketing for the BaZi name generator is the highest-ROI activity.

6. **Blended COGS of $5.80 is conservative** — at scale (1,000+ units), bulk discounts could push blended COGS to $4.00–$4.50, improving margins by ~$1.30–$1.80/unit.

---

*Financial model generated from Agent 2 supplier research data. All figures in USD. Scenarios assume flat monthly performance; real-world results would include ramp-up periods, seasonal fluctuations, and growth curves.*

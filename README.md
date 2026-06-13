# BaZi (八字) — Four Pillars of Destiny Research

> Complete research project: fundamentals, calculator, interpretation engine, name converter, and educational web app.  
> Built from bilingual (Chinese/English) source PDFs with deep web research to fill curriculum gaps.

## 📦 Repository Contents

| File | Type | Description |
|------|------|-------------|
| `consolidated-knowledge-base.md` | 📄 Research | Merged PDF content — all stems, branches, hidden stems, interactions, 60-cycle, void branches |
| `bazi_seasonal_power_nayin_reference.md` | 📄 Research | 旺相休囚死 (Seasonal Power) full table + Na Yin (纳音) all 30 tones |
| `bazi_luck_pillar_calculation.md` | 📄 Research | Luck Pillar (大运) formulas — direction, starting age, derivation, classical quotes |
| `bazi_special_patterns.md` | 📄 Research | 专旺格 (5 types) + 从格 (4 types) + 假格 + elemental balance + decision trees + 4 examples |
| `interpretation-guide.md` | 📄 Guide | Step-by-step reading flow, Day Master scoring (1-10), 10 named configurations, 3 full chart walkthroughs |
| `bazi-master-handbook.md` | 📄 Handbook | All-in-one 10-section reference with quick charts, glossaries, and cheat sheets |
| `bazi_calculator.py` | 🐍 Tool | **Working CLI calculator** — Four Pillars, Day Master, Seasonal Power, Hidden Stems, Ten Gods, Luck Pillars, Special Patterns, Void Branches, Na Yin |
| `bazi_luck_pillar_algorithm.py` | 🐍 Tool | Standalone Luck Pillar calculator (embedded in `bazi_calculator.py`) |
| `name_converter.py` | 🐍 Tool | CLI — Chinese pinyin conversion + character meanings (388 chars) + name analysis + search |
| `name_converter.html` | 🌐 App | Web UI — 4-tab interface for pinyin, meaning, analysis, search |
| `name-converter-v2.html` | 🌐 App | **v2** — Single-page compact, auto-demo loop with 10 names, all JS, zero dependencies |
| `bazi-academy.html` | 🌐 App | **Full educational app** — 6 modules (free + paid), chart calculator, name converter, progress tracking |

## 🚀 Quick Start

```bash
# BaZi chart from date of birth
python3 bazi_calculator.py -y 1990 -m 3 -d 15 -H 14 -g male --name "Example"

# Name conversion (requires: pip3 install pypinyin)
python3 name_converter.py --pinyin 阿历山大 --no-tone --caps
python3 name_converter.py --meaning 伟
python3 name_converter.py --name 张伟明

# Open web apps (no server needed)
open bazi-academy.html
open name-converter-v2.html
```

### Calculator Features
- Four Pillars computation from Gregorian DOB (solar term–aware)
- Day Master identification + seasonal power assessment (旺相休囚死)
- Hidden Stems extraction (地支藏干)
- Ten Gods mapping (十神)
- Luck Pillar calculation (大运) — 8 pillars with age ranges
- Special pattern detection (专旺格, 从格)
- Void Branches (空亡) detection
- Na Yin (纳音) tones for each pillar
- 17 built-in self-tests: `python3 bazi_calculator.py --test`

## 📊 Research Process

7 phases executed via subagent workflow:

```
Phase 1: Consolidate PDFs → knowledge base
Phase 2: 3 parallel deep research agents → seasonal power, luck pillars, special patterns
Phase 3: Build integrated Python calculator
Phase 4: Interpretation patterns synthesis
Phase 5: Master handbook & cheat sheets
Phase 6a: Name Converter (CLI + Web)
Phase 6b: BaZi Academy educational app
```

Total: ~6.3M tokens across 8 subagents + direct work.

## License

MIT — free for study, reference, and building your own BaZi tools.

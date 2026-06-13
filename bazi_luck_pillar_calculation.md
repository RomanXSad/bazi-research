# Luck Pillar (大运 / Dà Yùn) Complete Calculation Method

> Research reference: 渊海子平 (Yuan Hai Zi Ping), 三命通会 (San Ming Tong Hui)
> Compiled for deep BaZi research project — chart calculator implementation

---

## Table of Contents

1. [Fundamental Concepts](#1-fundamental-concepts)
2. [Forward vs Reverse Cycle (顺逆)](#2-forward-vs-reverse-cycle-顺逆)
3. [Starting Age Calculation (起运数)](#3-starting-age-calculation-起运数)
4. [Deriving Luck Pillars from the Month Pillar](#4-deriving-luck-pillars-from-the-month-pillar)
5. [The 10-Year Period Per Pillar](#5-the-10-year-period-per-pillar)
6. [Annual Pillars — 流年 (Liú Nián)](#6-annual-pillars--流年-liú-nián)
7. [Interaction: Natal Chart × Luck Pillar × Annual Pillar](#7-interaction-natal-chart--luck-pillar--annual-pillar)
8. [Classical Formulas from 渊海子平 & 三命通会](#8-classical-formulas-from-渊海子平--三命通会)
9. [Worked Examples](#9-worked-examples)
10. [Algorithm Summary for Implementation](#10-algorithm-summary-for-implementation)
11. [Special Cases & Edge Cases](#11-special-cases--edge-cases)

---

## 1. Fundamental Concepts

### 1.1 What is a Luck Pillar?

A Luck Pillar (大运, Dà Yùn, "Great Fortune") is a ten-year period of life governed by a specific Heavenly Stem (天干) and Earthly Branch (地支) pair. A complete BaZi chart has **eight Luck Pillars** (occasionally six or ten), covering the entire post-childhood lifespan of approximately 80 years.

> 渊海子平 卷一: "大运者，命运之流行也。运之为言，动也。"
> "Great Fortune is the flow of destiny. Fortune speaks of movement."

### 1.2 The Relationship to the Month Pillar

The Luck Pillars are derived **from the Month Pillar (月柱)** of the natal chart. They are not based on the Year Pillar or Day Pillar. The direction of derivation (forward or backward) and the offset magnitude are determined by two factors:

1. **The Yin/Yang nature of the Heavenly Stem of the Day Pillar (日干)**
2. **The gender (sex) of the person (男/女)**

---

## 2. Forward vs Reverse Cycle (顺逆)

### 2.1 The Cardinal Rule

| Birth Chart Condition | Direction of Luck Pillars |
|---|---|
| **Yang Male (阳男)** — Male born under a Yang Day Stem (甲丙戊庚壬) | **Forward (顺排)** — count up from Month Pillar |
| **Yin Female (阴女)** — Female born under a Yin Day Stem (乙丁己辛癸) | **Forward (顺排)** — count up from Month Pillar |
| **Yin Male (阴男)** — Male born under a Yin Day Stem (乙丁己辛癸) | **Reverse (逆排)** — count down from Month Pillar |
| **Yang Female (阳女)** — Female born under a Yang Day Stem (甲丙戊庚壬) | **Reverse (逆排)** — count down from Month Pillar |

> 渊海子平: "阳男阴女，顺行其运；阴男阳女，逆行其运。"
> "Yang male and Yin female, their luck moves forward; Yin male and Yang female, their luck moves backward."

### 2.2 Mnemonic

- **Yang Male + Yin Female** = FORWARD (顺) — like the natural flow of Yang energy, like Yin energy following its natural course
- **Yin Male + Yang Female** = REVERSE (逆) — against the natural flow, a counter-situation

### 2.3 Why?

In classical Chinese cosmology:
- Yang is associated with the exterior, the masculine, the forward-moving
- Yin is associated with the interior, the feminine, the receptive
- A Yang Day Master in a male body = double Yang — natural forward progression
- A Yin Day Master in a female body = double Yin — natural forward progression
- A Yin Day Master in a male body = Yin within Yang — reverse or counter-flow needed
- A Yang Day Master in a female body = Yang within Yin — reverse or counter-flow needed

---

## 3. Starting Age Calculation (起运数)

### 3.1 The Core Principle

The starting age (起运年龄) of the first Luck Pillar is determined by counting the **number of days between the birth date and the nearest Solar Term (节气) boundary**, then converting days into years and months.

### 3.2 Solar Term Boundaries

There are 12 major Solar Terms (节, Jié) used as boundaries:

| # | Solar Term | Approx Date | English |
|---|---|---|---|
| 1 | 立春 Lì Chūn | Feb 4 | Spring Begins |
| 2 | 惊蛰 Jīng Zhé | Mar 6 | Insects Awaken |
| 3 | 清明 Qīng Míng | Apr 5 | Pure Brightness |
| 4 | 立夏 Lì Xià | May 6 | Summer Begins |
| 5 | 芒种 Máng Zhòng | Jun 6 | Grain in Ear |
| 6 | 小暑 Xiǎo Shǔ | Jul 7 | Slight Heat |
| 7 | 立秋 Lì Qiū | Aug 8 | Autumn Begins |
| 8 | 白露 Bái Lù | Sep 8 | White Dew |
| 9 | 寒露 Hán Lù | Oct 8 | Cold Dew |
| 10 | 立冬 Lì Dōng | Nov 7 | Winter Begins |
| 11 | 大雪 Dà Xuě | Dec 7 | Great Snow |
| 12 | 小寒 Xiǎo Hán | Jan 6 | Slight Cold |

These correspond to the first day of each of the 12 lunar months in the Chinese calendar system.

### 3.3 Which Boundary to Count To?

- **Forward cycle (顺排)**: Count the days from the birth date **forward** to the **next** Solar Term boundary
- **Reverse cycle (逆排)**: Count the days from the birth date **backward** to the **previous** Solar Term boundary

**Important**: Count only the days in the interval. The counting method is:

- If the child is born **on or after** the current Solar Term → count forward days to the next Solar Term
- If the child is born **before** the current Solar Term → count backward days to the previous Solar Term

Wait — more precisely:

**Step 1**: Determine the current Solar Term that governs the birth month. Each month in the Chinese calendar begins with a major Solar Term (节).

**Step 2**:
- **Forward cycle**: Count the number of days from the birth date (inclusive or exclusive — see classical debate below) to the **next** major Solar Term.
- **Reverse cycle**: Count the number of days from the **previous** major Solar Term to the birth date (inclusive/exclusive).

### 3.4 The 3-Days-Equals-1-Year Formula

This is the classical conversion method from 渊海子平:

> **3 days = 1 year (3天 = 1年)**
> **1 day = 4 months (1天 = 4个月)**
> **1 two-hour period (时辰) = 5 days (1时辰 = 5天)**

| Days Counted | Starting Age |
|---|---|
| 3 days | 1 year old (周岁) |
| 6 days | 2 years old |
| 9 days | 3 years old |
| 12 days | 4 years old |
| ... | ... |
| N days | N/3 years (rounded) |

#### Inclusive vs Exclusive Counting (Classical Debate)

- **渊海子平 method**: Count by a "3 days = 1 year" ratio. If birth is on the boundary day itself, some schools count it as 0 days (starting age = 0, meaning first Luck Pillar begins at birth); others count it as 1 day (starting age = 4 months).
- **三命通会 method**: More precise. Count the actual number of days and hours. Use the full conversion:
  - 3 days = 1 year
  - Remainder days: 1 day = 4 months
  - Remainder 2-hour periods: 1 时辰 (2 hours) = 5 days (of life, not years)
  - Remainder hours: 1 hour ≈ 2.5 days

### 3.5 Modern Practical Formula

Most modern practitioners use this algorithm:

```
function calc_starting_age(birth_date, next_term_date, direction, birth_hour):
    if direction == FORWARD:
        day_diff = next_term_date - birth_date  // in days
    else: // REVERSE
        day_diff = birth_date - prev_term_date  // in days

    // 3 days = 1 year
    years = floor(day_diff / 3)
    remainder_days = day_diff % 3

    // 1 day = 4 months
    months = remainder_days * 4

    // Add fraction from birth hour
    // (birth hour as fraction of a 12-hour period, roughly)

    return { years: years, months: months }
```

> **Note**: Day_diff is usually treated as an integer (number of 24-hour periods). Some traditions count partial days based on the birth hour (时辰) within the birth date.

### 3.6 The "First Day or Two" Rule

There is a special classical consideration:

- If day_diff = 0 (birth exactly on the Solar Term boundary): Starting age = **0 years** (first Luck Pillar begins immediately at birth — or some say at age 1).
- If day_diff = 1 or 2: The person starts their first Luck Pillar at **4 months old** (1 day) or **8 months old** (2 days). In some traditions these are rounded up to 1 year.
- Some conservative schools always round up to the nearest whole year.

### 3.7 Example: Forward Cycle Counting

**Birth**: Male, Yang Day Stem (e.g., 甲), born May 20, 1985
**Next Solar Term**: 芒种 (June 6, 1985)
**Day difference**: June 6 - May 20 = 17 days
**Starting age**: 17/3 = 5 years, remainder 2 days
   → 5 years + (2 × 4 months) = **5 years 8 months old**
   → First Luck Pillar starts at approximately **age 6** (rounded up by convention)

---

## 4. Deriving Luck Pillars from the Month Pillar

### 4.1 The Forward Cycle (顺排)

Starting from the Month Pillar, each successive Luck Pillar advances by **one Heavenly Stem** and **one Earthly Branch** in the standard sexagenary cycle order.

**Example**: Month Pillar = 乙卯 (Yǐ-Mǎo), Forward

| Luck Pillar # | Formula | Result |
|---|---|---|
| LP1 (First Luck Pillar) | Month Pillar + 1 Stem + 1 Branch | 丙辰 (Bǐng-Chén) |
| LP2 | Month Pillar + 2 Stems + 2 Branches | 丁巳 (Dīng-Sì) |
| LP3 | Month Pillar + 3 Stems + 3 Branches | 戊午 (Wù-Wǔ) |
| LP4 | ... | 己未 (Jǐ-Wèi) |
| LP5 | ... | 庚申 (Gēng-Shēn) |
| LP6 | ... | 辛酉 (Xīn-Yǒu) |
| LP7 | ... | 壬戌 (Rén-Xū) |
| LP8 | ... | 癸亥 (Guǐ-Hài) |

### 4.2 The Reverse Cycle (逆排)

Starting from the Month Pillar, each successive Luck Pillar moves **backward** by **one Heavenly Stem** and **one Earthly Branch**.

**Example**: Month Pillar = 乙卯 (Yǐ-Mǎo), Reverse

| Luck Pillar # | Formula | Result |
|---|---|---|
| LP1 | Month Pillar - 1 Stem - 1 Branch | 甲寅 (Jiǎ-Yín) |
| LP2 | Month Pillar - 2 Stems - 2 Branches | 癸丑 (Guǐ-Chǒu) |
| LP3 | Month Pillar - 3 Stems - 3 Branches | 壬子 (Rén-Zǐ) |
| LP4 | ... | 辛亥 (Xīn-Hài) |
| LP5 | ... | 庚戌 (Gēng-Xū) |
| LP6 | ... | 己酉 (Jǐ-Yǒu) |
| LP7 | ... | 戊申 (Wù-Shēn) |
| LP8 | ... | 丁未 (Dīng-Wèi) |

### 4.3 Stem and Branch Index Arithmetic

The Heavenly Stems (干) and Earthly Branches (支) are indexed 0-9 and 0-2 respectively (or 1-10 and 1-12):

**Forward shift:**
```
stem_index = (month_stem_index + offset) % 10
branch_index = (month_branch_index + offset) % 12
```

**Backward shift:**
```
stem_index = (month_stem_index - offset) % 10   // handle negative modulo
branch_index = (month_branch_index - offset) % 12  // handle negative modulo
```

Where `offset` ranges from 1 to N (number of Luck Pillars).

### 4.4 The Ten Stems Sequence

```
0: 甲 (Jiǎ, Yang Wood)     5: 己 (Jǐ, Yin Earth)
1: 乙 (Yǐ, Yin Wood)       6: 庚 (Gēng, Yang Metal)
2: 丙 (Bǐng, Yang Fire)    7: 辛 (Xīn, Yin Metal)
3: 丁 (Dīng, Yin Fire)     8: 壬 (Rén, Yang Water)
4: 戊 (Wù, Yang Earth)     9: 癸 (Guǐ, Yin Water)
```

### 4.5 The Twelve Branches Sequence

```
0: 子 (Zǐ, Yang Water/Rat)     6: 午 (Wǔ, Yin Fire/Horse)
1: 丑 (Chǒu, Yin Earth/Ox)     7: 未 (Wèi, Yin Earth/Sheep)
2: 寅 (Yín, Yang Wood/Tiger)   8: 申 (Shēn, Yang Metal/Monkey)
3: 卯 (Mǎo, Yin Wood/Rabbit)   9: 酉 (Yǒu, Yin Metal/Rooster)
4: 辰 (Chén, Yang Earth/Dragon) 10: 戌 (Xū, Yang Earth/Dog)
5: 巳 (Sì, Yin Fire/Snake)    11: 亥 (Hài, Yin Water/Pig)
```

---

## 5. The 10-Year Period Per Pillar

### 5.1 Basic Definition

Each Luck Pillar governs exactly **10 years** of a person's life. The first Luck Pillar covers from the starting age (起运年龄) to starting age + 10. The second from starting age + 10 to starting age + 20, and so on.

### 5.2 Life Stages Mapped

| Luck Pillar | Age Range | Life Stage (Classical) |
|---|---|---|
| LP1 (初运) | 0-10 or starting age + 10 | Childhood / Early youth |
| LP2 | starting age + 10 to + 20 | Adolescence / Young adult |
| LP3 | starting age + 20 to + 30 | Early career / Marriage |
| LP4 | starting age + 30 to + 40 | Peak career / Family |
| LP5 | starting age + 40 to + 50 | Mid-life / Maturity |
| LP6 | starting age + 50 to + 60 | Later career / Wisdom |
| LP7 | starting age + 60 to + 70 | Retirement / Reflection |
| LP8 | starting age + 70 to + 80 | Old age / Legacy |

### 5.3 Transition Year

At the precise age where one Luck Pillar ends and another begins, there is a transitional year called **交运 (Jiāo Yùn)** — "crossing fortunes." This is considered an unstable year where:
- The influence of both the ending and beginning Luck Pillars is present
- Events can be unpredictable
- It's traditionally advised to avoid major life decisions during this year

### 5.4 Fractional Starting Age Handling

If a person's starting age is 5 years 8 months:
- LP1 (丙辰): Age 5.67 to 15.67 (≈ age 6 to 16 in whole years)
- LP2 (丁巳): Age 15.67 to 25.67 (≈ age 16 to 26)

Most modern chart software rounds to the nearest whole year and displays as:
- LP1: Age 6-15
- LP2: Age 16-25
- LP3: Age 26-35
- etc.

### 5.5 Early vs Late Luck

- **Early Luck (早年运)**: Starting age ≤ 6 — person experiences Luck Pillars early in life; childhood environment is strongly shaped by Luck
- **Normal Luck (中运)**: Starting age 7-13 — most common; Luck Pillars begin around adolescence
- **Late Luck (晚运)**: Starting age ≥ 14 — person experiences childhood without Luck Pillar influence, more dependent on natal chart alone

> 三命通会: "运早者早发，运晚者晚成。"
> "Those with early luck achieve early; those with late luck succeed late."

---

## 6. Annual Pillars — 流年 (Liú Nián)

### 6.1 Definition

Each year has its own Pillar called the **Annual Pillar** (流年/太岁, Liú Nián/Tài Suì). It is simply the sexagenary pair for any given year. For example, 2024 is 甲辰 (Jiǎ-Chén, Yang Wood/Dragon).

The Annual Pillar represents the external environment, the "weather" of that year — collective trends, social forces, and opportunities/challenges that everyone experiences to some degree.

### 6.2 The Three-Pillar Interaction

The reading of any given year involves analyzing the interaction between:

```
Natal Chart (八字/四柱)  ←  foundation / intrinsic nature
    ×
Current Luck Pillar (大运)  ←  10-year trend / macro environment
    ×
Annual Pillar (流年太岁)  ←  current year's energy / micro environment
```

> 渊海子平: "大运如君，流年如臣；君臣合德，吉凶可断。"
> "The Luck Pillar is like the ruler, the Annual Pillar is like the minister; when ruler and minister are in harmony, fortune and misfortune can be determined."

### 6.3 Interaction Types

#### 6.3.1 Annual Pillar × Luck Pillar

| Interaction | Meaning |
|---|---|
| Same Heavenly Stem | Year amplifies the Luck Pillar's energy |
| Same Earthly Branch | Year activates the Luck Pillar's branch |
| Stem-Branch Combination (合) | Year merges with Luck — transformative events |
| Stem-Branch Clash (冲) | Conflict between year and decade trend — upheaval |
| Stem-Branch Harm (害) | Subtle friction — delays and obstacles |
| Stem-Branch Punishment (刑) | Legal/family/health issues activated |
| Stem-Branch Destruction (破) | Breakdown of plans, financial loss |

#### 6.3.2 Annual Pillar × Natal Chart Pillars

The Annual Pillar interacts with all four natal pillars:

1. **年柱 (Year Pillar)** — Family, ancestors, early life
   - Clash with Annual = family changes, moving, foundation shaken
2. **月柱 (Month Pillar)** — Career, parents, social life
   - Clash with Annual = career upheaval, relationship with parents
3. **日柱 (Day Pillar)** — Self, spouse, health
   - Clash with Annual = personal challenges, marriage issues, health crisis
4. **时柱 (Hour Pillar)** — Children, late life, hidden talents
   - Clash with Annual = issues with children, projects ending

#### 6.3.3 Annual Pillar × Day Master (日主)

This is the most critical interaction:

- **Annual Stem** generates, controls, or is generated/controlled by the Day Master
- **Annual Branch** contains Hidden Stems (藏干) that may interact with the Day Master's elemental needs (用神)
- **Nobleman** (天乙贵人) or **Demon** (羊刃/七杀) stars activated by the Annual Pillar

### 6.4 Annual Pillar Years and Calendrical Basis

The Annual Pillar changes at **Lì Chūn (立春)**, NOT at January 1 or Chinese New Year. This is a critical distinction:

- Before Lì Chūn in a given year → still under the previous year's Annual Pillar
- On or after Lì Chūn → under the new year's Annual Pillar

> 渊海子平: "立春为岁首。"
> "Lì Chūn is the beginning of the year."

### 6.5 The 60-Year Cycle and 本命年 (Běn Mìng Nián)

- Every 60 years, the Annual Pillar repeats the sexagenary cycle
- **本命年 (Ben Ming Nian / Year of One's Own Sign)**: The year whose Earthly Branch matches the Earthly Branch of the person's Year Pillar
  - Example: A person born in 甲子年 (Rat) — every 子 year (e.g., 2020, 2032) is their 本命年
  - Traditionally considered challenging (like confronting one's own Tai Sui)
  - The Luck Pillar's interaction can mitigate or worsen this

### 6.6 犯太岁 (Fàn Tài Suì) — Offending Tai Sui

When the Annual Pillar's Earthly Branch conflicts with a natal branch:

| Type | Meaning | Classical Description |
|---|---|---|
| **值太岁 (Zhí Tài Suì)** | Same branch (本命年) | Like running into yourself — destabilizing |
| **冲太岁 (Chōng Tài Suì)** | Opposite branch (六冲) | Direct confrontation — upheaval |
| **刑太岁 (Xíng Tài Suì)** | Punishment relationship | Legal/relational friction |
| **害太岁 (Hài Tài Suì)** | Harm relationship | Hidden sabotage, health issues |
| **破太岁 (Pò Tài Suì)** | Break relationship | Financial/commercial losses |

The six clashes (六冲):
- 子↔午, 丑↔未, 寅↔申, 卯↔酉, 辰↔戌, 巳↔亥

---

## 7. Interaction: Natal Chart × Luck Pillar × Annual Pillar

### 7.1 The Hierarchical Model

```
                    Annual Pillar (流年)
                    (1 year — surface weather)
                          ↓
                    Luck Pillar (大运)
                    (10 years — seasonal trend)
                          ↓
                ┌───────┴───────┐
                │ Natal Chart   │
                │  (Lifetime —  │
                │   foundation) │
                └───────────────┘
```

### 7.2 Reading Method (Classical Step-by-Step)

**Step 1**: Determine the **Day Master's elemental needs** (用神, Yòng Shén) — the element(s) that benefit the chart:
   - If the chart is too strong in one element → the controlling element is useful
   - If the chart is too weak → the generating element or the element itself is useful
   - If the chart has conflicts → the harmonizing element is useful

**Step 2**: Evaluate the **Luck Pillar** against the Day Master's needs:
   - Does the Luck Pillar's Stem provide the useful element (喜神)?
   - Does it bring a harmful element (忌神)?
   - Is the Luck Pillar's Branch favorable?

**Step 3**: Evaluate the **Annual Pillar** against both:
   - Does the Annual Pillar support the Luck Pillar's positive trend?
   - Does it counteract a negative Luck Pillar?
   - Does it trigger specific combinations/clashes with natal branches?

### 7.3 The 20-Year Sub-Period Analysis

Though each Luck Pillar is 10 years, some schools (紫微斗数-influenced, or certain 子平 methods) divide each Luck Pillar into two **5-year sub-periods**:

- **First 5 years (前五年)**: The Heaven Stem (天干) of the Luck Pillar is dominant
- **Last 5 years (后五年)**: The Earthly Branch (地支) of the Luck Pillar is dominant

> 渊海子平: "天干管五年，地支管五年。"
> "The Heavenly Stem governs five years, the Earthly Branch governs five years."

Alternatively, some practitioners say:
- **First 5 years**: Stronger influence from the Annual Pillar
- **Last 5 years**: Stronger influence from the Luck Pillar

### 7.4 Favorable vs Unfavorable Luck Pillars

| Luck Pillar Element vs 用神 (Useful God) | Classification |
|---|---|
| Luck Pillar Stem = 用神 (useful element) | **Favorable luck period** — opportunities, growth |
| Luck Pillar Stem = 忌神 (taboo element) | **Unfavorable luck period** — challenges, lessons |
| Luck Pillar Stem = 闲神 (neutral element) | **Mixed luck** — depends on Annual Pillar |
| Luck Pillar Branch contains 用神's hidden stem | **Favorable if the branch's energy is activated** |
| Luck Pillar Branch clashes with 日支 | **Relationship/spouse period challenges** |

---

## 8. Classical Formulas from 渊海子平 & 三命通会

### 8.1 渊海子平 — On Starting Age

> 原文: "凡人出生之后，看其阳男阴女、阴男阳女，顺逆数至节气之日。三日为一岁，一日为四月。又以节气之日定其运。"
>
> **Translation**: "After a person is born, observe whether they are Yang male / Yin female or Yin male / Yang female, then count forward or backward to the Solar Term day. Three days count as one year, one day counts as four months. Then use the Solar Term day to fix the Luck movement."

> 原文: "大运之法，从月柱起。阳男阴女顺行，阴男阳女逆行。"
>
> **Translation**: "The method of Great Luck begins from the Month Pillar. Yang males and Yin females move forward; Yin males and Yang females move backward."

### 8.2 三命通会 — Elaboration on the Formula

> 原文: "凡起运，以出生之时，距节气之日，计其日数。三日为一岁，一日为四月。又云：一刻为五天。盖一时辰有八刻，故刻数折半。"
>
> **Translation**: "For all starting luck calculations, use the time of birth, measure the days to the Solar Term day. Three days count as one year, one day counts as four months. It is also said: one ke (刻, ≈ 15 minutes) counts as five days. Since one two-hour period has eight ke, the ke count is halved."

**More precise version from 三命通会:**

- 1 day (24 hours) = 4 months
- 1 two-hour period (时辰) = 1/12 day = 4/12 months = 10 days (approximate)
- 1 ke (刻, ≈ 15 min) = 5 days

### 8.3 Classical Ratios Summary Table

| Time Gap | Classical Conversion |
|---|---|
| 3 days | 1 year (12 months) |
| 2 days | 8 months |
| 1 day | 4 months |
| 12 hours (半日) | 2 months |
| 1 two-hour period (1时辰) | ~10 days (approx) |
| 1 ke (刻, 15 min) | 5 days |
| Birth exactly on Solar Term | Start at 0 or 1 year (schools vary) |

### 8.4 三命通会 — On Luck Pillars and Life Phases

> 原文: "运有早发晚发之异。早发者，三岁以前起运；晚发者，十五岁以后起运。早发者多劳，晚发者多福。"
>
> **Translation**: "Luck has the difference of early and late onset. Early onset means luck begins before age three; late onset means luck begins after age fifteen. Those with early luck experience more toil; those with late luck experience more blessing."

> 原文: "大运步步留心，流年岁岁看验。"
>
> **Translation**: "Observe every step of the Great Luck carefully, examine the Annual Year each year for verification."

### 8.5 渊海子平 — On Interaction with Annual Pillar

> 原文: "太岁者，年中天子，一岁之尊神也。大运者，十年之主人也。运与岁相和，则吉；相战，则凶。"
>
> **Translation**: "Tai Sui (Annual Pillar) is the emperor of the year, the honored spirit of the entire year. The Great Luck is the master of ten years. When the Luck and the Year are in harmony, there is good fortune; when they are in conflict, there is misfortune."

### 8.6 渊海子平 — The "Few Days" Special Rule

> 原文: "若止一日，则运起四个月；二日则八个月；三日方为一岁。若有零刻，亦当以刻算之。"
>
> **Translation**: "If there is only one day [between birth and Solar Term], then luck begins at four months; two days → eight months; only at three days does it become one full year. If there are remaining ke, they should also be calculated."

---

## 9. Worked Examples

### 9.1 Example 1: Yang Male, Forward Cycle

**Person**: Male, born January 15, 1990, 14:30 (2:30 PM)
**Day Stem**: 戊 (Wù — Yang Earth) → Yang Male = FORWARD
**Month Pillar**: Let's calculate from the date.

**Step 1 — Determine Month Pillar**:
- January 15, 1990 falls within the 丑 (Chǒu/Ox) month
- The Heavenly Stem for the month is derived from the year. 1990 is 庚午 (Gēng-Wǔ) year
- Year Stem 庚 (index 6), using the month stem formula for the 丑 month (month index 1):
  - Month Stem = (Year Stem index × 2 + Month index) % 10
  - = (6 × 2 + 1) % 10 = (12 + 1) % 10 = 13 % 10 = 3 → 丁 (Dīng)
- Month Pillar = **丁丑** (Dīng-Chǒu)

**Step 2 — Determine starting age**:
- Forward cycle: count to next Solar Term
- The Solar Term before January 15 is 小寒 (Jan 6, 1990)
- The next Solar Term is **大寒** (Jan 20, 1990)

Wait — let me reconsider the Solar Terms. In the Chinese calendar:

**年柱 (Year Pillar)**: For January 15, 1990, we need to check if it's before or after Lì Chūn (Feb 4, 1990).
- Jan 15 < Feb 4 → still under the previous year's year pillar
- The previous year is 1989 (己巳)
- But for month determination, the month boundary system is independent

Actually, for Luck Pillar calculation, the key point is: the Month Pillar is determined by the Solar Term boundaries, not the lunar month.

Let me trace properly:

For birth January 15, 1990:
- 小寒 (Xiǎo Hán): Jan 5-6, 1990 → beginning of 丑 month
- 大寒 (Dà Hán): Jan 20, 1990

Birth date (Jan 15) is after 小寒 but before 大寒.
- Forward cycle: count from Jan 15 to 大寒 (Jan 20) = 5 days
- Starting age: 5/3 = 1 year, remainder 2 days
  = 1 year + (2 × 4 months) = **1 year 8 months**
  ≈ **Age 2** (rounded up)

**Step 3 — Derive Luck Pillars** (Forward from 丁丑):
```
LP1: 戊寅 (Wù-Yín)  — Age 2 to 12
LP2: 己卯 (Jǐ-Mǎo)   — Age 12 to 22
LP3: 庚辰 (Gēng-Chén) — Age 22 to 32
LP4: 辛巳 (Xīn-Sì)   — Age 32 to 42
LP5: 壬午 (Rén-Wǔ)   — Age 42 to 52
LP6: 癸未 (Guǐ-Wèi)  — Age 52 to 62
LP7: 甲申 (Jiǎ-Shēn)  — Age 62 to 72
LP8: 乙酉 (Yǐ-Yǒu)   — Age 72 to 82
```

### 9.2 Example 2: Yin Female, Forward Cycle

**Person**: Female, born August 8, 2005, 06:15 AM
**Day Stem**: 癸 (Guǐ — Yin Water) → Yin Female = FORWARD

**Step 1 — Month Pillar**:
- August 8, 2005. The Solar Term 立秋 (Lì Qiū) is around Aug 7-8
- Need to check: before or after 立秋?
  - Let's say 立秋 is Aug 7, 2005 → Aug 8 is after → 申 (Shēn) month
- Year 2005 is 乙酉 (Yǐ-Yǒu)
- Month formula for 申 (index 7):
  - (Year Stem index × 2 + Month index) % 10
  - Year Stem 乙 = index 1
  - (1×2 + 7) % 10 = (2+7) % 10 = 9 → 壬 (Rén)
- Month Pillar = **壬申** (Rén-Shēn)

**Step 2 — Starting age**:
- Forward cycle
- The next Solar Term from Aug 8: **处暑** (Chù Shǔ, around Aug 23)
- August 8 to August 23 = 15 days
- Starting age: 15/3 = **5 years exactly** (no remainder)
- → Age 5

**Step 3 — Luck Pillars** (Forward from 壬申):
```
LP1: 癸酉 (Guǐ-Yǒu)   — Age 5 to 15
LP2: 甲戌 (Jiǎ-Xū)    — Age 15 to 25
LP3: 乙亥 (Yǐ-Hài)    — Age 25 to 35
LP4: 丙子 (Bǐng-Zǐ)   — Age 35 to 45
LP5: 丁丑 (Dīng-Chǒu)  — Age 45 to 55
LP6: 戊寅 (Wù-Yín)    — Age 55 to 65
LP7: 己卯 (Jǐ-Mǎo)    — Age 65 to 75
LP8: 庚辰 (Gēng-Chén)  — Age 75 to 85
```

### 9.3 Example 3: Yin Male, Reverse Cycle

**Person**: Male, born March 20, 1980, 22:00 (10 PM)
**Day Stem**: 乙 (Yǐ — Yin Wood) → Yin Male = REVERSE

**Step 1 — Month Pillar**:
- March 20, 1980. 惊蛰 (Jīng Zhé) is Mar 5-6; 清明 (Qīng Míng) is Apr 5
- Mar 20 is between 惊蛰 and 清明 → 卯 (Mǎo) month
- Year 1980 is 庚申 (Gēng-Shēn). Year Stem 庚 = index 6
- Month 卯 = index 2 (Feb-Mar)
- (6×2 + 2) % 10 = 14 % 10 = 4 → 戊 (Wù)
- Month Pillar = **戊卯 (Wù-Mǎo)** ... wait, this doesn't look right.

Let me recalculate. Month indices (0-based):
子(Zǐ)=0, 丑(Chǒu)=1, 寅(Yín)=2, 卯(Mǎo)=3, 辰(Chén)=4, ...

Actually, for the formula, the month mapping is:
寅=2 (first month of year), 卯=3 (second month), 辰=4, 巳=5, 午=6, 未=7, 申=8, 酉=9, 戌=10, 亥=11, 子=0, 丑=1

For 卯 month (index 3):
(YearStemIndex × 2 + MonthIndex) % 10
= (6 × 2 + 3) % 10 = 15 % 10 = 5 → 己 (Jǐ)

Month Pillar = **己卯** (Jǐ-Mǎo)

**Step 2 — Starting age**:
- Reverse cycle: count from previous Solar Term to birth
- Previous Solar Term from Mar 20: 惊蛰 (Mar 5, 1980)
- March 5 to March 20 = 15 days
- Starting age: 15/3 = **5 years**
- → Age 5

**Step 3 — Luck Pillars** (Reverse from 己卯):
```
LP1: 戊寅 (Wù-Yín)  — Age 5 to 15
LP2: 丁丑 (Dīng-Chǒu) — Age 15 to 25
LP3: 丙子 (Bǐng-Zǐ)  — Age 25 to 35
LP4: 乙亥 (Yǐ-Hài)  — Age 35 to 45
LP5: 甲戌 (Jiǎ-Xū)  — Age 45 to 55
LP6: 癸酉 (Guǐ-Yǒu)  — Age 55 to 65
LP7: 壬申 (Rén-Shēn)  — Age 65 to 75
LP8: 辛未 (Xīn-Wèi)  — Age 75 to 85
```

### 9.4 Example 4: Year-by-Year Interaction

**Person from Example 3**, in 2025 (currently at age 45):
- Current Luck Pillar LP5: **甲戌** (Jiǎ-Xū) — Age 45-55
- Day Master: 乙 (Yin Wood)
- 2005 was 乙酉 (Yǐ-Yǒu) year
- 2025 is 乙巳 (Yǐ-Sì) year

**Analysis**:
- LP5 stem 甲 (Yang Wood) — generates the Day Master 乙 (Wood). Favorable.
- 2025 stem 乙 (Yin Wood) — same element as Day Master, more support. Favorable.
- LP5 branch 戌 (Dog) — Earth branch
- 2025 branch 巳 (Snake) — Fire branch

Interactions:
- 巳 + 戌 = Fire generates Earth → Earth is the wealth element (财星) for 乙 Wood
- Day Master 乙 + Support from LP 甲 + Support from Annual 乙 → strong Wood
- Strong Wood controls Earth (wealth) → potential financial gain
- 巳 + 戌 also forms a combination (巳戌合?) — need to check combination relationships

This is a simplified reading. A full reading requires analyzing Hidden Stems (藏干), the interaction with all four natal pillars, and checking for Nobleman/Demon stars.

---

## 10. Algorithm Summary for Implementation

### 10.1 Complete Algorithm

```
function calculate_luck_pillars(natal_chart, gender):
    // 1. Extract inputs
    day_stem = natal_chart.day_pillar.stem      // 日干
    month_pillar = natal_chart.month_pillar     // 月柱
    birth_date = natal_chart.birth_date
    birth_hour = natal_chart.birth_hour

    // 2. Determine direction
    day_stem_yang = is_yang(day_stem)           // 甲丙戊庚壬 = Yang
    is_male = (gender == 'male')

    if (day_stem_yang AND is_male) OR (NOT day_stem_yang AND NOT is_male):
        direction = FORWARD                      // 阳男阴女 = 顺排
    else:
        direction = REVERSE                      // 阴男阳女 = 逆排

    // 3. Find relevant Solar Term boundaries
    current_term = find_current_solar_term(birth_date)  // 当前节气
    if direction == FORWARD:
        boundary = find_next_solar_term(birth_date)     // 下一节气
        day_diff = days_between(birth_date, boundary)
    else:
        boundary = find_prev_solar_term(birth_date)     // 上一节气
        day_diff = days_between(boundary, birth_date)

    // 4. Convert days to starting age
    // Formula: 3 days = 1 year, 1 day = 4 months
    years = floor(day_diff / 3)
    months = (day_diff % 3) * 4
    // Optional: add hour fraction
    // hour_fraction_months = (birth_hour_in_decimal / 24) * 4
    // months = months + hour_fraction_months

    starting_age = years + (months / 12)
    starting_age_rounded = ceil(starting_age)  // convention: round up to whole year

    // 5. Derive 8 Luck Pillars
    luck_pillars = []
    for i in 1 to 8:
        if direction == FORWARD:
            stem_index = (month_pillar.stem_index + i) % 10
            branch_index = (month_pillar.branch_index + i) % 12
        else:
            stem_index = mod(month_pillar.stem_index - i, 10)   // positive modulo
            branch_index = mod(month_pillar.branch_index - i, 12) // positive modulo

        stem = STEMS[stem_index]
        branch = BRANCHES[branch_index]

        start_age = starting_age_rounded + (i - 1) * 10
        end_age = starting_age_rounded + i * 10 - 1

        luck_pillars.append({
            number: i,
            pillar: { stem: stem, branch: branch },
            age_range: { start: start_age, end: end_age },
            label: stem + branch
        })

    return {
        direction: direction,
        starting_age: starting_age,
        starting_age_rounded: starting_age_rounded,
        boundary_term: boundary,
        day_diff: day_diff,
        luck_pillars: luck_pillars
    }
```

### 10.2 Positive Modulo Helper

```python
def mod(a, b):
    """Positive modulo for Python/Javascript compatibility"""
    return ((a % b) + b) % b
```

### 10.3 STEMS and BRANCHES Constants

```javascript
const STEMS = ['甲','乙','丙','丁','戊','己','庚','辛','壬','癸'];
const BRANCHES = ['子','丑','寅','卯','辰','巳','午','未','申','酉','戌','亥'];
const STEM_YANG = [true, false, true, false, true, false, true, false, true, false];
```

### 10.4 Solar Term Date Calculation

For implementation, Solar Term dates can be:
1. **Lookup table**: Pre-calculated dates for years 1900-2100
2. **Astronomical calculation**: Using a library like `ephem` or `astronomy-engine`
3. **Approximation formula**: Using a sinusoidal approximation based on the Earth's orbit

The astronomical method is most accurate. The approximate longitudes:
- Each Solar Term occurs at 15° intervals of solar longitude
- 立春 = 315°, 惊蛰 = 345°, 清明 = 15°, etc.

---

## 11. Special Cases & Edge Cases

### 11.1 Birth on the Solar Term Boundary

If the birth date falls exactly on the day of a Solar Term:
- The person's Month Pillar may be ambiguous (one chart considers it the ending month, another the starting month)
- For Luck Pillar starting age: 0 days difference → starting age 0
- Some esoteric schools say the first Luck Pillar begins in the womb

### 11.2 Leap Year / Gregorian Calendar Considerations

- The Solar Term system is tropical (solar-based), so Gregorian dates of Solar Terms shift slightly from year to year but stay within ±1-2 days
- A robust implementation should use astronomical calculations, not fixed dates

### 11.3 Birth Near Midnight (子时, 23:00-01:00)

A special case:
- 早子时 (Early Zǐ, 23:00-00:00): Some schools consider this part of the CURRENT day
- 晚子时 (Late Zǐ, 00:00-01:00): Part of the NEXT day
- This affects the Day Pillar, which in turn affects the Day Stem's Yin/Yang determination
- Controversial — multiple schools have different rules

### 11.4 Different Number of Luck Pillars

- Standard: 8 Luck Pillars (80 years)
- Some traditions: 6 or 10 Luck Pillars
- For very long-lived individuals: the Luck Pillars simply continue the sequence

### 11.5 The "Empty" Luck Pillar

When the Luck Pillar's branch is the same as the Empty Branch (旬空, Xún Kōng) of the natal chart's year/day pillar cycle, that 10-year period is considered "empty" — the Luck Pillar's influence is diminished or manifests in unexpected ways.

### 11.6 Gender Transition

If a person has transitioned gender, the practitioner typically uses:
- The gender recorded at birth (for traditional schools)
- The current gender (for modern progressive schools)
This is a matter of ongoing debate in the BaZi community.

---

## References

1. **渊海子平** (Yuan Hai Zi Ping) — attributed to 徐子平 (Xú Zǐpíng), Song Dynasty. Foundational text of BaZi.
2. **三命通会** (San Ming Tong Hui) — compiled by 万民英 (Wàn Mín Yīng), Ming Dynasty. Encyclopedia of BaZi methods.
3. **命理探源** (Mìng Lǐ Tàn Yuán) — by 袁树珊 (Yuán Shù Shān), Republic of China era.
4. **穷通宝鉴** (Qióng Tōng Bǎo Jiàn) — Qing Dynasty commentary on 渊海子平.

---

*Document compiled for deep BaZi research project — chart calculator implementation.*
*Last updated: 2026-06-14*

#!/usr/bin/env python3
"""
Integrated BaZi (Four Pillars / 八字) Calculator
===============================================
Computes the complete BaZi chart from a Gregorian date of birth.

Features:
  1. Four Pillars (Year, Month, Day, Hour) via sexagenary cycle
  2. Solar term (Jie Qi) boundaries for Month Pillar
  3. Day Master identification
  4. Seasonal Power Assessment (旺相休囚死)
  5. Hidden Stems extraction (地支藏干)
  6. Ten Gods mapping (十神) relative to Day Master
  7. Luck Pillar calculation (大运) — forward/reverse, starting age, 8 pillars
  8. Special Pattern detection (专旺格, 从格)
  9. Void Branches (旬空)
  10. CLI interface with formatted chart output

All data tables are embedded — no external file dependencies.
Uses pypinyin for romanisation.

References: 渊海子平, 三命通会
"""

import argparse
import sys
import math
from datetime import date, datetime, timedelta
from typing import Dict, List, Optional, Tuple

try:
    from pypinyin import pinyin, Style
except ImportError:
    # Fallback — pypinyin not available
    def pinyin(text, style=0):
        return [[c] for c in text]

    class Style:
        TONE3 = 0
        NORMAL = 0


# ═══════════════════════════════════════════════════════════════════════════
# 1. DATA TABLES (embedded, no external files)
# ═══════════════════════════════════════════════════════════════════════════

# Heavenly Stems (天干) — 10 stems
HEAVENLY_STEMS = [
    {'char': '甲', 'pinyin': 'jiǎ', 'yin_yang': '阳', 'element': 'Wood', 'element_cn': '木', 'index': 0},
    {'char': '乙', 'pinyin': 'yǐ',  'yin_yang': '阴', 'element': 'Wood', 'element_cn': '木', 'index': 1},
    {'char': '丙', 'pinyin': 'bǐng','yin_yang': '阳', 'element': 'Fire', 'element_cn': '火', 'index': 2},
    {'char': '丁', 'pinyin': 'dīng','yin_yang': '阴', 'element': 'Fire', 'element_cn': '火', 'index': 3},
    {'char': '戊', 'pinyin': 'wù',  'yin_yang': '阳', 'element': 'Earth','element_cn': '土', 'index': 4},
    {'char': '己', 'pinyin': 'jǐ',  'yin_yang': '阴', 'element': 'Earth','element_cn': '土', 'index': 5},
    {'char': '庚', 'pinyin': 'gēng','yin_yang': '阳', 'element': 'Metal','element_cn': '金', 'index': 6},
    {'char': '辛', 'pinyin': 'xīn', 'yin_yang': '阴', 'element': 'Metal','element_cn': '金', 'index': 7},
    {'char': '壬', 'pinyin': 'rén', 'yin_yang': '阳', 'element': 'Water','element_cn': '水', 'index': 8},
    {'char': '癸', 'pinyin': 'guǐ', 'yin_yang': '阴', 'element': 'Water','element_cn': '水', 'index': 9},
]

# Earthly Branches (地支) — 12 branches
EARTHLY_BRANCHES = [
    {'char': '子', 'pinyin': 'zǐ',   'animal': 'Rat',    'element': 'Water', 'element_cn': '水', 'index': 0, 'season': 'Winter'},
    {'char': '丑', 'pinyin': 'chǒu',  'animal': 'Ox',     'element': 'Earth', 'element_cn': '土', 'index': 1, 'season': 'Winter'},
    {'char': '寅', 'pinyin': 'yín',   'animal': 'Tiger',  'element': 'Wood',  'element_cn': '木', 'index': 2, 'season': 'Spring'},
    {'char': '卯', 'pinyin': 'mǎo',   'animal': 'Rabbit', 'element': 'Wood',  'element_cn': '木', 'index': 3, 'season': 'Spring'},
    {'char': '辰', 'pinyin': 'chén',  'animal': 'Dragon', 'element': 'Earth', 'element_cn': '土', 'index': 4, 'season': 'Spring'},
    {'char': '巳', 'pinyin': 'sì',    'animal': 'Snake',  'element': 'Fire',  'element_cn': '火', 'index': 5, 'season': 'Summer'},
    {'char': '午', 'pinyin': 'wǔ',    'animal': 'Horse',  'element': 'Fire',  'element_cn': '火', 'index': 6, 'season': 'Summer'},
    {'char': '未', 'pinyin': 'wèi',   'animal': 'Goat',   'element': 'Earth', 'element_cn': '土', 'index': 7, 'season': 'Summer'},
    {'char': '申', 'pinyin': 'shēn',  'animal': 'Monkey', 'element': 'Metal', 'element_cn': '金', 'index': 8, 'season': 'Autumn'},
    {'char': '酉', 'pinyin': 'yǒu',   'animal': 'Rooster','element': 'Metal', 'element_cn': '金', 'index': 9, 'season': 'Autumn'},
    {'char': '戌', 'pinyin': 'xū',    'animal': 'Dog',    'element': 'Earth', 'element_cn': '土', 'index': 10, 'season': 'Autumn'},
    {'char': '亥', 'pinyin': 'hài',   'animal': 'Pig',    'element': 'Water', 'element_cn': '水', 'index': 11, 'season': 'Winter'},
]

# Hidden Stems (地支藏干) — each branch contains 1-3 hidden heavenly stems
# Format: branch_index -> list of (stem_index, is_main)
HIDDEN_STEMS = {
    0:  [{'stem': 9,  'is_main': True}],                           # 子 → 癸
    1:  [{'stem': 5,  'is_main': True},                            # 丑 → 己
         {'stem': 9,  'is_main': False},                           #      癸
         {'stem': 7,  'is_main': False}],                          #      辛
    2:  [{'stem': 0,  'is_main': True},                            # 寅 → 甲
         {'stem': 2,  'is_main': False},                           #      丙
         {'stem': 4,  'is_main': False}],                          #      戊
    3:  [{'stem': 1,  'is_main': True}],                           # 卯 → 乙
    4:  [{'stem': 4,  'is_main': True},                            # 辰 → 戊
         {'stem': 1,  'is_main': False},                           #      乙
         {'stem': 9,  'is_main': False}],                          #      癸
    5:  [{'stem': 2,  'is_main': True},                            # 巳 → 丙
         {'stem': 4,  'is_main': False},                           #      戊
         {'stem': 6,  'is_main': False}],                          #      庚
    6:  [{'stem': 3,  'is_main': True},                            # 午 → 丁
         {'stem': 5,  'is_main': False}],                          #      己
    7:  [{'stem': 5,  'is_main': True},                            # 未 → 己
         {'stem': 3,  'is_main': False},                           #      丁
         {'stem': 1,  'is_main': False}],                          #      乙
    8:  [{'stem': 6,  'is_main': True},                            # 申 → 庚
         {'stem': 8,  'is_main': False},                           #      壬
         {'stem': 4,  'is_main': False}],                          #      戊
    9:  [{'stem': 7,  'is_main': True}],                           # 酉 → 辛
    10: [{'stem': 4,  'is_main': True},                            # 戌 → 戊
         {'stem': 7,  'is_main': False},                           #      辛
         {'stem': 3,  'is_main': False}],                          #      丁
    11: [{'stem': 8,  'is_main': True},                            # 亥 → 壬
         {'stem': 0,  'is_main': False}],                          #      甲
}

# Element indices for computational use
# 0=Wood, 1=Fire, 2=Earth, 3=Metal, 4=Water
ELEMENT_INDICES = {'Wood': 0, 'Fire': 1, 'Earth': 2, 'Metal': 3, 'Water': 4}

# Stem element mapping: stem_index -> element_index
STEM_ELEMENT = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]  # 甲乙=Wood, 丙丁=Fire, etc.

# Branch element mapping: branch_index -> element_index
BRANCH_ELEMENT = [4, 2, 0, 0, 2, 1, 1, 2, 3, 3, 2, 4]

# Element names
ELEMENT_NAMES = {0: 'Wood', 1: 'Fire', 2: 'Earth', 3: 'Metal', 4: 'Water'}
ELEMENT_NAMES_CN = {0: '木', 1: '火', 2: '土', 3: '金', 4: '水'}

# Yang stems (甲丙戊庚壬 = True, 乙丁己辛癸 = False)
STEM_IS_YANG = [True, False, True, False, True, False, True, False, True, False]

# ═══════════════════════════════════════════════════════════════════════════
# 2. SOLAR TERM (节气) SYSTEM
# ═══════════════════════════════════════════════════════════════════════════

# The 12 major Solar Terms (节 / Jie) that define month boundaries
# Each is listed with its approximate day-of-year and pinyin
SOLAR_TERMS = [
    {'name': '立春', 'pinyin': 'Lì Chūn',     'month': 2,  'day': 4,  'longitude': 315},
    {'name': '惊蛰', 'pinyin': 'Jīng Zhé',    'month': 3,  'day': 6,  'longitude': 345},
    {'name': '清明', 'pinyin': 'Qīng Míng',   'month': 4,  'day': 5,  'longitude': 15},
    {'name': '立夏', 'pinyin': 'Lì Xià',      'month': 5,  'day': 6,  'longitude': 45},
    {'name': '芒种', 'pinyin': 'Máng Zhòng',  'month': 6,  'day': 6,  'longitude': 75},
    {'name': '小暑', 'pinyin': 'Xiǎo Shǔ',    'month': 7,  'day': 7,  'longitude': 105},
    {'name': '立秋', 'pinyin': 'Lì Qiū',      'month': 8,  'day': 8,  'longitude': 135},
    {'name': '白露', 'pinyin': 'Bái Lù',      'month': 9,  'day': 8,  'longitude': 165},
    {'name': '寒露', 'pinyin': 'Hán Lù',      'month': 10, 'day': 8,  'longitude': 195},
    {'name': '立冬', 'pinyin': 'Lì Dōng',     'month': 11, 'day': 7,  'longitude': 225},
    {'name': '大雪', 'pinyin': 'Dà Xuě',      'month': 12, 'day': 7,  'longitude': 255},
    {'name': '小寒', 'pinyin': 'Xiǎo Hán',    'month': 1,  'day': 6,  'longitude': 285},
]

def _sun_longitude_to_date(year: int, longitude: float) -> date:
    """
    Approximate the date when the sun reaches a given ecliptic longitude.

    Uses a lookup table based on mean solar term dates with a yearly drift
    correction. Accuracy is typically within ±1 day.

    The solar terms drift by ~0.2422 days per year relative to the Gregorian
    calendar. We compensate by computing the exact day offset from a base year.

    Args:
        year: Gregorian year
        longitude: Desired ecliptic longitude in degrees (0-360)

    Returns:
        Approximate date
    """
    # Base year with known solar term dates (use a non-leap year for cleaner math)
    BASE_YEAR = 2023

    # Approximate day-of-year for each major solar term in the non-leap base year
    # 立春(315°) starts the first month (寅) of the Chinese calendar year
    TERM_DOY_BASE = {
        315: 35,   # 立春: Feb 4
        330: 50,   # 雨水: Feb 19
        345: 65,   # 惊蛰: Mar 6
        0:   79,   # 春分: Mar 20
        15:  95,   # 清明: Apr 5
        30:  109,  # 谷雨: Apr 19
        45:  125,  # 立夏: May 5
        60:  140,  # 小满: May 20
        75:  156,  # 芒种: Jun 5
        90:  172,  # 夏至: Jun 21
        105: 187,  # 小暑: Jul 6
        120: 203,  # 大暑: Jul 22
        135: 219,  # 立秋: Aug 7
        150: 235,  # 处暑: Aug 23
        165: 250,  # 白露: Sep 7
        180: 265,  # 秋分: Sep 22
        195: 281,  # 寒露: Oct 8
        210: 296,  # 霜降: Oct 23
        225: 311,  # 立冬: Nov 7
        240: 326,  # 小雪: Nov 22
        255: 341,  # 大雪: Dec 7
        270: 355,  # 冬至: Dec 22
        285: 370,  # 小寒: Jan 5 (next year = day 5 + 365)
        300: 385,  # 大寒: Jan 20 (next year = day 20 + 365)
    }

    if longitude not in TERM_DOY_BASE:
        # Fallback: linear interpolation
        sorted_longs = sorted(TERM_DOY_BASE.keys())
        for i, l in enumerate(sorted_longs):
            if longitude <= float(l):
                if i == 0:
                    # Before first term, use first term
                    base_doy = TERM_DOY_BASE[sorted_longs[0]]
                else:
                    # Interpolate
                    l0, l1 = float(sorted_longs[i - 1]), float(sorted_longs[i])
                    d0, d1 = float(TERM_DOY_BASE[sorted_longs[i - 1]]), float(TERM_DOY_BASE[sorted_longs[i]])
                    base_doy = d0 + (d1 - d0) * (longitude - l0) / (l1 - l0)
                break
        else:
            base_doy = TERM_DOY_BASE[sorted_longs[-1]]
        base_doy = int(round(base_doy))
    else:
        base_doy = TERM_DOY_BASE[longitude]

    # Yearly drift: the tropical year is ~365.2422 days, so the terms drift
    # by about 0.2422 days per year relative to the Gregorian calendar.
    # However, leap years partially compensate. Net drift per year ≈ 0.2422.
    years_from_base = year - BASE_YEAR

    # Account for leap days that have occurred between base year and target year
    def count_leap_days(y1, y2):
        """Count leap days between years y1 (inclusive) and y2 (exclusive)."""
        count = 0
        for y in range(min(y1, y2), max(y1, y2)):
            if (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0):
                count += 1
        return count if y2 > y1 else -count

    leap_days = count_leap_days(BASE_YEAR, year)

    # Net drift = (year_diff * 0.2422) - leap_days
    # Actually, the drift is already compensated by leap years in the calendar.
    # The remaining drift is approximately:
    # drift_days = years_from_base * 0.2422 - leap_days
    # This gives the number of days the term has shifted relative to the calendar.
    drift_days = years_from_base * 0.2422 - leap_days

    # For longitudes towards the end of the year (> 345°, which is after mid-Dec),
    # the date might fall in the next year, or for early longitudes in the current year.
    adjusted_doy = base_doy + drift_days

    # Convert to date, handling year wrap
    jan1 = date(year, 1, 1)
    result_date = jan1 + timedelta(days=int(round(adjusted_doy - 1)))

    # If the result is more than 365 days from Jan 1 or negative, adjust year
    # For longitudes that map to the next year's early dates (like 小寒/大寒 at 285/300)
    if result_date.year < year:
        result_date = date(year + 1, 1, 1) + timedelta(days=int(round(adjusted_doy - 1)))
    elif (result_date - jan1).days > 360 and longitude < 300:
        # If we got a date in the next year for an early-term longitude, something's off
        pass

    return result_date


def get_solar_term_dates(year: int) -> List[Tuple[str, date]]:
    """
    Compute the 12 major Solar Term dates for a given year.

    Returns:
        List of (term_name, date) sorted chronologically
    """
    terms = []
    for term in SOLAR_TERMS:
        term_date = _sun_longitude_to_date(year, term['longitude'])
        terms.append((term['name'], term_date))
    # Sort by date
    terms.sort(key=lambda x: x[1])
    return terms


def get_month_branch_from_date(birth_date: date) -> int:
    """
    Determine the Earthly Branch of the Month Pillar based on Solar Term boundaries.

    The month begins at each Jie Qi (节):
        寅月 starts at 立春 (Feb 4)
        卯月 starts at 惊蛰 (Mar 6)
        辰月 starts at 清明 (Apr 5)
        巳月 starts at 立夏 (May 6)
        午月 starts at 芒种 (Jun 6)
        未月 starts at 小暑 (Jul 7)
        申月 starts at 立秋 (Aug 8)
        酉月 starts at 白露 (Sep 8)
        戌月 starts at 寒露 (Oct 8)
        亥月 starts at 立冬 (Nov 7)
        子月 starts at 大雪 (Dec 7)
        丑月 starts at 小寒 (Jan 6)

    Args:
        birth_date: The date of birth

    Returns:
        Branch index (0-11) for the month
    """
    year = birth_date.year
    # Get solar term dates for the current year
    # Note: 小寒 (丑月 start) happens in early January, so we need previous year's terms too
    prev_terms = get_solar_term_dates(year - 1)
    curr_terms = get_solar_term_dates(year)

    # Map term name to branch
    # 立春 -> 寅(2), 惊蛰 -> 卯(3), 清明 -> 辰(4), 立夏 -> 巳(5),
    # 芒种 -> 午(6), 小暑 -> 未(7), 立秋 -> 申(8), 白露 -> 酉(9),
    # 寒露 -> 戌(10), 立冬 -> 亥(11), 大雪 -> 子(0), 小寒 -> 丑(1)
    TERM_TO_BRANCH = {
        '立春': 2, '惊蛰': 3, '清明': 4, '立夏': 5,
        '芒种': 6, '小暑': 7, '立秋': 8, '白露': 9,
        '寒露': 10, '立冬': 11, '大雪': 0, '小寒': 1,
    }

    # Build ordered list of (date, branch) for all boundaries that could apply
    boundaries = []

    # Previous year's 小寒 through 大雪 (for Jan 1 to 立春 coverage)
    # Actually, the critical ones are the ones around the birth date
    # For January births, we need the previous year's 大雪 and 小寒
    for t_name, t_date in prev_terms:
        if t_name == '大雪':
            # 大雪 starts 子月 (branch 0)
            boundaries.append((t_date, 0))
        elif t_name == '小寒':
            # 小寒 starts 丑月 (branch 1)
            boundaries.append((t_date, 1))
        elif t_name == '立春':
            # 立春 starts 寅月 (branch 2)
            boundaries.append((t_date, 2))

    # Add current year's terms
    for t_name, t_date in curr_terms:
        if t_name in TERM_TO_BRANCH:
            boundaries.append((t_date, TERM_TO_BRANCH[t_name]))

    # Sort by date
    boundaries.sort(key=lambda x: x[0])

    # Find the latest boundary that is on or before the birth date
    # If birth is before the first boundary, use the last boundary from prev year
    # which means we wrap around
    latest_boundary = None
    latest_branch = None

    for b_date, b_branch in boundaries:
        if b_date <= birth_date:
            latest_boundary = b_date
            latest_branch = b_branch

    if latest_branch is not None:
        return latest_branch

    # Birth date is before the first boundary in our list
    # This means we should use the previous year's 大雪 or 小寒
    # Find the most recent boundary that is before birth
    all_boundaries = []
    for t_name, t_date in prev_terms:
        if t_name in TERM_TO_BRANCH:
            all_boundaries.append((t_date, TERM_TO_BRANCH[t_name]))
    for t_name, t_date in curr_terms:
        if t_name in TERM_TO_BRANCH:
            all_boundaries.append((t_date, TERM_TO_BRANCH[t_name]))
    all_boundaries.sort(key=lambda x: x[1])

    for b_date, b_branch in reversed(all_boundaries):
        if b_date <= birth_date:
            return b_branch

    # Fallback
    return 1  # 丑月


def get_days_to_next_term(birth_date: date) -> int:
    """Days from birth_date to the next Solar Term (for forward luck calculation)."""
    year = birth_date.year
    curr_terms = get_solar_term_dates(year)

    # Find all term dates after birth
    for _, t_date in curr_terms:
        if t_date > birth_date:
            diff = (t_date - birth_date).days
            return max(diff, 0)
    # If none in current year, check start of next year
    next_terms = get_solar_term_dates(year + 1)
    first_term_date = next_terms[0][1]
    diff = (first_term_date - birth_date).days
    return max(diff, 0)


def get_days_to_prev_term(birth_date: date) -> int:
    """Days from previous Solar Term to birth_date (for reverse luck calculation)."""
    year = birth_date.year
    curr_terms = get_solar_term_dates(year)

    # Find all term dates before birth (reversed)
    for _, t_date in reversed(curr_terms):
        if t_date < birth_date:
            diff = (birth_date - t_date).days
            return max(diff, 0)

    # Check previous year
    prev_terms = get_solar_term_dates(year - 1)
    last_term_date = prev_terms[-1][1]
    diff = (birth_date - last_term_date).days
    return max(diff, 0)


# ═══════════════════════════════════════════════════════════════════════════
# 3. FOUR PILLAR CALCULATIONS
# ═══════════════════════════════════════════════════════════════════════════

def compute_year_pillar(year: int, month: int, day: int) -> Dict:
    """
    Compute the Year Pillar (年柱).

    The Chinese year begins at 立春 (around Feb 4), not Jan 1.
    For dates before 立春, the year is the previous year.

    Reference: 1984 = 甲子年 (stem=0, branch=0)

    Args:
        year: Gregorian year
        month: Gregorian month (1-12)
        day: Gregorian day (1-31)

    Returns:
        Dict with stem/branch indices and labels
    """
    birth_date = date(year, month, day)
    li_chun_date = _sun_longitude_to_date(year, 315)  # 立春 at longitude 315°

    if birth_date < li_chun_date:
        # Still in the previous year
        bazi_year = year - 1
    else:
        bazi_year = year

    # 1984 = 甲子 = stem 0, branch 0
    REFERENCE_YEAR = 1984
    REFERENCE_STEM = 0
    REFERENCE_BRANCH = 0

    offset = bazi_year - REFERENCE_YEAR
    stem_idx = (REFERENCE_STEM + offset) % 10
    branch_idx = (REFERENCE_BRANCH + offset) % 12

    return _make_pillar(stem_idx, branch_idx, 'year')


def compute_month_pillar(year: int, month: int, day: int) -> Dict:
    """
    Compute the Month Pillar (月柱).

    The month is determined by Solar Term boundaries.
    The month's Heavenly Stem is derived from the Year's Heavenly Stem:
        Month Stem = (Year Stem Index × 2 + Month Branch Offset) % 10

    Month Branch Offset (0-indexed from 寅=0): 寅=0, 卯=1, ..., 丑=11

    Args:
        year: Gregorian year
        month: Gregorian month
        day: Gregorian day

    Returns:
        Dict with stem/branch indices and labels
    """
    birth_date = date(year, month, day)

    # Get the Year Pillar first (to handle 立春 boundary for year)
    yr_pillar = compute_year_pillar(year, month, day)
    year_stem_idx = yr_pillar['stem_index']

    # Get month branch from solar terms
    # Determine the branch of the month
    month_branch_idx = get_month_branch_from_date(birth_date)

    # Month stem formula: stem = (year_stem * 2 + month_offset) % 10
    # Where month_offset = (branch_idx - 2) % 12  (寅=0, 卯=1, ..., 丑=11)
    month_offset = (month_branch_idx - 2) % 12
    month_stem_idx = (year_stem_idx * 2 + month_offset) % 10

    return _make_pillar(month_stem_idx, month_branch_idx, 'month')


def _days_between(d1: date, d2: date) -> int:
    """Absolute days between two dates."""
    return abs((d2 - d1).days)


def compute_day_pillar(year: int, month: int, day: int) -> Dict:
    """
    Compute the Day Pillar (日柱).

    Uses a reference date (January 1, 1900 = 甲戌 / stem=0, branch=10)
    and counts days from that reference.

    Reference: 1900-01-01 = 甲戌 (stem_0, branch_10)

    Args:
        year: Gregorian year
        month: Gregorian month
        day: Gregorian day

    Returns:
        Dict with stem/branch indices and labels
    """
    birth_date = date(year, month, day)
    ref_date = date(1900, 1, 1)
    ref_stem = 0   # 甲
    ref_branch = 10  # 戌

    days_diff = (birth_date - ref_date).days
    stem_idx = (ref_stem + days_diff) % 10
    branch_idx = (ref_branch + days_diff) % 12

    return _make_pillar(stem_idx, branch_idx, 'day')


def compute_hour_pillar(day_stem_idx: int, hour: int) -> Dict:
    """
    Compute the Hour Pillar (时柱).

    The hour branch is determined by the time of day:
        子时 23:00-00:59 (branch 0)
        丑时 01:00-02:59 (branch 1)
        ...
        亥时 21:00-22:59 (branch 11)

    The hour stem is derived from the Day Stem:
        Hour Stem = (Day Stem Index × 2 + Hour Branch Index) % 10

    Args:
        day_stem_idx: Index of the Day's Heavenly Stem (0-9)
        hour: Hour of birth (0-23)

    Returns:
        Dict with stem/branch indices and labels
    """
    # Determine hour branch
    # 子时: 23:00-00:59 -> branch 0
    # 丑时: 01:00-02:59 -> branch 1
    # 寅时: 03:00-04:59 -> branch 2
    # ...
    # 亥时: 21:00-22:59 -> branch 11
    if hour == 23:
        branch_idx = 0  # 晚子时
    else:
        branch_idx = (hour + 1) // 2

    # Hour stem formula: stem = (day_stem * 2 + hour_branch) % 10
    stem_idx = (day_stem_idx * 2 + branch_idx) % 10

    return _make_pillar(stem_idx, branch_idx, 'hour')


def _make_pillar(stem_idx: int, branch_idx: int, pillar_type: str) -> Dict:
    """Create a pillar dictionary from stem and branch indices."""
    stem = HEAVENLY_STEMS[stem_idx]
    branch = EARTHLY_BRANCHES[branch_idx]
    return {
        'type': pillar_type,
        'stem_index': stem_idx,
        'branch_index': branch_idx,
        'stem': stem['char'],
        'branch': branch['char'],
        'label': stem['char'] + branch['char'],
        'stem_pinyin': stem['pinyin'],
        'branch_pinyin': branch['pinyin'],
        'element': stem['element'],
        'branch_element': branch['element'],
        'yin_yang': stem['yin_yang'],
        'animal': branch['animal'],
    }


def compute_sexagenary_index(stem_idx: int, branch_idx: int) -> int:
    """
    Compute the sexagenary cycle index (0-59) from stem and branch indices.

    Formula: index = (stem_idx * 6 - branch_idx * 5) % 60
    Only valid when (stem_idx % 2) == (branch_idx % 2) — same parity.

    Args:
        stem_idx: Heavenly Stem index (0-9)
        branch_idx: Earthly Branch index (0-11)

    Returns:
        Sexagenary index (0-59)
    """
    return (stem_idx * 6 - branch_idx * 5) % 60


# ═══════════════════════════════════════════════════════════════════════════
# 4. SEASONAL POWER ASSESSMENT (旺相休囚死)
# ═══════════════════════════════════════════════════════════════════════════

# Seasonal Power: 旺(Wàng) 相(Xiāng) 休(Xiū) 囚(Qiú) 死(Sǐ)
# Determined by the season of birth (from Month Branch)
# Indexing: 0=Wood, 1=Fire, 2=Earth, 3=Metal, 4=Water
SEASONAL_POWER = {
    # season -> {element_index: (state_name, state_cn, power_level)}
    'Spring': {
        0: ('Prosperous', '旺', 5),    # Wood 旺
        1: ('Nourished', '相', 4),     # Fire 相
        4: ('Resting', '休', 3),       # Water 休
        3: ('Imprisoned', '囚', 2),    # Metal 囚
        2: ('Dead', '死', 1),          # Earth 死
    },
    'Summer': {
        1: ('Prosperous', '旺', 5),    # Fire 旺
        2: ('Nourished', '相', 4),     # Earth 相
        0: ('Resting', '休', 3),       # Wood 休
        4: ('Imprisoned', '囚', 2),    # Water 囚
        3: ('Dead', '死', 1),          # Metal 死
    },
    'Autumn': {
        3: ('Prosperous', '旺', 5),    # Metal 旺
        4: ('Nourished', '相', 4),     # Water 相
        2: ('Resting', '休', 3),       # Earth 休
        1: ('Imprisoned', '囚', 2),    # Fire 囚
        0: ('Dead', '死', 1),          # Wood 死
    },
    'Winter': {
        4: ('Prosperous', '旺', 5),    # Water 旺
        0: ('Nourished', '相', 4),     # Wood 相
        3: ('Resting', '休', 3),       # Metal 休
        2: ('Imprisoned', '囚', 2),    # Earth 囚
        1: ('Dead', '死', 1),          # Fire 死
    },
}

# Branch index -> Season mapping
BRANCH_SEASON = {
    0: 'Winter',   # 子
    1: 'Winter',   # 丑
    2: 'Spring',   # 寅
    3: 'Spring',   # 卯
    4: 'Spring',   # 辰
    5: 'Summer',   # 巳
    6: 'Summer',   # 午
    7: 'Summer',   # 未
    8: 'Autumn',   # 申
    9: 'Autumn',   # 酉
    10: 'Autumn',  # 戌
    11: 'Winter',  # 亥
}


def get_seasonal_power(element_idx: int, month_branch_idx: int) -> Tuple[str, str, int]:
    """
    Get the seasonal power state for a given element in the birth season.

    Args:
        element_idx: Element index (0=Wood, 1=Fire, 2=Earth, 3=Metal, 4=Water)
        month_branch_idx: Month Branch index (0-11)

    Returns:
        Tuple of (state_name, state_cn, power_level)
    """
    season = BRANCH_SEASON[month_branch_idx]
    return SEASONAL_POWER[season][element_idx]


def get_season_name(month_branch_idx: int) -> str:
    """Get the season name for a given month branch index."""
    season_map = {0: 'Winter', 1: 'Winter', 2: 'Spring', 3: 'Spring',
                  4: 'Spring', 5: 'Summer', 6: 'Summer', 7: 'Summer',
                  8: 'Autumn', 9: 'Autumn', 10: 'Autumn', 11: 'Winter'}
    return season_map[month_branch_idx]


# ═══════════════════════════════════════════════════════════════════════════
# 5. TEN GODS (十神) MAPPING
# ═══════════════════════════════════════════════════════════════════════════

# Ten Gods relationship from Day Master perspective
# Each stem relative to Day Master is classified as one of 10 relationships

def get_ten_god(day_master_idx: int, other_stem_idx: int) -> Dict:
    """
    Determine the Ten God relationship between the Day Master and another stem.

    Args:
        day_master_idx: Day Master's Heavenly Stem index (0-9)
        other_stem_idx: Other stem's index (0-9)

    Returns:
        Dict with Chinese name, English description, relationship type
    """
    dm_elem = STEM_ELEMENT[day_master_idx]
    other_elem = STEM_ELEMENT[other_stem_idx]
    dm_yang = STEM_IS_YANG[day_master_idx]
    other_yang = STEM_IS_YANG[other_stem_idx]

    if dm_elem == other_elem:
        # Same element
        if dm_yang == other_yang:
            return {
                'name_cn': '比肩', 'name': 'Bi Jian',
                'type': 'Peer (Same), Same Polarity',
            }
        else:
            return {
                'name_cn': '劫财', 'name': 'Jie Cai',
                'type': 'Peer (Same), Different Polarity',
            }

    # I produce (我生): dm_elem -> (dm_elem+1)%5 = other_elem
    if (dm_elem + 1) % 5 == other_elem:
        if dm_yang == other_yang:
            return {
                'name_cn': '食神', 'name': 'Shi Shen',
                'type': 'Output, Same Polarity',
            }
        else:
            return {
                'name_cn': '伤官', 'name': 'Shang Guan',
                'type': 'Output, Different Polarity',
            }

    # Produces me (生我): (other_elem+1)%5 == dm_elem
    if (other_elem + 1) % 5 == dm_elem:
        if dm_yang == other_yang:
            return {
                'name_cn': '正印', 'name': 'Zheng Yin',
                'type': 'Resource, Same Polarity',
            }
        else:
            return {
                'name_cn': '偏印', 'name': 'Pian Yin',
                'type': 'Resource, Different Polarity',
            }

    # I control (我克): (dm_elem + 2) % 5 == other_elem
    if (dm_elem + 2) % 5 == other_elem:
        if dm_yang == other_yang:
            return {
                'name_cn': '偏财', 'name': 'Pian Cai',
                'type': 'Wealth, Same Polarity',
            }
        else:
            return {
                'name_cn': '正财', 'name': 'Zheng Cai',
                'type': 'Wealth, Different Polarity',
            }

    # Controls me (克我): (other_elem + 2) % 5 == dm_elem
    if (other_elem + 2) % 5 == dm_elem:
        if dm_yang == other_yang:
            return {
                'name_cn': '七杀', 'name': 'Qi Sha',
                'type': 'Authority, Same Polarity',
            }
        else:
            return {
                'name_cn': '正官', 'name': 'Zheng Guan',
                'type': 'Authority, Different Polarity',
            }

    # Should not reach here for valid stem pairs
    return {'name_cn': '?', 'name': 'Unknown', 'type': 'Unknown'}


# ═══════════════════════════════════════════════════════════════════════════
# 6. VOID BRANCHES (旬空 / Xun Kong)
# ═══════════════════════════════════════════════════════════════════════════

VOID_BRANCH_PAIRS = {
    0: [10, 11],  # 甲子旬 → 戌亥空
    1: [8, 9],    # 甲戌旬 → 申酉空
    2: [6, 7],    # 甲申旬 → 午未空
    3: [4, 5],    # 甲午旬 → 辰巳空
    4: [2, 3],    # 甲辰旬 → 寅卯空
    5: [0, 1],    # 甲寅旬 → 子丑空
}


def get_void_branches(day_stem_idx: int, day_branch_idx: int) -> List[int]:
    """
    Determine void branches (旬空) based on the Day Pillar's sexagenary index.

    The 60 sexagenary pairs are grouped into 6 旬 (xun) of 10 pairs each.
    Each 旬 has 2 branches that are "void" (空亡).

    Args:
        day_stem_idx: Day stem index (0-9)
        day_branch_idx: Day branch index (0-11)

    Returns:
        List of branch indices that are void
    """
    sx_idx = compute_sexagenary_index(day_stem_idx, day_branch_idx)
    xun = sx_idx // 10
    return VOID_BRANCH_PAIRS.get(xun, [])


# ═══════════════════════════════════════════════════════════════════════════
# 7. LUCK PILLAR CALCULATION (大运)
# ═══════════════════════════════════════════════════════════════════════════

def determine_luck_direction(day_stem_idx: int, is_male: bool) -> str:
    """
    Determine forward (顺排) or reverse (逆排) Luck Pillar cycle.

    Rule (渊海子平):
        Yang Male (阳男) + Yin Female (阴女) → FORWARD
        Yin Male (阴男) + Yang Female (阳女) → REVERSE

    Args:
        day_stem_idx: Day stem index (0-9)
        is_male: True if male

    Returns:
        'FORWARD' or 'REVERSE'
    """
    is_yang = STEM_IS_YANG[day_stem_idx]
    if (is_yang and is_male) or (not is_yang and not is_male):
        return 'FORWARD'
    return 'REVERSE'


def calc_starting_age(days_to_boundary: int) -> Tuple[int, int]:
    """
    Convert days to Solar Term boundary to starting age.

    Classical formula (渊海子平):
        3 days = 1 year
        1 day  = 4 months

    Args:
        days_to_boundary: Days from birth to nearest Solar Term

    Returns:
        (years, months) tuple
    """
    years = days_to_boundary // 3
    remainder = days_to_boundary % 3
    months = remainder * 4
    return (years, months)


def derive_luck_pillars(
    month_stem_idx: int,
    month_branch_idx: int,
    direction: str,
    num_pillars: int = 8,
) -> List[Dict]:
    """
    Derive Luck Pillars from the Month Pillar.

    Forward: LP(n) = MonthPillar + n stems + n branches
    Reverse: LP(n) = MonthPillar - n stems - n branches

    Args:
        month_stem_idx: Heavenly Stem index of Month Pillar
        month_branch_idx: Earthly Branch index of Month Pillar
        direction: 'FORWARD' or 'REVERSE'
        num_pillars: Number of Luck Pillars (default: 8)

    Returns:
        List of pillar dicts
    """
    pillars = []
    for i in range(1, num_pillars + 1):
        if direction == 'FORWARD':
            stem_idx = (month_stem_idx + i) % 10
            branch_idx = (month_branch_idx + i) % 12
        else:
            stem_idx = (month_stem_idx - i) % 10
            branch_idx = (month_branch_idx - i) % 12

        stem = HEAVENLY_STEMS[stem_idx]
        branch = EARTHLY_BRANCHES[branch_idx]

        pillars.append({
            'number': i,
            'stem_index': stem_idx,
            'branch_index': branch_idx,
            'stem': stem['char'],
            'branch': branch['char'],
            'label': stem['char'] + branch['char'],
            'stem_pinyin': stem['pinyin'],
            'branch_pinyin': branch['pinyin'],
        })
    return pillars


def build_luck_schedule(
    starting_age_years: int,
    starting_age_months: int,
    luck_pillars: List[Dict],
    num_pillars: int = 8,
) -> List[Dict]:
    """
    Build complete Luck Pillar schedule with age ranges.

    Each Luck Pillar governs ~10 years. Starting age is rounded up.

    Args:
        starting_age_years: Years component of starting age
        starting_age_months: Months component
        luck_pillars: List from derive_luck_pillars()
        num_pillars: Number of pillars to include

    Returns:
        List of pillar dicts with age ranges
    """
    start = starting_age_years + (1 if starting_age_months > 0 else 0)

    schedule = []
    for i, lp in enumerate(luck_pillars[:num_pillars]):
        age_start = start + (i * 10)
        age_end = start + ((i + 1) * 10) - 1
        schedule.append({
            **lp,
            'age_start': age_start,
            'age_end': age_end,
            'age_label': f"Age {int(age_start)}-{int(age_end)}",
        })
    return schedule


# ═══════════════════════════════════════════════════════════════════════════
# 8. SPECIAL PATTERN DETECTION (特殊格局)
# ═══════════════════════════════════════════════════════════════════════════

def check_special_patterns(pillars: Dict) -> Dict:
    """
    Check for Zhuan Wang Ge (专旺格) and Cong Ge (从格) special patterns.

    Uses the Day Master, all four pillars, and hidden stems for analysis.

    Args:
        pillars: Dict with 'year', 'month', 'day', 'hour' pillar dicts

    Returns:
        Dict describing any special patterns found
    """
    dm_idx = pillars['day']['stem_index']
    dm_elem = STEM_ELEMENT[dm_idx]

    # Collect all stem and branch elements from the four pillars
    all_stem_indices = [
        pillars['year']['stem_index'],
        pillars['month']['stem_index'],
        pillars['day']['stem_index'],
        pillars['hour']['stem_index'],
    ]

    all_branch_indices = [
        pillars['year']['branch_index'],
        pillars['month']['branch_index'],
        pillars['day']['branch_index'],
        pillars['hour']['branch_index'],
    ]

    # Count elements: for stems, use their element; for branches, use their element
    element_counts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
    for si in all_stem_indices:
        element_counts[STEM_ELEMENT[si]] += 1
    for bi in all_branch_indices:
        element_counts[BRANCH_ELEMENT[bi]] += 1

    total_chars = 8
    dm_element_pct = element_counts[dm_elem] / total_chars * 100

    # Check if DM element is dominant (≥50% of characters)
    dm_dominant = element_counts[dm_elem] >= 4

    # Check for controlling element presence
    controlling_elem = (dm_elem + 2) % 5  # The element that DM controls
    # Actually, check the element that CONTROLS DM
    # (dm_elem + 3) % 5 controls DM... no.
    # Controlling = (element + 2) % 5. So DM is controlled by (dm_elem + 3) % 5
    controller_elem = (dm_elem + 3) % 5
    # Wait: element e controls (e+2)%5. So if DM is at dm_elem, it is controlled by (dm_elem+3)%5.
    # Let me verify: Wood(0) controls Earth(2). What controls Wood? Metal(3). (0+3)%5 = 3 ✓.
    # Fire(1) controls Metal(3). What controls Fire? Water(4). (1+3)%5 = 4 ✓.
    # So controller_elem = (dm_elem + 3) % 5

    controller_present = element_counts[controller_elem] > 0

    # Check producer element (provider of DM)
    producer_elem = (dm_elem - 1) % 5  # The element that produces DM
    # (producer_elem + 1) % 5 == dm_elem
    producer_present = element_counts[producer_elem] > 0

    # === Zhuan Wang Ge (专旺格) checks ===
    # Conditions:
    # 1. DM element ≥ ~50% of chart (or with producer, ≥ ~75%)
    # 2. No controller element present (or very weak)
    # 3. Season supports DM

    month_branch_idx = pillars['month']['branch_index']
    month_season = BRANCH_SEASON[month_branch_idx]

    zhuan_wang = False
    zhuan_wang_type = None

    # DM + producer combined % (if DM is at least 2 chars + producer ≥ 1 char)
    dm_and_support_pct = (element_counts[dm_elem] + element_counts[producer_elem]) / total_chars * 100

    # Check if season supports DM (旺 or 相)
    seasonal_power, _, _ = SEASONAL_POWER[month_season][dm_elem]
    season_supports = seasonal_power in ('Prosperous', 'Nourished')

    # DM's element is dominant and controlling element is absent/weak
    if dm_dominant and not controller_present and season_supports:
        zhuan_wang = True
        zhuan_wang_type = get_zhuan_wang_name(dm_elem)

    # Borderline: DM has ≥ 5 chars of DM + producer, controller is weak
    if not zhuan_wang and dm_and_support_pct >= 62.5 and not controller_present:
        zhuan_wang = True
        zhuan_wang_type = get_zhuan_wang_name(dm_elem)

    # === Cong Ge (从格) checks ===
    cong_ge = False
    cong_ge_type = None

    # DM is very weak (≤ 1 char of DM element, no producer support)
    dm_weak = element_counts[dm_elem] <= 1
    producer_weak = element_counts[producer_elem] == 0

    if dm_weak and producer_weak and not dm_dominant:
        # Determine what's dominant in the chart
        sorted_elements = sorted(element_counts.items(), key=lambda x: -x[1])
        dominant_elem = sorted_elements[0][0]

        if dominant_elem == controller_elem and element_counts[dominant_elem] >= 3:
            cong_ge = True
            cong_ge_type = '从官杀格 (Cong Guan/Sha) - Following Authority'
        elif dominant_elem == (dm_elem + 2) % 5 and element_counts[dominant_elem] >= 3:
            # DM controls this, so it's Wealth
            cong_ge = True
            cong_ge_type = '从财格 (Cong Cai) - Following Wealth'
        elif dominant_elem == (dm_elem + 1) % 5 and element_counts[dominant_elem] >= 3:
            # DM produces this, so it's Output
            cong_ge = True
            cong_ge_type = '从食伤格 (Cong Shi Shen) - Following Output'
        elif element_counts[controller_elem] + element_counts[(dm_elem + 2) % 5] + \
                element_counts[(dm_elem + 1) % 5] >= 6:
            # Mixed opposing forces
            cong_ge = True
            cong_ge_type = '从势格 (Cong Shi) - Following Momentum'

    result = {
        'zhuan_wang_ge': zhuan_wang,
        'zhuan_wang_type': zhuan_wang_type,
        'cong_ge': cong_ge,
        'cong_ge_type': cong_ge_type,
        'dm_element_pct': dm_element_pct,
        'dm_and_support_pct': dm_and_support_pct,
    }
    return result


def get_zhuan_wang_name(elem_idx: int) -> str:
    """Get the Zhuan Wang name for a given element."""
    names = {
        0: '曲直格 (Qu Ge / Qu Zhi) - Wood Special Prosperity',
        1: '炎上格 (Yan Shang Ge) - Fire Special Prosperity',
        2: '稼穑格 (Jia Se Ge) - Earth Special Prosperity',
        3: '从革格 (Cong Ge) - Metal Special Prosperity',
        4: '润下格 (Run Xia Ge) - Water Special Prosperity',
    }
    return names[elem_idx]


# ═══════════════════════════════════════════════════════════════════════════
# 9. COMPLETE CHART CALCULATION
# ═══════════════════════════════════════════════════════════════════════════

def calculate_full_chart(
    year: int,
    month: int,
    day: int,
    hour: int,
    gender: str = 'male',
    name: str = '',
) -> Dict:
    """
    Calculate the complete BaZi chart from a Gregorian date of birth.

    Args:
        year: Birth year
        month: Birth month (1-12)
        day: Birth day (1-31)
        hour: Birth hour (0-23)
        gender: 'male' or 'female'
        name: Optional person name

    Returns:
        Complete chart as a nested dict
    """
    # Compute the four pillars
    year_pillar = compute_year_pillar(year, month, day)
    month_pillar = compute_month_pillar(year, month, day)
    day_pillar = compute_day_pillar(year, month, day)
    hour_pillar = compute_hour_pillar(day_pillar['stem_index'], hour)

    pillars = {
        'year': year_pillar,
        'month': month_pillar,
        'day': day_pillar,
        'hour': hour_pillar,
    }

    # Day Master
    day_master = day_pillar['stem']
    day_master_idx = day_pillar['stem_index']
    day_master_info = HEAVENLY_STEMS[day_master_idx]

    # Season
    month_branch_idx = month_pillar['branch_index']
    season = get_season_name(month_branch_idx)

    # Seasonal Power Assessment for all elements
    seasonal_powers = {}
    for elem_idx in range(5):
        state, state_cn, power = get_seasonal_power(elem_idx, month_branch_idx)
        seasonal_powers[ELEMENT_NAMES[elem_idx]] = {
            'state': state, 'state_cn': state_cn, 'power': power,
        }

    # Day Master's seasonal power
    dm_seasonal = get_seasonal_power(STEM_ELEMENT[day_master_idx], month_branch_idx)

    # Hidden Stems for each branch
    hidden_stems = {}
    for p_type, p_data in pillars.items():
        bi = p_data['branch_index']
        hidden = []
        for h in HIDDEN_STEMS[bi]:
            hs = HEAVENLY_STEMS[h['stem']]
            hidden.append({
                'stem': hs['char'],
                'pinyin': hs['pinyin'],
                'element': hs['element'],
                'is_main': h['is_main'],
            })
        hidden_stems[p_type] = hidden

    # Ten Gods for all stems (relative to Day Master)
    ten_gods = {}
    for p_type, p_data in pillars.items():
        ten_gods[p_type] = get_ten_god(day_master_idx, p_data['stem_index'])

    # Also Ten Gods for hidden stems
    hidden_ten_gods = {}
    for p_type, h_list in hidden_stems.items():
        htg = []
        for h in h_list:
            # Find stem index
            si = next(i for i, s in enumerate(HEAVENLY_STEMS) if s['char'] == h['stem'])
            htg.append(get_ten_god(day_master_idx, si))
        hidden_ten_gods[p_type] = htg

    # Void Branches
    void_branches = get_void_branches(day_pillar['stem_index'], day_pillar['branch_index'])
    void_branch_chars = [EARTHLY_BRANCHES[b]['char'] for b in void_branches]

    # Check which pillars have void branches
    void_in_pillars = {}
    for p_type, p_data in pillars.items():
        void_in_pillars[p_type] = p_data['branch_index'] in void_branches

    # Luck Pillars
    is_male = (gender.lower() == 'male')
    direction = determine_luck_direction(day_master_idx, is_male)

    if direction == 'FORWARD':
        days_diff = get_days_to_next_term(date(year, month, day))
    else:
        days_diff = get_days_to_prev_term(date(year, month, day))

    start_years, start_months = calc_starting_age(days_diff)
    luck_pillars = derive_luck_pillars(
        month_pillar['stem_index'], month_pillar['branch_index'], direction
    )
    luck_schedule = build_luck_schedule(start_years, start_months, luck_pillars)

    # Special Patterns
    special_patterns = check_special_patterns(pillars)

    # Sexagenary indices
    sexagenary = {}
    for p_type, p_data in pillars.items():
        sexagenary[p_type] = compute_sexagenary_index(
            p_data['stem_index'], p_data['branch_index']
        )

    # Na Yin lookup (based on sexagenary index)
    na_yin_table = _build_na_yin_table()
    na_yin = {}
    for p_type, sx_idx in sexagenary.items():
        na_yin[p_type] = na_yin_table[sx_idx]

    # Assemble complete chart
    chart = {
        'name': name,
        'birth_date': {'year': year, 'month': month, 'day': day, 'hour': hour},
        'gender': gender,
        'day_master': day_master,
        'day_master_info': day_master_info,
        'season': season,
        'dm_seasonal_power': {
            'state': dm_seasonal[0],
            'state_cn': dm_seasonal[1],
            'power': dm_seasonal[2],
        },
        'seasonal_powers': seasonal_powers,
        'pillars': pillars,
        'hidden_stems': hidden_stems,
        'ten_gods': ten_gods,
        'hidden_ten_gods': hidden_ten_gods,
        'void_branches': void_branches,
        'void_branch_chars': void_branch_chars,
        'void_in_pillars': void_in_pillars,
        'sexagenary': sexagenary,
        'na_yin': na_yin,
        'luck': {
            'direction': direction,
            'days_to_boundary': days_diff,
            'starting_age_years': start_years,
            'starting_age_months': start_months,
            'pillars': luck_pillars,
            'schedule': luck_schedule,
        },
        'special_patterns': special_patterns,
    }

    return chart


def _build_na_yin_table() -> Dict[int, Dict]:
    """
    Build the Na Yin (纳音) lookup table for all 60 sexagenary pairs.

    Returns:
        Dict mapping sexagenary index (0-59) to Na Yin info
    """
    na_yin_data = [
        ('甲子', '乙丑', '海中金', 'Metal in the Sea'),
        ('丙寅', '丁卯', '炉中火', 'Fire in the Furnace'),
        ('戊辰', '己巳', '大林木', 'Wood in the Great Forest'),
        ('庚午', '辛未', '路旁土', 'Earth by the Roadside'),
        ('壬申', '癸酉', '剑锋金', 'Metal of the Sword Blade'),
        ('甲戌', '乙亥', '山头火', 'Fire on the Mountain Peak'),
        ('丙子', '丁丑', '涧下水', 'Water in the Ravine'),
        ('戊寅', '己卯', '城头土', 'Earth on the City Wall'),
        ('庚辰', '辛巳', '白蜡金', 'Metal of White Wax'),
        ('壬午', '癸未', '杨柳木', 'Wood of the Willow'),
        ('甲申', '乙酉', '井泉水', 'Water from the Well Spring'),
        ('丙戌', '丁亥', '屋上土', 'Earth on the Roof'),
        ('戊子', '己丑', '霹雳火', 'Fire of Thunderbolt'),
        ('庚寅', '辛卯', '松柏木', 'Wood of the Pine & Cypress'),
        ('壬辰', '癸巳', '长流水', 'Flowing Long Water'),
        ('甲午', '乙未', '沙中金', 'Metal in the Sand'),
        ('丙申', '丁酉', '山下火', 'Fire at the Foot of the Mountain'),
        ('戊戌', '己亥', '平地木', 'Wood on the Flat Plain'),
        ('庚子', '辛丑', '壁上土', 'Earth on the Wall'),
        ('壬寅', '癸卯', '金箔金', 'Metal of Gold Leaf'),
        ('甲辰', '乙巳', '覆灯火', 'Fire of the Lamp'),
        ('丙午', '丁未', '天河水', 'Water of the Heavenly River'),
        ('戊申', '己酉', '大驿土', 'Earth of the Great Post-Road'),
        ('庚戌', '辛亥', '钗钏金', 'Metal of Hairpins & Bracelets'),
        ('壬子', '癸丑', '桑柘木', 'Wood of the Mulberry Tree'),
        ('甲寅', '乙卯', '大溪水', 'Water of the Great Stream'),
        ('丙辰', '丁巳', '沙中土', 'Earth in the Sand'),
        ('戊午', '己未', '天上火', 'Fire of the Sky / Sun'),
        ('庚申', '辛酉', '石榴木', 'Wood of the Pomegranate'),
        ('壬戌', '癸亥', '大海水', 'Water of the Great Ocean'),
    ]

    # Element mapping for Na Yin
    na_yin_elements = {
        '金': 'Metal', '木': 'Wood', '水': 'Water', '火': 'Fire', '土': 'Earth',
    }

    table = {}
    for idx, (pair1, pair2, name_cn, name_en) in enumerate(na_yin_data):
        sx1 = idx * 2
        sx2 = idx * 2 + 1
        # Extract element from name
        elem_cn = name_cn[-1]
        elem = na_yin_elements.get(elem_cn, 'Earth')
        info = {'name_cn': name_cn, 'name_en': name_en, 'element': elem}
        table[sx1] = info
        table[sx2] = info

    return table


# ═══════════════════════════════════════════════════════════════════════════
# 10. FORMATTING AND OUTPUT
# ═══════════════════════════════════════════════════════════════════════════

def _pinyin(text: str) -> str:
    """Convert Chinese text to pinyin."""
    try:
        return ''.join([p[0] for p in pinyin(text, style=Style.TONE3)])
    except Exception:
        return text


def format_chart(chart: Dict) -> str:
    """
    Format a complete BaZi chart for display.

    Args:
        chart: Dict from calculate_full_chart()

    Returns:
        Formatted string
    """
    lines = []
    lines.append("╔══════════════════════════════════════════════════════════════╗")
    lines.append("║               B A Z I   C H A R T                         ║")
    lines.append("╚══════════════════════════════════════════════════════════════╝")
    lines.append("")

    # Header
    name = chart.get('name', '')
    bd = chart['birth_date']
    header = f"Birth: {bd['year']}-{bd['month']:02d}-{bd['day']:02d} Hour: {bd['hour']:02d}:00"
    if name:
        header = f"{name} | " + header
    lines.append(f"  {header}")
    lines.append(f"  Gender: {chart['gender'].capitalize()}")
    lines.append(f"  Day Master: {chart['day_master']} ({chart['day_master_info']['pinyin']}) — "
                 f"{chart['day_master_info']['element']} {chart['day_master_info']['element_cn']} "
                 f"({chart['day_master_info']['yin_yang']})")
    lines.append(f"  Season: {chart['season']}")
    lines.append("")

    # ── Four Pillars ──
    lines.append("┌─────────────────────────────────────────────────────────────┐")
    lines.append("│                   F O U R   P I L L A R S                  │")
    lines.append("└─────────────────────────────────────────────────────────────┘")
    lines.append("")

    p_types = ['year', 'month', 'day', 'hour']
    p_labels = {'year': '年 Year', 'month': '月 Month', 'day': '日 Day', 'hour': '时 Hour'}

    # Header row
    lines.append(f"  {'':>12} {'Stem':>8} {'Branch':>8} {'Na Yin':>18} {'SexaIdx':>8}")
    lines.append(f"  {'─' * 56}")
    for pt in p_types:
        p = chart['pillars'][pt]
        sx = chart['sexagenary'][pt]
        ny = chart['na_yin'][pt]
        lines.append(
            f"  {p_labels[pt]:>12} {p['stem'] + p['branch']:>8}"
            f" ({p['stem_pinyin'] + p['branch_pinyin']:>14})"
            f"  {ny['name_cn']:>12}"
            f"  {sx:>3}/59"
        )
    lines.append("")

    # ── Pillar Details ──
    lines.append("  Pillar Details:")
    lines.append(f"  {'─' * 56}")
    for pt in p_types:
        p = chart['pillars'][pt]
        tg = chart['ten_gods'][pt]
        ny = chart['na_yin'][pt]
        vp = chart['void_in_pillars'][pt]
        void_mark = " ⚠ VOID" if vp else ""
        lines.append(
            f"  {p_labels[pt]:>12}: {p['stem']}({p['stem_pinyin']}){p['branch']}({p['branch_pinyin']})"
            f"  {p['element']:>6}/{p['yin_yang']}"
            f"  Ten God: {tg['name_cn']:>4}"
            f"  Na Yin: {ny['name_cn']}"
            f"{void_mark}"
        )
        # Hidden stems
        hs_list = chart['hidden_stems'][pt]
        hs_str = ', '.join([f"{h['stem']}({h['pinyin']}) {h['element']}{'★' if h['is_main'] else ''}"
                           for h in hs_list])
        lines.append(f"  {'':>12}  └─ Hidden: {hs_str}")
    lines.append("")

    # ── Seasonal Power ──
    lines.append("┌─────────────────────────────────────────────────────────────┐")
    lines.append("│              S E A S O N A L   P O W E R                   │")
    lines.append("└─────────────────────────────────────────────────────────────┘")
    lines.append("")

    dm_power = chart['dm_seasonal_power']
    lines.append(f"  Day Master ({chart['day_master']}) in {chart['season']}: "
                 f"{dm_power['state_cn']} ({dm_power['state']}) — Power Level {dm_power['power']}/5")
    lines.append("")

    lines.append(f"  {'Element':>10} {'State':>16} {'CN':>4} {'Power':>6}")
    lines.append(f"  {'─' * 38}")
    for elem_name in ['Wood', 'Fire', 'Earth', 'Metal', 'Water']:
        sp = chart['seasonal_powers'][elem_name]
        lines.append(f"  {elem_name:>10} {sp['state']:>16} {sp['state_cn']:>4} {sp['power']:>6}/5")
    lines.append("")

    # ── Ten Gods on Hidden Stems ──
    lines.append("  ── Hidden Stems Ten Gods ──")
    for pt in p_types:
        htg_list = chart['hidden_ten_gods'][pt]
        if htg_list:
            htg_str = ', '.join([
                f"{h['stem']}: {tg['name_cn']}"
                for h, tg in zip(chart['hidden_stems'][pt], htg_list)
            ])
            lines.append(f"  {p_labels[pt]:>12}: {htg_str}")
    lines.append("")

    # ── Void Branches ──
    lines.append("┌─────────────────────────────────────────────────────────────┐")
    lines.append("│               V O I D   B R A N C H E S                    │")
    lines.append("└─────────────────────────────────────────────────────────────┘")
    vc = chart['void_branch_chars']
    vp_info = ', '.join([f"{p_labels[pt]}: {'VOID' if chart['void_in_pillars'][pt] else '—'}"
                        for pt in p_types])
    lines.append(f"  Void Branches: {' '.join(vc)}")
    lines.append(f"  By Pillar: {vp_info}")
    lines.append("")

    # ── Luck Pillars ──
    lines.append("┌─────────────────────────────────────────────────────────────┐")
    lines.append("│              L U C K   P I L L A R S                       │")
    lines.append("└─────────────────────────────────────────────────────────────┘")
    lines.append("")

    luck = chart['luck']
    dir_label = '顺排 (Forward)' if luck['direction'] == 'FORWARD' else '逆排 (Reverse)'
    lines.append(f"  Direction: {dir_label}")
    lines.append(f"  Days to boundary: {luck['days_to_boundary']}")
    lines.append(f"  Starting age: {luck['starting_age_years']}y {luck['starting_age_months']}m")
    lines.append("")

    lines.append(f"  {'Pillar':>8} {'Stem-Branch':>12} {'Age Range':>16}")
    lines.append(f"  {'─' * 38}")
    for lp in luck['schedule']:
        lines.append(f"  LP{lp['number']:>1}: {lp['label']:>12} {lp['age_label']:>16}")
    lines.append("")

    # ── Special Patterns ──
    lines.append("┌─────────────────────────────────────────────────────────────┐")
    lines.append("│             S P E C I A L   P A T T E R N S                │")
    lines.append("└─────────────────────────────────────────────────────────────┘")
    lines.append("")

    sp = chart['special_patterns']
    if sp['zhuan_wang_ge']:
        lines.append(f"  ✅ 专旺格 (Zhuan Wang Ge): {sp['zhuan_wang_type']}")
    else:
        lines.append(f"  ❌ 专旺格 (Zhuan Wang Ge): Not detected")
    lines.append(f"     DM element in chart: {sp['dm_element_pct']:.0f}%")

    if sp['cong_ge']:
        lines.append(f"  ✅ 从格 (Cong Ge): {sp['cong_ge_type']}")
    else:
        lines.append(f"  ❌ 从格 (Cong Ge): Not detected")
    lines.append(f"     DM + support: {sp['dm_and_support_pct']:.0f}%")
    lines.append("")

    # ── Elemental Summary ──
    lines.append("┌─────────────────────────────────────────────────────────────┐")
    lines.append("│           E L E M E N T A L   S U M M A R Y               │")
    lines.append("└─────────────────────────────────────────────────────────────┘")
    lines.append("")

    # Count elements across all 8 characters (4 stems + 4 branches)
    elem_counts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
    for pt in p_types:
        p = chart['pillars'][pt]
        elem_counts[STEM_ELEMENT[p['stem_index']]] += 1
        elem_counts[BRANCH_ELEMENT[p['branch_index']]] += 1

    lines.append(f"  {'Element':>10} {'Count':>6} {'Seasonal':>12}")
    lines.append(f"  {'─' * 30}")
    for elem_idx in range(5):
        name = ELEMENT_NAMES[elem_idx]
        cnt = elem_counts[elem_idx]
        sp_state = chart['seasonal_powers'][name]['state_cn']
        bar = '█' * cnt + '░' * (8 - cnt)
        lines.append(f"  {name:>10} {cnt:>6} {sp_state:>8}  {bar}")
    lines.append("")

    return '\n'.join(lines)


# ═══════════════════════════════════════════════════════════════════════════
# 11. CLI INTERFACE
# ═══════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description='BaZi (Four Pillars) Calculator — Complete Chinese Astrology Chart',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -y 1990 -m 3 -d 15 -H 14 --gender male
  %(prog)s -y 2000 -m 6 -d 1 -H 10 --gender female --name "Jane Doe"
  %(prog)s -y 1985 -m 12 -d 25 -H 8 -g m --name "Test"
  %(prog)s -y 2023 -m 1 -d 1 -H 0 -g f    # Zi hour (midnight)
        """
    )
    parser.add_argument('-y', '--year', type=int, required=True, help='Birth year (Gregorian)')
    parser.add_argument('-m', '--month', type=int, required=True, help='Birth month (1-12)')
    parser.add_argument('-d', '--day', type=int, required=True, help='Birth day (1-31)')
    parser.add_argument('-H', '--hour', type=int, required=True, help='Birth hour (0-23)')
    parser.add_argument('-g', '--gender', type=str, default='male', choices=['male', 'female', 'm', 'f'],
                        help='Gender (male/female, default: male)')
    parser.add_argument('--name', type=str, default='', help='Optional person name')

    args = parser.parse_args()

    # Normalise gender
    gender_map = {'m': 'male', 'f': 'female'}
    gender = gender_map.get(args.gender, args.gender)

    try:
        chart = calculate_full_chart(
            year=args.year,
            month=args.month,
            day=args.day,
            hour=args.hour,
            gender=gender,
            name=args.name,
        )
        output = format_chart(chart)
        print(output)

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


# ═══════════════════════════════════════════════════════════════════════════
# 12. SELF-TEST
# ═══════════════════════════════════════════════════════════════════════════

def run_self_test():
    """Run built-in verification tests against known BaZi cases."""
    print("═══ BaZi Calculator Self-Test ═══\n")
    all_pass = True

    # Test 1: Year Pillar with 立春 boundary
    # 2024-02-04 (after 立春) → 甲辰年
    print("Test 1: Year Pillar (2024-02-04, after 立春)")
    p = compute_year_pillar(2024, 2, 4)
    expected = ('甲', '辰')
    result = (p['stem'], p['branch'])
    status = "PASS" if result == expected else f"FAIL (got {result})"
    print(f"  {status}: Expected {expected[0]+expected[1]}, got {p['label']}")
    if result != expected:
        all_pass = False

    # Test 2: Year Pillar before 立春
    # 2024-02-03 (before 立春) → 癸卯年 (previous year)
    print("Test 2: Year Pillar (2024-02-03, before 立春)")
    p = compute_year_pillar(2024, 2, 3)
    expected = ('癸', '卯')
    result = (p['stem'], p['branch'])
    status = "PASS" if result == expected else f"FAIL (got {result})"
    print(f"  {status}: Expected {expected[0]+expected[1]}, got {p['label']}")
    if result != expected:
        all_pass = False

    # Test 3: Day Pillar (known reference)
    # 1900-01-01 = 甲戌 (stem 0, branch 10)
    print("Test 3: Day Pillar (1900-01-01 = 甲戌)")
    p = compute_day_pillar(1900, 1, 1)
    expected = ('甲', '戌')
    result = (p['stem'], p['branch'])
    status = "PASS" if result == expected else f"FAIL (got {result})"
    print(f"  {status}: Expected {expected[0]+expected[1]}, got {p['label']}")
    if result != expected:
        all_pass = False

    # Test 4: Day Pillar second day
    # 1900-01-02 = 乙亥 (stem 1, branch 11)
    print("Test 4: Day Pillar (1900-01-02 = 乙亥)")
    p = compute_day_pillar(1900, 1, 2)
    expected = ('乙', '亥')
    result = (p['stem'], p['branch'])
    status = "PASS" if result == expected else f"FAIL (got {result})"
    print(f"  {status}: Expected {expected[0]+expected[1]}, got {p['label']}")
    if result != expected:
        all_pass = False

    # Test 5: Hour Pillar
    # Day stem 甲(0), hour 3 → 寅时(branch 2) → stem = (0*2+2)%10 = 2 → 丙
    # So hour pillar = 丙寅
    print("Test 5: Hour Pillar (甲日 + 03:00 = 丙寅时)")
    p = compute_hour_pillar(0, 3)
    expected = ('丙', '寅')
    result = (p['stem'], p['branch'])
    status = "PASS" if result == expected else f"FAIL (got {result})"
    print(f"  {status}: Expected {expected[0]+expected[1]}, got {p['label']}")
    if result != expected:
        all_pass = False

    # Test 6: Sexagenary Index
    # 甲子 = index 0
    print("Test 6: Sexagenary Index (甲子 = 0)")
    idx = compute_sexagenary_index(0, 0)
    status = "PASS" if idx == 0 else f"FAIL (got {idx})"
    print(f"  {status}: Expected 0, got {idx}")
    if idx != 0:
        all_pass = False

    # 癸亥 = index 59
    print("Test 7: Sexagenary Index (癸亥 = 59)")
    idx = compute_sexagenary_index(9, 11)
    status = "PASS" if idx == 59 else f"FAIL (got {idx})"
    print(f"  {status}: Expected 59, got {idx}")
    if idx != 59:
        all_pass = False

    # Test 8: Ten Gods
    # 甲 (day master) vs 乙 (other) → same element, diff polarity → 劫财
    print("Test 8: Ten Gods (甲 vs 乙 = 劫财)")
    tg = get_ten_god(0, 1)
    status = "PASS" if tg['name_cn'] == '劫财' else f"FAIL (got {tg['name_cn']})"
    print(f"  {status}: Expected 劫财, got {tg['name_cn']}")
    if tg['name_cn'] != '劫财':
        all_pass = False

    # 甲 (day master) vs 己 (other) → 甲克己 (I control, diff polarity) → 正财
    print("Test 9: Ten Gods (甲 vs 己 = 正财)")
    tg = get_ten_god(0, 5)
    status = "PASS" if tg['name_cn'] == '正财' else f"FAIL (got {tg['name_cn']})"
    print(f"  {status}: Expected 正财, got {tg['name_cn']}")
    if tg['name_cn'] != '正财':
        all_pass = False

    # 甲 (day master) vs 辛 (other) → 辛克甲 (controls me, diff polarity) → 正官
    print("Test 10: Ten Gods (甲 vs 辛 = 正官)")
    tg = get_ten_god(0, 7)
    status = "PASS" if tg['name_cn'] == '正官' else f"FAIL (got {tg['name_cn']})"
    print(f"  {status}: Expected 正官, got {tg['name_cn']}")
    if tg['name_cn'] != '正官':
        all_pass = False

    # Test 11: Void Branches for Day Pillar 甲子 (index 0, xun 0)
    # → 戌(10), 亥(11) are void
    print("Test 11: Void Branches (甲子日 → 戌亥空)")
    vb = get_void_branches(0, 0)
    expected = [10, 11]
    status = "PASS" if set(vb) == set(expected) else f"FAIL (got {vb})"
    print(f"  {status}: Expected 戌亥, got {[EARTHLY_BRANCHES[b]['char'] for b in vb]}")
    if set(vb) != set(expected):
        all_pass = False

    # Test 12: Hidden Stems for 子
    # 子 → 癸
    print("Test 12: Hidden Stems (子 → 癸)")
    hs = HIDDEN_STEMS[0]
    status = "PASS" if hs[0]['stem'] == 9 else f"FAIL (got stem idx {hs[0]['stem']})"
    print(f"  {status}: Expected 癸, got {HEAVENLY_STEMS[hs[0]['stem']]['char']}")
    if hs[0]['stem'] != 9:
        all_pass = False

    # Test 13: Hidden Stems for 寅
    # 寅 → 甲(主), 丙, 戊
    print("Test 13: Hidden Stems (寅 → 甲丙戊)")
    hs = HIDDEN_STEMS[2]
    stems = [HEAVENLY_STEMS[h['stem']]['char'] for h in hs]
    status = "PASS" if stems == ['甲', '丙', '戊'] else f"FAIL (got {stems})"
    print(f"  {status}: Expected ['甲','丙','戊'], got {stems}")
    if stems != ['甲', '丙', '戊']:
        all_pass = False

    # Test 14: Luck Direction
    # Yang Male (甲, idx 0) → FORWARD
    print("Test 14: Luck Direction (Yang Male 甲 → FORWARD)")
    d = determine_luck_direction(0, True)
    status = "PASS" if d == 'FORWARD' else f"FAIL (got {d})"
    print(f"  {status}: Expected FORWARD, got {d}")
    if d != 'FORWARD':
        all_pass = False

    # Yin Male (乙, idx 1) → REVERSE
    print("Test 15: Luck Direction (Yin Male 乙 → REVERSE)")
    d = determine_luck_direction(1, True)
    status = "PASS" if d == 'REVERSE' else f"FAIL (got {d})"
    print(f"  {status}: Expected REVERSE, got {d}")
    if d != 'REVERSE':
        all_pass = False

    # Test 16: Starting Age
    # 17 days → 17/3 = 5 years, remainder 2 → 8 months
    print("Test 16: Starting Age (17 days = 5y 8m)")
    y, m = calc_starting_age(17)
    status = "PASS" if (y, m) == (5, 8) else f"FAIL (got {y}y {m}m)"
    print(f"  {status}: Expected 5y 8m, got {y}y {m}m")
    if (y, m) != (5, 8):
        all_pass = False

    # Test 17: Full chart generation
    print("Test 17: Full chart generation (1990-03-15 14:00, male)")
    try:
        chart = calculate_full_chart(1990, 3, 15, 14, 'male', 'TestUser')
        print(f"  PASS: Chart generated successfully")
        print(f"  Day Master: {chart['day_master']}")
        print(f"  Four Pillars: {' '.join([chart['pillars'][t]['label'] for t in ['year','month','day','hour']])}")
        print(f"  Luck direction: {chart['luck']['direction']}")
        print(f"  Luck pillars: {' '.join([lp['label'] for lp in chart['luck']['pillars'][:5]])}")
    except Exception as e:
        print(f"  FAIL: {e}")
        all_pass = False

    print(f"\n{'═' * 40}")
    print(f"OVERALL: {'ALL TESTS PASSED' if all_pass else 'SOME TESTS FAILED'}")

    return all_pass


if __name__ == '__main__':
    if '--test' in sys.argv:
        sys.argv.remove('--test')
        run_self_test()
    elif '--chart' in sys.argv:
        idx = sys.argv.index('--chart')
        # Take remaining args as year month day hour gender
        args = sys.argv[idx + 1:]
        if len(args) >= 4:
            y, m, d, h = int(args[0]), int(args[1]), int(args[2]), int(args[3])
            g = args[4] if len(args) > 4 else 'male'
            n = args[5] if len(args) > 5 else ''
            chart = calculate_full_chart(y, m, d, h, g, n)
            print(format_chart(chart))
        else:
            print("Usage: --chart <year> <month> <day> <hour> [gender] [name]")
    else:
        main()

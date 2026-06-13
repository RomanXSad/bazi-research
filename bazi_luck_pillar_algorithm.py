#!/usr/bin/env python3
"""
Luck Pillar (Da Yun / 大运) Calculation Algorithm
Referenced from: 渊海子平, 三命通会
For BaZi chart calculator implementation.

Author: Research compiled 2026-06-14
"""

from typing import List, Dict, Tuple, Optional
from math import floor

# ─── Sexagenary Cycle Constants ──────────────────────────────────────────────

STIENS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
BRANCHES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

# Yang Heavenly Stems (Yang Day Master)
YANG_STEMS = {0: True, 1: False, 2: True, 3: False, 4: True,
              5: False, 6: True, 7: False, 8: True, 9: False}

# Solar Term names (12 major Jie / 节)
SOLAR_TERMS = [
    '立春', '惊蛰', '清明', '立夏', '芒种',
    '小暑', '立秋', '白露', '寒露', '立冬', '大雪', '小寒'
]


# ─── Core Direction Determination ─────────────────────────────────────────────

def determine_luck_direction(day_stem_index: int, is_male: bool) -> str:
    """
    Determine forward (顺排) or reverse (逆排) Luck Pillar cycle.

    Rule (渊海子平):
        - Yang Male (阳男) + Yin Female (阴女) → FORWARD
        - Yin Male (阴男) + Yang Female (阳女) → REVERSE

    Args:
        day_stem_index: Index of the Day Heavenly Stem (0-9)
        is_male: True if male, False if female

    Returns:
        'FORWARD' or 'REVERSE'
    """
    is_yang_day = YANG_STEMS[day_stem_index]

    if (is_yang_day and is_male) or (not is_yang_day and not is_male):
        return 'FORWARD'   # 阳男阴女 顺排
    else:
        return 'REVERSE'   # 阴男阳女 逆排


# ─── Starting Age Calculation ────────────────────────────────────────────────

def calc_starting_age(days_to_boundary: int) -> Tuple[int, int]:
    """
    Convert days between birth and Solar Term boundary to starting age.

    Classical formula (渊海子平):
        3 days = 1 year
        1 day  = 4 months
        1 时辰 (2 hours) ≈ 10 days (approximate)

    Args:
        days_to_boundary: Number of days from birth to nearest Solar Term
                          (FORWARD: next term; REVERSE: previous term)

    Returns:
        (years, months) tuple for starting age
    """
    years = days_to_boundary // 3
    remainder_days = days_to_boundary % 3
    months = remainder_days * 4  # 1 day = 4 months
    return (years, months)


def calc_starting_age_precise(
    days_to_boundary: int,
    birth_hour_decimal: float = 0.0
) -> Tuple[int, float]:
    """
    More precise starting age calculation including birth hour.

    Extended formula (三命通会):
        3 days = 1 year
        1 day  = 4 months
        1 ke (刻, ~15 min) = 5 days (converted to months)

    Args:
        days_to_boundary: Integer days from birth to boundary
        birth_hour_decimal: Birth hour as decimal (0.0-23.999)

    Returns:
        (years, months) tuple
    """
    years = days_to_boundary // 3
    remainder_days = days_to_boundary % 3
    months = remainder_days * 4

    # Add fractional months from birth hour
    # 24-hour day contributes to 4 months
    hour_fraction = birth_hour_decimal / 24.0
    fractional_months = hour_fraction * 4
    months += fractional_months

    # Carry over if months >= 12
    if months >= 12:
        extra_years = int(months // 12)
        years += extra_years
        months = months % 12

    return (years, months)


# ─── Luck Pillar Derivation ───────────────────────────────────────────────────

def mod(a: int, b: int) -> int:
    """Positive modulo (handles negative numbers correctly)."""
    return ((a % b) + b) % b


def derive_luck_pillars(
    month_stem_index: int,
    month_branch_index: int,
    direction: str,
    num_pillars: int = 8
) -> List[Dict]:
    """
    Derive Luck Pillars from the Month Pillar.

    Forward (顺排):
        LP(n) = MonthPillar + n stems + n branches

    Reverse (逆排):
        LP(n) = MonthPillar - n stems - n branches

    Args:
        month_stem_index: Heavenly Stem index of Month Pillar (0-9)
        month_branch_index: Earthly Branch index of Month Pillar (0-11)
        direction: 'FORWARD' or 'REVERSE'
        num_pillars: Number of Luck Pillars to generate (default: 8)

    Returns:
        List of dicts with stem/branch indices and labels
    """
    pillars = []
    for i in range(1, num_pillars + 1):
        if direction == 'FORWARD':
            stem_idx = (month_stem_index + i) % 10
            branch_idx = (month_branch_index + i) % 12
        else:  # REVERSE
            stem_idx = mod(month_stem_index - i, 10)
            branch_idx = mod(month_branch_index - i, 12)

        pillars.append({
            'number': i,
            'stem_index': stem_idx,
            'branch_index': branch_idx,
            'stem': STIENS[stem_idx],
            'branch': BRANCHES[branch_idx],
            'label': STIENS[stem_idx] + BRANCHES[branch_idx]
        })
    return pillars


# ─── Full Luck Pillar Schedule ────────────────────────────────────────────────

def build_luck_schedule(
    starting_age_years: int,
    starting_age_months: int,
    luck_pillars: List[Dict],
    round_to_whole: bool = True
) -> List[Dict]:
    """
    Build complete Luck Pillar schedule with age ranges.

    Each Luck Pillar governs 10 years.

    Args:
        starting_age_years: Years component of starting age
        starting_age_months: Months component of starting age
        luck_pillars: List of Luck Pillars from derive_luck_pillars()
        round_to_whole: If True, round starting age up to nearest whole year

    Returns:
        List of pillar dicts with age_range added
    """
    if round_to_whole:
        # Round up: if any months, add 1 year
        start = starting_age_years + (1 if starting_age_months > 0 else 0)
    else:
        start = starting_age_years + (starting_age_months / 12.0)

    schedule = []
    for i, lp in enumerate(luck_pillars):
        age_start = start + (i * 10)
        age_end = start + ((i + 1) * 10) - 1
        schedule.append({
            **lp,
            'age_start': age_start,
            'age_end': age_end,
            'age_label': f"Age {int(age_start)}-{int(age_end)}"
        })
    return schedule


# ─── Annual Pillar (流年) Interaction ────────────────────────────────────────

def get_annual_pillar(year_index: int, known_base: Optional[Tuple[int, int]] = None) -> Dict:
    """
    Get the Annual Pillar (流年) for a given year.

    The Chinese sexagenary cycle repeats every 60 years.
    Year 0 in the system is usually 甲子 (index 0,0).

    Args:
        year_index: Number of years from cycle start (e.g., Gregorian year offset)
        known_base: Optional (stem_idx, branch_idx) for a known year reference

    Returns:
        Dict with stem, branch, and label
    """
    if known_base:
        base_stem, base_branch = known_base
        # Calculate from known reference point
        stem_idx = (base_stem + year_index) % 10
        branch_idx = (base_branch + year_index) % 12
    else:
        # Using 1984甲子年 as conventional reference
        REFERENCE_YEAR = 1984
        REFERENCE_STEM = 0   # 甲
        REFERENCE_BRANCH = 0  # 子
        offset = year_index - REFERENCE_YEAR
        stem_idx = mod(REFERENCE_STEM + offset, 10)
        branch_idx = mod(REFERENCE_BRANCH + offset, 12)

    return {
        'stem_index': stem_idx,
        'branch_index': branch_idx,
        'stem': STIENS[stem_idx],
        'branch': BRANCHES[branch_idx],
        'label': STIENS[stem_idx] + BRANCHES[branch_idx]
    }


def check_tai_sui_conflict(
    annual_branch_index: int,
    natal_branch_indices: List[int]
) -> Dict:
    """
    Check if the Annual Pillar conflicts with natal chart branches.

    犯太岁 (Fan Tai Sui) conflicts:
        - 值太岁 (Zhi): Same branch (本命年)
        - 冲太岁 (Chong): Opposite branch (六冲)
        - 刑太岁 (Xing): Punishment relationship
        - 害太岁 (Hai): Harm relationship

    Args:
        annual_branch_index: Branch index of the current year
        natal_branch_indices: Branch indices of the four natal pillars

    Returns:
        Dict with conflict info
    """
    # Six Clashes (六冲): 子午, 丑未, 寅申, 卯酉, 辰戌, 巳亥
    SIX_CLASHES = {
        0: 6, 1: 7, 2: 8, 3: 9, 4: 10, 5: 11,
        6: 0, 7: 1, 8: 2, 9: 3, 10: 4, 11: 5
    }

    # Three Punishments (三刑): 寅巳申, 丑未戌, 子卯, 辰午酉亥
    # Simplified: checking direct punishment pairs
    PUNISHMENTS = {0: 3, 3: 0, 1: 7, 7: 1, 2: 5, 5: 8, 8: 2}

    # Six Harms (六害): 子未, 丑午, 寅巳, 卯辰, 申亥, 酉戌
    SIX_HARMS = {
        0: 7, 7: 0, 1: 6, 6: 1, 2: 5, 5: 2,
        3: 4, 4: 3, 8: 11, 11: 8, 9: 10, 10: 9
    }

    conflicts = []
    for n_idx in natal_branch_indices:
        if annual_branch_index == n_idx:
            conflicts.append({'type': '值太岁', 'natal_branch': n_idx,
                              'meaning': 'Same branch year (本命年) - destabilizing'})
        if SIX_CLASHES.get(annual_branch_index) == n_idx:
            conflicts.append({'type': '冲太岁', 'natal_branch': n_idx,
                              'meaning': 'Direct opposition - upheaval'})
        if PUNISHMENTS.get(annual_branch_index) == n_idx:
            conflicts.append({'type': '刑太岁', 'natal_branch': n_idx,
                              'meaning': 'Punishment - legal/relational friction'})
        if SIX_HARMS.get(annual_branch_index) == n_idx:
            conflicts.append({'type': '害太岁', 'natal_branch': n_idx,
                              'meaning': 'Harm - hidden sabotage/health issues'})

    return {'conflicts': conflicts, 'has_conflict': len(conflicts) > 0}


# ─── Complete Calculation Example ─────────────────────────────────────────────

def example_calculation():
    """
    Complete worked example.
    Person: Male, Day Stem = 乙 (Yin Wood, index 1)
            Month Pillar = 戊寅 (Wu-Yin), indices (4, 2)
            Born: 2000-03-15, 14:30
            Days to next Solar Term (清明, Apr 4) = 20 days
    """
    day_stem_index = 1   # 乙
    is_male = True
    month_stem_idx = 4   # 戊
    month_branch_idx = 2  # 寅
    days_diff = 20

    direction = determine_luck_direction(day_stem_index, is_male)
    print(f"Direction: {direction}")  # REVERSE (Yin Male)

    years, months = calc_starting_age(days_diff)
    print(f"Starting Age: {years}y {months}m (days: {days_diff})")
    # 20/3 = 6 years, 2*4 = 8 months

    pillars = derive_luck_pillars(month_stem_idx, month_branch_idx, direction)
    print(f"\nLuck Pillars (from {STIENS[month_stem_idx] + BRANCHES[month_branch_idx]}):")
    for p in pillars:
        print(f"  LP{p['number']}: {p['label']}")

    schedule = build_luck_schedule(years, months, pillars, round_to_whole=True)
    print(f"\nFinal Schedule (rounded start = {schedule[0]['age_start']}):")
    for s in schedule:
        print(f"  LP{s['number']}: {s['label']}  {s['age_label']}")

    # Annual Pillar for 2025 (乙巳年)
    annual = get_annual_pillar(2025)
    print(f"\n2025 Annual Pillar: {annual['label']}")
    lp4_label = schedule[3]['label'] if len(schedule) > 3 else 'N/A'
    print(f"Current LP (age ~31): LP{lp4_label}")


if __name__ == '__main__':
    example_calculation()

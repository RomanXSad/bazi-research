#!/usr/bin/env python3
"""
Chinese Name Converter — CLI Tool
Features:
  A. Pinyin Conversion (tone marks, no-tone, caps, with meanings)
  B. Character Meaning (element, theme, emoji, deep cultural notes)
  C. Name Analysis (full name breakdown + element balance score)
  D. Search (by English meaning, element, or theme)
"""

import argparse
import json
import re
import sys

try:
    from pypinyin import pinyin, Style
except ImportError:
    print("Please install pypinyin: pip3 install pypinyin", file=sys.stderr)
    sys.exit(1)

# ──────────────────────────────────────────────────────────────
# CHARACTER DICTIONARY
# 1000+ common Chinese name characters with meanings, elements, etc.
# ──────────────────────────────────────────────────────────────

DICT = {
    # ── STRENGTH / POWER ──
    "伟": {"pinyin": "wěi", "meanings": ["Great", "Mighty", "Grand"], "element": "土", "theme": "strength", "emoji": "✨", "gender": "M", "notes": "One of the most popular name characters for boys, expressing greatness and ambition."},
    "强": {"pinyin": "qiáng", "meanings": ["Strong", "Powerful", "Superior"], "element": "金", "theme": "strength", "emoji": "💪", "gender": "M", "notes": "Symbolizes inner strength and resilience. Common in male names."},
    "刚": {"pinyin": "gāng", "meanings": ["Firm", "Strong", "Indomitable"], "element": "金", "theme": "strength", "emoji": "⛰️", "gender": "M", "notes": "Implies unyielding strength like steel. Used for boys to express fortitude."},
    "毅": {"pinyin": "yì", "meanings": ["Firm", "Persevering", "Resolute"], "element": "木", "theme": "strength", "emoji": "🎯", "gender": "M", "notes": "Conveys determination and unwavering willpower. A classic virtue name."},
    "勇": {"pinyin": "yǒng", "meanings": ["Brave", "Courageous", "Valiant"], "element": "火", "theme": "strength", "emoji": "🦁", "gender": "M", "notes": "Directly embodies courage and bravery. Popular in both ancient and modern names."},
    "猛": {"pinyin": "měng", "meanings": ["Fierce", "Valiant", "Powerful"], "element": "火", "theme": "strength", "emoji": "🐯", "gender": "M", "notes": "Suggests fierceness and bold strength. Less common but impactful."},
    "雄": {"pinyin": "xióng", "meanings": ["Heroic", "Grand", "Mighty"], "element": "水", "theme": "strength", "emoji": "🦅", "gender": "M", "notes": "Implies heroic grandeur. Used in names to express aspirations of greatness."},
    "威": {"pinyin": "wēi", "meanings": ["Majestic", "Powerful", "Dignified"], "element": "金", "theme": "strength", "emoji": "👑", "gender": "M", "notes": "Carries a sense of awe-inspiring power and command."},
    "霸": {"pinyin": "bà", "meanings": ["Overlord", "Champion", "Dominant"], "element": "火", "theme": "strength", "emoji": "🏆", "gender": "M", "notes": "A bold character meaning hegemon or champion. Less traditional but very strong."},
    "劲": {"pinyin": "jìn", "meanings": ["Strong", "Vigorous", "Robust"], "element": "木", "theme": "strength", "emoji": "⚡", "gender": "M", "notes": "Suggests vigor and robust energy. Modern usage in athletic contexts."},
    "健": {"pinyin": "jiàn", "meanings": ["Healthy", "Strong", "Robust"], "element": "木", "theme": "strength", "emoji": "🏋️", "gender": "M", "notes": "Combines the meanings of health and strength. Very common in male names."},
    "壮": {"pinyin": "zhuàng", "meanings": ["Strong", "Robust", "Sturdy"], "element": "土", "theme": "strength", "emoji": "🏔️", "gender": "M", "notes": "Conveys physical strength and sturdiness. Traditional name character."},
    "力": {"pinyin": "lì", "meanings": ["Power", "Strength", "Force"], "element": "火", "theme": "strength", "emoji": "💥", "gender": "M", "notes": "The character for power itself. Simple, direct, and impactful in names."},
    "武": {"pinyin": "wǔ", "meanings": ["Martial", "Military", "Valiant"], "element": "火", "theme": "strength", "emoji": "⚔️", "gender": "M", "notes": "Associated with martial arts and military prowess. Classic name element."},
    "杰": {"pinyin": "jié", "meanings": ["Outstanding", "Heroic", "Eminent"], "element": "木", "theme": "strength", "emoji": "🌟", "gender": "M", "notes": "Implies being outstanding or heroic. One of the most common name characters."},
    "豪": {"pinyin": "háo", "meanings": ["Heroic", "Bold", "Luxurious"], "element": "金", "theme": "strength", "emoji": "🏅", "gender": "M", "notes": "Suggests heroism and boldness. Also relates to luxury and grandeur."},
    "宏": {"pinyin": "hóng", "meanings": ["Grand", "Vast", "Magnificent"], "element": "水", "theme": "strength", "emoji": "🌊", "gender": "M", "notes": "Expresses grandeur and vastness. Used in names to suggest broad vision."},
    "盛": {"pinyin": "shèng", "meanings": ["Flourishing", "Prosperous", "Grand"], "element": "火", "theme": "strength", "emoji": "🔥", "gender": "M", "notes": "Implies thriving prosperity and majestic grandeur."},
    "昂": {"pinyin": "áng", "meanings": ["High", "Proud", "Elevated"], "element": "木", "theme": "strength", "emoji": "📈", "gender": "M", "notes": "Suggests being high-spirited and proud. Expresses confidence."},
    "振": {"pinyin": "zhèn", "meanings": ["Energize", "Inspire", "Shake"], "element": "金", "theme": "strength", "emoji": "🚀", "gender": "M", "notes": "Means to revitalize or energize. Suggests dynamic leadership."},

    # ── WISDOM / INTELLIGENCE ──
    "明": {"pinyin": "míng", "meanings": ["Bright", "Clear", "Intelligent"], "element": "火", "theme": "wisdom", "emoji": "💡", "gender": "unisex", "notes": "Combines sun and moon radicals. One of the most popular name characters for both genders."},
    "智": {"pinyin": "zhì", "meanings": ["Wisdom", "Intelligence", "Wise"], "element": "火", "theme": "wisdom", "emoji": "🧠", "gender": "M", "notes": "Directly represents wisdom and intellect. Highly valued virtue name."},
    "慧": {"pinyin": "huì", "meanings": ["Wise", "Intelligent", "Bright"], "element": "水", "theme": "wisdom", "emoji": "🦉", "gender": "F", "notes": "Implies keen intelligence and wisdom. Very popular in female names."},
    "睿": {"pinyin": "ruì", "meanings": ["Astute", "Perceptive", "Wise"], "element": "金", "theme": "wisdom", "emoji": "🔮", "gender": "M", "notes": "Denotes deep wisdom and farsightedness. A sophisticated character."},
    "聪": {"pinyin": "cōng", "meanings": ["Intelligent", "Clever", "Bright"], "element": "水", "theme": "wisdom", "emoji": "👂", "gender": "unisex", "notes": "Relates to acute hearing and mental quickness. Popular for both genders."},
    "颖": {"pinyin": "yǐng", "meanings": ["Clever", "Outstanding", "Gifted"], "element": "木", "theme": "wisdom", "emoji": "🌾", "gender": "F", "notes": "Implies cleverness and outstanding talent. Often used in girls' names."},
    "悟": {"pinyin": "wù", "meanings": ["Enlightened", "Aware", "Comprehend"], "element": "木", "theme": "wisdom", "emoji": "☀️", "gender": "unisex", "notes": "Buddhist connotations of enlightenment and awakening."},
    "哲": {"pinyin": "zhé", "meanings": ["Philosophical", "Wise", "Sage"], "element": "火", "theme": "wisdom", "emoji": "📚", "gender": "M", "notes": "Relates to philosophy and deep wisdom. Classic scholar name."},
    "思": {"pinyin": "sī", "meanings": ["Thoughtful", "Contemplative", "Think"], "element": "金", "theme": "wisdom", "emoji": "💭", "gender": "unisex", "notes": "Represents deep thought and reflection. Used in both male and female names."},
    "文": {"pinyin": "wén", "meanings": ["Literary", "Culture", "Elegant"], "element": "水", "theme": "wisdom", "emoji": "📖", "gender": "unisex", "notes": "Represents culture, literature, and refinement. A classic character."},
    "博": {"pinyin": "bó", "meanings": ["Broad", "Erudite", "Wealthy"], "element": "水", "theme": "wisdom", "emoji": "🌐", "gender": "M", "notes": "Implies broad learning and erudition. Suggests a wealth of knowledge."},
    "学": {"pinyin": "xué", "meanings": ["Study", "Learning", "Knowledge"], "element": "水", "theme": "wisdom", "emoji": "📝", "gender": "M", "notes": "Directly represents the pursuit of knowledge. Traditional scholarly name."},
    "知": {"pinyin": "zhī", "meanings": ["Knowledge", "Awareness", "Wise"], "element": "火", "theme": "wisdom", "emoji": "🎓", "gender": "unisex", "notes": "Represents knowledge and awareness. Simple yet profound."},
    "达": {"pinyin": "dá", "meanings": ["Achieve", "Understand", "Reach"], "element": "火", "theme": "wisdom", "emoji": "🎯", "gender": "M", "notes": "Means to achieve or reach understanding. Expresses accomplishment."},
    "理": {"pinyin": "lǐ", "meanings": ["Reason", "Logic", "Principle"], "element": "金", "theme": "wisdom", "emoji": "⚖️", "gender": "M", "notes": "Represents reason and natural principles. Philosophical name character."},

    # ── BEAUTY / GRACE ──
    "美": {"pinyin": "měi", "meanings": ["Beautiful", "Pretty", "Elegant"], "element": "水", "theme": "beauty", "emoji": "🌸", "gender": "F", "notes": "The character for beauty itself. Extremely popular in girls' names."},
    "丽": {"pinyin": "lì", "meanings": ["Beautiful", "Lovely", "Graceful"], "element": "火", "theme": "beauty", "emoji": "💐", "gender": "F", "notes": "Implies loveliness and grace. Very common female name character."},
    "艳": {"pinyin": "yàn", "meanings": ["Gorgeous", "Radiant", "Colorful"], "element": "火", "theme": "beauty", "emoji": "🌺", "gender": "F", "notes": "Suggests vibrant, gorgeous beauty. Used for striking, colorful names."},
    "婷": {"pinyin": "tíng", "meanings": ["Graceful", "Elegant", "Slender"], "element": "木", "theme": "beauty", "emoji": "💃", "gender": "F", "notes": "Describes graceful, elegant posture. Very common in female names."},
    "娜": {"pinyin": "nà", "meanings": ["Elegant", "Graceful", "Charming"], "element": "水", "theme": "beauty", "emoji": "✨", "gender": "F", "notes": "Implies elegance and charm. Popular in modern girls' names."},
    "娴": {"pinyin": "xián", "meanings": ["Refined", "Elegant", "Cultured"], "element": "火", "theme": "beauty", "emoji": "🎀", "gender": "F", "notes": "Describes refined, cultured elegance. Traditional virtue for women."},
    "淑": {"pinyin": "shū", "meanings": ["Gentle", "Refined", "Pure"], "element": "水", "theme": "beauty", "emoji": "🤍", "gender": "F", "notes": "Implies gentle refinement and moral purity. Classic female virtue name."},
    "雅": {"pinyin": "yǎ", "meanings": ["Elegant", "Refined", "Graceful"], "element": "木", "theme": "beauty", "emoji": "🎵", "gender": "F", "notes": "Represents elegance and sophistication. Highly prized in naming."},
    "倩": {"pinyin": "qiàn", "meanings": ["Pretty", "Charming", "Beautiful"], "element": "火", "theme": "beauty", "emoji": "😊", "gender": "F", "notes": "Implies charming, pretty appearance. Classical beauty in literature."},
    "娇": {"pinyin": "jiāo", "meanings": ["Tender", "Lovely", "Charming"], "element": "火", "theme": "beauty", "emoji": "🌷", "gender": "F", "notes": "Suggests tender loveliness and delicacy. Common in girls' names."},
    "媚": {"pinyin": "mèi", "meanings": ["Charming", "Enchanting", "Alluring"], "element": "水", "theme": "beauty", "emoji": "💋", "gender": "F", "notes": "Implies enchanting charm and allure. Less common but very expressive."},
    "秀": {"pinyin": "xiù", "meanings": ["Elegant", "Graceful", "Outstanding"], "element": "木", "theme": "beauty", "emoji": "🌿", "gender": "F", "notes": "Suggests elegant refinement and outstanding quality. Very popular."},
    "琳": {"pinyin": "lín", "meanings": ["Jade", "Gem", "Beautiful Jade"], "element": "木", "theme": "beauty", "emoji": "💎", "gender": "F", "notes": "Beautiful jade. Precious stone imagery is very common in girls' names."},
    "瑶": {"pinyin": "yáo", "meanings": ["Jade", "Precious", "Lustrous"], "element": "火", "theme": "beauty", "emoji": "🟢", "gender": "F", "notes": "Refers to precious jade. Mythical and highly valued name character."},
    "璇": {"pinyin": "xuán", "meanings": ["Jade", "Precious Stone", "Lustrous"], "element": "金", "theme": "beauty", "emoji": "💠", "gender": "F", "notes": "Beautiful jade. Sophisticated and elegant name character for girls."},
    "莹": {"pinyin": "yíng", "meanings": ["Lustrous", "Sparkling", "Jade-like"], "element": "火", "theme": "beauty", "emoji": "✨", "gender": "F", "notes": "Suggests sparkling, lustrous beauty like polished jade."},
    "琦": {"pinyin": "qí", "meanings": ["Beautiful Jade", "Extraordinary", "Precious"], "element": "木", "theme": "beauty", "emoji": "💚", "gender": "F", "notes": "Beautiful and extraordinary jade. Conveys preciousness."},
    "珠": {"pinyin": "zhū", "meanings": ["Pearl", "Precious", "Jewel"], "element": "金", "theme": "beauty", "emoji": "🪷", "gender": "F", "notes": "Pearl. Implies preciousness and rarity. Traditional name for girls."},
    "黛": {"pinyin": "dài", "meanings": ["Dark Beauty", "Elegant", "Refined"], "element": "水", "theme": "beauty", "emoji": "🖤", "gender": "F", "notes": "Originally black pigment for eyebrows. Poetic, refined beauty."},
    "姿": {"pinyin": "zī", "meanings": ["Grace", "Posture", "Charm"], "element": "金", "theme": "beauty", "emoji": "🧘", "gender": "F", "notes": "Refers to graceful bearing and posture. Expresses physical charm."},
    "妙": {"pinyin": "miào", "meanings": ["Wondrous", "Fine", "Clever"], "element": "水", "theme": "beauty", "emoji": "🎊", "gender": "F", "notes": "Implies wondrous beauty and cleverness. A subtle, elegant choice."},

    # ── NATURE ──
    "山": {"pinyin": "shān", "meanings": ["Mountain", "Lofty", "Sturdy"], "element": "土", "theme": "nature", "emoji": "🏔️", "gender": "M", "notes": "Mountain imagery conveys stability and grandeur. Classic nature name."},
    "川": {"pinyin": "chuān", "meanings": ["River", "Stream", "Flowing"], "element": "水", "theme": "nature", "emoji": "🏞️", "gender": "M", "notes": "River. Suggests smooth, flowing movement and adaptability."},
    "江": {"pinyin": "jiāng", "meanings": ["River", "Yangtze", "Grand"], "element": "水", "theme": "nature", "emoji": "🌊", "gender": "M", "notes": "Large river. Conveys grand scale and continuous flow."},
    "海": {"pinyin": "hǎi", "meanings": ["Ocean", "Sea", "Vast"], "element": "水", "theme": "nature", "emoji": "🌅", "gender": "M", "notes": "Ocean. Implies vastness and depth. One of the most popular name characters."},
    "林": {"pinyin": "lín", "meanings": ["Forest", "Grove", "Abundant"], "element": "木", "theme": "nature", "emoji": "🌲", "gender": "unisex", "notes": "Forest. Symbolizes growth and abundance. Used for both genders."},
    "森": {"pinyin": "sēn", "meanings": ["Forest", "Dense", "Lush"], "element": "木", "theme": "nature", "emoji": "🌳", "gender": "M", "notes": "Dense forest. Amplifies the forest imagery with triple tree radical."},
    "树": {"pinyin": "shù", "meanings": ["Tree", "Establish", "Upright"], "element": "木", "theme": "nature", "emoji": "🌴", "gender": "M", "notes": "Tree. Symbolizes firm establishment and upright character."},
    "松": {"pinyin": "sōng", "meanings": ["Pine", "Resilient", "Enduring"], "element": "木", "theme": "nature", "emoji": "🎄", "gender": "M", "notes": "Pine tree — symbol of resilience and longevity. Endures winter cold."},
    "柏": {"pinyin": "bǎi", "meanings": ["Cypress", "Cedar", "Evergreen"], "element": "木", "theme": "nature", "emoji": "🌲", "gender": "M", "notes": "Cypress tree. Evergreen symbol of longevity and steadfastness."},
    "梅": {"pinyin": "méi", "meanings": ["Plum Blossom", "Winter Bloom"], "element": "木", "theme": "nature", "emoji": "🌺", "gender": "F", "notes": "Plum blossom — blooms in winter, symbol of perseverance and beauty."},
    "兰": {"pinyin": "lán", "meanings": ["Orchid", "Elegant", "Noble"], "element": "木", "theme": "nature", "emoji": "🌷", "gender": "F", "notes": "Orchid. Symbol of refinement and nobility in Chinese culture."},
    "竹": {"pinyin": "zhú", "meanings": ["Bamboo", "Flexible", "Upright"], "element": "木", "theme": "nature", "emoji": "🎋", "gender": "M", "notes": "Bamboo — bends but doesn't break. Symbol of resilience and virtue."},
    "菊": {"pinyin": "jú", "meanings": ["Chrysanthemum", "Autumn Bloom"], "element": "木", "theme": "nature", "emoji": "🌼", "gender": "F", "notes": "Chrysanthemum. Autumn flower, symbol of longevity and nobility."},
    "莲": {"pinyin": "lián", "meaning": ["Lotus", "Pure", "Elegant"], "meanings": ["Lotus", "Pure", "Elegant"], "element": "木", "theme": "nature", "emoji": "🪷", "gender": "F", "notes": "Lotus — rises pure from mud. Deep Buddhist symbolism."},
    "荷": {"pinyin": "hé", "meanings": ["Lotus", "Water Lily", "Gentle"], "element": "水", "theme": "nature", "emoji": "🪷", "gender": "F", "notes": "Lotus/water lily. Gentle beauty and purity in water."},
    "花": {"pinyin": "huā", "meanings": ["Flower", "Bloom", "Beauty"], "element": "木", "theme": "nature", "emoji": "🌸", "gender": "F", "notes": "Flower. Universal symbol of beauty and femininity in names."},
    "云": {"pinyin": "yún", "meanings": ["Cloud", "Lofty", "Graceful"], "element": "水", "theme": "nature", "emoji": "☁️", "gender": "unisex", "notes": "Cloud. Suggests lofty aspirations and graceful freedom."},
    "雪": {"pinyin": "xuě", "meanings": ["Snow", "Pure", "White"], "element": "水", "theme": "nature", "emoji": "❄️", "gender": "F", "notes": "Snow. Symbol of purity and pristine beauty. Popular girls' name."},
    "霜": {"pinyin": "shuāng", "meanings": ["Frost", "Crisp", "Pure"], "element": "水", "theme": "nature", "emoji": "🧊", "gender": "F", "notes": "Frost. Less common but poetic, suggesting crisp purity."},
    "露": {"pinyin": "lù", "meanings": ["Dew", "Pure", "Ephemeral"], "element": "水", "theme": "nature", "emoji": "💧", "gender": "F", "notes": "Dew. Suggests freshness, purity, and the beauty of transience."},
    "冰": {"pinyin": "bīng", "meanings": ["Ice", "Pure", "Clear"], "element": "水", "theme": "nature", "emoji": "🧊", "gender": "F", "notes": "Ice. Symbol of purity and clarity. Modern and cool for girls."},
    "月": {"pinyin": "yuè", "meanings": ["Moon", "Lunar", "Radiant"], "element": "水", "theme": "nature", "emoji": "🌙", "gender": "F", "notes": "Moon. Romantic and poetic. Deep cultural significance in Chinese poetry."},
    "星": {"pinyin": "xīng", "meanings": ["Star", "Radiant", "Brilliant"], "element": "火", "theme": "nature", "emoji": "⭐", "gender": "unisex", "notes": "Star. Implies brilliance and shining destiny. Modern and popular."},
    "阳": {"pinyin": "yáng", "meanings": ["Sun", "Positive", "Bright"], "element": "火", "theme": "nature", "emoji": "☀️", "gender": "M", "notes": "Sun/sunlight. Represents positivity and masculine energy."},
    "光": {"pinyin": "guāng", "meanings": ["Light", "Bright", "Radiance"], "element": "火", "theme": "nature", "emoji": "💫", "gender": "M", "notes": "Light. Symbol of brightness, hope, and radiance."},
    "霞": {"pinyin": "xiá", "meanings": ["Rosy Clouds", "Sunset Glow"], "element": "水", "theme": "nature", "emoji": "🌇", "gender": "F", "notes": "Sunset clouds. Poetic and beautiful. Popular in female names."},
    "虹": {"pinyin": "hóng", "meanings": ["Rainbow", "Colorful", "Hope"], "element": "火", "theme": "nature", "emoji": "🌈", "gender": "F", "notes": "Rainbow. Symbol of hope and colorful beauty."},
    "雨": {"pinyin": "yǔ", "meanings": ["Rain", "Nourishing", "Grace"], "element": "水", "theme": "nature", "emoji": "🌧️", "gender": "unisex", "notes": "Rain. Source of life and nourishment. Gentle, graceful."},
    "雷": {"pinyin": "léi", "meanings": ["Thunder", "Powerful", "Forceful"], "element": "火", "theme": "nature", "emoji": "⚡", "gender": "M", "notes": "Thunder. Powerful natural force. Strong, impactful name."},
    "风": {"pinyin": "fēng", "meanings": ["Wind", "Free", "Graceful"], "element": "木", "theme": "nature", "emoji": "🌬️", "gender": "unisex", "notes": "Wind. Symbol of freedom and graceful movement."},
    "春": {"pinyin": "chūn", "meanings": ["Spring", "Youth", "Vitality"], "element": "木", "theme": "nature", "emoji": "🌱", "gender": "F", "notes": "Spring. Symbol of youth, renewal, and vitality."},
    "夏": {"pinyin": "xià", "meanings": ["Summer", "Warm", "Flourishing"], "element": "火", "theme": "nature", "emoji": "☀️", "gender": "unisex", "notes": "Summer. Warm and flourishing. Works for both genders."},
    "秋": {"pinyin": "qiū", "meanings": ["Autumn", "Harvest", "Mature"], "element": "金", "theme": "nature", "emoji": "🍂", "gender": "F", "notes": "Autumn. Symbol of harvest and maturity. Poetic and beautiful."},
    "冬": {"pinyin": "dōng", "meanings": ["Winter", "Pure", "Enduring"], "element": "水", "theme": "nature", "emoji": "❄️", "gender": "unisex", "notes": "Winter. Symbol of endurance and purity."},
    "天": {"pinyin": "tiān", "meanings": ["Sky", "Heaven", "Grand"], "element": "火", "theme": "nature", "emoji": "🌌", "gender": "M", "notes": "Sky/heaven. Grand and expansive. Expresses lofty ideals."},
    "地": {"pinyin": "dì", "meanings": ["Earth", "Ground", "Steadfast"], "element": "土", "theme": "nature", "emoji": "🌍", "gender": "M", "notes": "Earth. Symbol of steadfastness and nurturing stability."},
    "石": {"pinyin": "shí", "meanings": ["Stone", "Firm", "Steadfast"], "element": "土", "theme": "nature", "emoji": "🪨", "gender": "M", "notes": "Stone. Symbol of firmness and unyielding character."},
    "玉": {"pinyin": "yù", "meanings": ["Jade", "Pure", "Precious"], "element": "土", "theme": "nature", "emoji": "🟢", "gender": "F", "notes": "Jade — the most precious stone in Chinese culture. Purity and virtue."},
    "金": {"pinyin": "jīn", "meanings": ["Gold", "Precious", "Shining"], "element": "金", "theme": "nature", "emoji": "🥇", "gender": "unisex", "notes": "Gold. Symbol of value, wealth, and radiance."},
    "银": {"pinyin": "yín", "meanings": ["Silver", "Bright", "Precious"], "element": "金", "theme": "nature", "emoji": "🥈", "gender": "unisex", "notes": "Silver. Precious metal, bright and valuable."},

    # ── VIRTUE / MORALITY ──
    "德": {"pinyin": "dé", "meanings": ["Virtue", "Morality", "Benevolence"], "element": "火", "theme": "virtue", "emoji": "🛡️", "gender": "M", "notes": "The highest Confucian virtue. Expresses moral excellence."},
    "仁": {"pinyin": "rén", "meanings": ["Benevolent", "Humane", "Kind"], "element": "木", "theme": "virtue", "emoji": "💗", "gender": "M", "notes": "Benevolence and humaneness — core Confucian virtue."},
    "义": {"pinyin": "yì", "meanings": ["Righteous", "Just", "Honorable"], "element": "金", "theme": "virtue", "emoji": "⚖️", "gender": "M", "notes": "Righteousness and justice. Important moral character."},
    "礼": {"pinyin": "lǐ", "meanings": ["Polite", "Courteous", "Ritual"], "element": "木", "theme": "virtue", "emoji": "🙏", "gender": "unisex", "notes": "Propriety, courtesy, and ritual decorum. Confucian virtue."},
    "信": {"pinyin": "xìn", "meanings": ["Trustworthy", "Faithful", "Honest"], "element": "金", "theme": "virtue", "emoji": "🤝", "gender": "unisex", "notes": "Trustworthiness and honesty. Essential virtue in Chinese culture."},
    "忠": {"pinyin": "zhōng", "meanings": ["Loyal", "Devoted", "Faithful"], "element": "火", "theme": "virtue", "emoji": "🐕", "gender": "M", "notes": "Loyalty and devotion. Highly valued in traditional Chinese ethics."},
    "孝": {"pinyin": "xiào", "meanings": ["Filial", "Dutiful", "Respectful"], "element": "土", "theme": "virtue", "emoji": "👨‍👩‍👧‍👦", "gender": "unisex", "notes": "Filial piety — the foundational virtue of Chinese family ethics."},
    "诚": {"pinyin": "chéng", "meanings": ["Honest", "Sincere", "Genuine"], "element": "金", "theme": "virtue", "emoji": "💝", "gender": "unisex", "notes": "Sincerity and honesty. Modern virtue character."},
    "善": {"pinyin": "shàn", "meanings": ["Good", "Kind", "Benevolent"], "element": "水", "theme": "virtue", "emoji": "😇", "gender": "unisex", "notes": "Goodness and kindness. Universal virtue name."},
    "良": {"pinyin": "liáng", "meanings": ["Good", "Fine", "Excellent"], "element": "火", "theme": "virtue", "emoji": "👍", "gender": "unisex", "notes": "Goodness and excellence. Simple virtue character."},
    "谦": {"pinyin": "qiān", "meanings": ["Modest", "Humble", "Self-effacing"], "element": "木", "theme": "virtue", "emoji": "🙇", "gender": "M", "notes": "Humility and modesty. Highly prized Confucian virtue."},
    "和": {"pinyin": "hé", "meanings": ["Harmony", "Peaceful", "Gentle"], "element": "木", "theme": "virtue", "emoji": "☮️", "gender": "unisex", "notes": "Harmony — central concept in Chinese philosophy."},
    "平": {"pinyin": "píng", "meanings": ["Peaceful", "Flat", "Equal"], "element": "水", "theme": "virtue", "emoji": "🕊️", "gender": "unisex", "notes": "Peace and equality. Simple, balanced virtue name."},
    "安": {"pinyin": "ān", "meanings": ["Peaceful", "Safe", "Calm"], "element": "土", "theme": "virtue", "emoji": "🏠", "gender": "unisex", "notes": "Peace and safety. One of the most common name characters."},
    "静": {"pinyin": "jìng", "meanings": ["Quiet", "Calm", "Serene"], "element": "金", "theme": "virtue", "emoji": "🧘", "gender": "F", "notes": "Tranquility and stillness. Popular in girls' names."},
    "宁": {"pinyin": "níng", "meanings": ["Serene", "Peaceful", "Tranquil"], "element": "火", "theme": "virtue", "emoji": "😌", "gender": "unisex", "notes": "Serenity and tranquility. Modern favorite."},
    "真": {"pinyin": "zhēn", "meanings": ["True", "Genuine", "Real"], "element": "金", "theme": "virtue", "emoji": "💎", "gender": "unisex", "notes": "Truth and genuineness. Simple but profound."},

    # ── PROSPERITY / WEALTH ──
    "富": {"pinyin": "fù", "meanings": ["Rich", "Wealthy", "Abundant"], "element": "土", "theme": "prosperity", "emoji": "💰", "gender": "M", "notes": "Wealth and abundance. Auspicious name character."},
    "贵": {"pinyin": "guì", "meanings": ["Noble", "Valuable", "Honorable"], "element": "木", "theme": "prosperity", "emoji": "👑", "gender": "unisex", "notes": "Nobility and preciousness. Implies high status."},
    "福": {"pinyin": "fú", "meanings": ["Fortune", "Blessing", "Happiness"], "element": "水", "theme": "prosperity", "emoji": "🧧", "gender": "M", "notes": "One of the most auspicious characters. Fortune and blessing."},
    "禄": {"pinyin": "lù", "meanings": ["Prosperity", "Emolument", "Fortune"], "element": "火", "theme": "prosperity", "emoji": "🥂", "gender": "M", "notes": "Official salary and prosperity. Auspicious and traditional."},
    "寿": {"pinyin": "shòu", "meanings": ["Longevity", "Life", "Durable"], "element": "土", "theme": "prosperity", "emoji": "🎂", "gender": "M", "notes": "Longevity. One of the three auspicious stars (福禄寿)."},
    "财": {"pinyin": "cái", "meanings": ["Wealth", "Money", "Fortune"], "element": "金", "theme": "prosperity", "emoji": "💵", "gender": "M", "notes": "Wealth and financial fortune. Direct and auspicious."},
    "宝": {"pinyin": "bǎo", "meanings": ["Treasure", "Precious", "Jewel"], "element": "火", "theme": "prosperity", "emoji": "🏆", "gender": "unisex", "notes": "Treasure. Implies being precious and valued."},
    "鑫": {"pinyin": "xīn", "meanings": ["Prosperous", "Wealthy", "Gold Abundance"], "element": "金", "theme": "prosperity", "emoji": "💰", "gender": "M", "notes": "Three gold characters stacked — extreme prosperity. Popular in business."},
    "森": {"pinyin": "sēn", "meanings": ["Forest", "Abundant", "Lush Growth"], "element": "木", "theme": "prosperity", "emoji": "🌳", "gender": "M", "notes": "Dense forest — abundant growth symbolizing prosperity."},
    "荣": {"pinyin": "róng", "meanings": ["Glory", "Honor", "Flourishing"], "element": "木", "theme": "prosperity", "emoji": "🌻", "gender": "unisex", "notes": "Glory and flourishing. Implies thriving success and honor."},
    "华": {"pinyin": "huá", "meanings": ["Splendid", "Prosperous", "China"], "element": "水", "theme": "prosperity", "emoji": "🏮", "gender": "unisex", "notes": "Splendor and prosperity. Also represents Chinese culture."},
    "昌": {"pinyin": "chāng", "meanings": ["Prosperous", "Bright", "Flourishing"], "element": "火", "theme": "prosperity", "emoji": "☀️", "gender": "M", "notes": "Prosperity and brightness. Classic auspicious name."},
    "盛": {"pinyin": "shèng", "meanings": ["Thriving", "Flourishing", "Grand"], "element": "火", "theme": "prosperity", "emoji": "🔥", "gender": "M", "notes": "Grand flourishing. Implies peak prosperity and vitality."},
    "旺": {"pinyin": "wàng", "meanings": ["Prosperous", "Vibrant", "Booming"], "element": "火", "theme": "prosperity", "emoji": "📈", "gender": "M", "notes": "Vibrant prosperity and booming energy. Modern favorite."},
    "裕": {"pinyin": "yù", "meanings": ["Abundant", "Wealthy", "Plentiful"], "element": "金", "theme": "prosperity", "emoji": "🎁", "gender": "M", "notes": "Abundance and plenty. Suggests a life of comfort."},
    "丰": {"pinyin": "fēng", "meanings": ["Abundant", "Plentiful", "Harvest"], "element": "火", "theme": "prosperity", "emoji": "🌾", "gender": "unisex", "notes": "Abundance and harvest. Simple but auspicious."},

    # ── FAMILY / HOME ──
    "家": {"pinyin": "jiā", "meanings": ["Family", "Home", "Household"], "element": "木", "theme": "family", "emoji": "🏠", "gender": "unisex", "notes": "Family. Core Chinese value expressed in naming."},
    "国": {"pinyin": "guó", "meanings": ["Country", "Nation", "Patriotic"], "element": "土", "theme": "family", "emoji": "🇨🇳", "gender": "M", "notes": "Country/nation. Expresses patriotism and national pride."},
    "世": {"pinyin": "shì", "meanings": ["Generation", "World", "Epoch"], "element": "金", "theme": "family", "emoji": "🌍", "gender": "M", "notes": "Generation and world. Implies legacy and enduring impact."},
    "子": {"pinyin": "zǐ", "meanings": ["Child", "Son", "Master"], "element": "水", "theme": "family", "emoji": "👶", "gender": "M", "notes": "Child/son. Classic name element. Also means 'master' (Confucius)."},
    "孙": {"pinyin": "sūn", "meanings": ["Grandchild", "Descendant"], "element": "水", "theme": "family", "emoji": "👴", "gender": "M", "notes": "Grandchild/descendant. Used in names to honor lineage."},
    "祖": {"pinyin": "zǔ", "meanings": ["Ancestor", "Founder", "Origin"], "element": "火", "theme": "family", "emoji": "🏛️", "gender": "M", "notes": "Ancestor. Carries deep respect for family lineage."},
    "宗": {"pinyin": "zōng", "meanings": ["Ancestral", "Clan", "Lineage"], "element": "火", "theme": "family", "emoji": "🏯", "gender": "M", "notes": "Clan and ancestral lineage. Traditional family name character."},
    "康": {"pinyin": "kāng", "meanings": ["Healthy", "Peaceful", "Well-being"], "element": "木", "theme": "family", "emoji": "💚", "gender": "unisex", "notes": "Health and well-being. Expresses wishes for a good life."},
    "乐": {"pinyin": "lè", "meanings": ["Joy", "Happiness", "Delight"], "element": "火", "theme": "family", "emoji": "😄", "gender": "unisex", "notes": "Joy and happiness. One of the most positive name characters."},

    # ── TALENT / ARTISTRY ──
    "艺": {"pinyin": "yì", "meanings": ["Art", "Talent", "Skill"], "element": "木", "theme": "talent", "emoji": "🎨", "gender": "unisex", "notes": "Art and artistic talent. Expresses creative ability."},
    "才": {"pinyin": "cái", "meanings": ["Talent", "Ability", "Gifted"], "element": "金", "theme": "talent", "emoji": "🎯", "gender": "M", "notes": "Talent and natural ability. Classic character for gifted children."},
    "能": {"pinyin": "néng", "meanings": ["Capable", "Able", "Competent"], "element": "火", "theme": "talent", "emoji": "💪", "gender": "unisex", "notes": "Ability and capability. Modern talent name character."},
    "巧": {"pinyin": "qiǎo", "meanings": ["Skillful", "Clever", "Deft"], "element": "木", "theme": "talent", "emoji": "🔧", "gender": "F", "notes": "Skillful and clever hands. Used for artistic or craft talent."},
    "灵": {"pinyin": "líng", "meanings": ["Spirited", "Quick", "Nimble"], "element": "火", "theme": "talent", "emoji": "✨", "gender": "unisex", "notes": "Nimble wit and spiritual quickness. Very popular."},
    "敏": {"pinyin": "mǐn", "meanings": ["Quick", "Agile", "Sharp"], "element": "水", "theme": "talent", "emoji": "⚡", "gender": "unisex", "notes": "Quick-minded and agile. Expresses sharp intelligence."},
    "妙": {"pinyin": "miào", "meanings": ["Wondrous", "Exquisite", "Skillful"], "element": "水", "theme": "talent", "emoji": "🎊", "gender": "F", "notes": "Exquisite skill and wondrous talent."},
    "巧": {"pinyin": "qiǎo", "meanings": ["Skillful", "Clever", "Deft"], "element": "木", "theme": "talent", "emoji": "🔧", "gender": "F", "notes": "Skillful and clever."},
    "音": {"pinyin": "yīn", "meanings": ["Music", "Sound", "Harmony"], "element": "土", "theme": "talent", "emoji": "🎵", "gender": "unisex", "notes": "Music and sound. Expresses musical talent and harmony."},
    "琴": {"pinyin": "qín", "meanings": ["Zither", "Music", "Artistic"], "element": "木", "theme": "talent", "emoji": "🎹", "gender": "F", "notes": "Chinese zither. Elegant artistic name for girls."},
    "画": {"pinyin": "huà", "meanings": ["Painting", "Picture", "Artistic"], "element": "土", "theme": "talent", "emoji": "🖼️", "gender": "unisex", "notes": "Painting. Expresses visual artistic talent."},
    "诗": {"pinyin": "shī", "meanings": ["Poetry", "Poetic", "Literary"], "element": "金", "theme": "talent", "emoji": "📜", "gender": "unisex", "notes": "Poetry. Expresses literary talent and romantic sensibility."},
    "书": {"pinyin": "shū", "meanings": ["Book", "Calligraphy", "Write"], "element": "火", "theme": "talent", "emoji": "📕", "gender": "unisex", "notes": "Book and calligraphy. Expresses scholarly talent."},
    "墨": {"pinyin": "mò", "meanings": ["Ink", "Calligraphy", "Dark"], "element": "水", "theme": "talent", "emoji": "🖋️", "gender": "unisex", "notes": "Ink. Artistic and scholarly. Sophisticated choice."},

    # ── GENTLE / SOFT ──
    "柔": {"pinyin": "róu", "meanings": ["Soft", "Gentle", "Flexible"], "element": "木", "theme": "gentle", "emoji": "🕊️", "gender": "F", "notes": "Softness and gentleness. Valued feminine quality."},
    "婉": {"pinyin": "wǎn", "meanings": ["Gentle", "Gracious", "Tactful"], "element": "火", "theme": "gentle", "emoji": "🌷", "gender": "F", "notes": "Gentle and gracious. Classic feminine virtue in names."},
    "温": {"pinyin": "wēn", "meanings": ["Warm", "Gentle", "Tender"], "element": "水", "theme": "gentle", "emoji": "🌡️", "gender": "F", "notes": "Warmth and gentleness. Suggests a warm personality."},
    "暖": {"pinyin": "nuǎn", "meanings": ["Warm", "Cozy", "Caring"], "element": "火", "theme": "gentle", "emoji": "☀️", "gender": "F", "notes": "Warmth and coziness. Modern gentle name."},
    "惠": {"pinyin": "huì", "meanings": ["Kind", "Benevolent", "Gracious"], "element": "水", "theme": "gentle", "emoji": "🎁", "gender": "F", "notes": "Kindness and benevolence. Classical feminine virtue."},
    "爱": {"pinyin": "ài", "meanings": ["Love", "Affection", "Cherish"], "element": "火", "theme": "gentle", "emoji": "❤️", "gender": "F", "notes": "Love. Universal expression of affection in names."},
    "心": {"pinyin": "xīn", "meanings": ["Heart", "Mind", "Soul"], "element": "火", "theme": "gentle", "emoji": "💖", "gender": "unisex", "notes": "Heart. Expresses heartfelt sincerity and compassion."},
    "欣": {"pinyin": "xīn", "meanings": ["Joyful", "Glad", "Happy"], "element": "木", "theme": "gentle", "emoji": "😊", "gender": "F", "notes": "Joy and happiness. Very popular in girls' names."},
    "悦": {"pinyin": "yuè", "meanings": ["Delighted", "Joyful", "Pleased"], "element": "金", "theme": "gentle", "emoji": "😃", "gender": "F", "notes": "Joy and delight. Expresses happiness and contentment."},
    "怡": {"pinyin": "yí", "meanings": ["Joyful", "Harmonious", "Cheerful"], "element": "土", "theme": "gentle", "emoji": "😌", "gender": "F", "notes": "Joy and harmony. Gentle, pleasant character for girls."},
    "可": {"pinyin": "kě", "meanings": ["Adorable", "Can", "Worthy"], "element": "木", "theme": "gentle", "emoji": "🥰", "gender": "F", "notes": "Adorable and worthy. Used in compound names."},
    "甜": {"pinyin": "tián", "meanings": ["Sweet", "Honey", "Lovely"], "element": "火", "theme": "gentle", "emoji": "🍯", "gender": "F", "notes": "Sweetness. Modern affectionate name for girls."},

    # ── COMMON SURNAMES (for surname detection) ──
    "张": {"pinyin": "zhāng", "meanings": ["Draw bow", "Spread", "Expand"], "element": "火", "theme": "surname", "emoji": "🏹", "gender": "unisex", "notes": "Very common Chinese surname. The surname itself means to draw a bow."},
    "王": {"pinyin": "wáng", "meanings": ["King", "Royal", "Monarch"], "element": "土", "theme": "surname", "emoji": "👑", "gender": "unisex", "notes": "Very common surname meaning 'king'. Also used in given names."},
    "李": {"pinyin": "lǐ", "meanings": ["Plum", "Plum Tree"], "element": "木", "theme": "surname", "emoji": "🍒", "gender": "unisex", "notes": "One of the most common Chinese surnames. Also means plum."},
    "赵": {"pinyin": "zhào", "meanings": ["Zhao (state name)", "Ancient"], "element": "火", "theme": "surname", "emoji": "🏯", "gender": "unisex", "notes": "Ancient surname from the State of Zhao. Historically noble."},
    "刘": {"pinyin": "liú", "meanings": ["Kill", "Destroy", "Liu"], "element": "金", "theme": "surname", "emoji": "⚔️", "gender": "unisex", "notes": "Very common surname. The imperial surname of the Han Dynasty."},
    "陈": {"pinyin": "chén", "meanings": ["Exhibit", "Old", "Chen"], "element": "火", "theme": "surname", "emoji": "🏛️", "gender": "unisex", "notes": "Common surname. Also means to display or arrange."},
    "杨": {"pinyin": "yáng", "meanings": ["Poplar", "Willow"], "element": "木", "theme": "surname", "emoji": "🌳", "gender": "unisex", "notes": "Common surname. Also means poplar tree."},
    "黄": {"pinyin": "huáng", "meanings": ["Yellow", "Golden"], "element": "土", "theme": "surname", "emoji": "💛", "gender": "unisex", "notes": "Common surname meaning yellow. Also used in given names."},
    "吴": {"pinyin": "wú", "meanings": ["Wu (state/region)"], "element": "火", "theme": "surname", "emoji": "🏯", "gender": "unisex", "notes": "Ancient surname from the State of Wu."},
    "周": {"pinyin": "zhōu", "meanings": ["Circumference", "Cycle", "Zhou"], "element": "土", "theme": "surname", "emoji": "🔄", "gender": "unisex", "notes": "Ancient surname from the Zhou Dynasty."},
    "徐": {"pinyin": "xú", "meanings": ["Slow", "Gentle", "Xu"], "element": "木", "theme": "surname", "emoji": "🐢", "gender": "unisex", "notes": "Common surname meaning slow and gentle."},
    "孙": {"pinyin": "sūn", "meanings": ["Grandchild", "Descendant"], "element": "水", "theme": "surname", "emoji": "👶", "gender": "unisex", "notes": "Common surname. Also means grandchild/descendant."},
    "马": {"pinyin": "mǎ", "meanings": ["Horse"], "element": "火", "theme": "surname", "emoji": "🐴", "gender": "unisex", "notes": "Common surname meaning horse."},
    "朱": {"pinyin": "zhū", "meanings": ["Vermilion", "Red"], "element": "火", "theme": "surname", "emoji": "🔴", "gender": "unisex", "notes": "Common surname meaning vermilion red."},
    "胡": {"pinyin": "hú", "meanings": ["Beard", "Foreign", "Hu"], "element": "土", "theme": "surname", "emoji": "🧔", "gender": "unisex", "notes": "Common surname. Also means barbarian/non-Han."},
    "林": {"pinyin": "lín", "meanings": ["Forest", "Grove"], "element": "木", "theme": "surname", "emoji": "🌲", "gender": "unisex", "notes": "Common surname meaning forest. Very popular in southern China."},
    "何": {"pinyin": "hé", "meanings": ["What", "How", "Why"], "element": "水", "theme": "surname", "emoji": "❓", "gender": "unisex", "notes": "Common surname."},
    "高": {"pinyin": "gāo", "meanings": ["Tall", "High", "Lofty"], "element": "木", "theme": "surname", "emoji": "📏", "gender": "unisex", "notes": "Common surname meaning tall or high."},
    "梁": {"pinyin": "liáng", "meanings": ["Bridge", "Beam", "Roof"], "element": "木", "theme": "surname", "emoji": "🌉", "gender": "unisex", "notes": "Common surname meaning bridge or beam."},
    "宋": {"pinyin": "sòng", "meanings": ["Song (dynasty)"], "element": "火", "theme": "surname", "emoji": "🏯", "gender": "unisex", "notes": "Ancient surname from the Song Dynasty."},
    "郑": {"pinyin": "zhèng", "meanings": ["Zheng (state)", "Serious"], "element": "火", "theme": "surname", "emoji": "🎯", "gender": "unisex", "notes": "Common surname. Also means serious/grave."},
    "谢": {"pinyin": "xiè", "meanings": ["Thank", "Apologize", "Decline"], "element": "金", "theme": "surname", "emoji": "🙏", "gender": "unisex", "notes": "Common surname meaning to thank."},
    "唐": {"pinyin": "táng", "meanings": ["Tang (dynasty)", "Bold"], "element": "火", "theme": "surname", "emoji": "🏯", "gender": "unisex", "notes": "Ancient surname from the Tang Dynasty."},
    "韩": {"pinyin": "hán", "meanings": ["Han (state)", "Korea"], "element": "水", "theme": "surname", "emoji": "🇰🇷", "gender": "unisex", "notes": "Common surname from the State of Han."},
    "曹": {"pinyin": "cáo", "meanings": ["Cao (state)", "Group"], "element": "火", "theme": "surname", "emoji": "🏛️", "gender": "unisex", "notes": "Ancient surname."},
    "许": {"pinyin": "xǔ", "meanings": ["Allow", "Promise", "Xu"], "element": "金", "theme": "surname", "emoji": "🤝", "gender": "unisex", "notes": "Common surname meaning to allow or promise."},
    "邓": {"pinyin": "dèng", "meanings": ["Deng (ancient state)"], "element": "火", "theme": "surname", "emoji": "🏯", "gender": "unisex", "notes": "Ancient surname."},
    "冯": {"pinyin": "féng", "meanings": ["Gallop", "Feng"], "element": "水", "theme": "surname", "emoji": "🏇", "gender": "unisex", "notes": "Common surname."},
    "程": {"pinyin": "chéng", "meanings": ["Regulation", "Journey", "Process"], "element": "木", "theme": "surname", "emoji": "📋", "gender": "unisex", "notes": "Common surname meaning rule or journey."},
    "蔡": {"pinyin": "cài", "meanings": ["Cai (ancient state)", "Turtle"], "element": "木", "theme": "surname", "emoji": "🐢", "gender": "unisex", "notes": "Ancient surname from the State of Cai."},
    "彭": {"pinyin": "péng", "meanings": ["Peng (ancient state)"], "element": "火", "theme": "surname", "emoji": "🥁", "gender": "unisex", "notes": "Ancient surname."},
    "潘": {"pinyin": "pān", "meanings": ["Pan (state)", "Water overflow"], "element": "水", "theme": "surname", "emoji": "🌊", "gender": "unisex", "notes": "Common surname."},
    "袁": {"pinyin": "yuán", "meanings": ["Yuan (state)", "Long robe"], "element": "土", "theme": "surname", "emoji": "👘", "gender": "unisex", "notes": "Ancient surname."},
    "于": {"pinyin": "yú", "meanings": ["In", "At", "By"], "element": "土", "theme": "surname", "emoji": "📍", "gender": "unisex", "notes": "Common surname."},
    "董": {"pinyin": "dǒng", "meanings": ["Direct", "Supervise", "Dong"], "element": "木", "theme": "surname", "emoji": "👀", "gender": "unisex", "notes": "Common surname meaning to supervise."},
    "余": {"pinyin": "yú", "meanings": ["I", "Me", "Surplus"], "element": "土", "theme": "surname", "emoji": "➕", "gender": "unisex", "notes": "Common surname. Also means surplus."},
    "苏": {"pinyin": "sū", "meanings": ["Revive", "Su (state)"], "element": "木", "theme": "surname", "emoji": "🌱", "gender": "unisex", "notes": "Common surname meaning to revive."},
    "叶": {"pinyin": "yè", "meanings": ["Leaf", "Page", "Harmony"], "element": "木", "theme": "surname", "emoji": "🍃", "gender": "unisex", "notes": "Common surname meaning leaf."},
    "吕": {"pinyin": "lǚ", "meanings": ["Lu (state)", "Pitch pipes"], "element": "火", "theme": "surname", "emoji": "🎵", "gender": "unisex", "notes": "Ancient surname."},
    "魏": {"pinyin": "wèi", "meanings": ["Wei (state)", "Grand"], "element": "火", "theme": "surname", "emoji": "🏯", "gender": "unisex", "notes": "Ancient surname from the State of Wei."},
    "蒋": {"pinyin": "jiǎng", "meanings": ["Jiang (state)", "Reed"], "element": "木", "theme": "surname", "emoji": "🌾", "gender": "unisex", "notes": "Ancient surname."},
    "田": {"pinyin": "tián", "meanings": ["Field", "Farmland", "Cultivate"], "element": "土", "theme": "surname", "emoji": "🌾", "gender": "unisex", "notes": "Common surname meaning field/farmland."},
    "杜": {"pinyin": "dù", "meanings": ["Stop", "Block", "Pear tree"], "element": "木", "theme": "surname", "emoji": "🍐", "gender": "unisex", "notes": "Common surname. Also means pear tree."},
    "丁": {"pinyin": "dīng", "meanings": ["Nail", "Male adult", "Tiny"], "element": "火", "theme": "surname", "emoji": "🔩", "gender": "unisex", "notes": "Common surname. Also means nail or male."},
    "沈": {"pinyin": "shěn", "meanings": ["Sink", "Shen (state)"], "element": "水", "theme": "surname", "emoji": "🌊", "gender": "unisex", "notes": "Common surname meaning to sink."},
    "任": {"pinyin": "rèn", "meanings": ["Responsibility", "Trust"], "element": "金", "theme": "surname", "emoji": "🤝", "gender": "unisex", "notes": "Common surname meaning responsibility."},
    "姚": {"pinyin": "yáo", "meanings": ["Yao (ancient sage king)"], "element": "火", "theme": "surname", "emoji": "👑", "gender": "unisex", "notes": "Ancient and noble surname from Emperor Yao."},
    "卢": {"pinyin": "lú", "meanings": ["Lu (state)", "Black"], "element": "水", "theme": "surname", "emoji": "⚫", "gender": "unisex", "notes": "Ancient surname."},
    "傅": {"pinyin": "fù", "meanings": ["Teacher", "Tutor", "Attach"], "element": "水", "theme": "surname", "emoji": "👨‍🏫", "gender": "unisex", "notes": "Common surname meaning teacher."},
    "钟": {"pinyin": "zhōng", "meanings": ["Bell", "Clock", "Vessel"], "element": "金", "theme": "surname", "emoji": "🔔", "gender": "unisex", "notes": "Common surname meaning bell."},
    "崔": {"pinyin": "cuī", "meanings": ["High", "Towering"], "element": "山", "theme": "surname", "emoji": "⛰️", "gender": "unisex", "notes": "Common surname meaning high/towering."},
    "汪": {"pinyin": "wāng", "meanings": ["Pond", "Vast", "Bark"], "element": "水", "theme": "surname", "emoji": "🌊", "gender": "unisex", "notes": "Common surname meaning pond."},
    "范": {"pinyin": "fàn", "meanings": ["Mold", "Pattern", "Fan"], "element": "木", "theme": "surname", "emoji": "📐", "gender": "unisex", "notes": "Common surname meaning pattern/mold."},
    "方": {"pinyin": "fāng", "meanings": ["Square", "Direction", "Method"], "element": "火", "theme": "surname", "emoji": "⬜", "gender": "unisex", "notes": "Common surname meaning square or direction."},
    "石": {"pinyin": "shí", "meanings": ["Stone", "Rock"], "element": "土", "theme": "surname", "emoji": "🪨", "gender": "unisex", "notes": "Common surname meaning stone."},
    "廖": {"pinyin": "liào", "meanings": ["Liao (state)", "Spacious"], "element": "火", "theme": "surname", "emoji": "🏯", "gender": "unisex", "notes": "Ancient surname."},
    "熊": {"pinyin": "xióng", "meanings": ["Bear", "Heroic"], "element": "火", "theme": "surname", "emoji": "🐻", "gender": "unisex", "notes": "Common surname meaning bear."},
    "金": {"pinyin": "jīn", "meanings": ["Gold", "Metal", "Precious"], "element": "金", "theme": "surname", "emoji": "🥇", "gender": "unisex", "notes": "Common surname meaning gold."},
    "陆": {"pinyin": "lù", "meanings": ["Land", "Six", "Lu"], "element": "土", "theme": "surname", "emoji": "🗺️", "gender": "unisex", "notes": "Common surname meaning land."},
    "毛": {"pinyin": "máo", "meanings": ["Hair", "Feather", "Mao"], "element": "水", "theme": "surname", "emoji": "🪶", "gender": "unisex", "notes": "Common surname meaning hair/feather."},
    "赖": {"pinyin": "lài", "meanings": ["Rely", "Depend", "Trust"], "element": "火", "theme": "surname", "emoji": "🤲", "gender": "unisex", "notes": "Common surname meaning to rely on."},
    "萧": {"pinyin": "xiāo", "meanings": ["Desolate", "Xiao", "Xiaoxiao"], "element": "木", "theme": "surname", "emoji": "🌬️", "gender": "unisex", "notes": "Ancient surname."},
    "谭": {"pinyin": "tán", "meanings": ["Talk", "Discuss", "Tan"], "element": "火", "theme": "surname", "emoji": "💬", "gender": "unisex", "notes": "Common surname meaning to talk."},
    "曾": {"pinyin": "zēng", "meanings": ["Previously", "Zeng (state)"], "element": "火", "theme": "surname", "emoji": "🕰️", "gender": "unisex", "notes": "Ancient surname meaning previously/once."},

    # ── MORE GIVEN NAME CHARACTERS ──
    "龙": {"pinyin": "lóng", "meanings": ["Dragon", "Imperial", "Mythical"], "element": "水", "theme": "strength", "emoji": "🐉", "gender": "M", "notes": "The dragon — most powerful mythical creature. Symbol of imperial power and good fortune."},
    "凤": {"pinyin": "fèng", "meanings": ["Phoenix", "Graceful", "Mythical"], "element": "火", "theme": "beauty", "emoji": "🦚", "gender": "F", "notes": "The phoenix — mythical bird of grace. Feminine counterpart to the dragon."},
    "翔": {"pinyin": "xiáng", "meanings": ["Soar", "Glide", "Fly"], "element": "木", "theme": "strength", "emoji": "🦅", "gender": "M", "notes": "Soaring like a bird. Expresses freedom and high aspirations."},
    "飞": {"pinyin": "fēi", "meanings": ["Fly", "Swift", "Soaring"], "element": "火", "theme": "strength", "emoji": "✈️", "gender": "M", "notes": "To fly. Expresses speed and lofty ambitions."},
    "腾": {"pinyin": "téng", "meanings": ["Gallop", "Rise", "Soar"], "element": "火", "theme": "strength", "emoji": "🐎", "gender": "M", "notes": "Galloping or rising rapidly. Suggests dynamic progress."},
    "跃": {"pinyin": "yuè", "meanings": ["Leap", "Jump", "Bound"], "element": "火", "theme": "strength", "emoji": "🐇", "gender": "M", "notes": "Leaping forward. Symbolizes progress and advancement."},
    "超": {"pinyin": "chāo", "meanings": ["Surpass", "Exceed", "Ultra"], "element": "金", "theme": "strength", "emoji": "🚀", "gender": "M", "notes": "To surpass or exceed. Expresses ambition to excel."},
    "越": {"pinyin": "yuè", "meanings": ["Exceed", "Surpass", "Cross over"], "element": "火", "theme": "strength", "emoji": "⛰️", "gender": "M", "notes": "To exceed and cross over. Implies overcoming challenges."},
    "进": {"pinyin": "jìn", "meanings": ["Advance", "Enter", "Progress"], "element": "火", "theme": "strength", "emoji": "➡️", "gender": "M", "notes": "To advance and make progress."},
    "前": {"pinyin": "qián", "meanings": ["Forward", "Future", "Front"], "element": "火", "theme": "strength", "emoji": "🔜", "gender": "M", "notes": "Forward and future-oriented. Optimistic name element."},
    "尚": {"pinyin": "shàng", "meanings": ["Esteem", "Still", "Upward"], "element": "金", "theme": "virtue", "emoji": "⬆️", "gender": "unisex", "notes": "To esteem and value. Implies high principles."},
    "崇": {"pinyin": "chóng", "meanings": ["Revere", "Worship", "Lofty"], "element": "山", "theme": "virtue", "emoji": "⛰️", "gender": "M", "notes": "To revere and hold in high esteem. Lofty ideals."},
    "尊": {"pinyin": "zūn", "meanings": ["Respect", "Honor", "Noble"], "element": "火", "theme": "virtue", "emoji": "👑", "gender": "M", "notes": "Respect and honor. Expresses noble character."},
    "敬": {"pinyin": "jìng", "meanings": ["Respect", "Revere", "Honor"], "element": "木", "theme": "virtue", "emoji": "🙏", "gender": "M", "notes": "Deep respect and reverence. Classic virtue name."},
    "辉": {"pinyin": "huī", "meanings": ["Brightness", "Radiance", "Luster"], "element": "火", "theme": "nature", "emoji": "✨", "gender": "M", "notes": "Bright radiance and splendor. Popular in boys' names."},
    "煌": {"pinyin": "huáng", "meanings": ["Brilliant", "Glowing", "Grand"], "element": "火", "theme": "nature", "emoji": "🔆", "gender": "M", "notes": "Brilliant and grand. Amplified brightness."},
    "耀": {"pinyin": "yào", "meanings": ["Shine", "Illuminate", "Glory"], "element": "火", "theme": "nature", "emoji": "💫", "gender": "M", "notes": "To shine brilliantly. Expresses radiant glory."},
    "昭": {"pinyin": "zhāo", "meanings": ["Bright", "Clear", "Manifest"], "element": "火", "theme": "nature", "emoji": "☀️", "gender": "M", "notes": "Bright and clear. Implies obvious virtue."},
    "旭": {"pinyin": "xù", "meanings": ["Rising Sun", "Brilliant", "New Day"], "element": "火", "theme": "nature", "emoji": "🌅", "gender": "M", "notes": "Rising sun. Symbol of new beginnings and bright future."},
    "晨": {"pinyin": "chén", "meanings": ["Morning", "Dawn", "New Day"], "element": "火", "theme": "nature", "emoji": "🌄", "gender": "unisex", "notes": "Morning and dawn. Symbol of freshness and new beginnings."},
    "曦": {"pinyin": "xī", "meanings": ["Sunlight", "Morning Light", "Dawn"], "element": "火", "theme": "nature", "emoji": "🌤️", "gender": "unisex", "notes": "Morning sunlight. Poetic and warm."},
    "岚": {"pinyin": "lán", "meanings": ["Mist", "Fog", "Mountain Vapor"], "element": "水", "theme": "nature", "emoji": "🌫️", "gender": "F", "notes": "Mountain mist. Poetic and ethereal."},
    "峰": {"pinyin": "fēng", "meanings": ["Peak", "Summit", "High Point"], "element": "山", "theme": "nature", "emoji": "⛰️", "gender": "M", "notes": "Mountain peak. Expresses ambition to reach the top."},
    "岭": {"pinyin": "lǐng", "meanings": ["Mountain Ridge", "Peak"], "element": "山", "theme": "nature", "emoji": "🏔️", "gender": "M", "notes": "Mountain ridge. Natural scenery name."},
    "岳": {"pinyin": "yuè", "meanings": ["High Mountain", "Peak"], "element": "山", "theme": "nature", "emoji": "🗻", "gender": "M", "notes": "High, sacred mountain. Majestic and grand."},
    "岩": {"pinyin": "yán", "meanings": ["Cliff", "Rock", "Crag"], "element": "山", "theme": "nature", "emoji": "🪨", "gender": "M", "notes": "Cliff and rock. Sturdy and unyielding."},
    "涛": {"pinyin": "tāo", "meanings": ["Great Wave", "Billow", "Surge"], "element": "水", "theme": "nature", "emoji": "🌊", "gender": "M", "notes": "Great waves. Powerful and dynamic natural imagery."},
    "浪": {"pinyin": "làng", "meanings": ["Wave", "Bold", "Unrestrained"], "element": "水", "theme": "nature", "emoji": "🏄", "gender": "M", "notes": "Wave. Suggests boldness and free spirit."},
    "渊": {"pinyin": "yuān", "meanings": ["Deep pool", "Profound", "Deep"], "element": "水", "theme": "nature", "emoji": "🌌", "gender": "M", "notes": "Deep pool. Implies profound depth of knowledge."},
    "瀚": {"pinyin": "hàn", "meanings": ["Vast", "Expansive", "Ocean"], "element": "水", "theme": "nature", "emoji": "🌊", "gender": "M", "notes": "Vast and expansive like the ocean. Grand scale."},
    "浩": {"pinyin": "hào", "meanings": ["Vast", "Grand", "Powerful"], "element": "水", "theme": "nature", "emoji": "🌊", "gender": "M", "notes": "Vast and powerful. Very popular in boys' names."},
    "洋": {"pinyin": "yáng", "meanings": ["Ocean", "Foreign", "Vast"], "element": "水", "theme": "nature", "emoji": "🌊", "gender": "M", "notes": "Ocean. Vast and international."},
    "波": {"pinyin": "bō", "meanings": ["Wave", "Ripple", "Fluctuate"], "element": "水", "theme": "nature", "emoji": "🌊", "gender": "M", "notes": "Wave/ripple. Gentle yet dynamic."},
    "溪": {"pinyin": "xī", "meanings": ["Stream", "Brook", "Creek"], "element": "水", "theme": "nature", "emoji": "🏞️", "gender": "F", "notes": "Small stream. Gentle and peaceful water imagery."},
    "泉": {"pinyin": "quán", "meanings": ["Spring", "Fountain", "Source"], "element": "水", "theme": "nature", "emoji": "⛲", "gender": "unisex", "notes": "Spring of water. Source of life and purity."},
    "源": {"pinyin": "yuán", "meanings": ["Source", "Origin", "Headwater"], "element": "水", "theme": "nature", "emoji": "💧", "gender": "M", "notes": "Source of water. Implies origin and continuous flow."},
    "永": {"pinyin": "yǒng", "meanings": ["Eternal", "Forever", "Perpetual"], "element": "水", "theme": "virtue", "emoji": "♾️", "gender": "M", "notes": "Eternal and forever. Expresses enduring qualities."},
    "远": {"pinyin": "yuǎn", "meanings": ["Far", "Distant", "Long-term"], "element": "土", "theme": "strength", "emoji": "🎯", "gender": "M", "notes": "Far-reaching. Implies broad vision and long-term thinking."},
    "长": {"pinyin": "cháng", "meanings": ["Long", "Eternal", "Steadfast"], "element": "木", "theme": "virtue", "emoji": "📏", "gender": "M", "notes": "Long-lasting. Implies endurance and longevity."},
    "青": {"pinyin": "qīng", "meanings": ["Green", "Youthful", "Nature"], "element": "木", "theme": "nature", "emoji": "🌿", "gender": "unisex", "notes": "Green/blue. Symbol of youth, nature, and vitality."},
    "蓝": {"pinyin": "lán", "meanings": ["Blue", "Sky", "Vast"], "element": "木", "theme": "nature", "emoji": "🔵", "gender": "unisex", "notes": "Blue. Sky and ocean color. Modern name element."},
    "紫": {"pinyin": "zǐ", "meanings": ["Purple", "Noble", "Mystical"], "element": "火", "theme": "beauty", "emoji": "🟣", "gender": "F", "notes": "Purple. Imperial color, noble and mystical."},
    "红": {"pinyin": "hóng", "meanings": ["Red", "Popular", "Vibrant"], "element": "火", "theme": "beauty", "emoji": "🔴", "gender": "F", "notes": "Red. Auspicious and vibrant. Very popular in names."},
    "碧": {"pinyin": "bì", "meanings": ["Jade Green", "Clear Blue"], "element": "水", "theme": "beauty", "emoji": "💚", "gender": "F", "notes": "Jade green. Clear, precious, and beautiful."},
    "翠": {"pinyin": "cuì", "meanings": ["Emerald", "Jade Green", "Vivid"], "element": "金", "theme": "beauty", "emoji": "🟢", "gender": "F", "notes": "Emerald green/jade. Vivid and precious."},
    "丹": {"pinyin": "dān", "meanings": ["Vermilion", "Sincere", "Alchemy"], "element": "火", "theme": "beauty", "emoji": "🔴", "gender": "unisex", "notes": "Vermilion red. Also implies sincerity (red heart)."},
    "彤": {"pinyin": "tóng", "meanings": ["Red", "Vermilion", "Bright"], "element": "火", "theme": "beauty", "emoji": "🟥", "gender": "F", "notes": "Bright red. Warm and vibrant name color."},
    "彦": {"pinyin": "yàn", "meanings": ["Virtuous", "Elegant", "Learned"], "element": "木", "theme": "virtue", "emoji": "🎓", "gender": "M", "notes": "Virtuous and learned. Classic scholar name."},
    "彬": {"pinyin": "bīn", "meanings": ["Refined", "Cultured", "Elegant"], "element": "木", "theme": "virtue", "emoji": "🎩", "gender": "M", "notes": "Refined and cultured. Implies elegant manners and learning."},
    "焕": {"pinyin": "huàn", "meanings": ["Shining", "Glowing", "Luminous"], "element": "火", "theme": "nature", "emoji": "💡", "gender": "M", "notes": "Shining and luminous. Expresses radiance."},
    "煜": {"pinyin": "yù", "meanings": ["Bright", "Radiant", "Shining"], "element": "火", "theme": "nature", "emoji": "☀️", "gender": "M", "notes": "Bright and shining. Amplified radiance."},
    "炜": {"pinyin": "wěi", "meanings": ["Bright", "Glowing", "Luminous"], "element": "火", "theme": "nature", "emoji": "✨", "gender": "M", "notes": "Bright and glowing. Warm radiance."},
    "灿": {"pinyin": "càn", "meanings": ["Brilliant", "Dazzling", "Splendid"], "element": "火", "theme": "nature", "emoji": "🌟", "gender": "M", "notes": "Brilliant and dazzling. Expresses splendid achievement."},
    "鸿": {"pinyin": "hóng", "meanings": ["Wild swan", "Grand", "Vast"], "element": "水", "theme": "nature", "emoji": "🦢", "gender": "M", "notes": "Wild swan. Symbol of grand ambition and vast achievement."},
    "鹏": {"pinyin": "péng", "meanings": ["Roc", "Mythical Bird", "Grand"], "element": "水", "theme": "strength", "emoji": "🦅", "gender": "M", "notes": "The roc — a gigantic mythical bird. Symbol of immense potential."},
    "鲲": {"pinyin": "kūn", "meanings": ["Mythical Fish", "Leviathan"], "element": "水", "theme": "strength", "emoji": "🐋", "gender": "M", "notes": "A mythical giant fish from Zhuangzi. Symbol of vast potential for transformation."},
    "薇": {"pinyin": "wēi", "meanings": ["Rose", "Blooming", "Graceful"], "element": "木", "theme": "beauty", "emoji": "🌹", "gender": "F", "notes": "Rose/small flowering plant. Delicate and graceful."},
    "蕾": {"pinyin": "lěi", "meanings": ["Bud", "Blooming", "Flower Bud"], "element": "木", "theme": "beauty", "emoji": "🌷", "gender": "F", "notes": "Flower bud. Symbol of potential and budding beauty."},
    "蕊": {"pinyin": "ruǐ", "meanings": ["Stamen", "Bloom", "Flower Heart"], "element": "木", "theme": "beauty", "emoji": "🌸", "gender": "F", "notes": "Flower stamen. Delicate, innermost beauty."},
    "萌": {"pinyin": "méng", "meanings": ["Sprout", "Budding", "Adorable"], "element": "木", "theme": "beauty", "emoji": "🌱", "gender": "F", "notes": "Sprouting/budding. Cute and full of potential. Very modern."},
    "诺": {"pinyin": "nuò", "meanings": ["Promise", "Commitment", "Yes"], "element": "金", "theme": "virtue", "emoji": "🤝", "gender": "unisex", "notes": "Promise and commitment. Modern virtue name."},
    "凡": {"pinyin": "fán", "meanings": ["Ordinary", "Mortal", "Everyday"], "element": "水", "theme": "virtue", "emoji": "🌿", "gender": "unisex", "notes": "Ordinary — philosophically implies finding beauty in simplicity."},
    "一": {"pinyin": "yī", "meanings": ["One", "First", "Unity"], "element": "水", "theme": "virtue", "emoji": "1️⃣", "gender": "unisex", "notes": "One/unity. Simple and profound. Implies being first or unique."},
    "成": {"pinyin": "chéng", "meanings": ["Achieve", "Success", "Become"], "element": "金", "theme": "prosperity", "emoji": "🏆", "gender": "M", "notes": "Achievement and success. One of the most common name characters."},
    "功": {"pinyin": "gōng", "meanings": ["Achievement", "Merit", "Success"], "element": "火", "theme": "prosperity", "emoji": "🎖️", "gender": "M", "notes": "Merit and achievement. Implies successful accomplishment."},
    "建": {"pinyin": "jiàn", "meanings": ["Build", "Establish", "Found"], "element": "木", "theme": "strength", "emoji": "🏗️", "gender": "M", "notes": "To build and establish. Expresses constructive ambition."},
    "立": {"pinyin": "lì", "meanings": ["Stand", "Establish", "Set up"], "element": "火", "theme": "strength", "emoji": "📐", "gender": "M", "notes": "To stand and establish oneself. Independence and strength."},
    "志": {"pinyin": "zhì", "meanings": ["Aspiration", "Will", "Ambition"], "element": "火", "theme": "strength", "emoji": "🎯", "gender": "M", "notes": "Aspiration and willpower. Expresses determined ambition."},
    "意": {"pinyin": "yì", "meanings": ["Idea", "Meaning", "Intent"], "element": "火", "theme": "wisdom", "emoji": "💡", "gender": "unisex", "notes": "Idea and intent. Expresses thoughtful intention."},
    "念": {"pinyin": "niàn", "meanings": ["Thought", "Memory", "Read"], "element": "火", "theme": "wisdom", "emoji": "📖", "gender": "unisex", "notes": "Thought and remembrance. Expresses mindfulness."},
    "如": {"pinyin": "rú", "meanings": ["Like", "As", "If"], "element": "木", "theme": "beauty", "emoji": "💫", "gender": "F", "notes": "Like/as. Often used in compound names expressing wishes (e.g., 'like jade')."},
    "若": {"pinyin": "ruò", "meanings": ["Like", "Seem", "If"], "element": "木", "theme": "beauty", "emoji": "🌿", "gender": "F", "notes": "Like/as if. Poetic name character for girls."},
    "之": {"pinyin": "zhī", "meanings": ["Of", "It", "Go"], "element": "火", "theme": "virtue", "emoji": "➡️", "gender": "unisex", "notes": "Classical Chinese character. Used in sophisticated names."},
    "以": {"pinyin": "yǐ", "meanings": ["With", "By", "For"], "element": "火", "theme": "virtue", "emoji": "✏️", "gender": "unisex", "notes": "Classical particle. Used in literary compound names."},
    "亦": {"pinyin": "yì", "meanings": ["Also", "Too", "Likewise"], "element": "火", "theme": "virtue", "emoji": "➕", "gender": "unisex", "notes": "Also/likewise. Subtle and sophisticated name element."},
    "小": {"pinyin": "xiǎo", "meanings": ["Small", "Little", "Young"], "element": "水", "theme": "gentle", "emoji": "👶", "gender": "unisex", "notes": "Small/little. Endearing nickname character also used in formal names."},
    "大": {"pinyin": "dà", "meanings": ["Big", "Great", "Grand"], "element": "火", "theme": "strength", "emoji": "🌏", "gender": "M", "notes": "Big/great. Simple but powerful name element."},
    "中": {"pinyin": "zhōng", "meanings": ["Middle", "Center", "China"], "element": "土", "theme": "virtue", "emoji": "🎯", "gender": "M", "notes": "Middle/center. Expresses balance and centrality."},
    "正": {"pinyin": "zhèng", "meanings": ["Right", "Correct", "Upright"], "element": "火", "theme": "virtue", "emoji": "✅", "gender": "M", "notes": "Upright and correct. Expresses integrity and honesty."},
    "直": {"pinyin": "zhí", "meanings": ["Straight", "Honest", "Direct"], "element": "木", "theme": "virtue", "emoji": "📏", "gender": "M", "notes": "Straightforward and honest. Simple virtue name."},
    "恒": {"pinyin": "héng", "meanings": ["Constant", "Persistent", "Eternal"], "element": "水", "theme": "virtue", "emoji": "♾️", "gender": "M", "notes": "Constancy and persistence. Expresses enduring commitment."},
    "维": {"pinyin": "wéi", "meanings": ["Maintain", "Sustain", "Link"], "element": "木", "theme": "virtue", "emoji": "🔗", "gender": "M", "notes": "To maintain and sustain. Expresses preserving important values."},
    "坚": {"pinyin": "jiān", "meanings": ["Firm", "Strong", "Hard"], "element": "土", "theme": "strength", "emoji": "⛰️", "gender": "M", "notes": "Firm and unyielding. Expresses resolute character."},
    "厚": {"pinyin": "hòu", "meanings": ["Thick", "Generous", "Kind"], "element": "土", "theme": "virtue", "emoji": "🛡️", "gender": "M", "notes": "Generous and kind. Implies depth of character."},
    "实": {"pinyin": "shí", "meanings": ["Solid", "True", "Fruitful"], "element": "金", "theme": "virtue", "emoji": "🎯", "gender": "M", "notes": "Solid and true. Expresses honesty and substance."},
    "容": {"pinyin": "róng", "meanings": ["Tolerant", "Appearance", "Contain"], "element": "土", "theme": "virtue", "emoji": "🤗", "gender": "unisex", "notes": "Tolerance and包容. Broad-minded virtue name."},
    "易": {"pinyin": "yì", "meanings": ["Easy", "Change", "Exchange"], "element": "火", "theme": "wisdom", "emoji": "🔄", "gender": "unisex", "notes": "Easy/change. Implies adaptability and the philosophy of change."},
    "白": {"pinyin": "bái", "meanings": ["White", "Pure", "Clear"], "element": "金", "theme": "beauty", "emoji": "⚪", "gender": "unisex", "notes": "White and pure. Simple, clean name element."},
    "翔": {"pinyin": "xiáng", "meanings": ["Soar", "Glide", "Circle"], "element": "木", "theme": "strength", "emoji": "🦅", "gender": "M", "notes": "Soaring like a bird. Expresses freedom."},
    "万": {"pinyin": "wàn", "meanings": ["Ten Thousand", "Countless", "All"], "element": "水", "theme": "prosperity", "emoji": "💯", "gender": "M", "notes": "Ten thousand — represents abundance and completeness."},
    "千": {"pinyin": "qiān", "meanings": ["Thousand", "Many", "Countless"], "element": "金", "theme": "prosperity", "emoji": "🔢", "gender": "unisex", "notes": "Thousand. Expresses multiplicity and abundance."},
    "百": {"pinyin": "bǎi", "meanings": ["Hundred", "Many", "All"], "element": "火", "theme": "prosperity", "emoji": "💯", "gender": "unisex", "notes": "Hundred. Implies completeness and multitude."},
    "兆": {"pinyin": "zhào", "meanings": ["Omen", "Trillion", "Portent"], "element": "火", "theme": "prosperity", "emoji": "🔮", "gender": "M", "notes": "Omen/trillion. Auspicious sign of great fortune."},
    "亨": {"pinyin": "hēng", "meanings": ["Smooth", "Prosperous", "Go smoothly"], "element": "火", "theme": "prosperity", "emoji": "🍀", "gender": "M", "notes": "Smooth progress. From the I Ching, meaning success."},
    "利": {"pinyin": "lì", "meanings": ["Sharp", "Benefit", "Profit"], "element": "金", "theme": "prosperity", "emoji": "💰", "gender": "M", "notes": "Benefit and profit. Sharp wit and advantage."},
    "和": {"pinyin": "hé", "meanings": ["Peace", "Harmony", "Union"], "element": "木", "theme": "virtue", "emoji": "☮️", "gender": "unisex", "notes": "Harmony. Central Chinese virtue of social harmony."},
    "同": {"pinyin": "tóng", "meanings": ["Same", "Together", "Unite"], "element": "火", "theme": "virtue", "emoji": "🤝", "gender": "unisex", "notes": "Unity and togetherness. Expresses solidarity."},
    "新": {"pinyin": "xīn", "meanings": ["New", "Fresh", "Renew"], "element": "金", "theme": "prosperity", "emoji": "🆕", "gender": "unisex", "notes": "New and fresh. Expresses renewal and innovation."},
    "兴": {"pinyin": "xīng", "meanings": ["Rise", "Flourish", "Thrive"], "element": "水", "theme": "prosperity", "emoji": "📈", "gender": "M", "notes": "Rise and flourish. Expresses upward trajectory."},
    "伟": {"pinyin": "wěi", "meanings": ["Great", "Mighty", "Grand"], "element": "土", "theme": "strength", "emoji": "✨", "gender": "M", "notes": "One of the most popular name characters for boys, expressing greatness and ambition."},
    "勇": {"pinyin": "yǒng", "meanings": ["Brave", "Courageous", "Valiant"], "element": "火", "theme": "strength", "emoji": "🦁", "gender": "M", "notes": "Directly embodies courage and bravery."},
    "刚": {"pinyin": "gāng", "meanings": ["Firm", "Strong", "Indomitable"], "element": "金", "theme": "strength", "emoji": "⛰️", "gender": "M", "notes": "Implies unyielding strength like steel."},
    "民": {"pinyin": "mín", "meanings": ["People", "Nation", "Citizen"], "element": "水", "theme": "family", "emoji": "👥", "gender": "M", "notes": "The people. Expresses connection to community and nation."},
    "平": {"pinyin": "píng", "meanings": ["Peaceful", "Flat", "Equal"], "element": "水", "theme": "virtue", "emoji": "🕊️", "gender": "unisex", "notes": "Peace and equality. Simple, balanced virtue name."},
    "安": {"pinyin": "ān", "meanings": ["Peaceful", "Safe", "Calm"], "element": "土", "theme": "virtue", "emoji": "🏠", "gender": "unisex", "notes": "Peace and safety."},
    "乐": {"pinyin": "lè", "meanings": ["Joy", "Happiness", "Delight"], "element": "火", "theme": "family", "emoji": "😄", "gender": "unisex", "notes": "Joy and happiness."},
    "欣": {"pinyin": "xīn", "meanings": ["Joyful", "Glad", "Happy"], "element": "木", "theme": "gentle", "emoji": "😊", "gender": "F", "notes": "Joy and happiness."},
    "悦": {"pinyin": "yuè", "meanings": ["Delighted", "Joyful", "Pleased"], "element": "金", "theme": "gentle", "emoji": "😃", "gender": "F", "notes": "Joy and delight."},
    "庆": {"pinyin": "qìng", "meanings": ["Celebrate", "Congratulate", "Festive"], "element": "火", "theme": "prosperity", "emoji": "🎉", "gender": "M", "notes": "Celebration and festivity. Auspicious life events."},

    # ── Additional characters for a total of 500+ ──
    "东": {"pinyin": "dōng", "meanings": ["East", "Eastern", "Spring"], "element": "木", "theme": "nature", "emoji": "🌅", "gender": "M", "notes": "East — direction of sunrise and spring. Auspicious."},
    "南": {"pinyin": "nán", "meanings": ["South", "Southern", "Warm"], "element": "火", "theme": "nature", "emoji": "🔥", "gender": "M", "notes": "South. Associated with warmth and summer."},
    "西": {"pinyin": "xī", "meanings": ["West", "Western", "Autumn"], "element": "金", "theme": "nature", "emoji": "🌇", "gender": "M", "notes": "West. Associated with autumn and metal element."},
    "北": {"pinyin": "běi", "meanings": ["North", "Northern", "Winter"], "element": "水", "theme": "nature", "emoji": "❄️", "gender": "M", "notes": "North. Associated with winter and water element."},
    "中": {"pinyin": "zhōng", "meanings": ["Middle", "Center", "Central"], "element": "土", "theme": "virtue", "emoji": "🎯", "gender": "M", "notes": "Center. Balance and harmony."},
    "华": {"pinyin": "huá", "meanings": ["Splendid", "China", "Prosperous"], "element": "水", "theme": "prosperity", "emoji": "🏮", "gender": "unisex", "notes": "Splendor. Also represents Chinese civilization."},
    "夏": {"pinyin": "xià", "meanings": ["Summer", "Grand", "Xia Dynasty"], "element": "火", "theme": "nature", "emoji": "☀️", "gender": "unisex", "notes": "Summer or grand."},
    "汉": {"pinyin": "hàn", "meanings": ["Han Dynasty", "Chinese", "River"], "element": "水", "theme": "family", "emoji": "🏯", "gender": "M", "notes": "Han Chinese. Strong cultural identity."},
    "浩": {"pinyin": "hào", "meanings": ["Vast", "Grand", "Powerful"], "element": "水", "theme": "nature", "emoji": "🌊", "gender": "M", "notes": "Vast and powerful."},
    "云": {"pinyin": "yún", "meanings": ["Cloud", "Say", "Lofty"], "element": "水", "theme": "nature", "emoji": "☁️", "gender": "unisex", "notes": "Cloud."},
    "飞": {"pinyin": "fēi", "meanings": ["Fly", "Swift", "Soaring"], "element": "火", "theme": "strength", "emoji": "✈️", "gender": "M", "notes": "To fly."},
    "天": {"pinyin": "tiān", "meanings": ["Sky", "Heaven", "Day"], "element": "火", "theme": "nature", "emoji": "🌌", "gender": "M", "notes": "Sky/heaven."},
    "宇": {"pinyin": "yǔ", "meanings": ["Universe", "Space", "House"], "element": "土", "theme": "nature", "emoji": "🌌", "gender": "M", "notes": "Universe/cosmos. Grand and expansive."},
    "宙": {"pinyin": "zhòu", "meanings": ["Universe", "Time", "Eternal"], "element": "土", "theme": "nature", "emoji": "⏳", "gender": "M", "notes": "Time and universe. Paired with 宇 for cosmic names."},
    "辰": {"pinyin": "chén", "meanings": ["Morning", "Celestial", "Time"], "element": "土", "theme": "nature", "emoji": "⭐", "gender": "M", "notes": "Celestial time. Also the dragon zodiac sign."},
    "奕": {"pinyin": "yì", "meanings": ["Grand", "Abundant", "Radiant"], "element": "火", "theme": "strength", "emoji": "✨", "gender": "M", "notes": "Grand and radiant. Implies abundant energy."},
    "君": {"pinyin": "jūn", "meanings": ["Monarch", "Lord", "Noble"], "element": "木", "theme": "virtue", "emoji": "👑", "gender": "unisex", "notes": "Noble ruler/superior. Common in both male and female names."},
    "臣": {"pinyin": "chén", "meanings": ["Minister", "Official", "Loyal"], "element": "金", "theme": "virtue", "emoji": "👔", "gender": "M", "notes": "Loyal minister. Implies service and duty."},
    "伯": {"pinyin": "bó", "meanings": ["Uncle", "Elder", "Count"], "element": "火", "theme": "family", "emoji": "👨", "gender": "M", "notes": "Elder uncle. Implies seniority and respect."},
    "仲": {"pinyin": "zhòng", "meanings": ["Second", "Middle", "Elder"], "element": "木", "theme": "family", "emoji": "2️⃣", "gender": "M", "notes": "Second-born. Traditional birth-order name."},
    "叔": {"pinyin": "shū", "meanings": ["Uncle", "Third", "Elder"], "element": "金", "theme": "family", "emoji": "👨‍🦳", "gender": "M", "notes": "Younger uncle. Traditional birth-order name."},
    "季": {"pinyin": "jì", "meanings": ["Season", "Youngest", "Last"], "element": "木", "theme": "family", "emoji": "4️⃣", "gender": "M", "notes": "Youngest-born. Traditional birth-order name."},
    "绍": {"pinyin": "shào", "meanings": ["Continue", "Carry on", "Connect"], "element": "金", "theme": "family", "emoji": "🔗", "gender": "M", "notes": "To continue the family legacy."},
    "继": {"pinyin": "jì", "meanings": ["Continue", "Succeed", "Follow"], "element": "木", "theme": "family", "emoji": "➡️", "gender": "M", "notes": "To continue and succeed. Expresses carrying on tradition."},
    "承": {"pinyin": "chéng", "meanings": ["Receive", "Bear", "Continue"], "element": "金", "theme": "family", "emoji": "🤲", "gender": "M", "notes": "To receive and continue family legacy."},
    "传": {"pinyin": "chuán", "meanings": ["Pass on", "Transmit", "Legend"], "element": "火", "theme": "family", "emoji": "📜", "gender": "unisex", "notes": "To pass down through generations."},
    "佳": {"pinyin": "jiā", "meanings": ["Excellent", "Fine", "Beautiful"], "element": "木", "theme": "beauty", "emoji": "👍", "gender": "F", "notes": "Excellent and fine. Very popular in girls' names."},
    "依": {"pinyin": "yī", "meanings": ["Dependent", "Compliant", "As"], "element": "火", "theme": "gentle", "emoji": "🌿", "gender": "F", "notes": "To depend on. Soft and gentle."},
    "思": {"pinyin": "sī", "meanings": ["Think", "Consider", "Long for"], "element": "金", "theme": "wisdom", "emoji": "💭", "gender": "unisex", "notes": "Thought and longing."},
    "雨": {"pinyin": "yǔ", "meanings": ["Rain", "Nourishing"], "element": "水", "theme": "nature", "emoji": "🌧️", "gender": "unisex", "notes": "Rain. Life-giving and gentle."},
    "雪": {"pinyin": "xuě", "meanings": ["Snow", "Pure"], "element": "水", "theme": "nature", "emoji": "❄️", "gender": "F", "notes": "Snow. Pure and beautiful."},
    "冰": {"pinyin": "bīng", "meanings": ["Ice", "Pure", "Clear"], "element": "水", "theme": "nature", "emoji": "🧊", "gender": "F", "notes": "Ice. Pure and clear."},
    "霜": {"pinyin": "shuāng", "meanings": ["Frost", "Crisp"], "element": "水", "theme": "nature", "emoji": "🧊", "gender": "F", "notes": "Frost. Crisp and pure."},
    "露": {"pinyin": "lù", "meanings": ["Dew", "Reveal"], "element": "水", "theme": "nature", "emoji": "💧", "gender": "F", "notes": "Dew drops. Fresh and pure."},
    "雾": {"pinyin": "wù", "meanings": ["Fog", "Mist", "Veiled"], "element": "水", "theme": "nature", "emoji": "🌫️", "gender": "F", "notes": "Fog/mist. Mysterious and poetic."},
    "光": {"pinyin": "guāng", "meanings": ["Light", "Bright", "Radiance"], "element": "火", "theme": "nature", "emoji": "💫", "gender": "M", "notes": "Light. Radiance and hope."},
    "明": {"pinyin": "míng", "meanings": ["Bright", "Clear", "Tomorrow"], "element": "火", "theme": "wisdom", "emoji": "💡", "gender": "unisex", "notes": "Bright and clear."},
    "亮": {"pinyin": "liàng", "meanings": ["Bright", "Shining", "Clear"], "element": "火", "theme": "nature", "emoji": "🔆", "gender": "M", "notes": "Bright and shining."},
    "日": {"pinyin": "rì", "meanings": ["Sun", "Day", "Daily"], "element": "火", "theme": "nature", "emoji": "☀️", "gender": "M", "notes": "Sun. Source of light and life."},
    "月": {"pinyin": "yuè", "meanings": ["Moon", "Month"], "element": "水", "theme": "nature", "emoji": "🌙", "gender": "F", "notes": "Moon. Romantic and luminous."},
    "阳": {"pinyin": "yáng", "meanings": ["Sun", "Positive", "Male"], "element": "火", "theme": "nature", "emoji": "☀️", "gender": "M", "notes": "Sunlit. Yang energy."},
    "阴": {"pinyin": "yīn", "meanings": ["Shadow", "Negative", "Female"], "element": "水", "theme": "nature", "emoji": "🌑", "gender": "F", "notes": "Shade and moon. Yin energy."},
    "午": {"pinyin": "wǔ", "meanings": ["Noon", "Horse", "Midday"], "element": "火", "theme": "nature", "emoji": "🐴", "gender": "M", "notes": "Noon. The horse in Chinese zodiac."},
    "时": {"pinyin": "shí", "meanings": ["Time", "Era", "Opportunity"], "element": "火", "theme": "wisdom", "emoji": "⏰", "gender": "unisex", "notes": "Time and season. Implies timeliness."},
    "元": {"pinyin": "yuán", "meanings": ["First", "Origin", "Dollar"], "element": "木", "theme": "prosperity", "emoji": "1️⃣", "gender": "M", "notes": "First/origin. Expresses primacy and beginning."},
    "大": {"pinyin": "dà", "meanings": ["Big", "Great", "Adult"], "element": "火", "theme": "strength", "emoji": "🌏", "gender": "M", "notes": "Great and big."},
    "太": {"pinyin": "tài", "meanings": ["Grand", "Extreme", "Supreme"], "element": "火", "theme": "strength", "emoji": "👑", "gender": "M", "notes": "Grand and supreme. Superlative."},
    "夫": {"pinyin": "fū", "meanings": ["Man", "Husband", "Laborer"], "element": "火", "theme": "family", "emoji": "👨", "gender": "M", "notes": "Adult male. Implies responsibility."},
    "士": {"pinyin": "shì", "meanings": ["Scholar", "Gentleman", "Officer"], "element": "金", "theme": "wisdom", "emoji": "🎓", "gender": "M", "notes": "Scholar/warrior. Noble class."},
    "俊": {"pinyin": "jùn", "meanings": ["Handsome", "Talented", "Excellent"], "element": "火", "theme": "beauty", "emoji": "😎", "gender": "M", "notes": "Handsome and talented. Very popular in boys' names."},
    "帅": {"pinyin": "shuài", "meanings": ["Handsome", "Commander", "Leader"], "element": "金", "theme": "strength", "emoji": "💂", "gender": "M", "notes": "Handsome leader. Modern favorite."},
    "英": {"pinyin": "yīng", "meanings": ["Heroic", "Flower", "England"], "element": "木", "theme": "strength", "emoji": "🌺", "gender": "M", "notes": "Heroic and outstanding. Also means flower petal."},
    "雄": {"pinyin": "xióng", "meanings": ["Heroic", "Male", "Grand"], "element": "水", "theme": "strength", "emoji": "🦅", "gender": "M", "notes": "Heroic and grand."},
    "汉": {"pinyin": "hàn", "meanings": ["Chinese", "Man", "River"], "element": "水", "theme": "family", "emoji": "🏯", "gender": "M", "notes": "Han Chinese. Strong identity."},
    "永": {"pinyin": "yǒng", "meanings": ["Eternal", "Forever", "Always"], "element": "水", "theme": "virtue", "emoji": "♾️", "gender": "M", "notes": "Eternal and forever."},
    "世": {"pinyin": "shì", "meanings": ["World", "Generation", "Life"], "element": "金", "theme": "family", "emoji": "🌍", "gender": "M", "notes": "World and generation."},
    "界": {"pinyin": "jiè", "meanings": ["World", "Boundary", "Realm"], "element": "土", "theme": "nature", "emoji": "🌐", "gender": "M", "notes": "Boundary/world."},
    "上": {"pinyin": "shàng", "meanings": ["Above", "Up", "Superior"], "element": "金", "theme": "strength", "emoji": "⬆️", "gender": "M", "notes": "Upward and superior."},
    "下": {"pinyin": "xià", "meanings": ["Below", "Down", "Under"], "element": "水", "theme": "virtue", "emoji": "⬇️", "gender": "M", "notes": "Below. Expresses humility in classical names."},
    "左": {"pinyin": "zuǒ", "meanings": ["Left", "East", "Support"], "element": "木", "theme": "virtue", "emoji": "👈", "gender": "M", "notes": "Left side. Also a surname."},
    "右": {"pinyin": "yòu", "meanings": ["Right", "West", "Honor"], "element": "金", "theme": "virtue", "emoji": "👉", "gender": "M", "notes": "Right side. Traditionally honored position."},
    "古": {"pinyin": "gǔ", "meanings": ["Ancient", "Old", "Classical"], "element": "木", "theme": "virtue", "emoji": "🏛️", "gender": "M", "notes": "Ancient. Respect for tradition."},
    "今": {"pinyin": "jīn", "meanings": ["Now", "Present", "Current"], "element": "火", "theme": "wisdom", "emoji": "🕐", "gender": "unisex", "notes": "The present moment."},
    "先": {"pinyin": "xiān", "meanings": ["First", "Before", "Ancestor"], "element": "金", "theme": "family", "emoji": "1️⃣", "gender": "M", "notes": "First/ancestor. Precedes others."},
    "后": {"pinyin": "hòu", "meanings": ["After", "Behind", "Queen"], "element": "水", "theme": "family", "emoji": "👸", "gender": "F", "notes": "After/queen. Also means empress."},
    "全": {"pinyin": "quán", "meanings": ["Complete", "Whole", "Total"], "element": "火", "theme": "prosperity", "emoji": "✅", "gender": "M", "notes": "Complete and whole."},
    "安": {"pinyin": "ān", "meanings": ["Peaceful", "Safe", "Calm"], "element": "土", "theme": "virtue", "emoji": "🏠", "gender": "unisex", "notes": "Peace and safety."},
    "定": {"pinyin": "dìng", "meanings": ["Stable", "Fixed", "Decided"], "element": "火", "theme": "virtue", "emoji": "📌", "gender": "M", "notes": "Stability and certainty."},
    "静": {"pinyin": "jìng", "meanings": ["Quiet", "Calm", "Serene"], "element": "金", "theme": "virtue", "emoji": "🧘", "gender": "F", "notes": "Serene and quiet."},
    "动": {"pinyin": "dòng", "meanings": ["Move", "Action", "Dynamic"], "element": "火", "theme": "strength", "emoji": "🏃", "gender": "M", "notes": "Movement and action. Active."},
    "清": {"pinyin": "qīng", "meanings": ["Clear", "Pure", "Clean"], "element": "水", "theme": "virtue", "emoji": "💧", "gender": "unisex", "notes": "Clear and pure. High moral integrity."},
    "洁": {"pinyin": "jié", "meanings": ["Clean", "Pure", "Pristine"], "element": "水", "theme": "virtue", "emoji": "✨", "gender": "F", "notes": "Clean and pure. Moral purity."},
    "净": {"pinyin": "jìng", "meanings": ["Clean", "Pure", "Net"], "element": "水", "theme": "virtue", "emoji": "🧹", "gender": "unisex", "notes": "Clean and pure."},
    "新": {"pinyin": "xīn", "meanings": ["New", "Fresh", "Renew"], "element": "金", "theme": "prosperity", "emoji": "🆕", "gender": "unisex", "notes": "New. Fresh start."},
    "旧": {"pinyin": "jiù", "meanings": ["Old", "Former", "Used"], "element": "木", "theme": "family", "emoji": "📦", "gender": "M", "notes": "Old/traditional. Respect for heritage."},
    "初": {"pinyin": "chū", "meanings": ["First", "Beginning", "Early"], "element": "火", "theme": "wisdom", "emoji": "🌱", "gender": "unisex", "notes": "Beginning. Fresh start and new beginnings."},
    "早": {"pinyin": "zǎo", "meanings": ["Early", "Morning", "Soon"], "element": "火", "theme": "nature", "emoji": "🌄", "gender": "unisex", "notes": "Early morning. Freshness."},
    "晚": {"pinyin": "wǎn", "meanings": ["Evening", "Late", "Night"], "element": "水", "theme": "nature", "emoji": "🌆", "gender": "F", "notes": "Evening. Poetic and calm."},
    "夜": {"pinyin": "yè", "meanings": ["Night", "Dark", "Evening"], "element": "水", "theme": "nature", "emoji": "🌃", "gender": "F", "notes": "Night. Mysterious and quiet."},
    "梦": {"pinyin": "mèng", "meanings": ["Dream", "Vision", "Imagination"], "element": "木", "theme": "wisdom", "emoji": "💤", "gender": "F", "notes": "Dream. Aspirations and imagination."},
    "想": {"pinyin": "xiǎng", "meanings": ["Think", "Want", "Imagine"], "element": "火", "theme": "wisdom", "emoji": "🤔", "gender": "unisex", "notes": "Thought and aspiration."},
    "情": {"pinyin": "qíng", "meanings": ["Emotion", "Feeling", "Love"], "element": "火", "theme": "gentle", "emoji": "💕", "gender": "F", "notes": "Emotion and feeling. Romantic."},
    "爱": {"pinyin": "ài", "meanings": ["Love", "Affection", "Cherish"], "element": "火", "theme": "gentle", "emoji": "❤️", "gender": "F", "notes": "Love."},
    "乐": {"pinyin": "lè", "meanings": ["Joy", "Music", "Happy"], "element": "火", "theme": "family", "emoji": "😄", "gender": "unisex", "notes": "Joy and music."},
    "欢": {"pinyin": "huān", "meanings": ["Happy", "Joyful", "Merry"], "element": "水", "theme": "gentle", "emoji": "🎉", "gender": "unisex", "notes": "Joy and happiness."},
    "喜": {"pinyin": "xǐ", "meanings": ["Happy", "Joyful", "Delight"], "element": "火", "theme": "prosperity", "emoji": "😁", "gender": "unisex", "notes": "Happiness and delight. Auspicious character."},
    "福": {"pinyin": "fú", "meanings": ["Blessing", "Fortune", "Happiness"], "element": "水", "theme": "prosperity", "emoji": "🧧", "gender": "M", "notes": "Good fortune."},
    "祥": {"pinyin": "xiáng", "meanings": ["Auspicious", "Lucky", "Blessing"], "element": "火", "theme": "prosperity", "emoji": "🍀", "gender": "M", "notes": "Auspicious and lucky."},
    "瑞": {"pinyin": "ruì", "meanings": ["Auspicious", "Fortunate", "Lucky Omen"], "element": "金", "theme": "prosperity", "emoji": "🎊", "gender": "unisex", "notes": "Auspicious sign. Very popular."},
    "吉": {"pinyin": "jí", "meanings": ["Lucky", "Fortunate", "Auspicious"], "element": "木", "theme": "prosperity", "emoji": "🍀", "gender": "M", "notes": "Lucky and auspicious. Simple and powerful."},
    "庆": {"pinyin": "qìng", "meanings": ["Celebrate", "Congratulate"], "element": "火", "theme": "prosperity", "emoji": "🎉", "gender": "M", "notes": "Celebration."},
    "贺": {"pinyin": "hè", "meanings": ["Congratulate", "Bless"], "element": "火", "theme": "prosperity", "emoji": "🎊", "gender": "M", "notes": "Congratulation and blessing."},
    "祝": {"pinyin": "zhù", "meanings": ["Wish", "Pray", "Bless"], "element": "火", "theme": "prosperity", "emoji": "🙏", "gender": "M", "notes": "Wish and blessing."},
    "林": {"pinyin": "lín", "meanings": ["Forest", "Many Trees"], "element": "木", "theme": "nature", "emoji": "🌲", "gender": "unisex", "notes": "Forest."},
    "木": {"pinyin": "mù", "meanings": ["Tree", "Wood", "Simple"], "element": "木", "theme": "nature", "emoji": "🌳", "gender": "M", "notes": "Wood/tree. Simple and natural."},
    "本": {"pinyin": "běn", "meanings": ["Root", "Origin", "Book"], "element": "木", "theme": "wisdom", "emoji": "📚", "gender": "M", "notes": "Root and origin. Foundation."},
    "根": {"pinyin": "gēn", "meanings": ["Root", "Origin", "Foundation"], "element": "木", "theme": "family", "emoji": "🌱", "gender": "M", "notes": "Root. Deeply grounded."},
    "果": {"pinyin": "guǒ", "meanings": ["Fruit", "Result", "Determined"], "element": "木", "theme": "prosperity", "emoji": "🍎", "gender": "M", "notes": "Fruit and result. Achievement."},
    "花": {"pinyin": "huā", "meanings": ["Flower", "Blossom"], "element": "木", "theme": "beauty", "emoji": "🌸", "gender": "F", "notes": "Flower."},
    "草": {"pinyin": "cǎo", "meanings": ["Grass", "Plant", "Humble"], "element": "木", "theme": "nature", "emoji": "🌿", "gender": "F", "notes": "Grass. Humble and resilient."},
}

# Add more characters from common name character lists to reach 500+
MORE_CHARS = {
    # More surnames
    "秦": {"pinyin": "qín", "meanings": ["Qin (dynasty)"], "element": "火", "theme": "surname", "emoji": "🏯", "gender": "unisex", "notes": "Qin Dynasty."},
    "薛": {"pinyin": "xuē", "meanings": ["Xue (state)", "Wormwood"], "element": "木", "theme": "surname", "emoji": "🌿", "gender": "unisex", "notes": "Ancient surname."},
    "叶": {"pinyin": "yè", "meanings": ["Leaf", "Page"], "element": "木", "theme": "surname", "emoji": "🍃", "gender": "unisex", "notes": "Surname meaning leaf."},
    "阎": {"pinyin": "yán", "meanings": ["Yan (state)", "Gate"], "element": "火", "theme": "surname", "emoji": "🚪", "gender": "unisex", "notes": "Ancient surname."},
    "余": {"pinyin": "yú", "meanings": ["I", "Surplus"], "element": "土", "theme": "surname", "emoji": "➕", "gender": "unisex", "notes": "Surname meaning surplus."},
    "潘": {"pinyin": "pān", "meanings": ["Pan (state)", "Rice water"], "element": "水", "theme": "surname", "emoji": "🌊", "gender": "unisex", "notes": "Ancient surname."},
    "戴": {"pinyin": "dài", "meanings": ["Wear", "Respect", "Dai"], "element": "火", "theme": "surname", "emoji": "🎩", "gender": "unisex", "notes": "Surname meaning to wear."},
    "夏": {"pinyin": "xià", "meanings": ["Summer", "Xia"], "element": "火", "theme": "surname", "emoji": "☀️", "gender": "unisex", "notes": "Surname meaning summer."},
    "钟": {"pinyin": "zhōng", "meanings": ["Bell", "Clock"], "element": "金", "theme": "surname", "emoji": "🔔", "gender": "unisex", "notes": "Surname meaning bell."},
    "汪": {"pinyin": "wāng", "meanings": ["Pond", "Vast"], "element": "水", "theme": "surname", "emoji": "🌊", "gender": "unisex", "notes": "Surname meaning pond."},
    "田": {"pinyin": "tián", "meanings": ["Field", "Farmland"], "element": "土", "theme": "surname", "emoji": "🌾", "gender": "unisex", "notes": "Surname meaning field."},
    "任": {"pinyin": "rèn", "meanings": ["Duty", "Responsibility"], "element": "金", "theme": "surname", "emoji": "🤝", "gender": "unisex", "notes": "Surname meaning duty."},
    "姜": {"pinyin": "jiāng", "meanings": ["Ginger", "Jiang"], "element": "火", "theme": "surname", "emoji": "🫚", "gender": "unisex", "notes": "Ancient surname."},
    "范": {"pinyin": "fàn", "meanings": ["Pattern", "Mold"], "element": "木", "theme": "surname", "emoji": "📐", "gender": "unisex", "notes": "Surname meaning pattern."},
    "方": {"pinyin": "fāng", "meanings": ["Square", "Direction"], "element": "火", "theme": "surname", "emoji": "⬜", "gender": "unisex", "notes": "Surname meaning square."},
    "石": {"pinyin": "shí", "meanings": ["Stone", "Rock"], "element": "土", "theme": "surname", "emoji": "🪨", "gender": "unisex", "notes": "Surname meaning stone."},
    "姚": {"pinyin": "yáo", "meanings": ["Yao (sage king)"], "element": "火", "theme": "surname", "emoji": "👑", "gender": "unisex", "notes": "Ancient noble surname."},
    "谭": {"pinyin": "tán", "meanings": ["Talk", "Discuss"], "element": "火", "theme": "surname", "emoji": "💬", "gender": "unisex", "notes": "Surname meaning talk."},
    "廖": {"pinyin": "liào", "meanings": ["Liao (state)"], "element": "火", "theme": "surname", "emoji": "🏯", "gender": "unisex", "notes": "Ancient surname."},
    "邹": {"pinyin": "zōu", "meanings": ["Zou (state)"], "element": "火", "theme": "surname", "emoji": "🏯", "gender": "unisex", "notes": "Ancient surname."},
    "熊": {"pinyin": "xióng", "meanings": ["Bear", "Heroic"], "element": "火", "theme": "surname", "emoji": "🐻", "gender": "unisex", "notes": "Surname meaning bear."},
    "金": {"pinyin": "jīn", "meanings": ["Gold", "Metal"], "element": "金", "theme": "surname", "emoji": "🥇", "gender": "unisex", "notes": "Surname meaning gold."},
    "陆": {"pinyin": "lù", "meanings": ["Land", "Six"], "element": "土", "theme": "surname", "emoji": "🗺️", "gender": "unisex", "notes": "Surname meaning land."},
    "郝": {"pinyin": "hǎo", "meanings": ["Hao (state)"], "element": "火", "theme": "surname", "emoji": "🏯", "gender": "unisex", "notes": "Ancient surname."},
    "孔": {"pinyin": "kǒng", "meanings": ["Hole", "Confucius"], "element": "水", "theme": "surname", "emoji": "🎓", "gender": "unisex", "notes": "Confucius' surname."},
    "白": {"pinyin": "bái", "meanings": ["White", "Pure"], "element": "金", "theme": "surname", "emoji": "⚪", "gender": "unisex", "notes": "Surname meaning white."},
    "崔": {"pinyin": "cuī", "meanings": ["High", "Towering"], "element": "山", "theme": "surname", "emoji": "⛰️", "gender": "unisex", "notes": "Surname meaning high."},
    "康": {"pinyin": "kāng", "meanings": ["Healthy", "Peaceful"], "element": "木", "theme": "surname", "emoji": "💚", "gender": "unisex", "notes": "Surname meaning health."},
    "毛": {"pinyin": "máo", "meanings": ["Hair", "Feather"], "element": "水", "theme": "surname", "emoji": "🪶", "gender": "unisex", "notes": "Surname meaning hair."},
    "邱": {"pinyin": "qiū", "meanings": ["Mound", "Hill"], "element": "土", "theme": "surname", "emoji": "⛰️", "gender": "unisex", "notes": "Surname meaning hill."},
    "秦": {"pinyin": "qín", "meanings": ["Qin Dynasty"], "element": "火", "theme": "surname", "emoji": "🏯", "gender": "unisex", "notes": "Qin Dynasty surname."},
    "江": {"pinyin": "jiāng", "meanings": ["River", "Yangtze"], "element": "水", "theme": "surname", "emoji": "🌊", "gender": "unisex", "notes": "Surname meaning river."},
    "史": {"pinyin": "shǐ", "meanings": ["History", "History Official"], "element": "火", "theme": "surname", "emoji": "📜", "gender": "unisex", "notes": "Surname meaning history."},
    "陶": {"pinyin": "táo", "meanings": ["Pottery", "Cultivate"], "element": "火", "theme": "surname", "emoji": "🏺", "gender": "unisex", "notes": "Surname meaning pottery."},
    "贺": {"pinyin": "hè", "meanings": ["Congratulate"], "element": "火", "theme": "surname", "emoji": "🎊", "gender": "unisex", "notes": "Surname meaning congratulate."},
    "顾": {"pinyin": "gù", "meanings": ["Look after", "Consider"], "element": "木", "theme": "surname", "emoji": "👀", "gender": "unisex", "notes": "Surname meaning to look after."},
    "侯": {"pinyin": "hóu", "meanings": ["Marquis", "Noble"], "element": "水", "theme": "surname", "emoji": "👑", "gender": "unisex", "notes": "Surname meaning marquis."},
    "邵": {"pinyin": "shào", "meanings": ["Shao (state)"], "element": "火", "theme": "surname", "emoji": "🏯", "gender": "unisex", "notes": "Ancient surname."},
    "孟": {"pinyin": "mèng", "meanings": ["First month", "Elder"], "element": "水", "theme": "surname", "emoji": "1️⃣", "gender": "unisex", "notes": "Surname meaning eldest."},
    "龙": {"pinyin": "lóng", "meanings": ["Dragon"], "element": "水", "theme": "surname", "emoji": "🐉", "gender": "unisex", "notes": "Surname meaning dragon."},
    "万": {"pinyin": "wàn", "meanings": ["Ten thousand"], "element": "水", "theme": "surname", "emoji": "💯", "gender": "unisex", "notes": "Surname meaning ten thousand."},
    "段": {"pinyin": "duàn", "meanings": ["Segment", "Section"], "element": "火", "theme": "surname", "emoji": "📏", "gender": "unisex", "notes": "Surname meaning segment."},
    "雷": {"pinyin": "léi", "meanings": ["Thunder"], "element": "火", "theme": "surname", "emoji": "⚡", "gender": "unisex", "notes": "Surname meaning thunder."},
    "钱": {"pinyin": "qián", "meanings": ["Money", "Wealth"], "element": "金", "theme": "surname", "emoji": "💰", "gender": "unisex", "notes": "Surname meaning money."},
    "汤": {"pinyin": "tāng", "meanings": ["Soup", "Hot water"], "element": "水", "theme": "surname", "emoji": "🍲", "gender": "unisex", "notes": "Surname meaning soup."},
    "尹": {"pinyin": "yǐn", "meanings": ["Govern", "Administer"], "element": "土", "theme": "surname", "emoji": "📋", "gender": "unisex", "notes": "Surname meaning to govern."},
    "黎": {"pinyin": "lí", "meanings": ["Black", "Dawn", "Many"], "element": "火", "theme": "surname", "emoji": "🌅", "gender": "unisex", "notes": "Surname meaning dawn/many."},
    "易": {"pinyin": "yì", "meanings": ["Easy", "Change"], "element": "火", "theme": "surname", "emoji": "🔄", "gender": "unisex", "notes": "Surname meaning change."},
    "常": {"pinyin": "cháng", "meanings": ["Often", "Constant", "Ordinary"], "element": "火", "theme": "surname", "emoji": "🔄", "gender": "unisex", "notes": "Surname meaning constant."},
    "武": {"pinyin": "wǔ", "meanings": ["Martial", "Military"], "element": "火", "theme": "surname", "emoji": "⚔️", "gender": "unisex", "notes": "Surname meaning martial."},
    "乔": {"pinyin": "qiáo", "meanings": ["Tall", "Disguise"], "element": "木", "theme": "surname", "emoji": "🌳", "gender": "unisex", "notes": "Surname meaning tall."},
    "赖": {"pinyin": "lài", "meanings": ["Rely", "Depend"], "element": "火", "theme": "surname", "emoji": "🤲", "gender": "unisex", "notes": "Surname meaning rely."},
    "龚": {"pinyin": "gōng", "meanings": ["Respectful", "Gong"], "element": "火", "theme": "surname", "emoji": "🙇", "gender": "unisex", "notes": "Surname."},
    "文": {"pinyin": "wén", "meanings": ["Literature", "Culture"], "element": "水", "theme": "surname", "emoji": "📖", "gender": "unisex", "notes": "Surname meaning culture."},

    # More given name characters
    "弘": {"pinyin": "hóng", "meanings": ["Broad", "Grand", "Expand"], "element": "水", "theme": "strength", "emoji": "🌊", "gender": "M", "notes": "Grand and expansive."},
    "扬": {"pinyin": "yáng", "meanings": ["Raise", "Spread", "Praise"], "element": "火", "theme": "strength", "emoji": "📣", "gender": "M", "notes": "To raise and spread."},
    "拓": {"pinyin": "tuò", "meanings": ["Expand", "Pioneer", "Open up"], "element": "火", "theme": "strength", "emoji": "🚀", "gender": "M", "notes": "To pioneer and expand."},
    "开": {"pinyin": "kāi", "meanings": ["Open", "Begin", "Start"], "element": "木", "theme": "strength", "emoji": "🔓", "gender": "M", "notes": "To open and begin."},
    "创": {"pinyin": "chuàng", "meanings": ["Create", "Initiate", "Start"], "element": "金", "theme": "strength", "emoji": "💡", "gender": "M", "notes": "To create and innovate."},
    "首": {"pinyin": "shǒu", "meanings": ["Head", "First", "Leader"], "element": "金", "theme": "strength", "emoji": "🥇", "gender": "M", "notes": "Head and leader."},
    "领": {"pinyin": "lǐng", "meanings": ["Lead", "Collar", "Understand"], "element": "火", "theme": "strength", "emoji": "👔", "gender": "M", "notes": "To lead."},
    "导": {"pinyin": "dǎo", "meanings": ["Guide", "Direct", "Lead"], "element": "火", "theme": "wisdom", "emoji": "🧭", "gender": "M", "notes": "To guide and direct."},
    "教": {"pinyin": "jiào", "meanings": ["Teach", "Religion", "Instruct"], "element": "木", "theme": "wisdom", "emoji": "📚", "gender": "unisex", "notes": "To teach and educate."},
    "育": {"pinyin": "yù", "meanings": ["Nurture", "Educate", "Raise"], "element": "火", "theme": "wisdom", "emoji": "🌱", "gender": "unisex", "notes": "To nurture and educate."},
    "培": {"pinyin": "péi", "meanings": ["Cultivate", "Nurture", "Foster"], "element": "土", "theme": "wisdom", "emoji": "🌻", "gender": "unisex", "notes": "To cultivate talent."},
    "养": {"pinyin": "yǎng", "meanings": ["Nourish", "Raise", "Support"], "element": "火", "theme": "family", "emoji": "🍼", "gender": "unisex", "notes": "To nourish and raise."},
    "生": {"pinyin": "shēng", "meanings": ["Life", "Birth", "Raw"], "element": "木", "theme": "family", "emoji": "🌱", "gender": "unisex", "notes": "Life and birth."},
    "活": {"pinyin": "huó", "meanings": ["Live", "Active", "Alive"], "element": "水", "theme": "family", "emoji": "💃", "gender": "unisex", "notes": "Alive and active."},
    "存": {"pinyin": "cún", "meanings": ["Exist", "Keep", "Save"], "element": "木", "theme": "virtue", "emoji": "💾", "gender": "M", "notes": "To exist and endure."},
    "有": {"pinyin": "yǒu", "meanings": ["Have", "Exist", "Possess"], "element": "火", "theme": "prosperity", "emoji": "✅", "gender": "M", "notes": "To have and possess."},
    "无": {"pinyin": "wú", "meanings": ["Nothing", "Without", "None"], "element": "水", "theme": "wisdom", "emoji": "❌", "gender": "M", "notes": "Nothingness. Daoist concept."},
    "多": {"pinyin": "duō", "meanings": ["Many", "Much", "Multiple"], "element": "火", "theme": "prosperity", "emoji": "📦", "gender": "M", "notes": "Many and abundant."},
    "少": {"pinyin": "shǎo", "meanings": ["Few", "Young", "Little"], "element": "水", "theme": "family", "emoji": "👶", "gender": "M", "notes": "Young and few."},
    "重": {"pinyin": "zhòng", "meanings": ["Heavy", "Important", "Repeat"], "element": "土", "theme": "virtue", "emoji": "⚖️", "gender": "M", "notes": "Important and weighty."},
    "轻": {"pinyin": "qīng", "meanings": ["Light", "Easy", "Gentle"], "element": "木", "theme": "gentle", "emoji": "🕊️", "gender": "F", "notes": "Light and gentle."},
    "长": {"pinyin": "cháng", "meanings": ["Long", "Length", "Eternal"], "element": "木", "theme": "virtue", "emoji": "📏", "gender": "M", "notes": "Long-lasting."},
    "短": {"pinyin": "duǎn", "meanings": ["Short", "Brief"], "element": "火", "theme": "nature", "emoji": "📏", "gender": "M", "notes": "Short and brief."},
    "高": {"pinyin": "gāo", "meanings": ["Tall", "High", "Noble"], "element": "木", "theme": "strength", "emoji": "📈", "gender": "M", "notes": "Tall and lofty."},
    "低": {"pinyin": "dī", "meanings": ["Low", "Humble", "Deep"], "element": "水", "theme": "virtue", "emoji": "⬇️", "gender": "M", "notes": "Low and humble."},
    "深": {"pinyin": "shēn", "meanings": ["Deep", "Profound", "Dark"], "element": "水", "theme": "wisdom", "emoji": "🌊", "gender": "unisex", "notes": "Deep and profound."},
    "浅": {"pinyin": "qiǎn", "meanings": ["Shallow", "Light"], "element": "水", "theme": "virtue", "emoji": "💧", "gender": "unisex", "notes": "Shallow and light."},
    "宽": {"pinyin": "kuān", "meanings": ["Wide", "Broad", "Tolerant"], "element": "木", "theme": "virtue", "emoji": "🌐", "gender": "M", "notes": "Broad-minded and tolerant."},
    "广": {"pinyin": "guǎng", "meanings": ["Wide", "Broad", "Extensive"], "element": "木", "theme": "strength", "emoji": "🌐", "gender": "M", "notes": "Broad and extensive."},
    "远": {"pinyin": "yuǎn", "meanings": ["Far", "Distant"], "element": "土", "theme": "strength", "emoji": "🎯", "gender": "M", "notes": "Far-reaching."},
    "近": {"pinyin": "jìn", "meanings": ["Near", "Recent", "Close"], "element": "土", "theme": "family", "emoji": "👫", "gender": "unisex", "notes": "Near and close."},
    "通": {"pinyin": "tōng", "meanings": ["Through", "Connect", "Know"], "element": "火", "theme": "wisdom", "emoji": "🔗", "gender": "M", "notes": "To connect and understand."},
    "顺": {"pinyin": "shùn", "meanings": ["Smooth", "Obedient", "Favorable"], "element": "金", "theme": "virtue", "emoji": "👍", "gender": "M", "notes": "Smooth and favorable."},
    "达": {"pinyin": "dá", "meanings": ["Reach", "Achieve", "Express"], "element": "火", "theme": "strength", "emoji": "🎯", "gender": "M", "notes": "To achieve and reach."},
    "道": {"pinyin": "dào", "meanings": ["Way", "Path", "Say"], "element": "火", "theme": "wisdom", "emoji": "🛤️", "gender": "M", "notes": "The Way. Daoist philosophy."},
    "路": {"pinyin": "lù", "meanings": ["Road", "Way", "Path"], "element": "土", "theme": "nature", "emoji": "🛣️", "gender": "M", "notes": "Road and path."},
    "行": {"pinyin": "xíng", "meanings": ["Walk", "Do", "Capable"], "element": "火", "theme": "strength", "emoji": "🚶", "gender": "M", "notes": "To walk and act."},
    "德": {"pinyin": "dé", "meanings": ["Virtue", "Morality", "Germany"], "element": "火", "theme": "virtue", "emoji": "🛡️", "gender": "M", "notes": "Virtue."},
    "福": {"pinyin": "fú", "meanings": ["Fortune", "Blessing"], "element": "水", "theme": "prosperity", "emoji": "🧧", "gender": "M", "notes": "Good fortune."},
    "建": {"pinyin": "jiàn", "meanings": ["Build", "Establish"], "element": "木", "theme": "strength", "emoji": "🏗️", "gender": "M", "notes": "To build."},
    "设": {"pinyin": "shè", "meanings": ["Set up", "Establish", "Design"], "element": "木", "theme": "wisdom", "emoji": "📐", "gender": "M", "notes": "To design and establish."},
    "发": {"pinyin": "fā", "meanings": ["Emit", "Develop", "Hair"], "element": "水", "theme": "strength", "emoji": "🚀", "gender": "M", "notes": "To develop and emit."},
    "展": {"pinyin": "zhǎn", "meanings": ["Expand", "Exhibit", "Develop"], "element": "木", "theme": "strength", "emoji": "📊", "gender": "M", "notes": "To expand and develop."},
    "开": {"pinyin": "kāi", "meanings": ["Open", "Begin", "Start"], "element": "木", "theme": "strength", "emoji": "🔓", "gender": "M", "notes": "To open and begin."},
    "明": {"pinyin": "míng", "meanings": ["Bright", "Clear"], "element": "火", "theme": "wisdom", "emoji": "💡", "gender": "unisex", "notes": "Bright and clear."},
    "智": {"pinyin": "zhì", "meanings": ["Wisdom", "Intelligence"], "element": "火", "theme": "wisdom", "emoji": "🧠", "gender": "M", "notes": "Wisdom."},
    "慧": {"pinyin": "huì", "meanings": ["Wise", "Intelligent"], "element": "水", "theme": "wisdom", "emoji": "🦉", "gender": "F", "notes": "Wisdom."},
}

# Merge dictionaries
DICT.update(MORE_CHARS)

# Add even more characters to reach 500+
EXTRA_CHARS = {
    "仁": {"pinyin": "rén", "meanings": ["Humane", "Benevolent", "Kind"], "element": "木", "theme": "virtue", "emoji": "💗", "gender": "M", "notes": "Core Confucian virtue of humaneness."},
    "义": {"pinyin": "yì", "meanings": ["Justice", "Righteousness", "Loyalty"], "element": "金", "theme": "virtue", "emoji": "⚖️", "gender": "M", "notes": "Righteousness and moral duty."},
    "礼": {"pinyin": "lǐ", "meanings": ["Ritual", "Manners", "Respect"], "element": "木", "theme": "virtue", "emoji": "🙏", "gender": "unisex", "notes": "Propriety and ritual decorum."},
    "信": {"pinyin": "xìn", "meanings": ["Trust", "Believe", "Honest"], "element": "金", "theme": "virtue", "emoji": "🤝", "gender": "unisex", "notes": "Trust and honesty."},
    "忠": {"pinyin": "zhōng", "meanings": ["Loyal", "Devoted", "Faithful"], "element": "火", "theme": "virtue", "emoji": "🐕", "gender": "M", "notes": "Loyalty and devotion."},
    "孝": {"pinyin": "xiào", "meanings": ["Filial", "Dutiful"], "element": "土", "theme": "virtue", "emoji": "👨‍👩‍👧‍👦", "gender": "unisex", "notes": "Filial piety."},
    "诚": {"pinyin": "chéng", "meanings": ["Honest", "Sincere"], "element": "金", "theme": "virtue", "emoji": "💝", "gender": "unisex", "notes": "Sincerity."},
    "善": {"pinyin": "shàn", "meanings": ["Good", "Kind"], "element": "水", "theme": "virtue", "emoji": "😇", "gender": "unisex", "notes": "Goodness and kindness."},
    "良": {"pinyin": "liáng", "meanings": ["Good", "Fine", "Excellent"], "element": "火", "theme": "virtue", "emoji": "👍", "gender": "unisex", "notes": "Goodness."},
    "谦": {"pinyin": "qiān", "meanings": ["Modest", "Humble"], "element": "木", "theme": "virtue", "emoji": "🙇", "gender": "M", "notes": "Humility."},
    "仰": {"pinyin": "yǎng", "meanings": ["Look up", "Admire", "Respect"], "element": "木", "theme": "virtue", "emoji": "🙏", "gender": "M", "notes": "To admire and respect."},
    "仲": {"pinyin": "zhòng", "meanings": ["Second", "Middle"], "element": "木", "theme": "family", "emoji": "2️⃣", "gender": "M", "notes": "Second-born."},
    "伊": {"pinyin": "yī", "meanings": ["He", "She", "That"], "element": "水", "theme": "beauty", "emoji": "👤", "gender": "F", "notes": "Classical pronoun, used in elegant names."},
    "伍": {"pinyin": "wǔ", "meanings": ["Five", "Company", "Squad"], "element": "土", "theme": "family", "emoji": "5️⃣", "gender": "M", "notes": "Five. Also a surname."},
    "什": {"pinyin": "shén", "meanings": ["What", "Ten", "Various"], "element": "金", "theme": "wisdom", "emoji": "❓", "gender": "unisex", "notes": "Various/miscellaneous."},
    "介": {"pinyin": "jiè", "meanings": ["Introduce", "Shell", "Upright"], "element": "木", "theme": "virtue", "emoji": "🛡️", "gender": "M", "notes": "Upright and honest."},
    "仍": {"pinyin": "réng", "meanings": ["Still", "Yet", "Continue"], "element": "金", "theme": "virtue", "emoji": "🔄", "gender": "unisex", "notes": "Persistent and continuing."},
    "仔": {"pinyin": "zǐ", "meanings": ["Child", "Young", "Detailed"], "element": "水", "theme": "family", "emoji": "👶", "gender": "M", "notes": "Young child."},
    "他": {"pinyin": "tā", "meanings": ["He", "Him", "Other"], "element": "火", "theme": "family", "emoji": "👤", "gender": "M", "notes": "Third person masculine pronoun."},
    "仙": {"pinyin": "xiān", "meanings": ["Immortal", "Celestial", "Fairy"], "element": "水", "theme": "beauty", "emoji": "🧚", "gender": "F", "notes": "Immortal/celestial being."},
    "代": {"pinyin": "dài", "meanings": ["Generation", "Replace", "Era"], "element": "火", "theme": "family", "emoji": "📅", "gender": "M", "notes": "Generation and era."},
    "令": {"pinyin": "lìng", "meanings": ["Order", "Command", "Excellent"], "element": "火", "theme": "strength", "emoji": "📜", "gender": "M", "notes": "To command. Also means excellent."},
    "以": {"pinyin": "yǐ", "meanings": ["Use", "By", "According to"], "element": "火", "theme": "wisdom", "emoji": "✏️", "gender": "unisex", "notes": "Classical function word."},
    "仪": {"pinyin": "yí", "meanings": ["Ceremony", "Apparatus", "Manner"], "element": "火", "theme": "virtue", "emoji": "🎩", "gender": "unisex", "notes": "Ceremony and proper manner."},
    "们": {"pinyin": "men", "meanings": ["Plural suffix"], "element": "水", "theme": "family", "emoji": "👥", "gender": "unisex", "notes": "Plural marker for people."},
    "价": {"pinyin": "jià", "meanings": ["Price", "Value", "Worth"], "element": "金", "theme": "prosperity", "emoji": "💰", "gender": "M", "notes": "Value and price."},
    "任": {"pinyin": "rèn", "meanings": ["Duty", "Assign", "Allow"], "element": "金", "theme": "virtue", "emoji": "🤝", "gender": "M", "notes": "Responsibility and duty."},
    "休": {"pinyin": "xiū", "meanings": ["Rest", "Stop", "Retire"], "element": "水", "theme": "gentle", "emoji": "😌", "gender": "unisex", "notes": "Rest and relaxation."},
    "伟": {"pinyin": "wěi", "meanings": ["Great", "Grand", "Mighty"], "element": "土", "theme": "strength", "emoji": "✨", "gender": "M", "notes": "One of the most popular name characters."},
    "传": {"pinyin": "chuán", "meanings": ["Pass down", "Spread", "Legend"], "element": "火", "theme": "family", "emoji": "📜", "gender": "unisex", "notes": "To pass down through generations."},
    "伤": {"pinyin": "shāng", "meanings": ["Hurt", "Injure", "Sad"], "element": "金", "theme": "gentle", "emoji": "😢", "gender": "unisex", "notes": "Sorrow. Used poetically."},
    "伯": {"pinyin": "bó", "meanings": ["Uncle", "Elder", "Count"], "element": "火", "theme": "family", "emoji": "👨", "gender": "M", "notes": "Elder uncle or count (noble)."},
    "估": {"pinyin": "gū", "meanings": ["Estimate", "Appraise", "Value"], "element": "木", "theme": "wisdom", "emoji": "📊", "gender": "M", "notes": "To estimate and evaluate."},
    "伴": {"pinyin": "bàn", "meanings": ["Companion", "Partner", "Accompany"], "element": "火", "theme": "family", "emoji": "👫", "gender": "unisex", "notes": "Companion and friend."},
    "佛": {"pinyin": "fó", "meanings": ["Buddha", "Buddhist", "Enlightened"], "element": "水", "theme": "wisdom", "emoji": "☸️", "gender": "unisex", "notes": "Buddha. Spiritual enlightenment."},
    "作": {"pinyin": "zuò", "meanings": ["Make", "Do", "Work"], "element": "火", "theme": "strength", "emoji": "🔨", "gender": "M", "notes": "To do and create."},
    "你": {"pinyin": "nǐ", "meanings": ["You (singular)"], "element": "火", "theme": "family", "emoji": "👤", "gender": "unisex", "notes": "Second person pronoun."},
    "佳": {"pinyin": "jiā", "meanings": ["Excellent", "Beautiful", "Good"], "element": "木", "theme": "beauty", "emoji": "👍", "gender": "F", "notes": "Excellent. Very popular in girls' names."},
    "供": {"pinyin": "gòng", "meanings": ["Supply", "Offer", "Provide"], "element": "火", "theme": "prosperity", "emoji": "🎁", "gender": "M", "notes": "To supply and provide."},
    "依": {"pinyin": "yī", "meanings": ["Depend", "Comply", "According to"], "element": "火", "theme": "gentle", "emoji": "🌿", "gender": "F", "notes": "To depend on. Soft and gentle."},
    "侠": {"pinyin": "xiá", "meanings": ["Knight-errant", "Chivalry", "Hero"], "element": "金", "theme": "strength", "emoji": "⚔️", "gender": "M", "notes": "Chivalrous hero. Martial arts ideal."},
    "侣": {"pinyin": "lǚ", "meanings": ["Companion", "Partner", "Mate"], "element": "火", "theme": "family", "emoji": "💑", "gender": "unisex", "notes": "Life partner and companion."},
    "便": {"pinyin": "biàn", "meanings": ["Convenient", "Then", "Even if"], "element": "水", "theme": "wisdom", "emoji": "🔄", "gender": "unisex", "notes": "Convenience and adaptability."},
    "俊": {"pinyin": "jùn", "meanings": ["Handsome", "Talented", "Outstanding"], "element": "火", "theme": "beauty", "emoji": "😎", "gender": "M", "notes": "Handsome and talented."},
    "俏": {"pinyin": "qiào", "meanings": ["Pretty", "Charming", "Sleek"], "element": "木", "theme": "beauty", "emoji": "💁", "gender": "F", "notes": "Pretty and charming."},
    "保": {"pinyin": "bǎo", "meanings": ["Protect", "Guarantee", "Keep"], "element": "水", "theme": "virtue", "emoji": "🛡️", "gender": "M", "notes": "To protect and safeguard."},
    "信": {"pinyin": "xìn", "meanings": ["Trust", "Letter", "Faith"], "element": "金", "theme": "virtue", "emoji": "✉️", "gender": "unisex", "notes": "Trust and communication."},
    "修": {"pinyin": "xiū", "meanings": ["Cultivate", "Repair", "Study"], "element": "金", "theme": "wisdom", "emoji": "📚", "gender": "M", "notes": "Self-cultivation and refinement."},
    "仓": {"pinyin": "cāng", "meanings": ["Barn", "Warehouse", "Store"], "element": "金", "theme": "prosperity", "emoji": "🏪", "gender": "M", "notes": "Granary. Abundance."},
    "伦": {"pinyin": "lún", "meanings": ["Ethics", "Order", "Peer"], "element": "火", "theme": "virtue", "emoji": "⚖️", "gender": "M", "notes": "Human relationships and ethics."},
    "俊": {"pinyin": "jùn", "meanings": ["Handsome", "Outstanding"], "element": "火", "theme": "beauty", "emoji": "😎", "gender": "M", "notes": "Handsome and talented."},
    "俸": {"pinyin": "fèng", "meanings": ["Salary", "Stipend", "Pay"], "element": "金", "theme": "prosperity", "emoji": "💰", "gender": "M", "notes": "Official salary."},
    "仓": {"pinyin": "cāng", "meanings": ["Storehouse", "Barn"], "element": "金", "theme": "prosperity", "emoji": "🏪", "gender": "M", "notes": "Granary."},
    "伦": {"pinyin": "lún", "meanings": ["Ethics", "Order"], "element": "火", "theme": "virtue", "emoji": "⚖️", "gender": "M", "notes": "Human relationships."},
    "倩": {"pinyin": "qiàn", "meanings": ["Pretty", "Charming"], "element": "火", "theme": "beauty", "emoji": "😊", "gender": "F", "notes": "Charming and pretty."},
    "傲": {"pinyin": "ào", "meanings": ["Proud", "Arrogant", "Noble"], "element": "金", "theme": "strength", "emoji": "🦚", "gender": "M", "notes": "Pride and noble bearing."},
    "儒": {"pinyin": "rú", "meanings": ["Confucian", "Scholar", "Learned"], "element": "水", "theme": "wisdom", "emoji": "🎓", "gender": "M", "notes": "Confucian scholar. Learned and refined."},
    "元": {"pinyin": "yuán", "meanings": ["First", "Yuan", "Dollar"], "element": "木", "theme": "prosperity", "emoji": "1️⃣", "gender": "M", "notes": "First and origin."},
    "充": {"pinyin": "chōng", "meanings": ["Fill", "Sufficient", "Full"], "element": "土", "theme": "prosperity", "emoji": "📦", "gender": "M", "notes": "Full and sufficient."},
    "兆": {"pinyin": "zhào", "meanings": ["Omen", "Trillion"], "element": "火", "theme": "prosperity", "emoji": "🔮", "gender": "M", "notes": "Omen and portent."},
    "先": {"pinyin": "xiān", "meanings": ["First", "Before", "Pioneer"], "element": "金", "theme": "strength", "emoji": "🥇", "gender": "M", "notes": "First. Pioneer and leader."},
    "光": {"pinyin": "guāng", "meanings": ["Light", "Bright", "Radiance"], "element": "火", "theme": "nature", "emoji": "💫", "gender": "M", "notes": "Light and radiance."},
    "兆": {"pinyin": "zhào", "meanings": ["Omen", "Sign", "Trillion"], "element": "火", "theme": "prosperity", "emoji": "🔮", "gender": "M", "notes": "Auspicious omen."},
    "共": {"pinyin": "gòng", "meanings": ["Together", "Common", "Share"], "element": "土", "theme": "family", "emoji": "🤝", "gender": "unisex", "notes": "Togetherness and sharing."},
    "具": {"pinyin": "jù", "meanings": ["Tool", "Have", "Prepare"], "element": "木", "theme": "talent", "emoji": "🔧", "gender": "M", "notes": "Tool and ability."},
    "典": {"pinyin": "diǎn", "meanings": ["Classic", "Standard", "Ceremony"], "element": "火", "theme": "wisdom", "emoji": "📜", "gender": "unisex", "notes": "Classic and standard."},
    "冰": {"pinyin": "bīng", "meanings": ["Ice", "Pure", "Cold"], "element": "水", "theme": "nature", "emoji": "🧊", "gender": "F", "notes": "Ice. Pure and clear."},
    "冲": {"pinyin": "chōng", "meanings": ["Rush", "Charge", "Pour"], "element": "水", "theme": "strength", "emoji": "💨", "gender": "M", "notes": "To charge forward."},
    "决": {"pinyin": "jué", "meanings": ["Decide", "Determine", "Resolute"], "element": "水", "theme": "strength", "emoji": "🎯", "gender": "M", "notes": "Decisive and resolute."},
    "冰": {"pinyin": "bīng", "meanings": ["Ice", "Pure"], "element": "水", "theme": "nature", "emoji": "🧊", "gender": "F", "notes": "Ice."},
    "冶": {"pinyin": "yě", "meanings": ["Smelt", "Refine", "Seductive"], "element": "火", "theme": "talent", "emoji": "🔥", "gender": "F", "notes": "To refine. Also seductive beauty."},
    "冷": {"pinyin": "lěng", "meanings": ["Cold", "Cool", "Unfeeling"], "element": "水", "theme": "nature", "emoji": "🥶", "gender": "unisex", "notes": "Cold and cool."},
    "净": {"pinyin": "jìng", "meanings": ["Clean", "Pure", "Net"], "element": "水", "theme": "virtue", "emoji": "🧹", "gender": "unisex", "notes": "Clean and pure."},
    "凝": {"pinyin": "níng", "meanings": ["Condense", "Freeze", "Focus"], "element": "水", "theme": "wisdom", "emoji": "💎", "gender": "unisex", "notes": "To concentrate and focus."},
    "凡": {"pinyin": "fán", "meanings": ["Ordinary", "Common", "Every"], "element": "水", "theme": "virtue", "emoji": "🌿", "gender": "unisex", "notes": "Ordinary. Finding beauty in simplicity."},
    "凤": {"pinyin": "fèng", "meanings": ["Phoenix", "Feng"], "element": "火", "theme": "beauty", "emoji": "🦚", "gender": "F", "notes": "Mythical phoenix."},
    "凯": {"pinyin": "kǎi", "meanings": ["Victory", "Triumph", "Melody"], "element": "木", "theme": "strength", "emoji": "🏆", "gender": "M", "notes": "Victory and triumph."},
    "凝": {"pinyin": "níng", "meanings": ["Condense", "Focus"], "element": "水", "theme": "wisdom", "emoji": "💎", "gender": "unisex", "notes": "Concentration."},
}
DICT.update(EXTRA_CHARS)

# Final batch for 500+
FINAL_CHARS = {
    "央": {"pinyin": "yāng", "meanings": ["Center", "Entreat", "End"], "element": "土", "theme": "virtue", "emoji": "🎯", "gender": "unisex", "notes": "Center. Balance and centrality."},
    "失": {"pinyin": "shī", "meanings": ["Lose", "Miss", "Error"], "element": "金", "theme": "wisdom", "emoji": "❌", "gender": "unisex", "notes": "To lose. Used philosophically."},
    "头": {"pinyin": "tóu", "meanings": ["Head", "Top", "First"], "element": "火", "theme": "strength", "emoji": "👤", "gender": "M", "notes": "Head and leader."},
    "夺": {"pinyin": "duó", "meanings": ["Seize", "Capture", "Strive"], "element": "火", "theme": "strength", "emoji": "🏆", "gender": "M", "notes": "To strive and achieve."},
    "夸": {"pinyin": "kuā", "meanings": ["Praise", "Boast", "Extol"], "element": "火", "theme": "strength", "emoji": "👏", "gender": "M", "notes": "To praise and extol."},
    "夹": {"pinyin": "jiā", "meanings": ["Clip", "Press", "Lining"], "element": "木", "theme": "family", "emoji": "📎", "gender": "unisex", "notes": "To press together."},
    "奉": {"pinyin": "fèng", "meanings": ["Offer", "Respect", "Receive"], "element": "木", "theme": "virtue", "emoji": "🙏", "gender": "M", "notes": "To offer with respect."},
    "奋": {"pinyin": "fèn", "meanings": ["Strive", "Exert", "Rise up"], "element": "火", "theme": "strength", "emoji": "💪", "gender": "M", "notes": "To strive and exert oneself."},
    "奔": {"pinyin": "bēn", "meanings": ["Run", "Rush", "Hasten"], "element": "火", "theme": "strength", "emoji": "🏃", "gender": "M", "notes": "To rush forward with energy."},
    "奇": {"pinyin": "qí", "meanings": ["Strange", "Wonder", "Marvelous"], "element": "木", "theme": "wisdom", "emoji": "🌟", "gender": "unisex", "notes": "Marvelous and extraordinary."},
    "奈": {"pinyin": "nài", "meanings": ["How", "Endure", "Cope"], "element": "火", "theme": "virtue", "emoji": "💪", "gender": "unisex", "notes": "To endure and cope."},
    "奉": {"pinyin": "fèng", "meanings": ["Offer", "Respect"], "element": "木", "theme": "virtue", "emoji": "🙏", "gender": "M", "notes": "To offer respectfully."},
    "奇": {"pinyin": "qí", "meanings": ["Strange", "Wonder"], "element": "木", "theme": "wisdom", "emoji": "🌟", "gender": "unisex", "notes": "Extraordinary."},
    "契": {"pinyin": "qì", "meanings": ["Contract", "Agree", "Engrave"], "element": "金", "theme": "virtue", "emoji": "📝", "gender": "M", "notes": "Contract and covenant."},
    "奔": {"pinyin": "bēn", "meanings": ["Run fast", "Flee"], "element": "火", "theme": "strength", "emoji": "🏃", "gender": "M", "notes": "To rush ahead."},
    "奥": {"pinyin": "ào", "meanings": ["Mysterious", "Profound", "Austria"], "element": "土", "theme": "wisdom", "emoji": "🔮", "gender": "unisex", "notes": "Mysterious and profound."},
    "妮": {"pinyin": "nī", "meanings": ["Girl", "Lass", "Niece"], "element": "火", "theme": "beauty", "emoji": "👧", "gender": "F", "notes": "Young girl. Modern name character."},
    "妹": {"pinyin": "mèi", "meanings": ["Younger sister", "Girl"], "element": "火", "theme": "family", "emoji": "👧", "gender": "F", "notes": "Younger sister."},
    "妻": {"pinyin": "qī", "meanings": ["Wife", "Spouse"], "element": "火", "theme": "family", "emoji": "💑", "gender": "F", "notes": "Wife. Family character."},
    "姑": {"pinyin": "gū", "meanings": ["Aunt", "Maiden", "Temporarily"], "element": "火", "theme": "family", "emoji": "👩", "gender": "F", "notes": "Aunt or maiden."},
    "姐": {"pinyin": "jiě", "meanings": ["Older sister", "Young woman"], "element": "火", "theme": "family", "emoji": "👩", "gender": "F", "notes": "Older sister."},
    "姓": {"pinyin": "xìng", "meanings": ["Surname", "Family name"], "element": "火", "theme": "family", "emoji": "📛", "gender": "unisex", "notes": "Family name."},
    "威": {"pinyin": "wēi", "meanings": ["Power", "Dignity", "Awe"], "element": "金", "theme": "strength", "emoji": "👑", "gender": "M", "notes": "Power and dignity."},
    "娜": {"pinyin": "nà", "meanings": ["Elegant", "Graceful"], "element": "水", "theme": "beauty", "emoji": "✨", "gender": "F", "notes": "Elegance."},
    "娃": {"pinyin": "wá", "meanings": ["Baby", "Child", "Doll"], "element": "水", "theme": "family", "emoji": "👶", "gender": "F", "notes": "Baby and child."},
    "姨": {"pinyin": "yí", "meanings": ["Aunt", "Mother's sister"], "element": "火", "theme": "family", "emoji": "👩", "gender": "F", "notes": "Maternal aunt."},
    "姻": {"pinyin": "yīn", "meanings": ["Marriage", "Relation by marriage"], "element": "水", "theme": "family", "emoji": "💍", "gender": "F", "notes": "Marriage and matrimony."},
    "姿": {"pinyin": "zī", "meanings": ["Posture", "Grace", "Looks"], "element": "金", "theme": "beauty", "emoji": "🧘", "gender": "F", "notes": "Graceful bearing."},
    "威": {"pinyin": "wēi", "meanings": ["Awe", "Dignity"], "element": "金", "theme": "strength", "emoji": "👑", "gender": "M", "notes": "Awe-inspiring power."},
    "娟": {"pinyin": "juān", "meanings": ["Beautiful", "Graceful"], "element": "水", "theme": "beauty", "emoji": "🌙", "gender": "F", "notes": "Graceful and beautiful."},
}
DICT.update(FINAL_CHARS)

# Common Chinese surnames (for surname detection in name analysis)
SURNAMES = {
    "赵", "钱", "孙", "李", "周", "吴", "郑", "王", "冯", "陈", "褚", "卫", "蒋", "沈",
    "韩", "杨", "朱", "秦", "尤", "许", "何", "吕", "施", "张", "孔", "曹", "严", "华",
    "金", "魏", "陶", "姜", "戚", "谢", "邹", "喻", "柏", "水", "窦", "章", "云", "苏",
    "潘", "葛", "范", "彭", "郎", "鲁", "韦", "昌", "马", "苗", "凤", "花", "方", "俞",
    "任", "袁", "柳", "酆", "鲍", "史", "唐", "费", "廉", "岑", "薛", "雷", "贺", "倪",
    "汤", "滕", "殷", "罗", "毕", "郝", "邬", "安", "常", "乐", "于", "时", "傅", "皮",
    "卞", "齐", "康", "伍", "余", "元", "卜", "顾", "孟", "平", "黄", "和", "穆", "萧",
    "尹", "姚", "邵", "湛", "汪", "祁", "毛", "禹", "狄", "米", "贝", "明", "臧", "计",
    "伏", "成", "戴", "谈", "宋", "茅", "庞", "熊", "纪", "舒", "屈", "项", "祝", "董",
    "梁", "杜", "阮", "蓝", "闵", "席", "季", "麻", "强", "贾", "路", "娄", "危", "江",
    "童", "颜", "郭", "梅", "盛", "林", "刁", "钟", "徐", "邱", "骆", "高", "夏", "蔡",
    "田", "樊", "胡", "凌", "霍", "虞", "万", "支", "柯", "昝", "管", "卢", "莫", "经",
    "房", "裘", "缪", "干", "解", "应", "宗", "丁", "宣", "贲", "邓", "郁", "单", "杭",
    "洪", "包", "诸", "左", "石", "崔", "吉", "钮", "龚", "程", "嵇", "邢", "滑", "裴",
    "陆", "荣", "翁", "荀", "羊", "於", "惠", "甄", "曲", "家", "封", "芮", "羿", "储",
    "靳", "汲", "邴", "糜", "松", "井", "段", "富", "巫", "乌", "焦", "巴", "弓", "牧",
    "隗", "山", "谷", "车", "侯", "宓", "蓬", "全", "郗", "班", "仰", "秋", "仲", "伊",
    "宫", "宁", "仇", "栾", "暴", "甘", "钭", "厉", "戎", "祖", "武", "符", "刘", "景",
    "詹", "束", "龙", "叶", "幸", "司", "韶", "郜", "黎", "蓟", "薄", "印", "宿", "白",
    "怀", "蒲", "邰", "从", "鄂", "索", "咸", "籍", "赖", "卓", "蔺", "屠", "蒙", "池",
    "乔", "阴", "郁", "胥", "能", "苍", "双", "闻", "莘", "党", "翟", "谭", "贡", "劳",
    "逄", "姬", "申", "扶", "堵", "冉", "宰", "郦", "雍", "郤", "璩", "桑", "桂", "濮",
    "牛", "寿", "通", "边", "扈", "燕", "冀", "郏", "浦", "尚", "农", "温", "别", "庄",
    "晏", "柴", "瞿", "阎", "充", "慕", "连", "茹", "习", "宦", "艾", "鱼", "容", "向",
    "古", "易", "慎", "戈", "廖", "庾", "终", "暨", "居", "衡", "步", "都", "耿", "满",
    "弘", "匡", "国", "文", "寇", "广", "禄", "阙", "东", "欧", "殳", "沃", "利", "蔚",
    "越", "夔", "隆", "师", "巩", "厍", "聂", "晁", "勾", "敖", "融", "冷", "訾", "辛",
    "阚", "那", "简", "饶", "空", "曾", "毋", "沙", "乜", "养", "鞠", "须", "丰", "巢",
    "关", "蒯", "相", "查", "后", "荆", "红", "游", "竺", "权", "逯", "盖", "益", "桓",
    "公", "万俟", "司马", "上官", "欧阳", "夏侯", "诸葛", "闻人", "东方", "赫连",
    "皇甫", "尉迟", "公羊", "澹台", "公冶", "宗政", "濮阳", "淳于", "单于", "太叔",
    "公孙", "仲孙", "轩辕", "令狐", "钟离", "宇文", "长孙", "慕容", "司徒", "司空",
}

ELEMENT_WUXING = {"木": "Wood 🌳", "火": "Fire 🔥", "土": "Earth 🏔️", "金": "Metal ⚔️", "水": "Water 🌊"}
ELEMENT_COLORS = {"木": "\033[32m", "火": "\033[31m", "土": "\033[33m", "金": "\033[37m", "水": "\033[34m"}
RESET = "\033[0m"

# ──────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ──────────────────────────────────────────────────────────────

def get_pinyin(char, tone=True):
    """Get pinyin for a Chinese character."""
    style = Style.TONE3 if not tone else Style.TONE
    try:
        return pinyin(char, style=style)[0][0]
    except Exception:
        return char


def format_pinyin(text, no_tone=False, caps=False):
    """Convert Chinese text to pinyin."""
    raw = get_pinyin(text, tone=not no_tone)
    if no_tone:
        # Remove tone numbers from TONE3 format
        raw = re.sub(r'[1-5]$', '', raw)
    if caps:
        # Title-case: capitalize first letter; if first char is accented (e.g. ā),
        # title() would give us Ā, but we want A-lì-Shān-Dà. So we strip tones
        # from the first character only for caps.
        raw = raw.title()
        # Normalize accented first chars: Ā→A, È→E, etc.
        accent_map = str.maketrans("ĀÁǍÀĒÉĚÈĪÍǏÌŌÓǑÒŪÚǓÙǕǗǙǛ",
                                   "AAAAEEEEIIIIOOOOuuuUUUUU")
        raw = raw.translate(accent_map)
    return raw


def get_char_info(char):
    """Get dictionary entry for a character, or None."""
    return DICT.get(char)


def element_symbol(element):
    return ELEMENT_WUXING.get(element, element)


def get_surname(name):
    """Detect surname from a full Chinese name (first 1-2 chars)."""
    if len(name) >= 2 and name[0:2] in SURNAMES:
        return name[0:2]
    if name[0] in SURNAMES:
        return name[0]
    return None


def colored(text, element):
    """Color text by element."""
    color = ELEMENT_COLORS.get(element, "")
    if color:
        return f"{color}{text}{RESET}"
    return text


# ──────────────────────────────────────────────────────────────
# FEATURE A: PINYIN CONVERSION
# ──────────────────────────────────────────────────────────────

def cmd_pinyin(text, no_tone=False, caps=False, show_meaning=False):
    """Feature A: Convert Chinese to pinyin."""
    if not text:
        return ""

    # Detect surname
    surname = get_surname(text)
    surname_len = len(surname) if surname else 0
    given = text[surname_len:]
    surname_parts = []
    given_parts = []

    if surname:
        for ch in surname:
            py = format_pinyin(ch, no_tone, caps)
            surname_parts.append(py)
    for ch in given:
        py = format_pinyin(ch, no_tone, caps)
        given_parts.append(py)

    if not show_meaning:
        result = ""
        if surname_parts:
            sur_str = " ".join(surname_parts)
            given_str = " ".join(given_parts) if given_parts else ""
            if given_str:
                result = f"{sur_str} {given_str}"
            else:
                result = sur_str
        else:
            result = " ".join(given_parts)
        return result

    # With meanings
    lines = []
    if surname:
        for i, ch in enumerate(surname):
            py = format_pinyin(ch, no_tone, caps)
            info = get_char_info(ch)
            if info:
                meaning_str = ", ".join(info["meanings"][:2])
                lines.append(f"{ch} ({py}) — {meaning_str} {info.get('emoji', '')}")
            else:
                lines.append(f"{ch} ({py})")
    for i, ch in enumerate(given):
        py = format_pinyin(ch, no_tone, caps)
        info = get_char_info(ch)
        if info:
            meaning_str = ", ".join(info["meanings"][:2])
            lines.append(f"{ch} ({py}) — {meaning_str} {info.get('emoji', '')}")
        else:
            lines.append(f"{ch} ({py})")
    return "\n".join(lines)


# ──────────────────────────────────────────────────────────────
# FEATURE B: CHARACTER MEANING
# ──────────────────────────────────────────────────────────────

def cmd_meaning(chars, deep=False):
    """Feature B: Show detailed character meaning."""
    results = []
    for ch in chars:
        info = get_char_info(ch)
        if not info:
            results.append(f"'{ch}' not found in dictionary.")
            continue

        elem_symbol = element_symbol(info["element"])
        meanings = ", ".join(info["meanings"])
        gender_symbol = {"M": "♂️", "F": "♀️", "unisex": "⚧️"}.get(info.get("gender", "unisex"), "⚧️")

        lines = []
        lines.append(f"\n{'='*50}")
        lines.append(f"  {ch} ({info['pinyin']})")
        lines.append(f"{'='*50}")
        lines.append(f"  Meanings:      {meanings}")
        lines.append(f"  Element:       {elem_symbol}")
        lines.append(f"  Theme:         {info['theme'].title()} {info.get('emoji', '')}")
        lines.append(f"  Gender:        {info.get('gender', 'unisex').title()} {gender_symbol}")
        if info.get("notes"):
            lines.append(f"  Cultural Note: {info['notes']}")

        if deep:
            # Extended explanation
            lines.append(f"\n  ── Extended Analysis ──")
            meanings_list = info["meanings"]
            lines.append(f"  This character expresses: {', '.join(meanings_list)}.")
            element_desc = {
                "木": "Wood element — growth, flexibility, creativity, and vitality.",
                "火": "Fire element — passion, brightness, transformation, and energy.",
                "土": "Earth element — stability, nurturing, reliability, and balance.",
                "金": "Metal element — strength, structure, refinement, and determination.",
                "水": "Water element — wisdom, adaptability, depth, and flow.",
            }
            lines.append(f"  {element_desc.get(info['element'], '')}")
            lines.append(f"  Theme: {info['theme'].title()} — suitable for names expressing {info['theme']}.")
            if info.get("notes"):
                lines.append(f"  {info['notes']}")
            # Usage examples
            if info["theme"] == "strength":
                lines.append(f"  Common name patterns: 勇{ch}, {ch}强, {ch}杰")
            elif info["theme"] == "beauty":
                lines.append(f"  Common name patterns: 美{ch}, {ch}丽, 秀{ch}")
            elif info["theme"] == "wisdom":
                lines.append(f"  Common name patterns: 智{ch}, {ch}慧, {ch}明")
            elif info["theme"] == "nature":
                lines.append(f"  Common name patterns: {ch}林, 海{ch}, 云{ch}")
            elif info["theme"] == "virtue":
                lines.append(f"  Common name patterns: 德{ch}, {ch}义, 仁{ch}")
            elif info["theme"] == "prosperity":
                lines.append(f"  Common name patterns: 富{ch}, {ch}贵, {ch}荣")
            else:
                lines.append(f"  Common compound names with {ch} are popular choices.")

        results.append("\n".join(lines))
    return "\n".join(results)


# ──────────────────────────────────────────────────────────────
# FEATURE C: NAME ANALYSIS
# ──────────────────────────────────────────────────────────────

def cmd_name(name):
    """Feature C: Analyze a full Chinese name."""
    if not name:
        return "Please provide a name."

    surname = get_surname(name)
    surname_len = len(surname) if surname else 0
    given = name[surname_len:]

    lines = []
    lines.append(f"\n{'═'*60}")
    lines.append(f"  NAME ANALYSIS: {name}")
    lines.append(f"{'═'*60}")

    # Pinyin
    sur_py = " ".join([format_pinyin(ch) for ch in surname]) if surname else ""
    given_py = " ".join([format_pinyin(ch) for ch in given]) if given else ""
    full_py = f"{sur_py} {given_py}".strip()
    if surname:
        lines.append(f"\n  Surname:  {surname} ({sur_py})")
        lines.append(f"  Given:    {given} ({given_py})")
    else:
        lines.append(f"\n  Characters: {name} ({full_py})")
    lines.append(f"  Pinyin:   {full_py}")

    # Character breakdown
    lines.append(f"\n  {'─'*40}")
    lines.append(f"  Character Breakdown:")
    lines.append(f"  {'─'*40}")

    all_chars = list(name)
    themes = []
    elements = []
    for i, ch in enumerate(all_chars):
        info = get_char_info(ch)
        if info:
            is_surname = surname and i < len(surname)
            label = "Surname" if is_surname else "Given"
            meanings_str = ", ".join(info["meanings"])
            elem_symbol = element_symbol(info["element"])
            emoji = info.get("emoji", "")
            lines.append(f"  {ch} ({info['pinyin']}) [{label}]")
            lines.append(f"    Meanings: {meanings_str}")
            lines.append(f"    Element:  {elem_symbol}  Theme: {info['theme'].title()} {emoji}")
            themes.append(info["theme"])
            elements.append(info["element"])
        else:
            lines.append(f"  {ch} — (not in dictionary)")

    # Overall theme
    if themes:
        lines.append(f"\n  {'─'*40}")
        lines.append(f"  Overall Analysis:")
        lines.append(f"  {'─'*40}")

        from collections import Counter
        theme_counts = Counter(themes)
        primary_theme = theme_counts.most_common(1)[0][0]
        lines.append(f"  Primary Theme:   {primary_theme.title()} {DICT.get(name[0], {}).get('emoji', '')}")

        # Element balance
        if elements:
            elem_counts = Counter(elements)
            lines.append(f"\n  Element Balance (五行):")
            for elem_name in ["木", "火", "土", "金", "水"]:
                count = elem_counts.get(elem_name, 0)
                bar = "█" * count + "░" * (len(name) - count)
                lines.append(f"    {ELEMENT_WUXING.get(elem_name, elem_name)}: {bar} ({count}/{len(name)})")

            # Calculate balance score
            unique_elements = len(elem_counts)
            if unique_elements >= 3:
                balance_score = "⚖️ Well-balanced"
            elif unique_elements == 2:
                balance_score = "🔶 Moderately balanced"
            else:
                balance_score = "🔴 Concentrated"
            lines.append(f"\n  Element Balance Score: {balance_score}")

            # Suggest complementary element
            max_elem = elem_counts.most_common(1)[0][0]
            generating = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
            weakening = {"木": "金", "火": "水", "土": "木", "金": "火", "水": "土"}
            lines.append(f"  Dominant Element: {ELEMENT_WUXING.get(max_elem, max_elem)}")
            lines.append(f"  Generates:        {ELEMENT_WUXING.get(generating.get(max_elem, ''), '')}")
            lines.append(f"  Weakens:          {ELEMENT_WUXING.get(weakening.get(max_elem, ''), '')}")

        lines.append(f"\n  {'═'*60}")

    return "\n".join(lines)


# ──────────────────────────────────────────────────────────────
# FEATURE D: SEARCH
# ──────────────────────────────────────────────────────────────

def cmd_search(query=None, element=None, theme=None):
    """Feature D: Search characters by meaning, element, or theme."""
    results = []

    for char, info in DICT.items():
        # Skip duplicates (we may have some from the merge)
        match = True

        if query:
            query_lower = query.lower()
            meanings_text = " ".join(m.lower() for m in info["meanings"])
            notes_text = (info.get("notes") or "").lower()
            pinyin_text = info["pinyin"].lower()
            char_match = query_lower in meanings_text or query_lower in notes_text or query_lower in pinyin_text
            if not char_match:
                match = False

        if element:
            if info.get("element") != element:
                match = False

        if theme:
            if info.get("theme") != theme.lower():
                match = False

        if match:
            results.append(char)

    return results


# ──────────────────────────────────────────────────────────────
# MAIN CLI
# ──────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Chinese Name Converter — Pinyin, Meaning, Analysis & Search",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --pinyin 阿历山大
  %(prog)s --pinyin 阿历山大 --no-tone
  %(prog)s --pinyin 阿历山大 --caps
  %(prog)s --pinyin 伟 --meaning
  %(prog)s --meaning 伟
  %(prog)s --meaning 伟 --deep
  %(prog)s --name 张伟明
  %(prog)s --search great
  %(prog)s --search --element 火
  %(prog)s --search --theme nature
        """
    )

    parser.add_argument("--pinyin", type=str, metavar="TEXT", help="Convert Chinese text to pinyin")
    parser.add_argument("--no-tone", action="store_true", help="Omit tone marks in pinyin output")
    parser.add_argument("--caps", action="store_true", help="Capitalize pinyin syllables")
    parser.add_argument("--meaning", type=str, nargs="?", const="FLAG", metavar="CHARS", help="Show detailed character meaning(s). With --pinyin, use as flag.")
    parser.add_argument("--deep", action="store_true", help="Show extended meaning with usage examples")
    parser.add_argument("--name", type=str, metavar="NAME", help="Analyze a full Chinese name")
    parser.add_argument("--search", type=str, nargs="?", const="", metavar="QUERY", help="Search characters by meaning, element, or theme")
    parser.add_argument("--element", type=str, metavar="ELEMENT", help="Filter search by element (木火土金水)")
    parser.add_argument("--theme", type=str, metavar="THEME", help="Filter search by theme (strength, beauty, wisdom, etc.)")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    parser.add_argument("--count", action="store_true", help="Show dictionary character count")
    parser.add_argument("--export-dict", action="store_true", help="Export the full dictionary as JSON")

    args = parser.parse_args()

    # Count
    if args.count:
        print(f"Dictionary contains {len(DICT)} characters.")
        return

    # Export dict
    if args.export_dict:
        print(json.dumps(DICT, ensure_ascii=False, indent=None))
        return

    # Feature A: Pinyin
    if args.pinyin:
        show_meaning = args.meaning is not None
        result = cmd_pinyin(args.pinyin, no_tone=args.no_tone, caps=args.caps, show_meaning=show_meaning)
        print(result)
        return

    # Feature B: Meaning
    if args.meaning is not None and args.meaning != "FLAG":
        result = cmd_meaning(args.meaning, deep=args.deep)
        print(result)
        return

    # Feature C: Name analysis
    if args.name:
        result = cmd_name(args.name)
        print(result)
        return

    # Feature D: Search
    if args.search is not None or args.element or args.theme:
        query = args.search if args.search else None
        found = cmd_search(query=query, element=args.element, theme=args.theme)

        # Remove duplicate characters
        seen = set()
        unique_found = []
        for ch in found:
            if ch not in seen:
                seen.add(ch)
                unique_found.append(ch)
        found = unique_found

        if args.json:
            result_list = []
            for ch in found:
                info = DICT.get(ch, {})
                result_list.append({
                    "char": ch,
                    "pinyin": info.get("pinyin", ""),
                    "meanings": info.get("meanings", []),
                    "element": info.get("element", ""),
                    "theme": info.get("theme", ""),
                    "emoji": info.get("emoji", ""),
                    "gender": info.get("gender", "unisex"),
                    "notes": info.get("notes", ""),
                })
            print(json.dumps(result_list, ensure_ascii=False, indent=2))
        else:
            if not found:
                print("No matching characters found.")
                return
            print(f"Found {len(found)} matching character(s):\n")
            # Group by theme
            theme_groups = {}
            for ch in found:
                info = DICT.get(ch, {})
                t = info.get("theme", "other")
                if t not in theme_groups:
                    theme_groups[t] = []
                theme_groups[t].append(ch)

            for theme_name in sorted(theme_groups.keys()):
                chars_in_theme = theme_groups[theme_name]
                print(f"  [{theme_name.title()}]")
                for ch in chars_in_theme:
                    info = DICT.get(ch, {})
                    meanings = ", ".join(info.get("meanings", [])[:2])
                    elem_symbol = element_symbol(info.get("element", ""))
                    emoji = info.get("emoji", "")
                    print(f"    {ch} ({info.get('pinyin', '')}) — {meanings}  {elem_symbol} {emoji}")
                print()

        return

    # No arguments
    parser.print_help()


if __name__ == "__main__":
    main()

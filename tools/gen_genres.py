"""Generate a pvr.iptvsimple genre mapping file for Mirakurun's /api/iptv/xmltv.

Category strings are read straight from Mirakurun's xmltv.ts so they match exactly.
Writes an English-commented and a Japanese-commented file; the mappings are identical.
Usage: python3 gen_genres.py <path/to/Mirakurun/src/Mirakurun/api/iptv/xmltv.ts> <out_dir>
"""
import re
import sys

src = open(sys.argv[1], encoding="utf-8").read()


def table(name):
    body = re.search(name + r"[^=]*= \{(.*?)\n\};", src, re.S).group(1)
    return {int(k, 16): v for k, v in re.findall(r'^\s*(0x[0-9A-Fa-f]+): "([^"]+)"', body, re.M)}


LV1, LV2, UNEX = table("GENRE_LV1"), table("GENRE_LV2"), table("GENRE_UNEX")

# ARIB (lv1<<4 | lv2) -> DVB genreId (EN 300 468), as used by Kodi
STD = {
    # ニュース／報道 -> News / Current Affairs
    0x00: 0x20, 0x01: 0x21, 0x02: 0x22, 0x03: 0x80, 0x04: 0x82, 0x05: 0x20,
    0x06: 0x22, 0x07: 0x24, 0x08: 0x20, 0x09: 0x20, 0x0A: 0x21, 0x0F: 0x20,
    # スポーツ -> Sports
    0x10: 0x42, 0x11: 0x45, 0x12: 0x43, 0x13: 0x40, 0x14: 0x45, 0x15: 0x4B,
    0x16: 0x41, 0x17: 0x46, 0x18: 0x47, 0x19: 0x48, 0x1A: 0x4A, 0x1F: 0x40,
    # 情報／ワイドショー -> Show / Leisure
    0x20: 0x33, 0x21: 0x7B, 0x22: 0xA0, 0x23: 0xA4, 0x24: 0xA6, 0x25: 0xA5,
    0x26: 0xA0, 0x27: 0x78, 0x2F: 0xA0,
    # ドラマ -> Movie / Drama
    0x30: 0x10, 0x31: 0x10, 0x32: 0x17, 0x3F: 0x10,
    # 音楽 -> Music
    0x40: 0x61, 0x41: 0x61, 0x42: 0x62, 0x43: 0x64, 0x44: 0x63, 0x45: 0x60,
    0x46: 0x61, 0x47: 0x60, 0x48: 0x63, 0x49: 0x50, 0x4A: 0x63, 0x4F: 0x60,
    # バラエティ -> Show / Game Show
    0x50: 0x31, 0x51: 0x31, 0x52: 0x33, 0x53: 0x32, 0x54: 0x32, 0x55: 0x32,
    0x56: 0x32, 0x5F: 0x32,
    # 映画 -> Movie
    0x60: 0x10, 0x61: 0x10, 0x62: 0x10, 0x6F: 0x10,
    # アニメ／特撮 -> Children's (cartoons)
    0x70: 0x55, 0x71: 0x55, 0x72: 0x50, 0x7F: 0x55,
    # ドキュメンタリー／教養 -> Education / Factual
    0x80: 0x81, 0x81: 0x94, 0x82: 0x91, 0x83: 0x92, 0x84: 0x74, 0x85: 0x75,
    0x86: 0x42, 0x87: 0x90, 0x88: 0x24, 0x8F: 0x90,
    # 劇場／公演 -> Arts / Music
    0x90: 0x71, 0x91: 0x65, 0x92: 0x66, 0x93: 0x74, 0x94: 0x74, 0x9F: 0x71,
    # 趣味／教育 -> Leisure / Education
    0xA0: 0xA1, 0xA1: 0xA7, 0xA2: 0xA2, 0xA3: 0xA0, 0xA4: 0xA0, 0xA5: 0xA3,
    0xA6: 0xA0, 0xA7: 0x97, 0xA8: 0x54, 0xA9: 0x54, 0xAA: 0x96, 0xAB: 0x96,
    0xAC: 0x90, 0xAF: 0xA0,
    # 福祉 -> Social / Political
    0xB0: 0x80, 0xB1: 0x80, 0xB2: 0x82, 0xB3: 0x80, 0xB4: 0x80, 0xB5: 0x80,
    0xB6: 0x80, 0xBF: 0x80,
}

# Fallback when Mirakurun has no lv2 name (it prints "<lv1> - undefined")
LV1_FALLBACK = {0x0: 0x20, 0x1: 0x40, 0x2: 0xA0, 0x3: 0x10, 0x4: 0x60, 0x5: 0x30,
                0x6: 0x10, 0x7: 0x55, 0x8: 0x90, 0x9: 0x70, 0xA: 0xA0, 0xB: 0x80}

# CS extended genres (lv1 = 拡張). Broadcast notes (0x00x) are left unmapped on
# purpose so the programme's real genre, listed alongside them, is used instead.
EXT = {
    0x100: 0x44, 0x101: 0x45, 0x102: 0x45, 0x103: 0x45, 0x104: 0x4B, 0x105: 0x4B, 0x10F: 0x40,
    0x110: 0x12, 0x111: 0x13, 0x112: 0x14, 0x113: 0x11, 0x114: 0x16, 0x115: 0x13, 0x116: 0x12,
    0x117: 0x17, 0x118: 0x10, 0x119: 0x10, 0x11A: 0x12, 0x11B: 0x10, 0x11C: 0x15, 0x11F: 0x10,
    0x120: 0x12, 0x121: 0x13, 0x122: 0x14, 0x123: 0x11, 0x124: 0x16, 0x125: 0x13, 0x126: 0x10,
    0x127: 0x17, 0x128: 0x10, 0x129: 0x10, 0x12A: 0x12, 0x12B: 0x10, 0x12C: 0x15, 0x12F: 0x10,
}

# Kodi / DVB genre names (EN 300 468) for the IDs used above: (English, Japanese)
DVB = {
    0x10: ("Movie/Drama", "映画／ドラマ"),
    0x11: ("Detective/Thriller", "探偵／スリラー"),
    0x12: ("Adventure/Western/War", "冒険／西部劇／戦争"),
    0x13: ("Science Fiction/Fantasy/Horror", "SF／ファンタジー／ホラー"),
    0x14: ("Comedy", "コメディ"),
    0x15: ("Soap/Melodrama/Folklore", "ホームドラマ／メロドラマ"),
    0x16: ("Romance", "ロマンス"),
    0x17: ("Serious/Classical/Religious/Historical", "シリアス／古典／歴史"),
    0x20: ("News/Current Affairs", "ニュース／時事"),
    0x21: ("News/Weather Report", "ニュース／天気予報"),
    0x22: ("News Magazine", "ニュースマガジン"),
    0x24: ("Discussion/Interview/Debate", "討論／インタビュー"),
    0x30: ("Show/Game Show", "ショー／ゲームショー"),
    0x31: ("Game Show/Quiz/Contest", "ゲームショー／クイズ"),
    0x32: ("Variety Show", "バラエティショー"),
    0x33: ("Talk Show", "トークショー"),
    0x40: ("Sports", "スポーツ"),
    0x41: ("Special Event", "特別イベント（五輪・W杯等）"),
    0x42: ("Sports Magazine", "スポーツマガジン"),
    0x43: ("Football", "サッカー"),
    0x44: ("Tennis/Squash", "テニス／スカッシュ"),
    0x45: ("Team Sports", "団体競技"),
    0x46: ("Athletics", "陸上競技"),
    0x47: ("Motor Sport", "モータースポーツ"),
    0x48: ("Water Sport", "ウォータースポーツ"),
    0x4A: ("Equestrian", "馬術"),
    0x4B: ("Martial Sports", "格闘技"),
    0x50: ("Children's/Youth Programmes", "子供／青少年向け"),
    0x54: ("Informational/Educational/School", "学習／教育"),
    0x55: ("Cartoons/Puppets", "アニメ／人形劇"),
    0x60: ("Music/Ballet/Dance", "音楽／バレエ／ダンス"),
    0x61: ("Rock/Pop", "ロック／ポップス"),
    0x62: ("Serious/Classical Music", "クラシック音楽"),
    0x63: ("Folk/Traditional Music", "民族／伝統音楽"),
    0x64: ("Jazz", "ジャズ"),
    0x65: ("Musical/Opera", "ミュージカル／オペラ"),
    0x66: ("Ballet", "バレエ"),
    0x70: ("Arts/Culture", "芸術／文化"),
    0x71: ("Performing Arts", "舞台芸術"),
    0x74: ("Popular Culture/Traditional Arts", "大衆文化／伝統芸能"),
    0x75: ("Literature", "文学"),
    0x78: ("Broadcasting/Press", "放送／報道機関"),
    0x7B: ("Fashion", "ファッション"),
    0x80: ("Social/Political/Economics", "社会／政治／経済"),
    0x81: ("Magazines/Reports/Documentary", "レポート／ドキュメンタリー"),
    0x82: ("Economics/Social Advisory", "経済／社会"),
    0x90: ("Education/Science/Factual", "教育／科学／教養"),
    0x91: ("Nature/Animals/Environment", "自然／動物／環境"),
    0x92: ("Technology/Natural Sciences", "技術／自然科学"),
    0x94: ("Foreign Countries/Expeditions", "海外／紀行"),
    0x96: ("Further Education", "生涯教育"),
    0x97: ("Languages", "語学"),
    0xA0: ("Leisure/Hobbies", "レジャー／趣味"),
    0xA1: ("Tourism/Travel", "観光／旅行"),
    0xA2: ("Handicraft", "手工芸"),
    0xA3: ("Motoring", "自動車"),
    0xA4: ("Fitness & Health", "フィットネス／健康"),
    0xA5: ("Cooking", "料理"),
    0xA6: ("Advertisement/Shopping", "広告／ショッピング"),
    0xA7: ("Gardening", "園芸"),
}

HEADER = {
    "en": [
        "  Genre mappings for Mirakurun /api/iptv/xmltv (ARIB genres) -> Kodi DVB genre IDs.",
        "  Copy to userdata/addon_data/pvr.iptvsimple/genres/genreTextMappings/ and select it in",
        "  IPTV Simple settings > EPG > Genres. Enable 'Use genre text from XMLTV when mapping",
        "  genres' to keep the Japanese genre names while getting the EPG colours.",
        "",
        "  Broadcast notes such as '延長の可能性あり' are left unmapped on purpose, so the",
        "  programme's real genre (listed next to them) is used instead.",
        "",
        "  Generated by tools/gen_genres.py - edit the mapping there, not in this file.",
    ],
    "ja": [
        "  Mirakurun の /api/iptv/xmltv（ARIB ジャンル）を Kodi の DVB ジャンル ID に変換する",
        "  マッピングファイルです。",
        "  userdata/addon_data/pvr.iptvsimple/genres/genreTextMappings/ にコピーし、",
        "  IPTV Simple の設定「EPG」タブ >「ジャンル」の「ジャンルのパス」に指定してください。",
        "  「ジャンルのマッピング時に、XMLTVのジャンル テキストを使用する」を有効にすると、",
        "  番組表は色分けされ、ジャンル名は日本語のまま表示されます。",
        "",
        "  「延長の可能性あり」などの番組付属情報は、番組本来のジャンルが使われるよう",
        "  意図的にマッピングしていません。",
        "",
        "  tools/gen_genres.py で生成しています。変更はこのファイルではなくスクリプト側で行ってください。",
    ],
}
NAME = {"en": "Mirakurun (ARIB) Genres", "ja": "Mirakurun（ARIB）ジャンル"}
CS_LABEL = {"en": "CS extended genres", "ja": "広帯域CS 拡張ジャンル"}


def build(lang):
    i = 0 if lang == "en" else 1

    def entry(gid, text):
        return f'  <genre genreId="0x{gid:02X}">{text}</genre>  <!-- {DVB[gid][i]} -->'

    lines = ['<?xml version="1.0" encoding="UTF-8"?>', "<!--", *HEADER[lang], "-->",
             "<genres>", f"  <name>{NAME[lang]}</name>"]
    for lv1 in sorted(LV1_FALLBACK):
        lines.append(f"  <!-- {LV1[lv1]} -->")
        for code in sorted(k for k in LV2 if k >> 4 == lv1):
            lines.append(entry(STD[code], f"{LV1[lv1]} - {LV2[code]}"))
        lines.append(entry(LV1_FALLBACK[lv1], f"{LV1[lv1]} - undefined"))
    lines.append(f"  <!-- {LV1[0xE]}: {CS_LABEL[lang]} -->")
    for code in sorted(UNEX):
        if code in EXT:
            lines.append(entry(EXT[code], UNEX[code]))
    lines.append("</genres>")
    return "\n".join(lines) + "\n"


missing = [hex(k) for k in LV2 if k >> 4 in LV1_FALLBACK and k not in STD]
if missing:
    sys.exit(f"unmapped ARIB codes: {missing}")

out_dir = sys.argv[2]
for lang, name in (("en", "mirakurun-genres.xml"), ("ja", "mirakurun-genres.ja.xml")):
    open(f"{out_dir}/{name}", "w", encoding="utf-8").write(build(lang))
    print(f"wrote {out_dir}/{name}")

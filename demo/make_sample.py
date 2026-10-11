"""Write a sample M3U + XMLTV in Mirakurun's /api/iptv format, for trying the mapping
without a tuner. Channels and titles are made up; categories use Mirakurun's exact text.

Usage: python3 make_sample.py <out_dir>
"""
import datetime as dt
import sys

out = sys.argv[1]

# (title, [categories]) - minutes are taken from the slot list below
CHANNELS = {
    "Demo 1": [
        ("朝のニュース", ["ニュース／報道 - 定時・総合"]),
        ("気象情報", ["ニュース／報道 - 天気"]),
        ("連続ドラマ　春の坂道", ["ドラマ - 国内ドラマ"]),
        ("釣り紀行", ["趣味／教育 - 旅・釣り・アウトドア"]),
        ("国会中継", ["ニュース／報道 - 政治・国会"]),
        ("ドキュメント　海の生きもの", ["ドキュメンタリー／教養 - 自然・動物・環境"]),
        ("夜のニュース", ["ニュース／報道 - 定時・総合"]),
    ],
    "Demo 2": [
        ("アニメ　ほしのこ", ["アニメ／特撮 - 国内アニメ"]),
        ("えいごであそぼ", ["趣味／教育 - 会話・語学"]),
        ("科学のじかん", ["ドキュメンタリー／教養 - 宇宙・科学・医学"]),
        ("みんなのうた", ["音楽 - 童謡・キッズ"]),
        ("クラシック音楽館", ["音楽 - クラシック・オペラ"]),
        ("手話ニュース", ["福祉 - 手話", "ニュース／報道 - 定時・総合"]),
        ("囲碁・将棋の時間", ["趣味／教育 - 囲碁・将棋"]),
    ],
    "Demo 3": [
        ("情報ワイド　あさ", ["情報／ワイドショー - 芸能・ワイドショー"]),
        ("ショッピング", ["情報／ワイドショー - ショッピング・通販"]),
        ("クイズ　ひらめき王", ["バラエティ - クイズ"]),
        ("お笑い劇場", ["バラエティ - お笑い・コメディ"]),
        ("グルメ探訪", ["情報／ワイドショー - グルメ・料理"]),
        ("プロ野球中継", ["延長の可能性あり", "スポーツ - 野球"]),
        ("スポーツニュース", ["スポーツ - スポーツニュース"]),
    ],
    "Demo 4": [
        ("サッカー　リーグ戦", ["スポーツ - サッカー"]),
        ("大相撲", ["スポーツ - 相撲・格闘技"]),
        ("映画　遠い山なみ", ["映画 - 邦画"]),
        ("ミュージックステージ", ["音楽 - 国内ロック・ポップス"]),
        ("落語名人会", ["劇場／公演 - 落語・演芸"]),
        ("時代劇　剣客日記", ["ドラマ - 時代劇"]),
        ("深夜アニメ", ["アニメ／特撮 - 国内アニメ"]),
    ],
    "Demo 5": [
        ("洋画劇場", ["映画 - 洋画"]),
        ("海外ドラマ", ["ドラマ - 海外ドラマ"]),
        ("世界の車窓", ["ドキュメンタリー／教養 - 歴史・紀行"]),
        ("テニス中継", ["スポーツ - その他の球技"]),
        ("ジャズ・ナイト", ["音楽 - ジャズ・フュージョン"]),
        ("経済マーケット", ["ニュース／報道 - 経済・市況"]),
        ("特撮ヒーロー", ["アニメ／特撮 - 特撮"]),
    ],
}
SLOTS = [60, 30, 90, 60, 90, 60, 60]  # 7.5 hours per channel

start = dt.datetime.now(dt.timezone.utc).replace(minute=0, second=0, microsecond=0) - dt.timedelta(hours=1)


def ts(t):
    return t.strftime("%Y%m%d%H%M%S +0000")


m3u = ["#EXTM3U"]
xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<!DOCTYPE tv SYSTEM "xmltv.dtd">',
       '<tv source-info-name="Mirakurun">']
for n, name in enumerate(CHANNELS, 1):
    cid = f"demo{n}"
    m3u += [f'#EXTINF:-1 tvg-id="{cid}" tvg-chno="{n}" group-title="GR",{name}',
            f"http://127.0.0.1:40772/api/services/{cid}/stream"]
    xml += [f'<channel id="{cid}">', f"<display-name>{name}</display-name>", "</channel>"]
for n, (name, progs) in enumerate(CHANNELS.items(), 1):
    t = start + dt.timedelta(minutes=30 * (n % 2))  # stagger channels a little
    for (title, cats), mins in zip(progs, SLOTS):
        end = t + dt.timedelta(minutes=mins)
        xml.append(f'<programme start="{ts(t)}" stop="{ts(end)}" channel="demo{n}">')
        xml.append(f"<title>{title}</title>")
        xml.append(f"<desc>{title}（サンプル番組）</desc>")
        xml += [f"<category>{c}</category>" for c in cats]
        xml.append("</programme>")
        t = end
xml.append("</tv>")

open(f"{out}/sample.m3u", "w", encoding="utf-8").write("\n".join(m3u) + "\n")
open(f"{out}/sample-xmltv.xml", "w", encoding="utf-8").write("\n".join(xml) + "\n")
print(f"wrote {out}/sample.m3u and {out}/sample-xmltv.xml")

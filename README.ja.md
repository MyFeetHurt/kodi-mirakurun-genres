# Mirakurun 用 Kodi ジャンルマッピング

[English](README.md)

Kodi の [IPTV Simple Client](https://github.com/kodi-pvr/pvr.iptvsimple)（`pvr.iptvsimple`）で [Mirakurun](https://github.com/Chinachu/Mirakurun) の番組表（`/api/iptv/xmltv`）を使うときのジャンルマッピングファイルです。

Mirakurun は `ニュース／報道 - 定時・総合` のような ARIB ジャンルを出力しますが、Kodi はこれを認識できないため、番組表がすべて灰色になります。このファイルで各 ARIB ジャンルを最も近い Kodi（DVB）ジャンルに割り当てると、ジャンル名は日本語のまま、番組表が色分けされるようになります。

![Kodi 番組表の変更前と変更後](docs/demo.gif)

動画: [docs/demo.mp4](docs/demo.mp4) ・ スクリーンショット: [変更前](docs/before.png) / [変更後](docs/after.png)

## ファイル

| ファイル | 内容 |
|---|---|
| [`genres/mirakurun-genres.ja.xml`](genres/mirakurun-genres.ja.xml) | マッピングファイル（日本語コメント） |
| [`genres/mirakurun-genres.xml`](genres/mirakurun-genres.xml) | 同じマッピング（英語コメント） |
| [`tools/gen_genres.py`](tools/gen_genres.py) | Mirakurun のソースから両ファイルを生成するスクリプト |
| [`demo/make_sample.py`](demo/make_sample.py) | チューナーなしで試せるサンプル M3U / XMLTV を作成 |

2つの XML ファイルのマッピング内容は同じです。どちらを使っても構いません。

## 設定方法

1. IPTV Simple に Mirakurun を設定します。
   - **M3U プレイリスト:** `http://<mirakurun>:40772/api/iptv/playlist`
   - **XMLTV:** `http://<mirakurun>:40772/api/iptv/xmltv`
2. `mirakurun-genres.ja.xml` を
   `userdata/addon_data/pvr.iptvsimple/genres/genreTextMappings/` にコピーします。
   （[userdata の場所](https://kodi.wiki/view/Userdata)）
3. IPTV Simple の設定で「**EPG**」タブを開き、「**ジャンル**」で次のように設定します。
   - **ジャンルのマッピング時に、XMLTVのジャンル テキストを使用する**: オン（日本語のジャンル名を表示。オフにすると Kodi の英語のジャンル名になります）
   - **ロケーション**: ローカルパス
   - **ジャンルのパス**: 手順 2 のファイル
4. アドオンを再起動します。番組表が変わらない場合は、Kodi の「Settings → PVR & Live TV → General → Clear data」を実行してください。

ファイルをコピーする代わりに、「ロケーション」を「リモートパス」にして、「ジャンルのURL」に次の URL を指定することもできます。

```
https://raw.githubusercontent.com/MyFeetHurt/kodi-mirakurun-genres/main/genres/mirakurun-genres.ja.xml
```

## ジャンルの割り当て

Kodi には DVB（EN 300 468）の 11 分類しかないため、各 ARIB ジャンルを最も近い分類に割り当てています。

| ARIB ジャンル | Kodi の分類 |
|---|---|
| ニュース／報道 | ニュース／時事 |
| スポーツ | スポーツ |
| 情報／ワイドショー | ショー、レジャー |
| ドラマ、映画 | 映画／ドラマ |
| 音楽 | 音楽 |
| バラエティ | ショー／ゲームショー |
| アニメ／特撮 | 子供向け（アニメ） |
| ドキュメンタリー／教養 | 教育／科学／教養 |
| 劇場／公演 | 芸術／文化 |
| 趣味／教育 | レジャー／趣味、教育 |
| 福祉 | 社会／政治 |
| 拡張（広帯域CS） | スポーツ、映画の詳細ジャンル |

より適切な場合は、同じ大分類でも別の分類に割り当てています（例: `ニュース／報道 - 政治・国会` → 社会／政治）。XML の各行に、割り当て先の Kodi ジャンルをコメントで記載しています。

**意図的に割り当てていないもの:**
- 「延長の可能性あり」などの番組付属情報。Mirakurun は本来のジャンルと並べてカテゴリとして出力するため、割り当てると本来のジャンルが使われなくなる場合があります。
- `その他 - その他` と `予備`。これらの番組は色なしでジャンル名だけが表示されます。

## マッピングの変更

`tools/gen_genres.py` の表を編集し、両ファイルを再生成してください。

```sh
git clone --depth 1 https://github.com/Chinachu/Mirakurun
python3 tools/gen_genres.py Mirakurun/src/Mirakurun/api/iptv/xmltv.ts genres
```

ジャンル名は Mirakurun のソースから直接読み込むため、Mirakurun の出力と常に一致します。

## チューナーなしで試す

`demo/make_sample.py` は、架空のチャンネルと番組で Mirakurun 形式の `sample.m3u` と `sample-xmltv.xml` を作成します。IPTV Simple にこれらを指定すると、マッピングを試せます。デモ動画もこの方法で録画しました（Kodi 20.5、IPTV Simple 20.13.0）。

```sh
python3 demo/make_sample.py /path/to/output
```

## ライセンス

[MIT](LICENSE)

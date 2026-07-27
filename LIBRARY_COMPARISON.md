# QRコード読み取りライブラリ 完全比較表

## ✅ 採用ライブラリ（商用無料）

このアプリで採用した3つのライブラリはすべて**Apache 2.0ライセンス**で、**商用利用無料・制限なし**です。

| ライブラリ | ライセンス | インストール | sudo必要 | 商用利用 | 特徴 | パフォーマンス |
|-----------|----------|------------|---------|---------|------|--------------|
| **OpenCV Standard** | Apache 2.0 | `pip install opencv-python` | ❌ 不要 | ✅ 無料 | 標準実装、軽量、高速 | ⭐⭐⭐⭐⭐ 非常に高速 |
| **zxing-cpp** | Apache 2.0 | `pip install zxing-cpp` | ❌ 不要 | ✅ 無料 | C++実装、多形式対応、正確な位置情報 | ⭐⭐⭐⭐⭐ 非常に高速 |
| **OpenCV WeChat** | Apache 2.0 | `pip install opencv-contrib-python` | ❌ 不要 | ✅ 無料 | CNN高精度、低品質画像に強い | ⭐⭐⭐⭐ 高速（やや遅い） |

### 詳細情報

#### 1. OpenCV Standard (cv2.QRCodeDetector)
```python
import cv2
detector = cv2.QRCodeDetector()
data, bbox, _ = detector.detectAndDecode(image)
```

**特徴:**
- ✅ OpenCVに標準搭載
- ✅ 追加モデル不要
- ✅ 軽量・高速
- ✅ 基本的なQRコード検出に最適
- ✅ 画像の一部にQRがあっても検出可能
- ✅ 暗い背景でも検出可能（QRが明るければ）

**商用利用:** 完全無料、制限なし

---

#### 2. zxing-cpp (C++版ZXing)
```python
import zxingcpp
results = zxingcpp.read_barcodes(image)
```

**特徴:**
- ✅ C++実装で高速
- ✅ sudo不要（pip installのみ）
- ✅ 多形式対応（QR、DataMatrix、Code128など）
- ✅ 正確な4点座標を返す
- ✅ フォーマット情報も取得可能
- ✅ pyzbarよりインストールが簡単

**商用利用:** 完全無料、制限なし

---

#### 3. OpenCV WeChat (高精度版)
```python
import cv2
detector = cv2.wechat_qrcode.WeChatQRCode()
data, points = detector.detectAndDecode(image)
```

**特徴:**
- ✅ CNNベースの高精度検出
- ✅ 低品質画像でも検出可能
- ✅ 超解像処理を含む
- ✅ OpenCV 5.0以降は内蔵モデル使用（外部ファイル不要）
- ✅ 複雑な背景に強い
- ⚠️ 他のライブラリより少し遅い

**商用利用:** 完全無料、制限なし

---

## ❌ 検討されたが却下されたライブラリ

### 却下理由別一覧

#### 【理由1】sudo権限が必要（システムライブラリのインストール必須）

| ライブラリ | ライセンス | 却下理由 | 代替採用 |
|-----------|----------|---------|---------|
| **pyzbar** | LGPL (libzbar) | libzbarのインストールにsudo必要<br>`sudo apt-get install libzbar0` | zxing-cpp |

**詳細:**
```python
# pyzbarの場合
import pyzbar.pyzbar as pyzbar
results = pyzbar.decode(image)
```

**問題点:**
- ❌ システムレベルのlibzbarインストールが必要
- ❌ Docker環境やサーバーレス環境で使いにくい
- ❌ sudo権限がない環境では使用不可
- ❌ Windows/Macで追加セットアップ必要

**なぜ却下:**
ユーザーが「sudoを使わずにZXingを利用することはできませんか？」と質問したため、sudo不要なzxing-cppを採用しました。

---

#### 【理由2】商用有料（ライセンス料が必要）

| ライブラリ | ライセンス | 価格 | 却下理由 |
|-----------|----------|------|---------|
| **Dynamsoft Barcode Reader** | 商用ライセンス | 有料 | 商用利用にライセンス料が必要 |
| **Scandit** | 商用ライセンス | 有料 | 商用利用にライセンス料が必要 |

**詳細:**

##### Dynamsoft Barcode Reader (dbr)
```python
from dbr import BarcodeReader
reader = BarcodeReader()
results = reader.decode_file(image_path)
```

**特徴:**
- 高精度
- 企業向けサポート
- ❌ 商用利用に年間ライセンス料が必要

**なぜ却下:**
ユーザーが「商用利用で完全無料なライブラリ以外の機能は削除しましょう」と指示したため。

##### Scandit
**特徴:**
- モバイルSDK
- AR機能
- ❌ 商用利用に年間ライセンス料が必要
- ❌ ライセンスキーが必要

**なぜ却下:**
商用利用にライセンス料が必要なため。

---

#### 【理由3】商用利用が条件付き

| ライブラリ | ライセンス | 却下理由 |
|-----------|----------|---------|
| **Google ML Kit** | 独自ライセンス | 商用利用に条件あり、Python直接利用不可 |

**詳細:**
```javascript
// ML Kit (モバイルアプリのみ)
const barcodeScanner = mlkit.barcodeScanning();
```

**特徴:**
- Googleの機械学習モデル
- モバイルアプリ向け
- ❌ Pythonから直接利用不可
- ❌ 商用利用に条件あり
- ❌ Firebase経由での利用が必要な場合あり

**なぜ却下:**
商用利用の条件が不明確で、Python直接利用ができないため。

---

#### 【理由4】パッケージが存在しない / インストール不可

| ライブラリ | 却下理由 |
|-----------|---------|
| **python-zxing** | PyPIに存在しない、`pip install`で失敗 |

**詳細:**
```bash
# 実行結果
$ pip install python-zxing
ERROR: Could not find a version that satisfies the requirement python-zxing
```

**なぜ却下:**
パッケージがPyPIに存在せず、インストールできないため。代わりにzxing-cppを採用。

---

## 📊 採用vs却下の比較表

| 項目 | OpenCV Standard | zxing-cpp | OpenCV WeChat | pyzbar | Dynamsoft | Scandit | ML Kit |
|-----|----------------|-----------|---------------|--------|-----------|---------|---------|
| **商用無料** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ⚠️ |
| **sudo不要** | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | - |
| **Python対応** | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ | ❌ |
| **pip install** | ✅ | ✅ | ✅ | ⚠️ | ✅ | ⚠️ | ❌ |
| **画像一部QR** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **暗い画像** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **処理速度** | 非常に高速 | 非常に高速 | 高速 | 高速 | 高速 | 高速 | 高速 |
| **精度** | 高 | 高 | 非常に高 | 高 | 非常に高 | 非常に高 | 非常に高 |
| **採用状況** | ✅ 採用 | ✅ 採用 | ✅ 採用 | ❌ sudo必要 | ❌ 有料 | ❌ 有料 | ❌ 条件付き |

---

## 🎯 最終決定の理由

### なぜこの3つを採用したのか？

1. **完全無料**
   - すべてApache 2.0ライセンス
   - 商用利用に制限なし
   - ライセンス料不要

2. **インストールが簡単**
   - sudo権限不要
   - `pip install`のみで完結
   - Docker/サーバーレス環境でも使用可能

3. **高い検出性能**
   - 画像の一部にQRコードがあっても検出可能
   - 暗い背景でも検出可能
   - 様々なサイズのQRコードに対応

4. **実用的**
   - Pythonから直接使用可能
   - ドキュメントが充実
   - コミュニティが活発

---

## 💼 商用プロジェクトでの使用について

### ✅ 採用ライブラリは完全無料

すべてのライブラリがApache 2.0ライセンスのため、以下が可能です：

- ✅ 商用プロジェクトで自由に使用
- ✅ ソースコード公開不要
- ✅ ライセンス料不要
- ✅ 利用制限なし
- ✅ エンタープライズ用途でも使用可能

### ⚠️ 却下ライブラリを使う場合

- **Dynamsoft/Scandit**: 年間ライセンス料が必要（数十万〜数百万円）
- **pyzbar**: LGPL（libzbar）のため、動的リンクなら商用利用可能だが、sudo必要
- **Google ML Kit**: 利用規約を確認し、商用利用の条件をクリアする必要あり

---

## 📝 まとめ

### 採用した3つのライブラリ

| # | ライブラリ | 主な理由 |
|---|-----------|---------|
| 1 | OpenCV Standard | 軽量・高速・標準実装 |
| 2 | zxing-cpp | sudo不要で多機能 |
| 3 | OpenCV WeChat | 高精度・低品質画像に強い |

### 却下した4つのライブラリ

| # | ライブラリ | 却下理由 |
|---|-----------|---------|
| 1 | pyzbar | sudo権限が必要 |
| 2 | Dynamsoft | 商用有料 |
| 3 | Scandit | 商用有料 |
| 4 | Google ML Kit | 商用条件付き、Python非対応 |
| 5 | python-zxing | パッケージ不存在 |

---

## 🚀 使い方

### 採用ライブラリのインストール

```bash
# すべて一括インストール
pip install -r requirements.txt

# 個別インストール
pip install opencv-python
pip install opencv-contrib-python
pip install zxing-cpp
```

### アプリの起動

```bash
streamlit run app.py
```

ブラウザで http://localhost:8501 にアクセスして、3つのライブラリの性能を比較できます！

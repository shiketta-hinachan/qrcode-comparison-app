# QRコード読み取りライブラリ比較検証アプリ（商用無料版）

このアプリは、**商用利用で完全無料**な3つのQRコード読み取りライブラリの読み取り精度と処理時間を比較検証するStreamlitアプリケーションです。

## 特徴

- 📊 商用無料ライブラリのみを厳選（すべてApache 2.0ライセンス）
- ⚡ 高速処理（ライブラリの内部最適化を最大活用）
- 📈 処理時間の可視化
- 🖼️ 複数画像の一括比較（何枚でも同時アップロード可能）
- 🔬 前処理パイプライン可視化（ライブラリの内部処理を再現）
- 📋 詳細な実行ログとエラートレース
- 🎯 シンプル設計（明度調整なし、ライブラリ側で自動処理）

## 搭載ライブラリ

すべてのライブラリが**Apache 2.0ライセンス**で、**商用利用無料・制限なし**です。

| ライブラリ | 説明 | 特徴 |
|-----------|------|------|
| OpenCV Standard | cv2.QRCodeDetector | 標準実装、軽量 |
| zxing-cpp | C++版ZXing | 高速、多機能 |
| OpenCV WeChat | cv2.wechat_qrcode.WeChatQRCode | 高精度、ディープラーニング |

### ✅ 画像の一部にQRコードがある場合でも検出可能

**すべてのライブラリは、QRコードが画像全体でなく一部にある場合でも正常に検出できます。**

検出成功の条件：
- QRコードのサイズが十分大きい（150x150ピクセル以上推奨）
- QRコードが画像の端から適切な距離がある
- QRコードが完全に画像内に収まっている

詳細なテスト結果は [DETECTION_RESULTS.md](DETECTION_RESULTS.md) を参照してください。

## セットアップ

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

**注意**: このアプリはOpenCV 4.10系を使用しており、WeChatQRCodeのモデルファイルは`wechat_qrcode_models/`ディレクトリに含まれています。

## 実行方法

```bash
streamlit run app.py
# または
python -m streamlit run app.py
```

ブラウザが自動的に開き、アプリが起動します。

## 使い方

1. **画像をアップロード**
   - 左カラムに画像1をアップロード
   - 右カラムに画像2をアップロード

2. **検証を実行**
   - 「🚀 比較検証を実行」ボタンをクリック
   - 各ライブラリでの読み取り結果が表示されます

3. **結果を確認**
   - 成功/失敗、処理時間、デコード結果
   - 処理時間比較グラフ
   - 詳細な実行ログ

## 出力結果

### 比較表

各ライブラリについて以下の情報が表示されます:

- ライブラリ名
- 成功/失敗
- デコード結果（QRコードの内容）
- 処理時間

### 統計情報

- 各画像の成功ライブラリ数
- 平均処理時間

### グラフ

- 処理時間の比較グラフ（棒グラフ）

### 実行ログ

- 各ライブラリの詳細な処理ログ
- エラー発生時のスタックトレース
- フィルタリング機能
- ログのダウンロード機能

## ライブラリの内部処理について

各ライブラリは以下の前処理を**自動的に**実行します:

1. **適応的2値化** - 暗い画像でも検出可能
2. **コントラスト正規化** - QRコードの白黒を最適化
3. **ノイズ除去** - エッジ検出と強調
4. **OpenCV WeChatはCNNベースの高度な前処理**

そのため、元画像をそのまま渡すことで**ライブラリの最適化を最大限活用**できます。

詳細は [PREPROCESSING_ANALYSIS.md](PREPROCESSING_ANALYSIS.md) を参照してください。

## ライブラリ詳細

### OpenCV Standard (cv2.QRCodeDetector)

- **ライセンス**: Apache 2.0
- **商用利用**: ✅ 完全無料
- **特徴**: 
  - 軽量で高速
  - 追加モデル不要
  - 基本的なQRコード検出

### zxing-cpp (C++版ZXing)

- **ライセンス**: Apache 2.0
- **商用利用**: ✅ 完全無料
- **インストール**: `pip install zxing-cpp`（sudo不要）
- **特徴**:
  - C++実装で高速
  - 多形式対応（QR、DataMatrix、Code128など）
  - pyzbarよりインストールが簡単

### OpenCV WeChat (高精度版)

- **ライセンス**: Apache 2.0
- **商用利用**: ✅ 完全無料
- **特徴**:
  - CNNベースの高精度検出
  - 低品質画像でも検出可能
  - 超解像処理を含む
  - モデルファイル同梱（wechat_qrcode_models/）

## トラブルシューティング

### zxing-cppが動作しない

```bash
pip uninstall zxing-cpp
pip install zxing-cpp
```

### OpenCV WeChatでエラーが出る

- OpenCV 4.10系を使用しているか確認: `python -c "import cv2; print(cv2.__version__)"`
- モデルファイルが`wechat_qrcode_models/`ディレクトリに存在するか確認

### OpenCVでQRコードが検出できない

- ログセクションで詳細なエラーを確認
- 画像の品質を確認
- 明度調整の範囲を広げる

## テスト画像の生成

テスト用のQRコード画像を自動生成できます：

```bash
pip install qrcode[pil]
python generate_test_images.py
```

`test_images/` ディレクトリに6枚のテスト画像が生成されます。

## 商用利用について

**すべてのライブラリがApache 2.0ライセンスです。**

- ✅ 商用プロジェクトで無料で使用可能
- ✅ 制限なし
- ✅ ライセンス料不要
- ✅ ソースコード公開不要

安心して商用プロジェクトでご利用ください。

**他のライブラリとの比較は [LIBRARY_COMPARISON.md](LIBRARY_COMPARISON.md) を参照してください。**

## 参考資料

- [OpenCV Documentation](https://docs.opencv.org/)
- [zxing-cpp GitHub](https://github.com/zxing-cpp/zxing-cpp)
- [OpenCV WeChat QRCode](https://docs.opencv.org/4.x/dd/d63/group__wechat__qrcode.html)

## ライセンス

このプロジェクトはMITライセンスです。

使用している各ライブラリはすべてApache 2.0ライセンスです。

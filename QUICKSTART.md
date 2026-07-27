# クイックスタートガイド

## 最小構成で動作させる（5分）

### 1. インストール

```bash
# プロジェクトディレクトリに移動
cd qrcode-comparison-app

# 依存関係をインストール
pip install streamlit opencv-python opencv-contrib-python pillow numpy pandas pyzbar plotly
```

### 2. システム依存関係（pyzbar用）

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install libzbar0
```

#### macOS
```bash
brew install zbar
```

#### Windows
- 通常は自動でインストールされます
- エラーが出る場合は[zbar公式](http://zbar.sourceforge.net/)からバイナリをダウンロード

### 3. アプリを起動

```bash
streamlit run app.py
```

ブラウザが自動的に開きます（開かない場合は http://localhost:8501 にアクセス）

### 4. テスト画像を準備

#### オプション1: 自分のQRコード画像を使用
- スマートフォンでQRコードを撮影
- または、オンラインQRコードジェネレーターで生成

#### オプション2: テスト画像を自動生成

```bash
# qrcodeライブラリをインストール
pip install qrcode[pil]

# テスト画像を生成
python generate_test_images.py
```

`test_images/` ディレクトリに6枚のQRコード画像が生成されます。

### 5. アプリで検証

1. ブラウザでアプリを開く
2. 「画像ファイル1をアップロード」で画像を選択
3. 「画像ファイル2をアップロード」で別の画像を選択
4. 「🚀 比較検証を実行」ボタンをクリック

## この構成で使えるライブラリ

- ✅ **OpenCV**: 完全に動作
- ✅ **ZXing (pyzbar)**: 完全に動作
- ⚠️ **Google ML Kit**: プレースホルダー（動作せず）
- ⚠️ **Dynamsoft**: ライセンスキー必要
- ⚠️ **Scandit**: プレースホルダー（動作せず）

**最小構成ではOpenCVとZXingの2つが動作します。**

## 商用ライブラリを追加する

### Dynamsoft を有効化

1. [Dynamsoft公式サイト](https://www.dynamsoft.com/customer/license/trialLicense?product=dbr)で無料トライアルライセンスを取得

2. ライセンスキーをコピー

3. アプリのサイドバー「Dynamsoft License Key」に貼り付け

4. 再度「比較検証を実行」

### Google Cloud Vision API を使用（高度）

1. GCPプロジェクトを作成

2. Cloud Vision APIを有効化

3. サービスアカウントキーを作成・ダウンロード

4. 環境変数を設定:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/key.json"
   ```

5. ライブラリをインストール:
   ```bash
   pip install google-cloud-vision
   ```

6. `app.py`の`test_mlkit_placeholder`関数を実装

## トラブルシューティング

### pyzbarがimportできない

```bash
# Ubuntu/Debian
sudo apt-get install libzbar0

# macOS
brew install zbar

# それでもダメな場合
pip uninstall pyzbar
pip install pyzbar
```

### Streamlitが起動しない

```bash
# Streamlitを再インストール
pip uninstall streamlit
pip install streamlit
```

### 画像がアップロードできない

- ファイル形式を確認（PNG, JPG, JPEGのみ対応）
- ファイルサイズを確認（200MB以下推奨）

## 次のステップ

- より多くのテスト画像で検証
- 明度調整のパラメータを調整
- 商用ライブラリのライセンスを取得して精度を比較
- 結果をCSVでエクスポート（カスタマイズ）

## サポート

問題が発生した場合:
1. README.mdの詳細を確認
2. requirements.txtの全ライブラリが正しくインストールされているか確認
3. Pythonバージョンを確認（3.8以上推奨）

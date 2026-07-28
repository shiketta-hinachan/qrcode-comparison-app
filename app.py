import streamlit as st
import cv2
import numpy as np
from PIL import Image
import time
import pandas as pd
import plotly.graph_objects as go
from preprocessing_visualizer import visualize_preprocessing, get_image_statistics, compare_preprocessing_methods

# zxing-cppのインポート
ZXING_CPP_AVAILABLE = False
try:
    import zxingcpp
    ZXING_CPP_AVAILABLE = True
except ImportError:
    st.warning("⚠️ zxing-cpp は利用できません")

# ページ設定
st.set_page_config(
    page_title="QRコード読み取りライブラリ比較検証",
    page_icon="📊",
    layout="wide"
)

# タイトル
st.title("📊 QRコード読み取りライブラリ比較検証アプリ")
st.markdown("""
このアプリは、**商用利用で完全無料**な3つのQRコード読み取りライブラリの性能を比較します。

**搭載ライブラリ（すべてApache 2.0ライセンス）:**
1. **OpenCV Standard** - 軽量・高速
2. **zxing-cpp** - C++実装、多機能
3. **OpenCV WeChat** - 高精度、ディープラーニング

**特徴:**
- ✅ 商用無料・制限なし
- ✅ sudo権限不要
- ✅ ライブラリの内部最適化を最大活用
- ✅ 明度調整なし（ライブラリ側で自動処理）
""")

# OpenCV情報を表示
with st.expander("🔧 環境情報", expanded=False):
    st.text(f"OpenCV Version: {cv2.__version__}")
    st.text(f"OpenCV Build Info:")
    st.code(cv2.getBuildInformation(), language="text")

    # wechat_qrcodeモジュールの状態を確認
    if hasattr(cv2, 'wechat_qrcode'):
        st.success("✅ cv2.wechat_qrcode module is available")
        if hasattr(cv2.wechat_qrcode, 'WeChatQRCode'):
            st.success("✅ cv2.wechat_qrcode.WeChatQRCode is available")
        else:
            st.error(f"❌ cv2.wechat_qrcode.WeChatQRCode NOT found. Available: {dir(cv2.wechat_qrcode)}")
    else:
        st.error("❌ cv2.wechat_qrcode module NOT found")

# 画像アップロード
st.header("📤 画像アップロード")
uploaded_files = st.file_uploader(
    "QRコード画像をアップロード（複数選択可）",
    type=['png', 'jpg', 'jpeg'],
    accept_multiple_files=True
)

if uploaded_files:
    st.info(f"✅ {len(uploaded_files)}枚の画像がアップロードされました")

    # プレビュー表示
    with st.expander("📷 アップロード画像プレビュー", expanded=True):
        cols = st.columns(min(len(uploaded_files), 4))
        for idx, file in enumerate(uploaded_files):
            col_idx = idx % 4
            with cols[col_idx]:
                img = Image.open(file)
                st.image(img, caption=file.name, use_column_width=True)


# ログ収集用
execution_logs = []

def add_log(message, level="INFO"):
    """ログメッセージを追加"""
    import datetime
    timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
    execution_logs.append({
        'timestamp': timestamp,
        'level': level,
        'message': message
    })


# 各ライブラリの読み取り関数
def test_opencv_standard(image_array, image_name):
    """OpenCV標準QRCodeDetectorで読み取る"""
    try:
        add_log(f"OpenCV Standard [{image_name}]: テスト開始")
        detector = cv2.QRCodeDetector()

        start_time = time.time()
        data, bbox, _ = detector.detectAndDecode(image_array)
        elapsed = time.time() - start_time

        if data:
            add_log(f"OpenCV Standard [{image_name}]: ✅ 成功 (処理時間: {elapsed:.4f}秒)", "SUCCESS")
            return {
                'success': True,
                'data': data,
                'time': elapsed,
                'error': None
            }
        else:
            add_log(f"OpenCV Standard [{image_name}]: ❌ 検出失敗 (処理時間: {elapsed:.4f}秒)", "WARNING")
            return {
                'success': False,
                'data': None,
                'time': elapsed,
                'error': 'QRコードを検出できませんでした'
            }

    except Exception as e:
        import traceback
        add_log(f"OpenCV Standard [{image_name}]: ❌ 例外 - {str(e)}", "ERROR")
        add_log(f"トレースバック:\n{traceback.format_exc()}", "ERROR")
        return {
            'success': False,
            'data': None,
            'time': 0.0,
            'error': str(e)
        }


def test_zxing_cpp(image_array, image_name):
    """zxing-cpp（C++版ZXing）で読み取る"""
    if not ZXING_CPP_AVAILABLE:
        add_log(f"zxing-cpp [{image_name}]: 利用不可", "WARNING")
        return {
            'success': False,
            'data': 'zxing-cpp not available',
            'time': 0.0,
            'error': 'zxing-cpp not installed'
        }

    try:
        add_log(f"zxing-cpp [{image_name}]: テスト開始")
        start_time = time.time()

        results = zxingcpp.read_barcodes(image_array)
        elapsed = time.time() - start_time

        if results:
            add_log(f"zxing-cpp [{image_name}]: ✅ 成功 (処理時間: {elapsed:.4f}秒)", "SUCCESS")
            return {
                'success': True,
                'data': results[0].text,
                'time': elapsed,
                'error': None
            }
        else:
            add_log(f"zxing-cpp [{image_name}]: ❌ 検出失敗 (処理時間: {elapsed:.4f}秒)", "WARNING")
            return {
                'success': False,
                'data': None,
                'time': elapsed,
                'error': 'QRコードを検出できませんでした'
            }

    except Exception as e:
        add_log(f"zxing-cpp [{image_name}]: ❌ 例外 - {str(e)}", "ERROR")
        return {
            'success': False,
            'data': None,
            'time': 0.0,
            'error': str(e)
        }


def test_opencv_wechat(image_array, image_name):
    """OpenCV WeChatQRCodeで読み取る"""
    try:
        add_log(f"OpenCV WeChat [{image_name}]: テスト開始")
        add_log(f"OpenCV version: {cv2.__version__}")

        # wechat_qrcodeモジュールの存在確認
        if not hasattr(cv2, 'wechat_qrcode'):
            error_msg = "cv2.wechat_qrcode module not found. opencv-contrib-python-headless may not be installed correctly."
            add_log(f"OpenCV WeChat [{image_name}]: ❌ {error_msg}", "ERROR")
            return {
                'success': False,
                'data': None,
                'time': 0.0,
                'error': error_msg
            }

        # WeChatQRCodeクラスの存在確認
        if not hasattr(cv2.wechat_qrcode, 'WeChatQRCode'):
            error_msg = f"cv2.wechat_qrcode.WeChatQRCode not found. Available: {dir(cv2.wechat_qrcode)}"
            add_log(f"OpenCV WeChat [{image_name}]: ❌ {error_msg}", "ERROR")
            return {
                'success': False,
                'data': None,
                'time': 0.0,
                'error': error_msg
            }

        # OpenCV 5.0以降は引数なしで初期化（内蔵モデル使用）
        add_log(f"OpenCV WeChat [{image_name}]: Initializing WeChatQRCode detector...")
        detector = cv2.wechat_qrcode.WeChatQRCode()
        add_log(f"OpenCV WeChat [{image_name}]: Detector initialized successfully")

        start_time = time.time()
        data, points = detector.detectAndDecode(image_array)
        elapsed = time.time() - start_time

        if data and data[0]:
            add_log(f"OpenCV WeChat [{image_name}]: ✅ 成功 (処理時間: {elapsed:.4f}秒)", "SUCCESS")
            return {
                'success': True,
                'data': data[0],
                'time': elapsed,
                'error': None
            }
        else:
            add_log(f"OpenCV WeChat [{image_name}]: ❌ 検出失敗 (処理時間: {elapsed:.4f}秒)", "WARNING")
            return {
                'success': False,
                'data': None,
                'time': elapsed,
                'error': 'QRコードを検出できませんでした'
            }

    except Exception as e:
        import traceback
        add_log(f"OpenCV WeChat [{image_name}]: ❌ 例外 - {str(e)}", "ERROR")
        add_log(f"トレースバック:\n{traceback.format_exc()}", "ERROR")
        add_log(f"cv2.__version__: {cv2.__version__}", "ERROR")
        add_log(f"cv2.__file__: {cv2.__file__}", "ERROR")
        return {
            'success': False,
            'data': None,
            'time': 0.0,
            'error': str(e)
        }


def run_comparison(image, image_name):
    """全ライブラリで比較検証を実行"""
    # PIL ImageをOpenCV形式に変換
    image_array = np.array(image)
    image_bgr = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)

    results = {}
    results['OpenCV Standard'] = test_opencv_standard(image_bgr, image_name)
    results['zxing-cpp'] = test_zxing_cpp(image_bgr, image_name)
    results['OpenCV WeChat'] = test_opencv_wechat(image_bgr, image_name)

    return results


def create_results_dataframe(all_results):
    """全画像の結果をDataFrameに変換"""
    rows = []
    for image_name, lib_results in all_results.items():
        for lib_name, result in lib_results.items():
            rows.append({
                '画像名': image_name,
                'ライブラリ': lib_name,
                '成功/失敗': '✓ 成功' if result['success'] else '✗ 失敗',
                'デコード結果': result['data'] if result['data'] else (result.get('error', '-')),
                '処理時間 (秒)': f"{result['time']:.4f}",
            })

    return pd.DataFrame(rows)


def create_performance_chart(all_results):
    """処理時間の比較チャートを作成"""
    libraries = ['OpenCV Standard', 'zxing-cpp', 'OpenCV WeChat']
    image_names = list(all_results.keys())

    data = []
    for lib in libraries:
        times = [all_results[img][lib]['time'] for img in image_names]
        data.append(go.Bar(name=lib, x=image_names, y=times))

    fig = go.Figure(data=data)

    fig.update_layout(
        title='処理時間比較（ライブラリ別）',
        xaxis_title='画像',
        yaxis_title='処理時間 (秒)',
        barmode='group',
        height=400
    )

    return fig


# 実行ボタン
if st.button("🚀 比較検証を実行", type="primary"):
    if not uploaded_files:
        st.error("⚠️ 画像をアップロードしてください")
    else:
        # ログをクリア
        execution_logs.clear()
        add_log("=== 比較検証を開始します ===")

        st.header("📊 比較結果")

        # 全画像の結果を格納
        all_results = {}

        # プログレスバー
        progress_bar = st.progress(0)
        status_text = st.empty()

        # 各画像でテスト
        for idx, file in enumerate(uploaded_files):
            status_text.text(f"処理中: {file.name} ({idx+1}/{len(uploaded_files)})")

            image = Image.open(file)
            results = run_comparison(image, file.name)
            all_results[file.name] = results

            progress_bar.progress((idx + 1) / len(uploaded_files))

        status_text.text("✅ 処理完了！")

        # 結果表示
        st.subheader("📋 全結果一覧")
        df_all = create_results_dataframe(all_results)
        st.dataframe(df_all, use_container_width=True)

        # 統計情報
        st.header("📈 統計情報")

        col1, col2, col3 = st.columns(3)

        with col1:
            total_tests = len(uploaded_files) * 3  # 3つのライブラリ
            total_success = sum(1 for img_results in all_results.values()
                              for result in img_results.values() if result['success'])
            st.metric("総成功数", f"{total_success} / {total_tests}")

        with col2:
            avg_time_all = sum(result['time']
                             for img_results in all_results.values()
                             for result in img_results.values()) / total_tests
            st.metric("平均処理時間", f"{avg_time_all:.4f}秒")

        with col3:
            success_rate = (total_success / total_tests) * 100
            st.metric("成功率", f"{success_rate:.1f}%")

        # ライブラリ別統計
        st.subheader("📊 ライブラリ別統計")
        lib_stats = []
        for lib in ['OpenCV Standard', 'zxing-cpp', 'OpenCV WeChat']:
            lib_success = sum(1 for img_results in all_results.values()
                            if img_results[lib]['success'])
            lib_avg_time = sum(img_results[lib]['time']
                             for img_results in all_results.values()) / len(uploaded_files)
            lib_stats.append({
                'ライブラリ': lib,
                '成功数': f"{lib_success} / {len(uploaded_files)}",
                '成功率': f"{(lib_success / len(uploaded_files)) * 100:.1f}%",
                '平均処理時間': f"{lib_avg_time:.4f}秒"
            })

        st.dataframe(pd.DataFrame(lib_stats), use_container_width=True)

        # 処理時間チャート
        st.subheader("⏱️ 処理時間比較グラフ")
        chart = create_performance_chart(all_results)
        st.plotly_chart(chart, use_container_width=True)

        # 前処理可視化
        st.header("🔬 前処理パイプライン可視化")
        st.markdown("""
        ライブラリが内部で行う可能性のある前処理を再現・可視化します。
        これにより、ライブラリがどのように画像を処理しているかを理解できます。
        """)

        # 可視化する画像を選択
        selected_image_name = st.selectbox(
            "可視化する画像を選択",
            list(all_results.keys())
        )

        # 選択された画像を読み込み
        selected_file = next(f for f in uploaded_files if f.name == selected_image_name)
        selected_pil = Image.open(selected_file)
        selected_array = np.array(selected_pil)
        selected_bgr = cv2.cvtColor(selected_array, cv2.COLOR_RGB2BGR)

        # 画像統計
        stats = get_image_statistics(selected_bgr)

        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("平均明度", f"{stats['mean']:.1f}")
        col2.metric("標準偏差", f"{stats['std']:.1f}")
        col3.metric("最小値", f"{stats['min']:.0f}")
        col4.metric("最大値", f"{stats['max']:.0f}")
        col5.metric("中央値", f"{stats['median']:.1f}")

        # タブで表示を切り替え
        tab1, tab2 = st.tabs(["📋 処理パイプライン", "🔄 2値化手法比較"])

        with tab1:
            st.markdown("### 一般的なQRコード前処理パイプライン")
            st.markdown("OpenCV、zxing-cpp、WeChatQRCodeが内部で行う可能性のある処理段階を可視化します。")

            # 前処理パイプラインを実行
            steps = visualize_preprocessing(selected_bgr)

            # グリッド表示（3列）
            step_items = list(steps.items())
            for i in range(0, len(step_items), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(step_items):
                        key, step = step_items[i + j]
                        with cols[j]:
                            # BGR to RGB変換
                            img_rgb = cv2.cvtColor(step['image'], cv2.COLOR_BGR2RGB)
                            st.image(img_rgb, caption=step['name'], use_column_width=True)
                            st.caption(step['description'])

        with tab2:
            st.markdown("### 2値化手法の比較")
            st.markdown("""
            QRコード検出で最も重要な処理は**2値化**（白黒に分ける処理）です。
            異なる2値化手法がどのように動作するかを比較します。
            """)

            # 2値化手法を比較
            methods = compare_preprocessing_methods(selected_bgr)

            # グリッド表示（2列）
            method_items = list(methods.items())
            for i in range(0, len(method_items), 2):
                cols = st.columns(2)
                for j in range(2):
                    if i + j < len(method_items):
                        key, method = method_items[i + j]
                        with cols[j]:
                            img_rgb = cv2.cvtColor(method['image'], cv2.COLOR_BGR2RGB)
                            st.image(img_rgb, caption=method['name'], use_column_width=True)
                            st.caption(method['description'])

            st.info("""
            💡 **重要な観察ポイント:**
            - **固定閾値**: 暗い画像では真っ黒、明るい画像では真っ白になりやすい
            - **大津の2値化**: 全体の明度分布から最適な閾値を決定（一般的に良好）
            - **適応的2値化**: 局所的な明度に応じて閾値を変える（暗い画像でも検出可能）

            ライブラリは主に**適応的2値化**または類似の手法を使用するため、
            元画像が暗くても正常に検出できます。
            """)

        # 詳細結果
        with st.expander("詳細結果を表示"):
            for image_name, results in all_results.items():
                st.subheader(f"📷 {image_name}")
                st.json(results)

        # 実行ログセクション
        st.header("📋 実行ログ")
        st.markdown("各ライブラリの詳細な実行ログです。")

        # ログレベルでフィルタリング
        log_filter = st.multiselect(
            "ログレベルでフィルタ",
            ["INFO", "SUCCESS", "WARNING", "ERROR"],
            default=["SUCCESS", "WARNING", "ERROR"]
        )

        filtered_logs = [log for log in execution_logs if log['level'] in log_filter]

        if filtered_logs:
            # ログをDataFrameで表示
            log_df = pd.DataFrame(filtered_logs)
            st.dataframe(log_df, use_container_width=True, height=400)

            # ログのダウンロードボタン
            log_text = "\n".join([f"[{log['timestamp']}] [{log['level']}] {log['message']}" for log in filtered_logs])
            st.download_button(
                label="📥 ログをダウンロード",
                data=log_text,
                file_name="qrcode_comparison_log.txt",
                mime="text/plain"
            )
        else:
            st.info("フィルタ条件に一致するログがありません")


# フッター
st.markdown("---")
st.markdown("""
### 📝 搭載ライブラリ（すべて商用無料）

| ライブラリ | ライセンス | 特徴 |
|-----------|----------|------|
| OpenCV Standard | Apache 2.0 | 標準のQRCodeDetector、軽量・高速 |
| zxing-cpp | Apache 2.0 | C++実装、多機能、正確な位置情報 |
| OpenCV WeChat | Apache 2.0 | CNN高精度、低品質画像に強い |

**すべてのライブラリは商用プロジェクトで無料で制限なく使用できます。**

### 💡 ライブラリの内部処理について

各ライブラリは以下の前処理を**自動的に**実行します:
- ✅ 適応的2値化（暗い画像でも検出可能）
- ✅ コントラスト正規化
- ✅ ノイズ除去とエッジ強調
- ✅ OpenCV WeChatはCNNベースの高度な前処理

そのため、元画像をそのまま渡すことで**ライブラリの最適化を最大限活用**できます。

### 🔗 詳細情報
- [ライブラリ比較表](LIBRARY_COMPARISON.md)
- [前処理分析レポート](PREPROCESSING_ANALYSIS.md)
- [検出結果詳細](DETECTION_RESULTS.md)
""")

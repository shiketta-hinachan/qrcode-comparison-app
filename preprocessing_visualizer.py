#!/usr/bin/env python3
"""
QRコード前処理の可視化
ライブラリが内部で行うであろう処理を再現
"""

import cv2
import numpy as np
from PIL import Image

def visualize_preprocessing(image_array):
    """
    QRコード検出の一般的な前処理パイプラインを可視化

    Returns:
        dict: 各処理段階の画像を含む辞書
    """
    steps = {}

    # ステップ0: 元画像
    steps['0_original'] = {
        'name': '元画像',
        'image': image_array.copy(),
        'description': 'アップロードされた元画像'
    }

    # ステップ1: グレースケール化
    if len(image_array.shape) == 3:
        gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
    else:
        gray = image_array.copy()

    steps['1_grayscale'] = {
        'name': 'グレースケール化',
        'image': cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR),
        'description': 'カラー情報を削除し、輝度のみを保持'
    }

    # ステップ2: ガウシアンブラー（ノイズ除去）
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    steps['2_blur'] = {
        'name': 'ガウシアンブラー',
        'image': cv2.cvtColor(blurred, cv2.COLOR_GRAY2BGR),
        'description': 'ノイズを除去し、滑らかにする'
    }

    # ステップ3: 適応的2値化
    adaptive_thresh = cv2.adaptiveThreshold(
        blurred, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, 2
    )
    steps['3_adaptive_threshold'] = {
        'name': '適応的2値化',
        'image': cv2.cvtColor(adaptive_thresh, cv2.COLOR_GRAY2BGR),
        'description': '局所的な明度に応じて閾値を調整（暗い画像でも検出可能に）'
    }

    # ステップ4: 大津の2値化（比較用）
    _, otsu_thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    steps['4_otsu_threshold'] = {
        'name': '大津の2値化',
        'image': cv2.cvtColor(otsu_thresh, cv2.COLOR_GRAY2BGR),
        'description': '全体の明度から最適な閾値を自動決定'
    }

    # ステップ5: モルフォロジー処理（ノイズ除去）
    kernel = np.ones((3, 3), np.uint8)
    morph_close = cv2.morphologyEx(adaptive_thresh, cv2.MORPH_CLOSE, kernel)
    steps['5_morphology'] = {
        'name': 'モルフォロジー処理',
        'image': cv2.cvtColor(morph_close, cv2.COLOR_GRAY2BGR),
        'description': '小さなノイズを除去し、パターンを強調'
    }

    # ステップ6: エッジ検出
    edges = cv2.Canny(gray, 50, 150)
    steps['6_edges'] = {
        'name': 'エッジ検出',
        'image': cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR),
        'description': 'QRコードの輪郭を検出'
    }

    # ステップ7: コントラスト強調（CLAHE）
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    steps['7_contrast_enhanced'] = {
        'name': 'コントラスト強調',
        'image': cv2.cvtColor(enhanced, cv2.COLOR_GRAY2BGR),
        'description': 'CLAHEによる適応的ヒストグラム均等化'
    }

    # ステップ8: 明度正規化
    normalized = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
    steps['8_normalized'] = {
        'name': '明度正規化',
        'image': cv2.cvtColor(normalized, cv2.COLOR_GRAY2BGR),
        'description': '明度範囲を0-255に正規化'
    }

    return steps


def get_image_statistics(image_array):
    """画像の統計情報を取得"""
    if len(image_array.shape) == 3:
        gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
    else:
        gray = image_array

    return {
        'mean': np.mean(gray),
        'std': np.std(gray),
        'min': np.min(gray),
        'max': np.max(gray),
        'median': np.median(gray)
    }


def compare_preprocessing_methods(image_array):
    """複数の2値化手法を比較"""
    if len(image_array.shape) == 3:
        gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
    else:
        gray = image_array.copy()

    methods = {}

    # 1. 固定閾値（127）
    _, fixed = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    methods['fixed_127'] = {
        'name': '固定閾値 (127)',
        'image': cv2.cvtColor(fixed, cv2.COLOR_GRAY2BGR),
        'description': '明度127を境界に2値化（暗い画像では失敗しやすい）'
    }

    # 2. 大津の方法
    _, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    methods['otsu'] = {
        'name': '大津の2値化',
        'image': cv2.cvtColor(otsu, cv2.COLOR_GRAY2BGR),
        'description': '全体の明度分布から最適な閾値を自動決定'
    }

    # 3. 適応的2値化（平均）
    adaptive_mean = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        11, 2
    )
    methods['adaptive_mean'] = {
        'name': '適応的2値化（平均）',
        'image': cv2.cvtColor(adaptive_mean, cv2.COLOR_GRAY2BGR),
        'description': '局所領域の平均値を閾値として使用'
    }

    # 4. 適応的2値化（ガウシアン）
    adaptive_gaussian = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, 2
    )
    methods['adaptive_gaussian'] = {
        'name': '適応的2値化（ガウシアン）',
        'image': cv2.cvtColor(adaptive_gaussian, cv2.COLOR_GRAY2BGR),
        'description': '局所領域のガウシアン重み付き平均を閾値として使用'
    }

    return methods


if __name__ == "__main__":
    # テスト
    import sys

    if len(sys.argv) < 2:
        print("使用方法: python preprocessing_visualizer.py <image_path>")
        sys.exit(1)

    img = cv2.imread(sys.argv[1])
    if img is None:
        print(f"画像を読み込めませんでした: {sys.argv[1]}")
        sys.exit(1)

    print("前処理パイプラインを実行中...")
    steps = visualize_preprocessing(img)

    print(f"\n{len(steps)}個の処理ステップを生成しました:")
    for key, step in steps.items():
        print(f"  - {step['name']}: {step['description']}")

    print("\n画像統計:")
    stats = get_image_statistics(img)
    for key, value in stats.items():
        print(f"  {key}: {value:.2f}")

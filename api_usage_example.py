#!/usr/bin/env python3
"""
云检测API使用示例
支持文件上传和Base64两种方式调用API
"""

import requests
import base64
import json
from pathlib import Path

# 配置API地址 - 部署后替换为实际地址
API_BASE_URL = "http://your-server-ip:5000"  # 或者 "https://your-domain.com"

def test_health():
    """测试API健康状态"""
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        print("🔍 健康检查结果:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 健康检查失败: {e}")
        return False

def detect_by_file(image_path, conf_threshold=0.5, nms_threshold=0.4):
    """通过文件上传方式进行检测"""
    try:
        with open(image_path, 'rb') as f:
            files = {'image': f}
            data = {
                'conf_threshold': conf_threshold,
                'nms_threshold': nms_threshold
            }
            
            response = requests.post(f"{API_BASE_URL}/detect", files=files, data=data)
            
        if response.status_code == 200:
            result = response.json()
            print(f"📷 文件上传检测结果 ({image_path}):")
            print(f"   检测到 {result['total_detections']} 个目标")
            for i, pred in enumerate(result['predictions']):
                print(f"   目标{i+1}: {pred['class_name']} (置信度: {pred['confidence']:.3f})")
            return result
        else:
            print(f"❌ 检测失败: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 文件上传检测失败: {e}")
        return None

def detect_by_base64(image_path, conf_threshold=0.5, nms_threshold=0.4):
    """通过Base64编码方式进行检测"""
    try:
        # 读取图片并转换为Base64
        with open(image_path, 'rb') as f:
            image_base64 = base64.b64encode(f.read()).decode('utf-8')
        
        data = {
            'image_base64': image_base64,
            'conf_threshold': conf_threshold,
            'nms_threshold': nms_threshold
        }
        
        response = requests.post(
            f"{API_BASE_URL}/detect",
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"📷 Base64检测结果 ({image_path}):")
            print(f"   检测到 {result['total_detections']} 个目标")
            for i, pred in enumerate(result['predictions']):
                print(f"   目标{i+1}: {pred['class_name']} (置信度: {pred['confidence']:.3f})")
            return result
        else:
            print(f"❌ 检测失败: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Base64检测失败: {e}")
        return None

def main():
    """主函数：演示API使用"""
    print("=== 云检测API使用示例 ===")
    print(f"API地址: {API_BASE_URL}")
    print()
    
    # 1. 健康检查
    if not test_health():
        print("❌ API服务不可用，请检查服务状态")
        return
    
    print()
    
    # 2. 图片检测示例
    # 请替换为实际的图片路径
    test_image = "test_image.jpg"  # 放一张测试图片在这里
    
    if Path(test_image).exists():
        print("🚀 开始测试图片检测...")
        print()
        
        # 方式1：文件上传
        detect_by_file(test_image, conf_threshold=0.5)
        print()
        
        # 方式2：Base64编码
        detect_by_base64(test_image, conf_threshold=0.3)
        
    else:
        print(f"⚠️  测试图片 {test_image} 不存在")
        print("请将测试图片放在脚本同目录下并重命名为 test_image.jpg")

if __name__ == "__main__":
    main() 
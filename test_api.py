#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import base64
import json
from PIL import Image
import io
import os

def test_health_check():
    """测试健康检查接口"""
    try:
        response = requests.get('http://localhost:5000/health')
        print("健康检查结果:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        return response.status_code == 200
    except Exception as e:
        print(f"健康检查失败: {e}")
        return False

def test_detection_with_file(image_path):
    """测试文件上传检测"""
    if not os.path.exists(image_path):
        print(f"测试图片不存在: {image_path}")
        return False
    
    try:
        with open(image_path, 'rb') as f:
            files = {'image': f}
            response = requests.post('http://localhost:5000/detect', files=files)
        
        print(f"文件上传检测结果 (状态码: {response.status_code}):")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        return response.status_code == 200
    except Exception as e:
        print(f"文件上传检测失败: {e}")
        return False

def test_detection_with_base64(image_path):
    """测试Base64编码检测"""
    if not os.path.exists(image_path):
        print(f"测试图片不存在: {image_path}")
        return False
    
    try:
        # 读取图片并转换为Base64
        with open(image_path, 'rb') as f:
            image_data = f.read()
            image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        # 发送请求
        data = {
            'image_base64': image_base64,
            'conf_threshold': 0.5,
            'nms_threshold': 0.4
        }
        
        response = requests.post(
            'http://localhost:5000/detect',
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Base64检测结果 (状态码: {response.status_code}):")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        return response.status_code == 200
    except Exception as e:
        print(f"Base64检测失败: {e}")
        return False

def create_test_image():
    """创建一个简单的测试图片"""
    # 创建一个简单的测试图片
    img = Image.new('RGB', (640, 640), color='white')
    
    # 保存测试图片
    test_image_path = 'test_image.jpg'
    img.save(test_image_path)
    print(f"创建测试图片: {test_image_path}")
    return test_image_path

def main():
    """主测试函数"""
    print("开始API测试...")
    print("=" * 50)
    
    # 测试健康检查
    print("1. 测试健康检查接口")
    health_ok = test_health_check()
    print()
    
    if not health_ok:
        print("健康检查失败，请确保服务正在运行")
        return
    
    # 创建测试图片
    print("2. 创建测试图片")
    test_image = create_test_image()
    print()
    
    # 测试文件上传检测
    print("3. 测试文件上传检测")
    file_ok = test_detection_with_file(test_image)
    print()
    
    # 测试Base64检测
    print("4. 测试Base64编码检测")
    base64_ok = test_detection_with_base64(test_image)
    print()
    
    # 清理测试文件
    if os.path.exists(test_image):
        os.remove(test_image)
        print(f"清理测试文件: {test_image}")
    
    # 总结
    print("=" * 50)
    print("测试总结:")
    print(f"健康检查: {'✓' if health_ok else '✗'}")
    print(f"文件上传检测: {'✓' if file_ok else '✗'}")
    print(f"Base64检测: {'✓' if base64_ok else '✗'}")
    
    if all([health_ok, file_ok, base64_ok]):
        print("所有测试通过！API服务运行正常。")
    else:
        print("部分测试失败，请检查服务配置。")

if __name__ == '__main__':
    main() 
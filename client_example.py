#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
YOLO检测API客户端示例
演示如何调用云端部署的YOLO检测API
"""

import requests
import base64
import json
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

class YOLOClient:
    def __init__(self, api_url="http://localhost:5000"):
        """初始化客户端"""
        self.api_url = api_url
        self.session = requests.Session()
    
    def health_check(self):
        """健康检查"""
        try:
            response = self.session.get(f"{self.api_url}/health")
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            print(f"健康检查失败: {e}")
            return None
    
    def detect_from_file(self, image_path, conf_threshold=0.5, nms_threshold=0.4):
        """从文件路径检测"""
        if not os.path.exists(image_path):
            print(f"图片文件不存在: {image_path}")
            return None
        
        try:
            with open(image_path, 'rb') as f:
                files = {'image': f}
                data = {
                    'conf_threshold': conf_threshold,
                    'nms_threshold': nms_threshold
                }
                response = self.session.post(f"{self.api_url}/detect", files=files, data=data)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"检测失败: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"文件检测失败: {e}")
            return None
    
    def detect_from_base64(self, image_path, conf_threshold=0.5, nms_threshold=0.4):
        """从Base64编码检测"""
        if not os.path.exists(image_path):
            print(f"图片文件不存在: {image_path}")
            return None
        
        try:
            # 读取图片并转换为Base64
            with open(image_path, 'rb') as f:
                image_data = f.read()
                image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            # 发送请求
            data = {
                'image_base64': image_base64,
                'conf_threshold': conf_threshold,
                'nms_threshold': nms_threshold
            }
            
            response = self.session.post(
                f"{self.api_url}/detect",
                json=data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"检测失败: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Base64检测失败: {e}")
            return None
    
    def detect_batch(self, image_paths, conf_threshold=0.5, nms_threshold=0.4):
        """批量检测"""
        try:
            # 读取所有图片并转换为Base64
            images_base64 = []
            for image_path in image_paths:
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as f:
                        image_data = f.read()
                        image_base64 = base64.b64encode(image_data).decode('utf-8')
                        images_base64.append(image_base64)
                else:
                    print(f"图片文件不存在: {image_path}")
                    images_base64.append("")  # 空字符串表示无效图片
            
            # 发送批量请求
            data = {
                'images': images_base64,
                'conf_threshold': conf_threshold,
                'nms_threshold': nms_threshold
            }
            
            response = self.session.post(
                f"{self.api_url}/detect_batch",
                json=data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"批量检测失败: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"批量检测失败: {e}")
            return None
    
    def visualize_results(self, image_path, results, output_path=None):
        """可视化检测结果"""
        if not results or 'predictions' not in results:
            print("没有检测结果")
            return
        
        # 读取原图
        image = cv2.imread(image_path)
        if image is None:
            print(f"无法读取图片: {image_path}")
            return
        
        # 绘制检测框
        for prediction in results['predictions']:
            bbox = prediction['bbox']
            confidence = prediction['confidence']
            class_name = prediction['class_name']
            
            # 绘制边界框
            cv2.rectangle(image, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
            
            # 绘制标签
            label = f"{class_name}: {confidence:.2f}"
            cv2.putText(image, label, (bbox[0], bbox[1] - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # 保存结果
        if output_path is None:
            output_path = image_path.replace('.', '_result.')
        
        cv2.imwrite(output_path, image)
        print(f"结果已保存到: {output_path}")
        
        return output_path

def main():
    """主函数示例"""
    # 创建客户端
    client = YOLOClient("http://localhost:5000")
    
    # 健康检查
    print("=== 健康检查 ===")
    health = client.health_check()
    if health:
        print("服务状态:", health)
    else:
        print("服务不可用")
        return
    
    # 示例图片路径（请替换为您的实际图片路径）
    test_image = "test_image.jpg"
    
    # 创建测试图片
    if not os.path.exists(test_image):
        print("创建测试图片...")
        img = Image.new('RGB', (640, 640), color='white')
        img.save(test_image)
    
    # 单张图片检测
    print("\n=== 单张图片检测 ===")
    result = client.detect_from_file(test_image)
    if result:
        print(f"检测到 {result['total_detections']} 个目标")
        for i, pred in enumerate(result['predictions']):
            print(f"  目标 {i+1}: {pred['class_name']} (置信度: {pred['confidence']:.2f})")
    
    # Base64检测
    print("\n=== Base64检测 ===")
    result_base64 = client.detect_from_base64(test_image)
    if result_base64:
        print(f"检测到 {result_base64['total_detections']} 个目标")
    
    # 批量检测
    print("\n=== 批量检测 ===")
    batch_result = client.detect_batch([test_image, test_image])
    if batch_result:
        for i, result in enumerate(batch_result['results']):
            if 'error' not in result:
                print(f"图片 {i+1}: 检测到 {result['total_detections']} 个目标")
            else:
                print(f"图片 {i+1}: {result['error']}")
    
    # 可视化结果
    if result:
        print("\n=== 可视化结果 ===")
        client.visualize_results(test_image, result)
    
    # 清理测试文件
    if os.path.exists(test_image):
        os.remove(test_image)
        print(f"清理测试文件: {test_image}")

if __name__ == '__main__':
    main() 
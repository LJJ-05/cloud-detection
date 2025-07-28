import os
import cv2
import numpy as np
from ultralytics import YOLO
from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime
import base64
import traceback
from PIL import Image
import io

print("=== PyTorch YOLO API loaded ===")

app = Flask(__name__, static_folder='static')

class YOLODetector:
    def __init__(self, model_path):
        """初始化YOLO检测器"""
        self.model_path = model_path
        self.model = None
        self.load_model()

    def load_model(self):
        """加载PyTorch模型"""
        try:
            # 使用ultralytics加载.pt模型
            self.model = YOLO(self.model_path)
            
            print(f"模型加载成功: {self.model_path}")
            print(f"模型类型: PyTorch (.pt)")
            print(f"类别数量: {len(self.model.names)}")
            print(f"类别名称: {self.model.names}")
            
        except Exception as e:
            print(f"模型加载失败: {e}")
            raise

    def detect(self, image, conf_threshold=0.5, nms_threshold=0.4):
        """执行检测"""
        try:
            # 直接使用ultralytics进行检测
            results = self.model(image, conf=conf_threshold, iou=nms_threshold, verbose=False)
            
            predictions = []
            
            # 处理检测结果
            if results and len(results) > 0:
                result = results[0]  # 第一个结果
                
                if result.boxes is not None and len(result.boxes) > 0:
                    boxes = result.boxes
                    
                    for i in range(len(boxes)):
                        # 获取边界框坐标 (xyxy格式)
                        box = boxes.xyxy[i].cpu().numpy()
                        x1, y1, x2, y2 = map(int, box)
                        
                        # 获取置信度
                        confidence = float(boxes.conf[i].cpu().numpy())
                        
                        # 获取类别ID和名称
                        class_id = int(boxes.cls[i].cpu().numpy())
                        class_name = self.model.names[class_id] if class_id in self.model.names else f'class_{class_id}'
                        
                        predictions.append({
                            'bbox': [x1, y1, x2, y2],
                            'confidence': confidence,
                            'class_id': class_id,
                            'class_name': class_name
                        })
            
            print(f"检测完成: {len(predictions)} 个目标")
            return predictions
            
        except Exception as e:
            print(f"检测异常: {e}")
            traceback.print_exc()
            return []

# 全局检测器实例
detector = None

@app.route('/')
def index():
    """主页 - 返回演示界面"""
    return send_from_directory('static', 'index.html')

@app.route('/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'model_loaded': detector is not None,
        'model_type': 'PyTorch (.pt)',
        'model_classes': detector.model.names if detector else None
    })

@app.route('/detect', methods=['POST'])
def detect_objects():
    global detector
    
    if detector is None:
        return jsonify({'error': '模型未加载'}), 500
    
    try:
        # 获取请求数据
        image = None
        
        if 'image' in request.files:
            # 文件上传方式
            file = request.files['image']
            image_bytes = file.read()
            image_array = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            
        elif request.is_json and 'image_base64' in request.json:
            # Base64编码方式
            image_base64 = request.json['image_base64']
            image_bytes = base64.b64decode(image_base64)
            image_array = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            
        else:
            return jsonify({'error': '请提供图像文件或Base64编码的图像'}), 400
        
        if image is None:
            return jsonify({'error': '无法解析图像'}), 400
        
        # 获取参数
        conf_threshold = request.json.get('conf_threshold', 0.5) if request.is_json else float(request.form.get('conf_threshold', 0.5))
        nms_threshold = request.json.get('nms_threshold', 0.4) if request.is_json else float(request.form.get('nms_threshold', 0.4))
        
        print(f"检测参数: conf_threshold={conf_threshold}, nms_threshold={nms_threshold}")
        print(f"图片尺寸: {image.shape}")
        
        # 执行检测
        predictions = detector.detect(image, conf_threshold, nms_threshold)
        
        # 返回结果
        result = {
            'success': True,
            'predictions': predictions,
            'total_detections': len(predictions),
            'timestamp': datetime.now().isoformat(),
            'model_type': 'PyTorch (.pt)'
        }
        
        return jsonify(result)
        
    except Exception as e:
        print("检测异常:", e)
        traceback.print_exc()
        return jsonify({'error': f'检测失败: {str(e)}'}), 500

if __name__ == '__main__':
    # 加载模型
    model_path = os.getenv('MODEL_PATH', '/app/models/best.pt')
    
    try:
        detector = YOLODetector(model_path)
        print("模型加载成功，启动服务...")
        
        # 支持云平台的PORT环境变量
        port = int(os.getenv('PORT', 5000))
        print(f"服务将在端口 {port} 启动")
        
        app.run(host='0.0.0.0', port=port, debug=False)
    except Exception as e:
        print(f"启动失败: {e}")
        traceback.print_exc() 
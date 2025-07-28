import os
import cv2
import numpy as np
from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime
import base64
import traceback
import gc
import sys

print("=== Minimal YOLO API for 512MB RAM ===")

app = Flask(__name__, static_folder='static')

class MinimalYOLODetector:
    def __init__(self, model_path):
        """极简YOLO检测器 - 专为低内存设计"""
        self.model_path = model_path
        self.model = None
        self.model_loaded = False
        self.load_error = None
        self.load_model()

    def load_model(self):
        """加载模型 - 带详细错误处理"""
        try:
            print(f"🚀 开始加载模型...")
            print(f"📁 模型路径: {self.model_path}")
            print(f"📂 文件存在: {os.path.exists(self.model_path)}")
            
            if not os.path.exists(self.model_path):
                raise FileNotFoundError(f"模型文件不存在: {self.model_path}")
            
            # 检查文件大小
            file_size = os.path.getsize(self.model_path) / (1024*1024)  # MB
            print(f"📊 模型文件大小: {file_size:.2f} MB")
            
            # 显示当前内存使用
            import psutil
            memory = psutil.virtual_memory()
            print(f"🧠 系统内存: 总计{memory.total//1024//1024}MB, 可用{memory.available//1024//1024}MB")
            
            # 延迟导入ultralytics
            print("📦 导入ultralytics...")
            from ultralytics import YOLO
            
            # 清理内存
            gc.collect()
            
            print("🔄 开始加载YOLO模型...")
            # 尝试加载模型，限制设备为CPU
            self.model = YOLO(self.model_path, task='detect')
            
            # 验证模型加载
            if self.model is None:
                raise Exception("模型对象为None")
            
            self.model_loaded = True
            print(f"✅ 模型加载成功！")
            print(f"🏷️  类别数量: {len(self.model.names)}")
            print(f"🔤 类别: {list(self.model.names.values())}")
            
            # 强制清理内存
            gc.collect()
            
        except ImportError as e:
            error_msg = f"导入ultralytics失败: {e}"
            print(f"❌ {error_msg}")
            self.load_error = error_msg
            self.model_loaded = False
            
        except FileNotFoundError as e:
            error_msg = f"模型文件错误: {e}"
            print(f"❌ {error_msg}")
            self.load_error = error_msg
            self.model_loaded = False
            
        except MemoryError as e:
            error_msg = f"内存不足: {e}"
            print(f"❌ {error_msg}")
            self.load_error = error_msg
            self.model_loaded = False
            
        except Exception as e:
            error_msg = f"模型加载失败: {str(e)}"
            print(f"❌ {error_msg}")
            print("📋 详细错误:")
            traceback.print_exc()
            self.load_error = error_msg
            self.model_loaded = False

    def detect(self, image, conf_threshold=0.5, nms_threshold=0.4):
        """执行检测"""
        if not self.model_loaded:
            raise Exception(f"模型未加载: {self.load_error}")
        
        try:
            print(f"🔍 开始检测...")
            
            # 强制调整图片大小以节省内存
            height, width = image.shape[:2]
            max_size = 416  # 使用更小的尺寸
            if width > max_size or height > max_size:
                scale = max_size / max(width, height)
                new_width = int(width * scale)
                new_height = int(height * scale)
                image = cv2.resize(image, (new_width, new_height))
                print(f"📏 图片调整: {width}x{height} -> {new_width}x{new_height}")
            
            # 执行检测
            results = self.model(image, conf=conf_threshold, iou=nms_threshold, verbose=False)
            
            predictions = []
            if results and len(results) > 0:
                result = results[0]
                if result.boxes is not None and len(result.boxes) > 0:
                    boxes = result.boxes
                    for i in range(len(boxes)):
                        box = boxes.xyxy[i].cpu().numpy()
                        x1, y1, x2, y2 = map(int, box)
                        confidence = float(boxes.conf[i].cpu().numpy())
                        class_id = int(boxes.cls[i].cpu().numpy())
                        class_name = self.model.names.get(class_id, f'class_{class_id}')
                        
                        predictions.append({
                            'bbox': [x1, y1, x2, y2],
                            'confidence': confidence,
                            'class_id': class_id,
                            'class_name': class_name
                        })
            
            print(f"✅ 检测完成: {len(predictions)} 个目标")
            gc.collect()  # 强制垃圾回收
            return predictions
            
        except Exception as e:
            print(f"❌ 检测异常: {e}")
            traceback.print_exc()
            return []

# 全局检测器
detector = None

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'model_loaded': detector.model_loaded if detector else False,
        'model_type': 'PyTorch (.pt)',
        'model_classes': detector.model.names if detector and detector.model_loaded else None,
        'load_error': detector.load_error if detector else None,
        'model_path_exists': os.path.exists(os.getenv('MODEL_PATH', '/app/models/best.pt'))
    })

@app.route('/debug', methods=['GET'])
def debug_info():
    """详细调试信息"""
    model_path = os.getenv('MODEL_PATH', '/app/models/best.pt')
    
    debug_data = {
        'model_path': model_path,
        'model_path_exists': os.path.exists(model_path),
        'working_directory': os.getcwd(),
        'python_version': sys.version,
        'model_loaded': detector.model_loaded if detector else False,
        'load_error': detector.load_error if detector else None,
        'env_vars': {
            'MODEL_PATH': os.getenv('MODEL_PATH'),
            'PORT': os.getenv('PORT'),
            'PYTHONUNBUFFERED': os.getenv('PYTHONUNBUFFERED')
        }
    }
    
    # 文件信息
    if os.path.exists(model_path):
        debug_data['model_file_size_mb'] = round(os.path.getsize(model_path) / (1024*1024), 2)
    
    # 内存信息
    try:
        import psutil
        memory = psutil.virtual_memory()
        debug_data['memory'] = {
            'total_mb': memory.total // 1024 // 1024,
            'available_mb': memory.available // 1024 // 1024,
            'used_mb': memory.used // 1024 // 1024,
            'percent': memory.percent
        }
    except ImportError:
        debug_data['memory'] = 'psutil not available'
    
    # 目录信息
    try:
        debug_data['app_directory'] = os.listdir('/app') if os.path.exists('/app') else 'not exists'
        debug_data['models_directory'] = os.listdir('/app/models') if os.path.exists('/app/models') else 'not exists'
    except Exception as e:
        debug_data['directory_error'] = str(e)
    
    return jsonify(debug_data)

@app.route('/detect', methods=['POST'])
def detect_objects():
    global detector
    
    if not detector or not detector.model_loaded:
        error_msg = detector.load_error if detector else "检测器未初始化"
        return jsonify({'error': f'模型未加载: {error_msg}'}), 500
    
    try:
        image = None
        
        if 'image' in request.files:
            file = request.files['image']
            image_bytes = file.read()
            image_array = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        elif request.is_json and 'image_base64' in request.json:
            image_base64 = request.json['image_base64']
            image_bytes = base64.b64decode(image_base64)
            image_array = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        else:
            return jsonify({'error': '请提供图像文件或Base64编码的图像'}), 400
        
        if image is None:
            return jsonify({'error': '无法解析图像'}), 400
        
        conf_threshold = request.json.get('conf_threshold', 0.5) if request.is_json else float(request.form.get('conf_threshold', 0.5))
        nms_threshold = request.json.get('nms_threshold', 0.4) if request.is_json else float(request.form.get('nms_threshold', 0.4))
        
        predictions = detector.detect(image, conf_threshold, nms_threshold)
        
        result = {
            'success': True,
            'predictions': predictions,
            'total_detections': len(predictions),
            'timestamp': datetime.now().isoformat(),
            'model_type': 'PyTorch (.pt)'
        }
        
        return jsonify(result)
        
    except Exception as e:
        print("❌ 检测异常:", e)
        traceback.print_exc()
        return jsonify({'error': f'检测失败: {str(e)}'}), 500

if __name__ == '__main__':
    model_path = os.getenv('MODEL_PATH', '/app/models/best.pt')
    
    print(f"🚀 启动极简YOLO API...")
    print(f"📁 模型路径: {model_path}")
    print(f"🌍 环境变量: {dict(os.environ)}")
    
    # 初始化检测器
    detector = MinimalYOLODetector(model_path)
    
    # 启动Flask应用
    port = int(os.getenv('PORT', 5000))
    print(f"🌐 启动Web服务，端口: {port}")
    app.run(host='0.0.0.0', port=port, debug=False) 
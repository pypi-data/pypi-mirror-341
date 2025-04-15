import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import numpy as np
from .utils import ModelManager
import time
import pathlib
from mediapipe.framework.formats import landmark_pb2

import threading
from collections import deque

class PoseLandmarkerError(Exception):
    """姿态关键点检测错误"""
    pass

class PoseLandmarker:
    def __init__(self, 
                 input_source=None,  # 输入源决定模式
                 min_pose_detection_confidence=0.5,
                 min_pose_presence_confidence=0.5,
                 min_tracking_confidence=0.5,
                 result_callback=None):  # 可选的回调函数 
        """
        姿态检测器
        Args:
            input_source: 输入源，决定运行模式
                - None: 实时流模式
                - np.ndarray: 图片数据，图片模式
                - str/Path: 图片路径，图片模式
            min_pose_detection_confidence: 最小姿态检测置信度
            min_pose_presence_confidence: 最小姿态存在置信度
            min_tracking_confidence: 最小跟踪置信度
            result_callback: 可选的回调函数，用于实时流模式
        """
        try:
            # 性能监控
            self._fps_counter = 0
            self._fps = 0
            self._start_time = time.time()
            self._fps_avg_frame_count = 10
            self._last_frame_time = 0
            self._skip_frame_count = 0
            
            # 同步控制
            self._result_lock = threading.RLock()
            self._latest_result = None
            self._latest_frame = None
            
            # 跳帧控制
            self._target_fps = 30  # 目标FPS
            self._min_process_interval = 1.0 / self._target_fps
            
            # 基础参数设置
            self.min_pose_detection_confidence = min_pose_detection_confidence
            self.min_pose_presence_confidence = min_pose_presence_confidence
            self.min_tracking_confidence = min_tracking_confidence
            self.result_callback = result_callback
            
            # 身体部位定义
            self.body_parts = {
                'face': list(range(0, 11)),
                'left_arm': [11, 13, 15, 17, 19, 21],
                'right_arm': [12, 14, 16, 18, 20, 22],
                'left_leg': [23, 25, 27, 29, 31],
                'right_leg': [24, 26, 28, 30, 32],
                'torso': [11, 12, 23, 24]
            }
            
            # 根据输入源确定模式
            self.running_mode = self._determine_mode(input_source)
            
            # 初始化检测器
            self._initialize_detector()
            
            # 如果是图片模式，立即处理输入图片
            if input_source is not None:
                self._process_input_source(input_source)
                
        except Exception as e:
            raise PoseLandmarkerError(f"初始化失败: {str(e)}")
            
    def _determine_mode(self, input_source):
        """根据输入源确定运行模式"""
        if input_source is None:
            return vision.RunningMode.LIVE_STREAM
            
        if isinstance(input_source, (str, pathlib.Path)):
            path = pathlib.Path(input_source)
            if not path.exists():
                raise FileNotFoundError(f"图片文件不存在: {path}")
            if not path.suffix.lower() in {'.jpg', '.jpeg', '.png', '.bmp'}:
                raise ValueError(f"不支持的图片格式: {path.suffix}")
                
        elif isinstance(input_source, np.ndarray):
            if len(input_source.shape) != 3:
                raise ValueError("输入图像必须是3通道图像")
                
        else:
            raise ValueError(f"不支持的输入类型: {type(input_source)}")
            
        return vision.RunningMode.IMAGE
            
    def _internal_callback(self, result, output_image, timestamp_ms):
        """回调函数，用于处理检测结果"""
        with self._result_lock:
            self._latest_result = result
        
        # 更新FPS计数
        if self._fps_counter % self._fps_avg_frame_count == 0:
            self._fps = self._fps_avg_frame_count / (time.time() - self._start_time)
            self._start_time = time.time()
        
        self._fps_counter += 1
        
        # 如果用户提供了回调，则调用它
        if self.result_callback:
            self.result_callback(result, output_image, timestamp_ms)
            
    def _initialize_detector(self):
        """初始化检测器"""
        try:
            base_options = python.BaseOptions(
                model_asset_path=ModelManager.get_model_path("pose_landmarker.task")
            )
            
            # 无论是图片模式还是实时流模式，都使用IMAGE运行模式
            # 这样可以确保同步处理
            options = vision.PoseLandmarkerOptions(
                base_options=base_options,
                running_mode=vision.RunningMode.IMAGE,
                min_pose_detection_confidence=self.min_pose_detection_confidence,
                min_pose_presence_confidence=self.min_pose_presence_confidence,
                min_tracking_confidence=self.min_tracking_confidence
            )
            
            self.detector = vision.PoseLandmarker.create_from_options(options)
            
        except Exception as e:
            raise PoseLandmarkerError(f"初始化检测器失败: {str(e)}")
            
    def _process_input_source(self, input_source):
        """处理输入源"""
        try:
            if isinstance(input_source, (str, pathlib.Path)):
                image = cv2.imread(str(input_source))
                if image is None:
                    raise ValueError(f"无法读取图片: {input_source}")
            else:
                image = input_source
                
            # 转换为RGB格式并检测
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
            self._latest_result = self.detector.detect(mp_image)
            self._latest_frame = image
            
        except Exception as e:
            raise PoseLandmarkerError(f"处理输入源失败: {str(e)}")

    def _process_result(self, detection_result, image_shape):
        """处理检测结果为格式化的数据"""
        if not detection_result or not detection_result.pose_landmarks:
            return None
            
        h, w = image_shape[:2]
        poses_data = []
        
        for pose_landmarks in detection_result.pose_landmarks:
            # 转换关键点坐标
            landmarks = []
            visibility = []
            for landmark in pose_landmarks:
                landmarks.append((int(landmark.x * w), int(landmark.y * h), landmark.z))
                visibility.append(landmark.visibility)
            
            poses_data.append({
                'landmarks': landmarks,
                'visibility': visibility,
                'body_parts': self.body_parts
            })
            
        return poses_data

    def run(self, frame=None):
        """运行检测"""
        try:
            if self.running_mode == vision.RunningMode.IMAGE:
                if frame is not None:
                    raise ValueError("图片模式下不应该传入frame参数")
                return self._latest_result and self._process_result(self._latest_result, self._latest_frame.shape)
            
            if frame is None:
                raise ValueError("实时流模式下必须传入frame参数")
            
            # 计算帧间隔，控制处理频率
            current_time = time.time()
            elapsed = current_time - self._last_frame_time
            
            # 控制帧率，避免过度处理导致积压
            if elapsed < self._min_process_interval:
                self._skip_frame_count += 1
                return self._latest_result and self._process_result(self._latest_result, frame.shape)
            
            # 记录时间以控制帧率
            self._last_frame_time = current_time
            
            # 转换为RGB并进行同步检测
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            
            # 直接使用同步方式进行检测
            with self._result_lock:
                self._latest_result = self.detector.detect(mp_image)
                self._latest_frame = frame
                
                # 更新FPS计数
                if self._fps_counter % self._fps_avg_frame_count == 0:
                    self._fps = self._fps_avg_frame_count / (time.time() - self._start_time)
                    self._start_time = time.time()
                
                self._fps_counter += 1
                
                # 如果用户提供了回调，则调用它
                if self.result_callback:
                    self.result_callback(self._latest_result, frame, time.time_ns() // 1_000_000)
                
                return self._process_result(self._latest_result, frame.shape)
                
        except Exception as e:
            raise PoseLandmarkerError(f"运行检测失败: {str(e)}")
            
    def draw(self, image, poses_data=None):
        """在图像上绘制检测结果"""
        if not self._latest_result or not self._latest_result.pose_landmarks:
            return image
            
        image_copy = image.copy()
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        mp_pose = mp.solutions.pose
        
        # 绘制每个检测到的姿态
        for pose_landmarks in self._latest_result.pose_landmarks:
            # 创建规范化的关键点列表
            pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            pose_landmarks_proto.landmark.extend([
                landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z)
                for landmark in pose_landmarks
            ])
            
            # 绘制姿态关键点和连接线
            mp_drawing.draw_landmarks(
                image=image_copy,
                landmark_list=pose_landmarks_proto,
                connections=mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
            )
        
        return image_copy
        
    def get_fps(self):
        """获取当前FPS"""
        return self._fps
        
    def get_skipped_frames(self):
        """获取跳过的帧数"""
        return self._skip_frame_count
        
    def close(self):
        """释放资源"""
        # 释放检测器
        if hasattr(self, 'detector'):
            self.detector.close()
        
        # 清理内部数据结构
        with self._result_lock:
            self._latest_frame = None
            self._latest_result = None

    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close() 
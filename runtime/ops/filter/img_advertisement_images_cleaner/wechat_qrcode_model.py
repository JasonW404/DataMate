# -- encoding: utf-8 --

import gc
import os
from pathlib import Path

import cv2


class WechatQRCodeModel:

    def __init__(self, *args, **kwargs):
        models_path = os.getenv("MODELS_PATH", "/home/models")
        self.resources_path = str(Path(models_path, 'img_QRcode_detect', 'resources'))
        self.wechat_qr_model = cv2.wechat_qrcode_WeChatQRCode(
            str(Path(self.resources_path, 'detect.prototxt')),
            str(Path(self.resources_path, 'detect.caffemodel')),
            str(Path(self.resources_path, 'sr.prototxt')),
            str(Path(self.resources_path, 'sr.caffemodel')))

    def __del__(self):
        del self.wechat_qr_model
        gc.collect()

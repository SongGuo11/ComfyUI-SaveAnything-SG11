import os
import torch
from PIL import Image
import numpy as np

class SaveAnything:
    def __init__(self):
        self.type = "output"
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "filename": ("STRING", {"default": "output"}),
                "image": ("IMAGE", ),
                "save_dir": ("STRING", {"default": "outputs"}),
                "format": (["PNG", "JPEG", "WEBP", "BMP", "TIFF"], {"default": "PNG"}),
            },
        }
    
    RETURN_TYPES = ()
    FUNCTION = "save_content"
    OUTPUT_NODE = True
    CATEGORY = "save"

    def save_content(self, filename, image, save_dir, format):
        os.makedirs(save_dir, exist_ok=True)
        
        # 根据选择的格式设置文件扩展名
        format = format.lower()
        ext = "jpg" if format == "jpeg" else format
        save_path = os.path.join(save_dir, f"{filename}.{ext}")
        
        # 优化图像处理
        if len(image.shape) == 4:
            image = image[0]
        
        # 使用 torch 操作进行图像转换，避免不必要的 CPU-GPU 传输
        image = (image.clamp(0, 1) * 255).to(torch.uint8)
        image = image.cpu().numpy()
        
        # 设置优化的保存参数
        save_args = {
            "optimize": True,  # 对所有格式启用优化
            "format": format.upper()
        }
        
        # 根据格式设置特定参数
        if format == "jpeg":
            save_args["quality"] = 95
            save_args["subsampling"] = 0  # 使用 4:4:4 采样以获得更好的质量
        elif format == "webp":
            save_args["quality"] = 90
            save_args["method"] = 4  # 使用较快的压缩方法
        elif format == "png":
            save_args["optimize"] = True
            save_args["compress_level"] = 6  # 平衡压缩率和速度
        
        # 直接创建 PIL 图像并保存
        Image.fromarray(image).save(save_path, **save_args)
        print(f"图片已保存到: {save_path}")
        
        return ()
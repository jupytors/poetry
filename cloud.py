from PIL import Image
import numpy as np

# 1. 准备形状模板（掩码）
# 图片背景最好为白色，词云将生成在非白色的区域
mask_image = np.array(Image.open("cloud.png")) # 例如一个心形、动物或Logo

# 2. 创建词云时传入mask参数
wc = WordCloud(
    
    background_color='white',
    mask=mask_image,  # 应用形状模板
    max_words=200
)
wc.generate(cut_text)
import warnings

# 忽略特定的 FutureWarning
warnings.filterwarnings("ignore", category=FutureWarning, message=".*image_processor_class.*")
import os
import re
import json
import time
from glob import glob
from tqdm import tqdm
from marker.convert import convert_single_pdf
from marker.output import markdown_exists, save_markdown
from marker.models import load_all_models
from PIL import Image
import logging
import base64
from loguru import logger
import concurrent.futures

# 设置环境变量
os.environ["HF_DATASETS_CACHE"] = "./cache_dir"     # 指定 Hugging Face Datasets 库缓存数据集的位置
os.environ["HF_HOME"] = "./cache_dir"               # 指定 Hugging Face 库的主目录
os.environ["HUGGINGFACE_HUB_CACHE"] = "./cache_dir/" # 指定 Hugging Face Hub 库缓存模型和数据集的位置
os.environ["TRANSFORMERS_CACHE"] = "./cache_dir/"    # 指定 Hugging Face Transformers 库缓存模型的位置。
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com" # 指定 Hugging Face 库访问模型和数据集的服务器地址

# 定义路径
base_path = '/mnt/workspace/XXX'
output_dir = '/mnt/workspace/output'

# 加载所有模型
model_lst = load_all_models()

# 设置日志记录
logging.basicConfig(filename='error_log.log', level=logging.ERROR)

# 定义将输入的 Markdown 文本分解为结构化数据的函数
def structure_markdown(markdown_text):
    structured_data = []
    lines = markdown_text.split('\n')

    for line in lines:
        if line.startswith('# '):
            structured_data.append({'type': 'title', 'content': line[2:]})
        elif line.startswith('## '):
            structured_data.append({'type': 'subtitle', 'content': line[3:]})
        elif re.match(r'!\[.*\]\(.*\)', line):
            structured_data.append({'type': 'image', 'content': line})
        elif line:
            structured_data.append({'type': 'paragraph', 'content': line})

    return structured_data

def convert(pdf_file_path):
    try:
        # 进行pdf到markdown的转化逻辑，调用convert_single_pdf函数来处理单个PDF文件
        result = convert_single_pdf(pdf_file_path, model_lst, max_pages=10, langs=['zh', 'en'], batch_multiplier=1, start_page=0)
        
        if not isinstance(result, tuple) or len(result) != 3:
            raise ValueError("convert_single_pdf 返回的结果不是包含三个元素的元组")
        
        full_text, doc_images, out_meta = result
        
        if not isinstance(doc_images, dict):
            raise ValueError("doc_images 不是一个字典")
        
        fname = os.path.basename(pdf_file_path).replace('.pdf', '')
        output_folder = os.path.join(output_dir, fname)
        os.makedirs(output_folder, exist_ok=True)  # 确保输出文件夹存在，如果不存在，就创建它
        
        markdown_file_path = os.path.join(output_folder, fname + '.md')
        
        # 保存图像并记录名称
        image_names = {}
        for i, (image_name, image) in enumerate(doc_images.items()):
            image_file_name = f'image_{i}.png'
            image_names[image_name] = image_file_name
            image_path = os.path.join(output_folder, image_file_name)
            
            if isinstance(image, Image.Image):
                image.save(image_path)
            elif isinstance(image, str):
                image_data = base64.b64decode(image)
                with open(image_path, 'wb') as img_f:
                    img_f.write(image_data)
            else:
                raise TypeError("Unsupported image type")
        
        # 更新Markdown中的图片路径
        for original_path, image_file_name in image_names.items():
            full_text = full_text.replace(original_path, image_file_name)
        
        # 保存Markdown文件
        with open(markdown_file_path, 'w') as f:
            f.write(full_text)
        
        # 保存元数据
        meta_file_path = os.path.join(output_folder, f'{fname}_meta.json')
        with open(meta_file_path, 'w') as meta_f:
            json.dump(out_meta, meta_f, ensure_ascii=False, indent=4)

        # 提取结构化数据
        structured_data = structure_markdown(full_text)

        return {
            'source_pdf': pdf_file_path,
            'markdown_file': markdown_file_path,
            'conversion_time': time.ctime(),
            'structured_data': structured_data,
            'output_folder': output_folder
        }
    except Exception as e:
        logging.error(f"Error processing {pdf_file_path}: {e}")
        return None

def collect_all_target_pdf():
    all_pdf_files = glob(os.path.join(base_path, '*.pdf'))
    print(f"Found {len(all_pdf_files)} PDF files.")
    if not all_pdf_files:
        print("No PDF files found. Please check the base_path and file structure.")

    markdown_files_info = []

    max_workers = 1
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(convert, pdf_file): pdf_file for pdf_file in all_pdf_files}
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(all_pdf_files)):
            try:
                result = future.result()
                if result is not None:
                    markdown_files_info.append(result)
            except Exception as e:
                logging.error(f"Error in future result: {e}")

    with open('result.json', 'w') as f:
        json.dump(markdown_files_info, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    collect_all_target_pdf()

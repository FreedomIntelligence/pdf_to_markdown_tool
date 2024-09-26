# pdf_to_markdown_tool
# PDF 转 Markdown 转换工具

这是一个简单的工具，用于将PDF文件转换为Markdown格式。

## 依赖

- Python 3.x
- `pdfplumber` 库
- `markdownify` 库
- `tqdm` 库
- `Pillow` 库
- `marker-pdf` 库
- `libgl1-mesa-glx` 软件包。等等

python 3.11（主要和torch，numpy等版本适配即可）

requirements.txt

建议先不要直接pip -r，先搭建pytorch环境，其他包如libgl1-mesa-glx，scapy,marker-pdf手动装，没有多少

如下：

```bash
apt install libgl1-mesa-glx
pip install marker-pdf
```

## 位置设置
```bash
os.environ["HF_DATASETS_CACHE"] = "xxx/xxx/xxx"       #指定了 Hugging Face Datasets 库缓存数据集的位置
os.environ["HF_HOME"] = "xxx/xxx/xxx"                 #指定了 Hugging Face 库的主目录
os.environ["HUGGINGFACE_HUB_CACHE"] = "xxx/xxx/xxx"   #指定了 Hugging Face Hub 库缓存模型和数据集的位置
os.environ["TRANSFORMERS_CACHE"] = "xxx/xxx/xxx"      #指定了 Hugging Face Transformers 库缓存模型的位置。
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"   #指定了 Hugging Face 库访问模型和数据集的服务器地址

base_path = '/xxx/xxx/'                               #指定存放 PDF 文件位置的地址
output_dir = '/xxx/xxx'                               #指定存放 Markdown文件、out_meta、image文件
```


## 参数调整
在`convert`函数`max_pages`中，可以设置最大转换页数。`langs`设置识别语言。`start_page`设置从第几页开始

在`collect_all_target_pdf`函数中，采用多进程的方式进行并行处理，可以进行更改为多线程。并且在`max_workers`中设置最大线程数。

## 运行脚本
 ```bash
python converter.py
```

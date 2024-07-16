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

建议先不要直接pip -r，先搭建pytorch环境，其他包如flask，scapy手动装，没有多少

可以使用pip -安装所需的库：

```bash
pip install libgl1-mesa-glx
pip install marker-pdf
```

通过手动设置huggingface加载镜像
 ```bash
export HF_ENDPOINT=https://hf-mirror.com
```

## 位置设置
完成`HF_DATASETS_CACHE`，`HF_HOME`，`HUGGINGFACE_HUB_CACHE`，`TRANSFORMERS_CACHE`，`HF_ENDPOINT`

这些指定位置以及你所要转换PDF文件的地址和转换完成后的输出地址。

## 参数调整
在`convert`函数`max_pages`中，可以设置最大转换页数。`langs`设置识别语言。`start_page`设置从第几页开始

在`collect_all_target_pdf`函数中，采用多进程的方式进行并行处理，可以进行更改为多线程。并且在`max_workers`中设置最大线程数。

## 运行脚本
 ```bash
python converter.py
```

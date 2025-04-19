# gptpdf

<p align="center">
<a href="README_CN.md"><img src="https://img.shields.io/badge/文档-中文版-blue.svg" alt="CN doc"></a>
<a href="README.md"><img src="https://img.shields.io/badge/document-English-blue.svg" alt="EN doc"></a>
</p>

Using VLLM (like GPT-4o) to parse PDF into markdown.

Our approach is very simple (only 293 lines of code), but can almost perfectly parse typography, math formulas, tables, pictures, charts, etc.

Average cost per page: $0.013

This package use [GeneralAgent](https://github.com/CosmosShadow/GeneralAgent) lib to interact with OpenAI API.

[pdfgpt-ui](https://github.com/daodao97/gptpdf-ui) is a visual tool based on gptpdf.



## Process steps

1. Use the PyMuPDF library to parse the PDF to find all non-text areas and mark them, for example:

![](docs/demo.jpg)

2. Use a large visual model (such as GPT-4o) to parse and get a markdown file.



## DEMO

1. [examples/attention_is_all_you_need/output.md](examples/attention_is_all_you_need/output.md) for PDF [examples/attention_is_all_you_need.pdf](examples/attention_is_all_you_need.pdf).


2. [examples/rh/output.md](examples/rh/output.md) for PDF [examples/rh.pdf](examples/rh.pdf).


## Installation

```bash
pip install gptpdf
```



## Usage

### Local Usage

```python
from gptpdf import parse_pdf
api_key = 'Your OpenAI API Key'
content, image_paths = parse_pdf(pdf_path, api_key=api_key)
print(content)
```

See more in [test/test.py](test/test.py)



### Google Colab

see [examples/gptpdf_Quick_Tour.ipynb](examples/gptpdf_Quick_Tour.ipynb)




## API

### parse_pdf

**Function**: 
```
def parse_pdf(
        pdf_path: str,
        output_dir: str = './',
        api_key = None,
        base_url = None,
        model = 'gpt-4o',
        gpt_worker: int = 1,
        prompt = DEFAULT_PROMPT,
        rect_prompt = DEFAULT_RECT_PROMPT,
        role_prompt = DEFAULT_ROLE_PROMPT,
) -> Tuple[str, List[str]]:
```

Parses a PDF file into a Markdown file and returns the Markdown content along with all image paths.

**Parameters**:

- **pdf_path**: *str*  
  Path to the PDF file

- **output_dir**: *str*, default: './'  
  Output directory to store all images and the Markdown file

- **api_key**: *str*  
  OpenAI API key. If not provided through this parameter, it must be set via the `OPENAI_API_KEY` environment variable.

- **base_url**: *str*, optional  
  OpenAI base URL. If not provided through this parameter, it must be set via the `OPENAI_BASE_URL` environment variable. Can be used to configure custom OpenAI API endpoints.

- **model**: *str*, default: 'gpt-4o'  
  OpenAI API formatted multimodal large model. If you need to use other models.

- **gpt_worker**: *int*, default: 1  
  Number of GPT parsing worker threads. If your machine has better performance, you can increase this value to speed up the parsing.

- **prompt**: *str*, default: uses built-in prompt  
  Custom main prompt used to guide the model on how to process and convert text content in images.

- **rect_prompt**: *str*, default: uses built-in prompt  
  Custom rectangle area prompt used to handle cases where specific areas (such as tables or images) are marked in the image.

- **role_prompt**: *str*, default: uses built-in prompt  
  Custom role prompt that defines the role of the model to ensure it understands it is performing a PDF document parsing task.

  You can customize these prompts to adapt to different models or specific needs, for example:

  ```python
  content, image_paths = parse_pdf(
      pdf_path=pdf_path,
      output_dir='./output',
      model="gpt-4o",
      prompt="Custom main prompt",
      rect_prompt="Custom rectangle area prompt",
      role_prompt="Custom role prompt",
      verbose=False,
  )
  ```

## Join Us 👏🏻

Scan the QR code below with WeChat to join our group chat or contribute.

<p align="center">
<img src="./docs/wechat.jpg" alt="wechat" width=400/>
</p>
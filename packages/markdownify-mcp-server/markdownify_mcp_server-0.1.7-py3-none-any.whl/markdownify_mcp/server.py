from mcp.server.fastmcp import FastMCP
from markitdown import MarkItDown
import os
import json
from datetime import datetime
# from typing import List, Dict, Any

mcp = FastMCP('markdownify-mcp-server')
# youtube-to-markdown: Convert YouTube videos to Markdown
# pdf-to-markdown: Convert PDF files to Markdown
# bing-search-to-markdown: Convert Bing search results to Markdown
# webpage-to-markdown: Convert web pages to Markdown
# image-to-markdown: Convert images to Markdown with metadata
# audio-to-markdown: Convert audio files to Markdown with transcription
# docx-to-markdown: Convert DOCX files to Markdown
# xlsx-to-markdown: Convert XLSX files to Markdown
# pptx-to-markdown: Convert PPTX files to Markdown
# get-markdown-file: Retrieve an existing Markdown file

# https://github.com/zcaceres/markdownify-mcp/blob/main/src/tools.ts
# https://github.com/microsoft/markitdown/blob/main/packages/markitdown-mcp/src/markitdown_mcp/__main__.py

def save_temp_file(content:str, path:str) ->str:
    now = datetime.now()
    file_path: str = os.path.join(path, f'markdown_output_{now.strftime("%Y-%m-%d-%H-%M-%S-%f")}.md')
    with open(file_path, "w") as file:
        file.write(content)

    return file_path

# def error_ret(filepath:str)->Dict[str, Any]:
#
#     # value = dict()
#     retval = list()
#     element = dict()
#     element['type'] = 'text'
#     element['text'] = f'文件不存在 {filepath}'
#     retval.append(element)
#     # value['content'] = retval
#     # value['isError'] = True
#     return {
#         "content": retval,
#         "isError": True
#     }
#     # return value

def build_error_ret(filepath:str)->str:
    # value = dict()
    # retval = list()
    # element = dict()
    # element['type'] = 'text'
    element['error'] = f'文件不存在 {filepath}'
    # retval.append(element)
    # value['content'] = retval


    return json.dumps(value, ensure_ascii=False)


# def exception_ret(exception :str)->Dict[str,Any]:
#     # value = dict()
#     retval = list()
#     element = dict()
#     element['type'] = 'text'
#     element['text'] = exception
#     retval.append(element)
#     # value['content'] = retval
#     # value['isError'] = True
#
#     return {
#         "content": retval,
#         "isError":True
#     }
#     # return value

def build_exception_ret(exception :str)->str:
    # value = dict()
    # retval = list()
    element = dict()
    # element['type'] = 'text'
    element['exception'] = exception
    # retval.append(element)
    # value['content'] = retval
    # value['isError'] = True

    return json.dumps(element, ensure_ascii=False)

# def ret_value(content:str, path:str)->Dict[str,Any]:
#     # value = dict()
#     retval = list()
#     element2 = dict()
#     element2['type'] = 'text'
#     element2['text'] = f'Output file: {path}'
#     retval.append(element2)
#     element1 = dict()
#     element1['type'] = 'text'
#     element1['text'] = 'Converted content:'
#     retval.append(element1)
#     element = dict()
#     element['type'] = 'text'
#     element['text'] = content
#     retval.append(element)
#     # value['content'] = retval
#     # value['isError'] = False
#     # return value
#
#     return {
#         "content": retval,
#         "isError": False
#     }


def build_ret_value(content:str, path:str)->str:

    # value = dict()
    retval = list()
    element2 = dict()
    element2['Output file:'] = path
    retval.append(element2)
    element = dict()
    element['content'] = content
    retval.append(element)
    # value['content'] = retval
    # value['isError'] = False


    return json.dumps(retval,ensure_ascii=False)

def local_file_to_markdown(filepath:str)->Dict[str,Any]:
    if os.path.exists(filepath):
        content = MarkItDown().convert_local(filepath).markdown
        path = os.path.dirname(filepath)
        tmp_path = save_temp_file(content, path)
        return build_ret_value(content, tmp_path)
    else:
        return build_error_ret(filepath)


def get_cache_path()->str:
    home_dir = os.path.expanduser("~")
    if not os.path.exists(home_dir):
        cache_dir = os.path.join(os.getcwd(),"temp")
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        return cache_dir
    else:
        cache_dir = os.path.join(home_dir, "temp")
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        return cache_dir

def url_to_markdown(url:str)->Dict[str,Any]:
    try:
        content = MarkItDown().convert_url(url).markdown
        path = get_cache_path()
        tmp_path = save_temp_file(content, path)
        return build_ret_value(content, tmp_path)
    except Exception as e:
        return build_exception_ret(str(e))

@mcp.tool('youtube-to-markdown')
def youtube_to_markdown(url:str)->Dict[str,Any]:
    """Convert a YouTube video to markdown, including transcript if available"""
    return url_to_markdown(url)


@mcp.tool('pdf-to-markdown')
def pdf_to_markdown(filepath:str)->Dict[str,Any]:
    """Convert a PDF file to markdown"""
    return local_file_to_markdown(filepath)

@mcp.tool('bing-search-to-markdown')
def bing_search_to_markdown(url:str)->Dict[str,Any]:
    """Convert a Bing search results page to markdown"""
    return url_to_markdown(url)

@mcp.tool('webpage-to-markdown')
def webpage_to_markdown(url : str)->Dict[str,Any]:
    """Convert a webpage to markdown"""
    return url_to_markdown(url)
    #convert_local

@mcp.tool('image-to-markdown')
def image_to_markdown(filepath:str)->Dict[str,Any]:
    """Convert an image to markdown, including metadata and description"""
    return local_file_to_markdown(filepath)

@mcp.tool('audio-to-markdown')
def audio_to_markdown(filepath:str)->Dict[str,Any]:
    """Convert an audio file to markdown, including transcription if possible"""
    return local_file_to_markdown(filepath)

@mcp.tool('docx-to-markdown')
def docx_to_markdown(filepath:str)->Dict[str,Any]:
    """Convert a DOCX file to markdown"""
    return local_file_to_markdown(filepath)

@mcp.tool('xlsx-to-markdown')
def xlsx_to_markdown(filepath:str)->Dict[str,Any]:
    """Convert an XLSX file to markdown"""
    return local_file_to_markdown(filepath)

@mcp.tool('pptx-to-markdown')
def pptx_to_markdown(filepath:str)->Dict[str,Any]:
    """Convert a PPTX file to markdown"""
    return local_file_to_markdown(filepath)

@mcp.tool('get-markdown-file')
def get_markdown_file(filepath:str)->Dict[str,Any]:
    """Get a markdown file by absolute file path"""
    try:
        with open(filepath, 'r') as file:
            content = file.read()
        return build_ret_value(content, filepath)
    except FileNotFoundError as e:
        return build_exception_ret(str(e))
    except PermissionError as e:
        return build_exception_ret(str(e))
    except IOError as e:
        return build_exception_ret(str(e))
    
def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()



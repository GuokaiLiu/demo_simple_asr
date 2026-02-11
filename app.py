from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
import re

# 从系统环境变量中获取API_KEY
api_key = os.environ.get('API_KEY')
if not api_key:
    print("错误: 未设置API_KEY环境变量")
    exit(1)

# 创建FastAPI应用
app = FastAPI()

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="."), name="static")

# 根路径处理
@app.get("/", response_class=HTMLResponse)
async def read_root():
    return await get_index_html()

# index.html路径处理
@app.get("/index.html", response_class=HTMLResponse)
async def read_index():
    return await get_index_html()

# 通用路径处理，支持查询参数
@app.get("/{path:path}", response_class=HTMLResponse)
async def read_path(path: str):
    # 如果请求的是其他路径，尝试返回静态文件
    try:
        with open(f"./{path}", "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except:
        # 如果文件不存在，返回index.html
        return await get_index_html()

# 读取并处理index.html的函数
async def get_index_html():
    try:
        # 读取index.html文件
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        print("成功读取index.html文件")
        
        # 打印文件的前200个字符，确认读取正确
        print("文件开头:", content[:200] + "...")
        
        # 替换API_KEY占位符
        print(f"环境变量API_KEY: '{api_key}'")
        
        # 打印替换前的API_KEY行
        match = re.search(r'const API_KEY = [\'"].*?[\'"];', content)
        if match:
            print(f"替换前的API_KEY行: '{match.group(0)}'")
        else:
            print("未找到API_KEY占位符")
        
        # 执行替换
        new_content = re.sub(r'const API_KEY = [\'"].*?[\'"];', f"const API_KEY = '{api_key}';", content)
        
        # 打印替换后的API_KEY行
        match = re.search(r'const API_KEY = [\'"].*?[\'"];', new_content)
        if match:
            print(f"替换后的API_KEY行: '{match.group(0)}'")
        else:
            print("替换后仍未找到API_KEY行")
        
        return new_content
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        return f"<html><body><h1>错误</h1><p>{e}</p></body></html>"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
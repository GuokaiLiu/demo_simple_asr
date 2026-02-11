import os
import http.server
import socketserver
import re


# 从系统环境变量中获取API_KEY
api_key = os.environ.get('API_KEY')
if not api_key:
    print("错误: 未设置API_KEY环境变量")
    exit(1)

# 自定义HTTP请求处理器
class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # 打印所有请求路径
        print(f"收到请求: {self.path}")
        
        # 如果请求的是根路径或index.html，动态替换API_KEY
        if self.path == '/' or self.path == '/index.html' or self.path.startswith('/?ide_webview_request_time='):
            print(f"处理请求: {self.path} - 匹配到index.html处理")
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
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
                import re
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
                
                # 发送修改后的内容
                self.wfile.write(new_content.encode('utf-8'))
                print("成功发送修改后的内容")
            except Exception as e:
                print(f"错误: {e}")
                import traceback
                traceback.print_exc()
                error_content = f"<html><body><h1>错误</h1><p>{e}</p></body></html>"
                self.wfile.write(error_content.encode('utf-8'))
            return
        
        # 其他文件正常处理
        super().do_GET()

# 启动服务器
if __name__ == '__main__':
    PORT = 8000
    
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print(f"服务器已启动，运行在 http://localhost:{PORT}")
        print(f"API_KEY 已从系统环境变量中获取: {api_key}")
        print("按 Ctrl+C 停止服务器")
        httpd.serve_forever()

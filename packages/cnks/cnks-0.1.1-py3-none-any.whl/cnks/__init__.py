from . import server
import asyncio
import sys
import json
from typing import Optional, Dict, Any

def add_note(name: str, content: str) -> None:
    """添加笔记到服务器"""
    server.notes[name] = content
    print(f"已添加笔记 '{name}': {content}")

def main():
    """主入口点"""
    # 处理命令行参数
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "add-note" and len(sys.argv) >= 4:
            add_note(sys.argv[2], sys.argv[3])
            return
        elif cmd == "help":
            print("使用方法:")
            print("  cnks add-note <名称> <内容>  - 添加笔记")
            print("  cnks help                   - 显示此帮助信息")
            print("  cnks                        - 启动MCP服务器")
            return
    
    # 默认启动服务器
    # 尝试使用FastMCP接口，如果可用
    fast_mcp = server.create_fastmcp_server()
    if fast_mcp:
        print("启动知网搜索FastMCP服务器...")
        fast_mcp.run()
    else:
        # 回退到标准接口
        print("启动知网搜索MCP服务器（低级接口）...")
        asyncio.run(server.main())

# 导出重要项目
__all__ = ['main', 'server', 'add_note']
import asyncio
import json
import os
import platform
import re
import subprocess
import sys
import time
import logging
import webbrowser
import traceback
from pathlib import Path
from urllib.parse import quote
from typing import Dict, List, Any, Optional, Union

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
from pydantic import AnyUrl
import mcp.server.stdio

# 配置日志记录
logging.basicConfig(
    level=logging.DEBUG, 
    filename="cnks.log",
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("cnks")

# 尝试导入playwright
try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    logger.warning("Playwright未安装，将使用传统方式打开Chrome")

# 存储当前页面内容和笔记
page_content = ""
current_url = ""
notes: dict[str, str] = {}
browser_instance = None

server = Server("cnks")

# 导入我们新创建的extractor模块
try:
    from . import chrome_extractor as extractor
except ImportError:
    try:
        import chrome_extractor as extractor
    except ImportError:
        extractor = None
        logger.warning("无法导入chrome_extractor模块，批量提取功能将不可用")

def find_chrome_executable():
    """查找Chrome可执行文件路径"""
    system = platform.system()
    
    # 定义可能的Chrome位置
    if system == "Windows":
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe"),
        ]
    elif system == "Darwin":  # MacOS
        chrome_paths = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            os.path.expanduser("~/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
        ]
    elif system == "Linux":
        chrome_paths = [
            "/usr/bin/google-chrome",
            "/usr/bin/chromium-browser",
            "/usr/bin/chromium",
        ]
    else:
        return None
    
    # 检查路径是否存在
    for path in chrome_paths:
        if os.path.exists(path):
            return path
    
    # 尝试从环境变量中查找
    chrome_env = os.environ.get("CHROME_PATH")
    if chrome_env and os.path.exists(chrome_env):
        return chrome_env
    
    return None

def open_chrome(url):
    """打开Chrome浏览器并访问指定URL"""
    try:
        chrome_path = find_chrome_executable()
        
        if not chrome_path:
            return "未找到Chrome可执行文件。请设置CHROME_PATH环境变量指向Chrome位置。"
        
        subprocess.Popen([
            chrome_path, 
            url
        ])
        time.sleep(2)  # 等待页面加载
        return True
    except Exception as e:
        return f"打开Chrome时出错: {str(e)}"

async def search_with_playwright(keywords):
    """使用playwright在知网搜索关键词"""
    global page_content
    
    if not PLAYWRIGHT_AVAILABLE:
        return "需要安装playwright模块：uv add playwright"
    
    try:
        chrome_path = find_chrome_executable()
        if not chrome_path:
            return "未找到Chrome可执行文件。请设置CHROME_PATH环境变量指向Chrome位置。"
        
        logger.debug(f"[DEBUG] 使用Playwright搜索，Chrome路径: {chrome_path}")
        
        # 创建全局浏览器实例，避免执行完关闭
        global browser_instance
        
        # 只打开一个playwright实例
        playwright = await async_playwright().start()
        
        # 尝试使用系统Chrome
        try:
            logger.debug("[DEBUG] 尝试使用channel='chrome'启动浏览器")
            browser = await playwright.chromium.launch(
                headless=False,
                channel="chrome"
            )
        except Exception as e:
            logger.debug(f"[DEBUG] channel='chrome'方式失败: {str(e)}")
            logger.debug("[DEBUG] 尝试使用executable_path启动浏览器")
            # 如果失败，尝试使用executable_path指定Chrome路径
            browser = await playwright.chromium.launch(
                headless=False, 
                executable_path=chrome_path
            )
        
        # 保存浏览器实例以防止被关闭
        browser_instance = browser
        
        page = await browser.new_page()
        
        # 导航到知网搜索页面
        await page.goto("https://kns.cnki.net/kns8s/search")
        logger.debug("[DEBUG] 成功打开知网搜索页面")
        
        # 等待页面加载
        await page.wait_for_load_state("networkidle")
        
        # 查找并填写搜索框
        try:
            # 尝试定位搜索框
            search_input = await page.query_selector('input.search-input')
            if search_input:
                # 清空搜索框
                await search_input.fill("")
                # 输入关键词
                await search_input.fill(keywords)
                logger.debug(f"[DEBUG] 已在搜索框中输入: {keywords}")
                
                # 增加短暂等待以确保用户可以看到输入过程
                await asyncio.sleep(1)
                
                # 查找并点击搜索按钮
                search_button = await page.query_selector('.search-btn')
                if search_button:
                    await search_button.click()
                    logger.debug("[DEBUG] 已点击搜索按钮")
                    # 等待搜索结果加载
                    await page.wait_for_load_state("networkidle")
                    
                    # 点击操作1：点击下拉框的三角形
                    try:
                        # 等待一下，确保页面元素都加载完成
                        await asyncio.sleep(2)
                        
                        # 尝试点击排序下拉框
                        logger.debug("[DEBUG] 尝试点击排序下拉框")
                        # 根据提供的HTML，尝试定位下拉框的三角形
                        sort_dropdown = await page.query_selector('div[class="sort"][id="perPageDiv"]')
                        if sort_dropdown:
                            await sort_dropdown.click()
                            logger.debug("[DEBUG] 成功点击排序下拉框")
                            
                            # 等待下拉菜单出现
                            await asyncio.sleep(1)
                            
                            # 点击操作2：点击数字50选项
                            logger.debug("[DEBUG] 尝试点击'50'选项")
                            # 尝试定位"50"选项
                            option_50 = await page.query_selector('li[data-val="50"]')
                            if option_50:
                                await option_50.click()
                                logger.debug("[DEBUG] 成功点击'50'选项")
                                await page.wait_for_load_state("networkidle")
                                
                                # 勾选来源类别中的CSSCI选项
                                try:
                                    # 等待一下确保页面完全加载
                                    await asyncio.sleep(2)
                                    
                                    logger.debug("[DEBUG] 尝试勾选CSSCI选项")
                                    
                                    # 首先尝试找到来源类别区域
                                    # 通常来源类别会有一个标题或者分组
                                    source_category = await page.query_selector('div.group-item:has-text("来源类别")')
                                    
                                    if source_category:
                                        logger.debug("[DEBUG] 找到来源类别区域")
                                        
                                        # 在来源类别区域内查找CSSCI选项
                                        cssci_checkbox = await source_category.query_selector('input[type="checkbox"]:near(:text("CSSCI"))')
                                        
                                        if cssci_checkbox:
                                            # 点击CSSCI复选框
                                            await cssci_checkbox.click()
                                            logger.debug("[DEBUG] 成功勾选CSSCI选项")
                                            
                                            # 等待页面刷新
                                            await page.wait_for_load_state("networkidle")
                                            
                                            # 查找所有包含"article/abstract?v="字样的链接
                                            links_count = await find_and_count_abstract_links(page)
                                            
                                            return links_count
                                        else:
                                            logger.debug("[DEBUG] 在来源类别区域未找到CSSCI选项")
                                            
                                            # 尝试另一种方式：直接在整个页面中查找CSSCI
                                            cssci_text = await page.query_selector(':text("CSSCI")')
                                            if cssci_text:
                                                # 尝试点击文本附近的复选框
                                                await cssci_text.click()
                                                logger.debug("[DEBUG] 通过文本找到并点击了CSSCI")
                                                await page.wait_for_load_state("networkidle")
                                                
                                                # 查找所有包含"article/abstract?v="字样的链接
                                                links_count = await find_and_count_abstract_links(page)
                                                
                                                return links_count
                                            else:
                                                # 查找所有包含"article/abstract?v="字样的链接
                                                links_count = await find_and_count_abstract_links(page)
                                                return links_count
                                    else:
                                        logger.debug("[DEBUG] 未找到来源类别区域")
                                        
                                        # 尝试直接在页面中查找CSSCI文本
                                        cssci_text = await page.query_selector(':text("CSSCI")')
                                        if cssci_text:
                                            # 尝试点击文本附近的复选框
                                            await cssci_text.click()
                                            logger.debug("[DEBUG] 直接找到并点击了CSSCI")
                                            await page.wait_for_load_state("networkidle")
                                            
                                            # 查找所有包含"article/abstract?v="字样的链接
                                            links_count = await find_and_count_abstract_links(page)
                                            
                                            return links_count
                                        else:
                                            # 查找所有包含"article/abstract?v="字样的链接
                                            links_count = await find_and_count_abstract_links(page)
                                            return links_count
                                except Exception as e:
                                    logger.debug(f"[DEBUG] 勾选CSSCI选项时出错: {str(e)}")
                                    # 查找所有包含"article/abstract?v="字样的链接
                                    links_count = await find_and_count_abstract_links(page)
                                    return links_count
                                
                                # 查找所有包含"article/abstract?v="字样的链接
                                links_count = await find_and_count_abstract_links(page)
                                return links_count
                            else:
                                logger.debug("[DEBUG] 未找到'50'选项")
                                page_content = {
                                    "count": 0,
                                    "links": [],
                                    "error": "已搜索并点击下拉框，但未找到'50'选项"
                                }
                                return 0
                        else:
                            logger.debug("[DEBUG] 未找到排序下拉框")
                            page_content = {
                                "count": 0,
                                "links": [],
                                "error": "已搜索，但未找到排序下拉框"
                            }
                            return 0
                    except Exception as e:
                        logger.debug(f"[DEBUG] 点击下拉框或选项时出错: {str(e)}")
                        page_content = {
                            "count": 0,
                            "links": [],
                            "error": f"已搜索，但在点击下拉框或选项时出错: {str(e)}"
                        }
                        return 0
                else:
                    # 不关闭浏览器
                    page_content = {
                        "count": 0,
                        "links": [],
                        "error": f"已填写搜索关键词: {keywords}，但未找到搜索按钮"
                    }
                    return 0
            else:
                # 不关闭浏览器
                page_content = {
                    "count": 0,
                    "links": [],
                    "error": f"未找到搜索框，无法搜索: {keywords}"
                }
                return 0
        except Exception as e:
            logger.debug(f"[DEBUG] 填写搜索框或点击搜索按钮时出错: {str(e)}")
            # 不关闭浏览器
            page_content = {
                "count": 0,
                "links": [],
                "error": f"自动搜索过程中出错: {str(e)}"
            }
            return 0
    except Exception as e:
        error_msg = str(e)
        logger.debug(f"[DEBUG] Playwright错误: {error_msg}")
        
        # 如果是找不到Chrome的错误，提供更明确的指导
        if "Executable doesn't exist" in error_msg and "ms-playwright" in error_msg:
            error_message = f"需要安装Playwright的浏览器: playwright install\n如果您想使用系统Chrome，请重新启动服务器。\n\n{error_msg}"
        else:
            error_message = f"使用Playwright启动Chrome失败: {error_msg}"
            
        page_content = {
            "count": 0,
            "links": [],
            "error": error_message
        }
        return 0

def search_with_direct_chrome(keywords):
    """直接使用Chrome搜索，不使用playwright"""
    global page_content
    
    logger.debug("[DEBUG] 正在使用search_with_direct_chrome函数")
    
    try:
        url = f"https://kns.cnki.net/kns8s/search?q={quote(keywords)}"
        logger.debug(f"[DEBUG] 打开URL: {url}")
        
        result = open_chrome(url)
        
        if isinstance(result, str) and "打开Chrome" in result:
            logger.debug(f"[DEBUG] 直接打开Chrome结果: {result}")
            
            page_content = {
                "count": 0,
                "links": [],
                "error": f"直接打开Chrome搜索: {result}"
            }
            
        else:
            logger.debug("[DEBUG] 直接打开Chrome成功")
            
            page_content = {
                "count": 0,
                "links": [],
                "message": "已打开Chrome并搜索关键词，但无法自动获取链接。请安装playwright以获取完整功能。"
            }
        
        return page_content
    except Exception as e:
        logger.debug(f"[DEBUG] search_with_direct_chrome出错: {str(e)}")
        
        page_content = {
            "count": 0,
            "links": [],
            "error": f"使用Chrome搜索时出错: {str(e)}"
        }
        
        return page_content

def get_page_content():
    """获取当前页面内容（简化模拟）"""
    global page_content, current_url
    if not current_url:
        return "尚未打开任何页面"
    
    # 实际应用中，这里可以使用Selenium或类似工具来获取实际页面内容
    # 此处为简化实现，返回模拟内容
    if "cnki" in current_url:
        return f"中国知网搜索页面\n当前URL: {current_url}\n可使用搜索工具查询文献。"
    return f"已打开页面: {current_url}"

@server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    """列出可用资源"""
    resources = []
    
    # 当前网页资源
    resources.append(
        types.Resource(
            uri=AnyUrl("webpage://current"),
            name="当前网页",
            description="当前打开的网页内容",
            mimeType="text/plain",
        )
    )
    
    # 知网搜索页资源
    resources.append(
        types.Resource(
            uri=AnyUrl("webpage://cnki/search"),
            name="知网搜索页",
            description="中国知网搜索页面",
            mimeType="text/plain",
        )
    )
    
    # 笔记资源
    for name in notes:
        resources.append(
            types.Resource(
                uri=AnyUrl(f"note://internal/{name}"),
                name=f"笔记: {name}",
                description=f"笔记: {name}",
                mimeType="text/plain",
            )
        )
    
    return resources

@server.read_resource()
async def handle_read_resource(uri: AnyUrl) -> str:
    """读取资源内容"""
    global current_url
    
    scheme = uri.scheme
    
    if scheme == "webpage":
        path = uri.path if uri.path else ""
        host = uri.host if uri.host else ""
        
        if host == "current":
            return get_page_content()
        elif host == "cnki" and path == "/search":
            # 打开知网搜索页
            current_url = "https://kns.cnki.net/kns8s/search"
            result = open_chrome(current_url)
            if result is True:
                return "已打开中国知网搜索页面，可使用搜索工具查询文献。"
            else:
                return result
    elif scheme == "note":
        name = uri.path
        if name is not None:
            name = name.lstrip("/")
            if name in notes:
                return notes[name]
            raise ValueError(f"笔记未找到: {name}")
    
    raise ValueError(f"不支持的URI方案或资源未找到: {uri}")

@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    """列出可用提示"""
    return [
        types.Prompt(
            name="search-literature",
            description="按主题搜索文献",
            arguments=[
                types.PromptArgument(
                    name="keywords",
                    description="搜索关键词",
                    required=True,
                )
            ],
        ),
        types.Prompt(
            name="advanced-search",
            description="高级文献搜索",
            arguments=[
                types.PromptArgument(
                    name="title",
                    description="论文标题",
                    required=False,
                ),
                types.PromptArgument(
                    name="author",
                    description="作者",
                    required=False,
                ),
                types.PromptArgument(
                    name="keywords",
                    description="关键词",
                    required=False,
                ),
                types.PromptArgument(
                    name="institution",
                    description="机构",
                    required=False,
                ),
            ],
        ),
        types.Prompt(
            name="summarize-notes",
            description="总结所有笔记",
            arguments=[
                types.PromptArgument(
                    name="style",
                    description="摘要风格 (brief/detailed)",
                    required=False,
                )
            ],
        )
    ]

@server.get_prompt()
async def handle_get_prompt(
    name: str, arguments: dict[str, str] | None
) -> types.GetPromptResult:
    """生成提示"""
    if name == "search-literature":
        keywords = (arguments or {}).get("keywords", "")
        return types.GetPromptResult(
            description="按主题搜索文献",
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"请在中国知网搜索关于\"{keywords}\"的文献，并分析主要研究趋势。"
                    ),
                )
            ],
        )
    elif name == "advanced-search":
        title = (arguments or {}).get("title", "")
        author = (arguments or {}).get("author", "")
        keywords = (arguments or {}).get("keywords", "")
        institution = (arguments or {}).get("institution", "")
        
        search_terms = []
        if title:
            search_terms.append(f"标题包含\"{title}\"")
        if author:
            search_terms.append(f"作者为\"{author}\"")
        if keywords:
            search_terms.append(f"关键词包含\"{keywords}\"")
        if institution:
            search_terms.append(f"机构为\"{institution}\"")
        
        search_criteria = "、".join(search_terms)
        
        return types.GetPromptResult(
            description="高级文献搜索",
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"请在中国知网搜索{search_criteria}的文献，并总结相关研究成果。"
                    ),
                )
            ],
        )
    elif name == "summarize-notes":
        style = (arguments or {}).get("style", "brief")
        detail_prompt = "请提供详细分析。" if style == "detailed" else ""
        
        return types.GetPromptResult(
            description="总结所有笔记",
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"以下是需要总结的笔记：{detail_prompt}\n\n"
                        + "\n".join(
                            f"- {name}: {content}"
                            for name, content in notes.items()
                        ),
                    ),
                )
            ],
        )
    
    raise ValueError(f"未知提示: {name}")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """列出可用工具"""
    tools = []
    
    # 只添加搜索并提取的组合工具
    if extractor is not None and PLAYWRIGHT_AVAILABLE:
        tools.append(
            types.Tool(
                name="mcp_cnks_search_and_extract",
                description="搜索知网关键词并提取所有论文的详细内容",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "keywords": {"type": "string", "description": "搜索关键词"},
                    },
                    "required": ["keywords"],
                },
            )
        )
    
    return tools

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """处理工具执行请求"""
    global current_url, page_content
    
    if name == "mcp_cnks_search_and_extract" and extractor is not None and PLAYWRIGHT_AVAILABLE:
        if not arguments:
            raise ValueError("缺少参数")
        
        keywords = arguments.get("keywords")
        if not keywords:
            raise ValueError("缺少关键词")
        
        try:
            # 第一步：执行搜索
            logger.info(f"开始执行搜索并提取：关键词 '{keywords}'")
            links_count = await search_with_playwright(keywords)
            current_url = "https://kns.cnki.net/kns8s/search"
            
            # 检查搜索结果
            if not isinstance(page_content, dict) or "links" not in page_content or not page_content["links"]:
                return [
                    types.TextContent(
                        type="text",
                        text=json.dumps({
                            "error": "搜索未返回有效链接",
                            "count": 0,
                            "results": []
                        }, ensure_ascii=False)
                    )
                ]
            
            # 提取链接
            urls = [link["url"] for link in page_content["links"] if "url" in link]
            if not urls:
                return [
                    types.TextContent(
                        type="text",
                        text=json.dumps({
                            "error": "未找到有效链接",
                            "count": 0,
                            "results": []
                        }, ensure_ascii=False)
                    )
                ]
            
            # 第二步：执行提取
            logger.info(f"搜索成功，找到 {len(urls)} 个链接，开始提取内容")
            results = await extractor.batch_extract_contents(urls)
            
            # 包装结果
            result_json = {
                "keywords": keywords,
                "count": len(results),
                "results": results,
                "success_count": sum(1 for r in results if "error" not in r or not r["error"]),
                "error_count": sum(1 for r in results if "error" in r and r["error"])
            }
            
            return [
                types.TextContent(
                    type="text",
                    text=json.dumps(result_json, ensure_ascii=False)
                )
            ]
        except Exception as e:
            logger.error(f"搜索并提取时出错: {str(e)}")
            logger.error(traceback.format_exc())
            return [
                types.TextContent(
                    type="text",
                    text=json.dumps({
                        "error": f"搜索并提取内容时出错: {str(e)}",
                        "keywords": keywords,
                        "count": 0,
                        "results": []
                    }, ensure_ascii=False)
                )
            ]
    
    else:
        raise ValueError(f"未知工具: {name}")

async def find_and_count_abstract_links(page):
    """查找并统计包含article/abstract?v=的链接"""
    global page_content
    
    try:
        logger.debug("[DEBUG] 开始查找所有包含article/abstract?v=的链接")
        
        # 等待确保页面完全加载
        await asyncio.sleep(2)
        
        # 查找所有链接
        all_links = await page.query_selector_all('a[href*="article/abstract?v="]')
        links_count = len(all_links)
        
        logger.debug(f"[DEBUG] 找到{links_count}条包含article/abstract?v=的链接")
        
        # 提取并记录每个链接的URL和文本
        links_info = []
        
        for i, link in enumerate(all_links):
            href = await link.get_attribute('href')
            
            links_info.append({
                'index': i + 1,
                'href': href
            })
            
            logger.debug(f"[DEBUG] 链接 {i+1}: {href}")
        
        # 判断数量是否符合预期(50条)
        if links_count == 50:
            logger.debug("[DEBUG] 链接数量正好是50条，符合预期")
        elif links_count < 50:
            logger.debug(f"[DEBUG] 链接数量为{links_count}条，少于预期的50条")
        else:
            logger.debug(f"[DEBUG] 链接数量为{links_count}条，多于预期的50条")
        
        # 存储结果 - 使用字典结构而不是纯文本
        page_content = {
            "count": links_count,
            "links": [{"index": link['index'], "url": link['href']} for link in links_info]
        }
        
        return links_count
    except Exception as e:
        logger.debug(f"[DEBUG] 查找链接时出错: {str(e)}")
        return 0

async def main():
    """主程序入口"""
    # 使用stdin/stdout流运行服务器
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="cnks",
                server_version="0.2.1",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

# 为符合README.md的要求，添加从FastMCP导出的接口
def create_fastmcp_server():
    """创建FastMCP服务器接口，符合README中的示例"""
    try:
        from mcp.server.fastmcp import FastMCP
        fast_mcp = FastMCP("知网搜索")
        
        # 只添加搜索并提取的工具
        if extractor is not None and PLAYWRIGHT_AVAILABLE:
            @fast_mcp.tool()
            async def mcp_cnks_search_and_extract(keywords: str) -> dict:
                """搜索关键词并提取所有论文的详细内容"""
                logger.debug("[DEBUG] 正在使用FastMCP的mcp_cnks_search_and_extract函数")
                try:
                    # 第一步：执行搜索
                    result_count = await search_with_playwright(keywords)
                    
                    # 检查搜索结果
                    if not isinstance(page_content, dict) or "links" not in page_content or not page_content["links"]:
                        return {
                            "error": "搜索未返回有效链接",
                            "keywords": keywords,
                            "count": 0,
                            "results": []
                        }
                    
                    # 提取链接
                    urls = [link["url"] for link in page_content["links"] if "url" in link]
                    if not urls:
                        return {
                            "error": "未找到有效链接",
                            "keywords": keywords,
                            "count": 0,
                            "results": []
                        }
                    
                    # 第二步：执行提取
                    results = await extractor.batch_extract_contents(urls)
                    
                    # 包装结果
                    return {
                        "keywords": keywords,
                        "count": len(results),
                        "results": results,
                        "success_count": sum(1 for r in results if "error" not in r or not r["error"]),
                        "error_count": sum(1 for r in results if "error" in r and r["error"])
                    }
                except Exception as e:
                    logger.error(f"搜索并提取时出错: {str(e)}")
                    return {
                        "error": f"搜索并提取内容时出错: {str(e)}",
                        "keywords": keywords,
                        "count": 0,
                        "results": []
                    }
        
        return fast_mcp
    except ImportError:
        logger.warning("警告: 无法导入FastMCP，请确保已安装最新版本的MCP")
        return None

if __name__ == "__main__":
    asyncio.run(main())
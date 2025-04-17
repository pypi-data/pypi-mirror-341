import asyncio
import json
import os
import platform
import re
import subprocess
import sys
import time
import logging
from pathlib import Path
from urllib.parse import quote

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
                                            
                                            return f"已完成全部操作：搜索关键词、设置每页显示50条、勾选CSSCI来源类别。找到{links_count}条包含article/abstract?v=的链接。浏览器将保持打开状态。"
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
                                                
                                                return f"已完成全部操作：搜索关键词、设置每页显示50条、勾选CSSCI来源类别。找到{links_count}条包含article/abstract?v=的链接。浏览器将保持打开状态。"
                                            else:
                                                return "已完成搜索和设置每页显示50条，但未找到CSSCI选项。浏览器将保持打开状态。"
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
                                            
                                            return f"已完成全部操作：搜索关键词、设置每页显示50条、勾选CSSCI来源类别。找到{links_count}条包含article/abstract?v=的链接。浏览器将保持打开状态。"
                                        else:
                                            return "已完成搜索和设置每页显示50条，但未找到来源类别区域或CSSCI选项。浏览器将保持打开状态。"
                                except Exception as e:
                                    logger.debug(f"[DEBUG] 勾选CSSCI选项时出错: {str(e)}")
                                    return f"已完成搜索和设置每页显示50条，但勾选CSSCI时出错: {str(e)}。浏览器将保持打开状态。"
                                
                                return "已完成全部操作：搜索关键词、点击排序下拉框、选择每页显示50条。浏览器将保持打开状态。"
                            else:
                                logger.debug("[DEBUG] 未找到'50'选项")
                                return "已搜索并点击下拉框，但未找到'50'选项。浏览器将保持打开状态。"
                        else:
                            logger.debug("[DEBUG] 未找到排序下拉框")
                            return "已搜索，但未找到排序下拉框。浏览器将保持打开状态。"
                    except Exception as e:
                        logger.debug(f"[DEBUG] 点击下拉框或选项时出错: {str(e)}")
                        return f"已搜索，但在点击下拉框或选项时出错: {str(e)}。浏览器将保持打开状态。"
                    
                    # 不关闭浏览器，让它保持打开状态
                    # 注意：不调用 browser.close() 和 playwright.stop()
                else:
                    # 不关闭浏览器
                    return f"已填写搜索关键词: {keywords}，但未找到搜索按钮。请手动点击搜索。"
            else:
                # 不关闭浏览器
                return f"未找到搜索框。已打开知网页面，请手动搜索: {keywords}"
        except Exception as e:
            logger.debug(f"[DEBUG] 填写搜索框或点击搜索按钮时出错: {str(e)}")
            # 不关闭浏览器
            return f"自动搜索过程中出错，请手动在页面中搜索: {keywords}"
    except Exception as e:
        error_msg = str(e)
        logger.debug(f"[DEBUG] Playwright错误: {error_msg}")
        
        # 如果是找不到Chrome的错误，提供更明确的指导
        if "Executable doesn't exist" in error_msg and "ms-playwright" in error_msg:
            return f"需要安装Playwright的浏览器: playwright install\n如果您想使用系统Chrome，请重新启动服务器。\n\n{error_msg}"
        
        # 如果Playwright启动失败，使用传统方式打开Chrome
        return f"使用Playwright启动Chrome失败: {error_msg}。尝试使用传统方式打开浏览器。"

def search_with_direct_chrome(keywords):
    """直接使用Chrome搜索，不使用playwright"""
    logger.debug("[DEBUG] 正在使用search_with_direct_chrome函数")
    
    # 构建知网搜索URL - 知网不支持URL参数搜索，所以只能打开页面
    url = "https://kns.cnki.net/kns8s/search"
    
    # 打开Chrome
    result = open_chrome(url)
    
    if result is True:
        return f"已打开知网页面。请在搜索框中输入并搜索: {keywords}"
    else:
        return f"打开Chrome浏览器失败: {result}"

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
    return [
        types.Tool(
            name="open-cnki",
            description="打开中国知网搜索页面",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name="search-keywords",
            description="在知网搜索关键词",
            inputSchema={
                "type": "object",
                "properties": {
                    "keywords": {"type": "string", "description": "搜索关键词"},
                },
                "required": ["keywords"],
            },
        ),
        types.Tool(
            name="add-note",
            description="添加笔记",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "笔记名称"},
                    "content": {"type": "string", "description": "笔记内容"},
                },
                "required": ["name", "content"],
            },
        ),
        types.Tool(
            name="get-abstract-links",
            description="获取最近一次搜索找到的论文摘要链接",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """处理工具执行请求"""
    global current_url, page_content
    
    if name == "open-cnki":
        current_url = "https://kns.cnki.net/kns8s/search"
        result = open_chrome(current_url)
        if result is True:
            return [
                types.TextContent(
                    type="text",
                    text="已打开中国知网搜索页面。"
                )
            ]
        else:
            return [
                types.TextContent(
                    type="text",
                    text=f"打开中国知网时出错: {result}"
                )
            ]
    
    elif name == "search-keywords":
        if not arguments:
            raise ValueError("缺少参数")
        
        keywords = arguments.get("keywords")
        if not keywords:
            raise ValueError("缺少关键词")
        
        # 优先使用playwright进行搜索
        if PLAYWRIGHT_AVAILABLE:
            result = await search_with_playwright(keywords)
            current_url = "https://kns.cnki.net/kns8s/search"
            
            return [
                types.TextContent(
                    type="text",
                    text=result
                )
            ]
        else:
            # 如果没有playwright，回退到传统方式
            result = search_with_direct_chrome(keywords)
            current_url = "https://kns.cnki.net/kns8s/search"
            
            return [
                types.TextContent(
                    type="text",
                    text=f"{result}。如需自动搜索功能，请安装: uv add playwright"
                )
            ]
    
    elif name == "add-note":
        if not arguments:
            raise ValueError("缺少参数")
        
        note_name = arguments.get("name")
        content = arguments.get("content")
        
        if not note_name or not content:
            raise ValueError("缺少名称或内容")
        
        # 更新服务器状态
        notes[note_name] = content
        
        # 通知客户端资源已更改
        await server.request_context.session.send_resource_list_changed()
        
        return [
            types.TextContent(
                type="text",
                text=f"已添加笔记 '{note_name}': {content}"
            )
        ]
    
    elif name == "get-abstract-links":
        if not page_content or "找到" not in page_content:
            return [
                types.TextContent(
                    type="text",
                    text="尚未执行搜索或未找到链接。请先使用search-keywords工具搜索。"
                )
            ]
        
        return [
            types.TextContent(
                type="text",
                text=page_content
            )
        ]
    
    raise ValueError(f"未知工具: {name}")

async def find_and_count_abstract_links(page):
    """查找并统计包含article/abstract?v=的链接"""
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
        
        # 存储结果 - 只包含编号和链接，不包含标题和连字符
        global page_content
        page_content = f"找到{links_count}条包含article/abstract?v=的链接\n\n" + "\n".join([
            f"{link['index']}. {link['href']}" for link in links_info
        ])
        
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
                server_version="0.1.0",
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
        
        @fast_mcp.tool()
        def open_cnki_search():
            """打开中国知网搜索页面"""
            return open_chrome("https://kns.cnki.net/kns8s/search")
        
        @fast_mcp.tool()
        async def search_keywords(keywords: str) -> str:
            """在知网搜索关键词"""
            logger.debug("[DEBUG] 正在使用FastMCP的search_keywords函数")
            if PLAYWRIGHT_AVAILABLE:
                result = await search_with_playwright(keywords)
                return result
            else:
                result = search_with_direct_chrome(keywords)
                return f"{result}。如需自动搜索功能，请安装: uv add playwright"
        
        @fast_mcp.tool()
        def get_abstract_links() -> str:
            """获取最近一次搜索找到的论文摘要链接"""
            if not page_content or "找到" not in page_content:
                return "尚未执行搜索或未找到链接。请先使用search_keywords工具搜索。"
            return page_content
        
        @fast_mcp.resource("webpage://current")
        def get_current_webpage() -> str:
            """获取当前网页内容"""
            return get_page_content()
        
        return fast_mcp
    except ImportError:
        logger.warning("警告: 无法导入FastMCP，请确保已安装最新版本的MCP")
        return None

if __name__ == "__main__":
    asyncio.run(main())
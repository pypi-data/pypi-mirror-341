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
from datetime import datetime
from pydantic import BaseModel, AnyUrl

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
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

# 定义数据模型
class CNKIContent(BaseModel):
    """CNKI论文内容模型"""
    title: str = ""
    authors: List[str] = []
    abstract: str = ""
    keywords: List[str] = []
    cite_format: str = ""
    url: str = ""  # 添加URL字段以记录来源

# 存储当前页面内容和笔记
page_content = ""
current_url = ""
notes: dict[str, str] = {}

server = Server("cnks")

# 添加全局变量来跟踪playwright状态
playwright_instance = None
browser_instance = None
context = None

def find_chrome_executable():
    """查找Chrome可执行文件路径"""
    # 首先检查环境变量
    chrome_env = os.environ.get("CHROME_PATH")
    if chrome_env and os.path.exists(chrome_env):
        logger.debug(f"[DEBUG] 从环境变量找到Chrome: {chrome_env}")
        return chrome_env
        
    system = platform.system()
    logger.debug(f"[DEBUG] 系统类型: {system}")
    
    # 定义可能的Chrome位置
    if system == "Windows":
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe"),
            # Edge浏览器也是基于Chromium的
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        ]
    elif system == "Darwin":  # MacOS
        chrome_paths = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            os.path.expanduser("~/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
            "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        ]
    elif system == "Linux":
        chrome_paths = [
            "/usr/bin/google-chrome",
            "/usr/bin/chromium-browser",
            "/usr/bin/chromium",
            "/usr/bin/microsoft-edge",
        ]
    else:
        logger.debug(f"[DEBUG] 未知系统类型: {system}")
        return None
    
    # 检查路径是否存在
    for path in chrome_paths:
        if os.path.exists(path):
            logger.debug(f"[DEBUG] 找到Chrome: {path}")
            return path
    
    # 如果上述路径都不存在，尝试使用which命令查找
    try:
        if system != "Windows":
            # 在Unix系统上尝试使用which命令
            for browser in ["google-chrome", "chromium", "chromium-browser", "microsoft-edge"]:
                try:
                    result = subprocess.check_output(["which", browser], universal_newlines=True).strip()
                    if result and os.path.exists(result):
                        logger.debug(f"[DEBUG] 使用which命令找到浏览器: {result}")
                        return result
                except subprocess.CalledProcessError:
                    pass
        else:
            # 在Windows上尝试使用where命令
            try:
                result = subprocess.check_output(["where", "chrome"], universal_newlines=True).strip()
                if result:
                    # where可能返回多行，取第一行
                    first_path = result.split('\n')[0].strip()
                    if os.path.exists(first_path):
                        logger.debug(f"[DEBUG] 使用where命令找到Chrome: {first_path}")
                        return first_path
            except subprocess.CalledProcessError:
                pass
                
            # 尝试查找Edge
            try:
                result = subprocess.check_output(["where", "msedge"], universal_newlines=True).strip()
                if result:
                    first_path = result.split('\n')[0].strip()
                    if os.path.exists(first_path):
                        logger.debug(f"[DEBUG] 使用where命令找到Edge: {first_path}")
                        return first_path
            except subprocess.CalledProcessError:
                pass
    except Exception as e:
        logger.debug(f"[DEBUG] 使用命令行查找浏览器时出错: {str(e)}")
    
    logger.debug("[DEBUG] 未找到Chrome或兼容的浏览器")
    return None

def open_chrome(url):
    """打开Chrome浏览器并访问指定URL"""
    try:
        logger.debug(f"[DEBUG] open_chrome函数被调用，URL: {url}")
        
        # 使用webbrowser模块打开URL（会使用系统默认浏览器，通常是已经打开的Chrome）
        logger.debug(f"[DEBUG] 尝试使用webbrowser.open打开URL: {url}")
        webbrowser.open(url)
        logger.debug(f"[DEBUG] webbrowser.open调用完成")
        
        # 等待页面加载
        time.sleep(2)
        logger.debug("[DEBUG] open_chrome函数执行完毕")
        return True
    except Exception as e:
        logger.debug(f"[DEBUG] open_chrome函数出错: {str(e)}")
        return f"打开Chrome时出错: {str(e)}"

async def search_with_playwright(keywords):
    """使用playwright在知网搜索关键词"""
    global page_content
    
    if not PLAYWRIGHT_AVAILABLE:
        return "需要安装playwright模块：uv add playwright"
    
    try:
        logger.debug(f"[DEBUG] 使用搜索功能，关键词: {keywords}")
        
        # 先访问知网首页而不是直接访问搜索结果页
        initial_url = "https://kns.cnki.net/"
        search_url = f"https://kns.cnki.net/kns8s/search?q={quote(keywords)}"
        logger.debug(f"[DEBUG] 初始URL: {initial_url}")
        
        # 创建全局变量来跟踪playwright状态
        global playwright_instance, browser_instance, context
        
        # 查找Chrome路径
        chrome_path = find_chrome_executable()
        if not chrome_path:
            logger.warning("[WARNING] 未找到Chrome可执行文件，将使用默认浏览器")
            # 使用webbrowser模块打开
            webbrowser.open(search_url)
            # 构造一个基本结果
            page_content = {
                "count": 1,
                "links": [{
                    "index": 1,
                    "url": search_url,
                    "title": f"搜索: {keywords}"
                }]
            }
            return 1
            
        logger.debug(f"[DEBUG] 找到Chrome路径: {chrome_path}")
        
        # 检查playwright是否已经运行
        if 'playwright_instance' not in globals() or playwright_instance is None:
            logger.debug("[DEBUG] 初始化新的playwright实例")
            # 第一次运行，初始化playwright
            playwright_instance = await async_playwright().start()
            
            # 设置启动选项
            browser_args = []
            
            # 使用系统已安装的Chrome
            if chrome_path:
                browser_args.extend([
                    '--no-sandbox',  # 在某些环境中可能需要
                    '--start-maximized'  # 最大化窗口
                ])
            
            # 启动浏览器 - 尝试使用系统Chrome
            try:
                # 首先尝试使用chrome_path启动
                logger.debug(f"[DEBUG] 尝试使用系统Chrome启动: {chrome_path}")
                browser_instance = await playwright_instance.chromium.launch(
                    headless=False,  # 显示浏览器界面
                    executable_path=chrome_path,
                    args=browser_args
                )
            except Exception as e:
                logger.warning(f"[WARNING] 使用系统Chrome启动失败: {str(e)}，尝试使用默认浏览器")
                # 如果失败，使用默认浏览器
                browser_instance = await playwright_instance.chromium.launch(
                    headless=False  # 显示浏览器界面
                )
            
            # 创建上下文
            context = await browser_instance.new_context(
                viewport=None  # 不限制视窗大小，使用浏览器默认设置
            )
            
            # 创建新页面
            page = await context.new_page()
            
            # 访问初始URL(知网首页)
            logger.debug(f"[DEBUG] 导航到知网首页: {initial_url}")
            await page.goto(initial_url)
            logger.debug("[DEBUG] 已打开新的浏览器窗口并访问知网首页")
        else:
            logger.debug("[DEBUG] 在现有playwright实例中打开新标签页")
            # playwright已经在运行，创建新标签页
            page = await context.new_page()
            # 访问初始URL(知网首页)
            await page.goto(initial_url)
            logger.debug("[DEBUG] 已在现有浏览器中打开新标签页并访问知网首页")
        
        # 等待页面加载完成
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(1)
        
        # 检查是否需要验证
        await check_and_wait_for_verification(page)
        
        # 尝试执行搜索操作
        try:
            # 方法1: 尝试在首页搜索框输入关键词
            logger.debug("[DEBUG] 尝试在首页查找搜索框")
            
            # 查找搜索框
            search_input_selectors = [
                '#txt_search', 
                'input[type="text"]', 
                '.search-input',
                '.input-box input',
                'input.search-textbox',
                'input[placeholder*="搜索"]'
            ]
            
            search_input = None
            for selector in search_input_selectors:
                try:
                    logger.debug(f"[DEBUG] 尝试查找搜索框选择器: {selector}")
                    search_input = await page.query_selector(selector)
                    if search_input:
                        logger.debug(f"[DEBUG] 找到搜索框: {selector}")
                        break
                except Exception as e:
                    logger.debug(f"[DEBUG] 查找选择器 {selector} 时出错: {str(e)}")
            
            if search_input:
                # 清空搜索框
                await search_input.fill("")
                # 输入关键词
                await search_input.type(keywords, delay=100)  # 添加延迟模拟真实输入
                logger.debug(f"[DEBUG] 已在搜索框中输入关键词: {keywords}")
                
                # 查找搜索按钮
                search_button_selectors = [
                    'button.search-btn', 
                    'button.search',
                    'button[type="submit"]',
                    'input[type="submit"]',
                    '.search-action',
                    'a.search-btn'
                ]
                
                search_button = None
                for selector in search_button_selectors:
                    try:
                        logger.debug(f"[DEBUG] 尝试查找搜索按钮选择器: {selector}")
                        search_button = await page.query_selector(selector)
                        if search_button:
                            logger.debug(f"[DEBUG] 找到搜索按钮: {selector}")
                            break
                    except Exception as e:
                        logger.debug(f"[DEBUG] 查找选择器 {selector} 时出错: {str(e)}")
                
                if search_button:
                    # 点击搜索按钮
                    logger.debug("[DEBUG] 点击搜索按钮")
                    await search_button.click()
                    
                    # 等待搜索结果加载
                    logger.debug("[DEBUG] 等待搜索结果加载")
                    await page.wait_for_load_state('networkidle')
                    await asyncio.sleep(2)
                else:
                    # 如果找不到搜索按钮，尝试按回车
                    logger.debug("[DEBUG] 未找到搜索按钮，尝试按回车键")
                    await search_input.press("Enter")
                    
                    # 等待搜索结果加载
                    logger.debug("[DEBUG] 等待搜索结果加载")
                    await page.wait_for_load_state('networkidle')
                    await asyncio.sleep(2)
            else:
                # 如果找不到搜索框，直接导航到搜索URL
                logger.debug(f"[DEBUG] 未找到搜索框，直接导航到搜索URL: {search_url}")
                await page.goto(search_url)
                await page.wait_for_load_state('networkidle')
                await asyncio.sleep(2)
        except Exception as e:
            logger.debug(f"[DEBUG] 执行搜索操作时出错: {str(e)}")
            logger.debug(traceback.format_exc())
            
            # 如果交互失败，直接导航到搜索URL
            logger.debug(f"[DEBUG] 导航到搜索URL: {search_url}")
            await page.goto(search_url)
            await page.wait_for_load_state('networkidle')
            await asyncio.sleep(2)
        
        # 在搜索结果页面再次检查是否需要验证
        await check_and_wait_for_verification(page)
        
        # 查找并计数链接
        links_count = await find_and_count_abstract_links(page)
        
        # 添加等待时间让用户可以查看结果
        await asyncio.sleep(5)
        
        logger.debug(f"[DEBUG] 搜索完成，找到 {links_count} 个链接")
        
        # 如果找不到链接，使用基本信息构造结果
        if links_count == 0:
            # 获取当前URL
            current_url = await page.url()
            page_content = {
                "count": 1,
                "links": [{
                    "index": 1,
                    "url": current_url,
                    "title": f"搜索: {keywords}"
                }]
            }
        
        return links_count
    except Exception as e:
        error_msg = str(e)
        logger.debug(f"[DEBUG] 搜索错误: {error_msg}")
        logger.debug(traceback.format_exc())
            
        # 尝试直接使用webbrowser打开
        try:
            logger.debug("[DEBUG] 尝试使用webbrowser打开URL")
            webbrowser.open(search_url)
            
            # 构造一个基本结果
            page_content = {
                "count": 1,
                "links": [{
                    "index": 1,
                    "url": search_url,
                    "title": f"搜索: {keywords}"
                }]
            }
            return 1
        except Exception as e2:
            logger.debug(f"[DEBUG] 使用webbrowser打开URL失败: {str(e2)}")
            
            page_content = {
                "count": 0,
                "links": [],
                "error": f"搜索过程中出错: {error_msg}"
            }
            return 0

async def check_and_wait_for_verification(page):
    """检查页面是否需要验证，如果需要则等待用户手动验证"""
    # 验证页面可能包含的特征
    verification_indicators = [
        '验证码',
        '人机验证',
        'captcha',
        'verify',
        '安全验证',
        '滑动验证',
        '拖动滑块',
        '请完成验证',
        '拼图验证'
    ]
    
    try:
        # 获取页面内容
        page_text = await page.content()
        
        # 检查是否包含验证指示词
        needs_verification = any(indicator in page_text for indicator in verification_indicators)
        
        # 尝试查找常见的验证元素
        verification_selectors = [
            '.verify-wrap', 
            '.captcha',
            '.verification',
            '#captcha',
            '.slidecode',
            '.verify-box',
            '.verify-img-panel',
            'iframe[src*="captcha"]',
            'iframe[src*="verify"]'
        ]
        
        for selector in verification_selectors:
            try:
                verify_elem = await page.query_selector(selector)
                if verify_elem:
                    needs_verification = True
                    logger.info(f"[INFO] 检测到验证元素: {selector}")
                    break
            except:
                pass
        
        if needs_verification:
            logger.info("[INFO] 检测到验证页面，等待用户手动验证...")
            print("\n*** 请注意 ***")
            print("检测到需要验证码验证，请在浏览器中完成验证...")
            print("验证完成后，程序将自动继续\n")
            
            # 等待用户完成验证，验证页面可能有不同的特征表明验证完成
            # 例如，特定元素消失或页面URL改变
            max_wait_time = 120  # 最长等待2分钟
            start_time = time.time()
            current_url = await page.url()
            
            while time.time() - start_time < max_wait_time:
                # 每隔一秒检查一次
                await asyncio.sleep(1)
                
                # 检查URL是否改变（可能表示验证成功）
                new_url = await page.url()
                if new_url != current_url:
                    logger.info("[INFO] 检测到URL变化，验证可能已完成")
                    break
                
                # 再次检查验证元素是否消失
                verification_still_present = False
                for selector in verification_selectors:
                    try:
                        verify_elem = await page.query_selector(selector)
                        if verify_elem:
                            verification_still_present = True
                            break
                    except:
                        pass
                
                if not verification_still_present:
                    logger.info("[INFO] 验证元素已消失，验证可能已完成")
                    break
                
                # 检查页面内容是否不再包含验证指示词
                page_text = await page.content()
                if not any(indicator in page_text for indicator in verification_indicators):
                    logger.info("[INFO] 验证指示词已消失，验证可能已完成")
                    break
            
            # 等待页面稳定
            await page.wait_for_load_state('networkidle')
            await asyncio.sleep(2)
            
            logger.info("[INFO] 继续执行，可能已完成验证")
            print("继续执行操作...\n")
        else:
            logger.debug("[DEBUG] 未检测到验证页面")
    
    except Exception as e:
        logger.error(f"[ERROR] 检查验证页面时出错: {str(e)}")
        logger.error(traceback.format_exc())

def search_with_direct_chrome(keywords):
    """直接使用Chrome搜索，不使用playwright"""
    global page_content
    
    logger.debug("[DEBUG] 正在使用search_with_direct_chrome函数")
    
    try:
        url = f"https://kns.cnki.net/kns8s/search?q={quote(keywords)}"
        logger.debug(f"[DEBUG] 打开URL: {url}")
        
        # 使用open_chrome函数打开URL
        result = open_chrome(url)
        
        if isinstance(result, str) and "错误" in result:
            logger.debug(f"[DEBUG] 打开Chrome失败: {result}")
            
            page_content = {
                "count": 0,
                "links": [],
                "error": f"打开Chrome搜索失败: {result}"
            }
            return page_content
        
        logger.debug("[DEBUG] 已尝试在已有Chrome窗口中打开新标签页")
        
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
    if PLAYWRIGHT_AVAILABLE:
        tools.append(
            types.Tool(
                name="search_and_extract",
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
    
    if name == "search_and_extract" and PLAYWRIGHT_AVAILABLE:
        if not arguments:
            raise ValueError("缺少参数")
        
        keywords = arguments.get("keywords")
        if not keywords:
            raise ValueError("缺少关键词")
        
        try:
            # 第一步：执行搜索
            logger.info(f"开始执行搜索并提取：关键词 '{keywords}'")
            
            # 构建URL
            url = f"https://kns.cnki.net/kns8s/search?q={quote(keywords)}"
            current_url = url
            logger.debug(f"[DEBUG] 搜索URL: {url}")
            
            # 如果playwright可用，使用playwright搜索
            if PLAYWRIGHT_AVAILABLE:
                logger.debug("[DEBUG] 使用playwright搜索")
                links_count = await search_with_playwright(keywords)
            else:
                # 否则直接用open_chrome打开URL
                logger.debug("[DEBUG] 直接使用open_chrome打开URL")
                result = open_chrome(url)
                
                if isinstance(result, str):
                    # 如果是错误信息，返回错误
                    return [
                        types.TextContent(
                            type="text",
                            text=json.dumps({
                                "error": f"打开Chrome失败: {result}",
                                "keywords": keywords,
                                "count": 0,
                                "results": []
                            })
                        )
                    ]
                else:
                    # 成功打开但无法获取链接
                    return [
                        types.TextContent(
                            type="text",
                            text=json.dumps({
                                "keywords": keywords,
                                "count": 0,
                                "message": "已直接在Chrome中打开搜索页面，但无法自动获取搜索结果。请安装playwright以获取完整功能。",
                                "results": []
                            })
                        )
                    ]
            
            # 检查搜索结果
            if not isinstance(page_content, dict) or "links" not in page_content or not page_content["links"]:
                # 如果没有找到链接，至少返回搜索页面作为结果
                logger.debug("[DEBUG] 搜索未返回有效链接，返回搜索页面作为结果")
                return [
                    types.TextContent(
                        type="text",
                        text=json.dumps({
                            "keywords": keywords,
                            "count": 1,
                            "results": [{
                                "title": f"搜索结果: {keywords}",
                                "authors": [],
                                "abstract": "请在浏览器中查看搜索结果",
                                "keywords": [],
                                "cite_format": "",
                                "url": url
                            }]
                        })
                    )
                ]
            
            # 提取链接
            urls = [link["url"] for link in page_content["links"] if "url" in link]
            if not urls:
                logger.debug("[DEBUG] 没有找到有效链接，返回搜索页面")
                return [
                    types.TextContent(
                        type="text",
                        text=json.dumps({
                            "keywords": keywords,
                            "count": 1,
                            "results": [{
                                "title": f"搜索结果: {keywords}",
                                "authors": [],
                                "abstract": "请在浏览器中查看搜索结果",
                                "keywords": [],
                                "cite_format": "",
                                "url": url
                            }]
                        })
                    )
                ]
            
            # 第二步：执行提取
            logger.info(f"搜索成功，找到 {len(urls)} 个链接，开始提取内容")
            results = await batch_extract_contents(urls)
            
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
                    text=json.dumps(result_json)
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
                    })
                )
            ]
    
    else:
        raise ValueError(f"未知工具: {name}")

async def find_and_count_abstract_links(page):
    """查找并统计知网搜索结果页面中的论文链接"""
    global page_content
    
    try:
        logger.debug("[DEBUG] 开始查找知网搜索结果中的论文链接")
        
        # 等待确保页面完全加载
        await asyncio.sleep(3)
        
        # 首先尝试设置每页显示50条记录
        try:
            logger.debug("[DEBUG] 尝试设置每页显示50条记录")
            
            # 使用更直接的JavaScript方法点击50条
            set_page_size_result = await page.evaluate("""() => {
                try {
                    // 更精确地找到下拉框并点击
                    const dropdowns = document.querySelectorAll('#perPageDiv, .perpage-content, .page-count, div[class*="perpage"]');
                    if (dropdowns && dropdowns.length > 0) {
                        // 记录找到的下拉框
                        console.log('找到下拉框元素:', dropdowns[0]);
                        // 点击下拉框
                        dropdowns[0].click();
                        console.log('已点击下拉框');
                        
                        // 直接等待而不使用setTimeout，确保下拉菜单显示
                        return new Promise(resolve => {
                            setTimeout(() => {
                                // 查找并点击50选项
                                const options = document.querySelectorAll('a[data-v="50"], a[href*="50"], li[data-val="50"]');
                                console.log('找到的50选项数量:', options.length);
                                
                                for (let option of options) {
                                    if (option.textContent.includes('50')) {
                                        option.click();
                                        console.log('已点击50选项:', option);
                                        resolve("点击了50选项：" + option.textContent);
                                        return;
                                    }
                                }
                                
                                // 如果没有找到特定的50选项，尝试点击最后一个选项（通常是最大数值）
                                const allOptions = document.querySelectorAll('.perpage-content a, .sort-list li');
                                if (allOptions && allOptions.length > 0) {
                                    const lastOption = allOptions[allOptions.length - 1];
                                    lastOption.click();
                                    console.log('点击了最后一个选项:', lastOption.textContent);
                                    resolve("点击了最后一个选项：" + lastOption.textContent);
                                    return;
                                }
                                
                                resolve("未找到50条/页选项");
                            }, 1000); // 等待一秒确保下拉菜单显示
                        });
                    }
                    
                    // 尝试另一种方式 - 直接点击带有"50"的链接
                    const directLinks = document.querySelectorAll('a:not([style*="display:none"]):not([style*="display: none"])');
                    for (let link of directLinks) {
                        if (link.textContent.trim() === '50' || 
                            link.textContent.includes('50条') || 
                            link.textContent.includes('50 条')) {
                            link.click();
                            return "直接点击了50条链接: " + link.textContent;
                        }
                    }
                    
                    return "未找到任何可点击的50条/页选项";
                } catch (e) {
                    return "设置每页显示50条记录时出错: " + e.toString();
                }
            }""")
            
            logger.debug(f"[DEBUG] 设置每页显示50条记录结果: {set_page_size_result}")
            
            # 等待页面刷新
            await page.wait_for_load_state('networkidle')
            await asyncio.sleep(2)
            
            # 检查是否有来源类别选项，并尝试勾选CSSCI
            await check_and_select_cssci(page)
            
        except Exception as e:
            logger.debug(f"[DEBUG] 设置每页显示50条记录时出错: {str(e)}")
            logger.debug(traceback.format_exc())
        
        # 尝试等待搜索结果加载
        try:
            await page.wait_for_selector('.result-table-list', timeout=5000)
            logger.debug("[DEBUG] 已找到搜索结果容器")
        except Exception as e:
            logger.debug(f"[DEBUG] 等待搜索结果容器超时: {str(e)}")
        
        # 优先查找带有article/abstract?v的链接
        try:
            logger.debug("[DEBUG] 尝试查找包含 article/abstract?v 的链接")
            
            abstract_links = await page.evaluate("""() => {
                const links = [];
                // 严格查找包含article/abstract?v的链接
                const abstractLinks = document.querySelectorAll('a[href*="article/abstract?v="]');
                
                console.log('找到包含article/abstract?v的链接数量:', abstractLinks.length);
                
                for (let i = 0; i < abstractLinks.length; i++) {
                    const link = abstractLinks[i];
                    const href = link.href;
                    const text = link.textContent.trim();
                    
                    // 确保链接有效且包含必要的字段
                    if (href && href.includes('article/abstract?v=') && text) {
                        links.push({
                            index: links.length + 1,
                            href: href,
                            text: text
                        });
                    }
                }
                
                return links;
            }""")
            
            logger.debug(f"[DEBUG] 找到 {len(abstract_links)} 个包含article/abstract?v的链接")
            
            if abstract_links and len(abstract_links) > 0:
                # 找到有效的摘要链接
                links_info = abstract_links
                links_count = len(abstract_links)
            else:
                # 没有找到摘要链接，尝试备用方法
                logger.debug("[DEBUG] 未找到包含article/abstract?v的链接，尝试备用方法")
                
                # 尝试查找可能的论文链接
                backup_links = await page.evaluate("""() => {
                    const links = [];
                    // 查找可能是论文链接的a标签
                    const allLinks = document.querySelectorAll('a.fz14, a[href*="/kcms"], .result-table-list a');
                    
                    for (let i = 0; i < allLinks.length; i++) {
                        const link = allLinks[i];
                        const href = link.href;
                        const text = link.textContent.trim();
                        
                        if (href && text && !links.some(l => l.href === href)) {
                            links.push({
                                index: links.length + 1,
                                href: href,
                                text: text
                            });
                        }
                    }
                    
                    return links;
                }""")
                
                if backup_links and len(backup_links) > 0:
                    logger.debug(f"[DEBUG] 使用备用方法找到 {len(backup_links)} 个可能的论文链接")
                    links_info = backup_links
                    links_count = len(backup_links)
                else:
                    # 回退到常规方法
                    links_info = []
                    links_count = 0
                    
                    # 尝试多种可能的选择器
                    selectors = [
                        'a[href*="article/abstract?v="]',  # 优先查找摘要链接
                        'a[href*="/kcms"]',                # 知网文献链接
                        '.fz14',                           # 标题样式类
                        'a.pc-link',                       # 搜索结果链接
                        '.c_font a',                       # 内容字体下的链接
                        '.result-table-list a',            # 结果表下的链接
                        'table tr td a'                    # 表格中的链接
                    ]
                    
                    for selector in selectors:
                        try:
                            all_links = await page.query_selector_all(selector)
                            logger.debug(f"[DEBUG] 使用选择器 {selector} 找到 {len(all_links)} 个链接")
                            
                            for i, link in enumerate(all_links):
                                try:
                                    href = await link.get_attribute('href')
                                    text = await link.text_content()
                                    
                                    # 确保链接包含论文相关URL，如果没有指定URL则使用当前页面URL
                                    if not href:
                                        continue
                                    
                                    # 处理相对URL
                                    if href.startswith('/'):
                                        href = f"https://kns.cnki.net{href}"
                                    elif not href.startswith('http'):
                                        href = f"https://kns.cnki.net/{href}"
                                        
                                    # 防止重复添加同一链接
                                    if any(link_info['href'] == href for link_info in links_info):
                                        continue
                                        
                                    links_info.append({
                                        'index': len(links_info) + 1,
                                        'href': href,
                                        'text': text.strip() if text else ""
                                    })
                                    
                                    logger.debug(f"[DEBUG] 链接 {len(links_info)}: {href}")
                                except Exception as e:
                                    logger.debug(f"[DEBUG] 处理链接时出错: {str(e)}")
                        except Exception as e:
                            logger.debug(f"[DEBUG] 使用选择器 {selector} 查找链接时出错: {str(e)}")
        except Exception as e:
            logger.debug(f"[DEBUG] 查找链接时出错: {str(e)}")
            logger.debug(traceback.format_exc())
            links_info = []
            links_count = 0
        
        # 过滤链接，只保留包含article/abstract?v的链接
        filtered_links = []
        for link in links_info:
            href = link['href']
            if 'article/abstract?v=' in href:
                filtered_links.append(link)
                logger.debug(f"[DEBUG] 保留包含article/abstract?v的链接: {href}")
        
        # 如果过滤后没有链接，可能是知网搜索结果的格式变化，使用原始链接
        if not filtered_links:
            logger.debug("[DEBUG] 过滤后没有包含article/abstract?v的链接，使用原始链接")
            filtered_links = links_info
        
        # 最终链接数量
        links_count = len(filtered_links)
        logger.debug(f"[DEBUG] 最终过滤后找到 {links_count} 个链接")
        
        # 如果没有找到链接，不再进行截图
        if links_count == 0:
            logger.debug("[DEBUG] 未找到链接")
        
        # 存储结果 - 使用字典结构而不是纯文本
        page_content = {
            "count": links_count,
            "links": [{"index": link['index'], "url": link['href'], "title": link['text']} for link in filtered_links]
        }
        
        return links_count
    except Exception as e:
        logger.debug(f"[DEBUG] 查找链接时出错: {str(e)}")
        logger.debug(traceback.format_exc())
        
        # 发生错误时，尝试获取当前页面URL
        try:
            current_url = await page.url()
            logger.debug(f"[DEBUG] 当前页面URL: {current_url}")
            
            # 至少返回当前页面作为链接
            page_content = {
                "count": 1,
                "links": [{"index": 1, "url": current_url, "title": "当前页面"}]
            }
            return 1
        except:
            page_content = {
                "count": 0,
                "links": []
            }
            return 0

async def check_and_select_cssci(page):
    """检查页面是否有来源类别选项，并尝试勾选CSSCI"""
    try:
        logger.debug("[DEBUG] 尝试查找来源类别并勾选CSSCI")
        
        # 使用JavaScript直接操作DOM
        cssci_result = await page.evaluate("""() => {
            try {
                // 查找包含"来源类别"的区域
                const categoryContainer = Array.from(document.querySelectorAll('div')).find(div => 
                    div.textContent.includes('来源类别')
                );
                
                if (categoryContainer) {
                    // 在来源类别容器中查找CSSCI复选框
                    const checkboxes = categoryContainer.querySelectorAll('input[type="checkbox"]');
                    for (let checkbox of checkboxes) {
                        // 查找CSSCI相关的复选框
                        const parentText = checkbox.parentElement.textContent;
                        if (parentText.includes('CSSCI') || 
                            checkbox.value.includes('CSSCI') || 
                            checkbox.id.includes('cssci')) {
                            
                            // 勾选复选框
                            if (!checkbox.checked) {
                                checkbox.click();
                                return "已勾选CSSCI复选框";
                            } else {
                                return "CSSCI复选框已经被勾选";
                            }
                        }
                    }
                    
                    // 如果没有找到复选框但找到了CSSCI的标签
                    const cssciLabels = categoryContainer.querySelectorAll('label, span');
                    for (let label of cssciLabels) {
                        if (label.textContent.includes('CSSCI')) {
                            label.click();
                            return "已点击CSSCI标签";
                        }
                    }
                    
                    return "在来源类别区域未找到CSSCI选项";
                }
                
                return "未找到来源类别区域";
            } catch (e) {
                return "勾选CSSCI时出错: " + e.toString();
            }
        }""")
        
        logger.debug(f"[DEBUG] CSSCI勾选结果: {cssci_result}")
        
        # 等待页面刷新
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(2)
            
    except Exception as e:
        logger.debug(f"[DEBUG] 勾选CSSCI时出错: {str(e)}")
        logger.debug(traceback.format_exc())

async def extract_content_from_url(url: str, page = None) -> CNKIContent:
    """从CNKI页面提取论文内容"""
    global playwright_instance, browser_instance, context
    
    if not url.startswith('http'):
        # 处理相对URL
        if url.startswith('/'):
            url = f"https://kns.cnki.net{url}"
        else:
            url = f"https://kns.cnki.net/{url}"
    
    # 创建基本内容对象
    content = CNKIContent(url=url)
    
    try:
        logger.info(f"开始从URL提取内容: {url}")
        
        # 如果没有提供page参数，检查playwright是否已初始化
        should_close_page = False
        if page is None:
            if playwright_instance is None or browser_instance is None or context is None:
                # 如果playwright未初始化，使用webbrowser打开URL
                logger.info(f"Playwright未初始化，使用webbrowser打开URL: {url}")
                webbrowser.open(url)
                
                # 设置基本信息
                content.title = "请在浏览器中手动获取内容"
                content.abstract = "系统已打开链接，请在浏览器中查看完整内容"
                return content
            else:
                # 使用现有的playwright实例创建新页面
                logger.debug("[DEBUG] 使用现有的playwright实例创建新页面")
                page = await context.new_page()
                should_close_page = True  # 后续需要关闭此页面
        
        # 访问URL
        logger.debug(f"[DEBUG] 导航到URL: {url}")
        
        try:
            await page.goto(url, wait_until='networkidle', timeout=30000)
        except Exception as e:
            logger.warning(f"导航超时，继续尝试提取: {str(e)}")
            
        # 等待页面加载
        await asyncio.sleep(2)
        
        # 检查是否需要验证
        await check_and_wait_for_verification(page)
        
        # 尝试使用JavaScript提取所有内容
        try:
            logger.debug("[DEBUG] 尝试使用JavaScript提取内容")
            
            content_result = await page.evaluate("""() => {
                try {
                    // 提取标题
                    const getTitle = () => {
                        const selectors = ['h1.title', '.wx-tit h1', '.title', 'h1', '.article-title', 'div.brief h2', '.wxTitle', 'span.title'];
                        for (const selector of selectors) {
                            const element = document.querySelector(selector);
                            if (element) {
                                const text = element.textContent.trim();
                                if (!text.includes('系统检测')) {
                                    return text;
                                }
                            }
                        }
                        return "";
                    };
                    
                    // 提取作者
                    const getAuthors = () => {
                        const selectors = ['.wx-tit .author', '.author', '.writers', '.authorinfo', 'div.brief p:first-child', 'span.author'];
                        for (const selector of selectors) {
                            const element = document.querySelector(selector);
                            if (element) {
                                const text = element.textContent.trim();
                                return text.split(/[,，;；、\\s]+/).filter(a => a.trim());
                            }
                        }
                        return [];
                    };
                    
                    // 提取摘要
                    const getAbstract = () => {
                        const selectors = ['#ChDivSummary', '.abstract', '.summary', '.Abstract', 'div.brief div.abstract', 'div.wxInfo span.abstract', 'div.wxInfo', 'span.abstract'];
                        for (const selector of selectors) {
                            const element = document.querySelector(selector);
                            if (element) {
                                let text = element.textContent.trim();
                                // 移除可能的"摘要:"前缀
                                text = text.replace(/^摘要[：:]/g, '').trim();
                                return text;
                            }
                        }
                        
                        // 查找含有"摘要"的段落
                        const paragraphs = document.querySelectorAll('p');
                        for (const p of paragraphs) {
                            if (p.textContent.includes('摘要')) {
                                let text = p.textContent.trim();
                                text = text.replace(/^摘要[：:]/g, '').trim();
                                return text;
                            }
                        }
                        
                        return "";
                    };
                    
                    // 提取关键词
                    const getKeywords = () => {
                        const selectors = ['.wx-tit-keys', '.keywords', '.Keyword', 'div.wxInfo span.keywords', 'span.keywords', 'div.brief span.keywords', 'p.keywords'];
                        for (const selector of selectors) {
                            const element = document.querySelector(selector);
                            if (element) {
                                let text = element.textContent.trim();
                                // 移除"关键词:"前缀
                                text = text.replace(/^关键词[：:]/g, '').trim();
                                return text.split(/[;；,，、\\s]+/).filter(k => k.trim());
                            }
                        }
                        
                        // 查找含有"关键词"的段落
                        const paragraphs = document.querySelectorAll('p');
                        for (const p of paragraphs) {
                            if (p.textContent.includes('关键词')) {
                                let text = p.textContent.trim();
                                const keywordText = text.split(/关键词[：:]/)[1];
                                if (keywordText) {
                                    return keywordText.split(/[;；,，、\\s]+/).filter(k => k.trim());
                                }
                            }
                        }
                        
                        return [];
                    };
                    
                    // 尝试获取引用格式
                    let citeFormat = "";
                    const getCiteFormat = () => {
                        // 首先检查是否有引用按钮
                        const citeButton = document.querySelector('button:has-text("引用"), [class*="cite"], [class*="quote"]');
                        if (citeButton) {
                            // 如果有引用按钮，暂不点击，防止页面跳转
                            return null;
                        }
                        
                        // 尝试直接获取引用区域
                        const selectors = ['.quote-info', '.citation', 'div.cite', 'div.quoted', 'div.wxInfo div.quoted', '.refer-info'];
                        for (const selector of selectors) {
                            const element = document.querySelector(selector);
                            if (element) {
                                return element.textContent.trim();
                            }
                        }
                        
                        return "";
                    };
                    
                    // 收集结果
                    return {
                        title: getTitle(),
                        authors: getAuthors(),
                        abstract: getAbstract(),
                        keywords: getKeywords(),
                        cite_format: getCiteFormat()
                    };
                } catch (e) {
                    return {
                        error: "提取内容时出错: " + e.toString(),
                        title: "",
                        authors: [],
                        abstract: "",
                        keywords: [],
                        cite_format: ""
                    };
                }
            }""")
            
            # 更新内容对象
            if content_result:
                if "error" in content_result and content_result["error"]:
                    logger.warning(f"[WARNING] JavaScript提取内容时出错: {content_result['error']}")
                else:
                    logger.debug("[DEBUG] JavaScript提取内容成功")
                    
                    # 更新标题
                    if content_result.get("title"):
                        content.title = content_result["title"]
                        logger.debug(f"[DEBUG] 提取到标题: {content.title}")
                    
                    # 更新作者
                    if content_result.get("authors"):
                        content.authors = content_result["authors"]
                        logger.debug(f"[DEBUG] 提取到作者: {content.authors}")
                    
                    # 更新摘要
                    if content_result.get("abstract"):
                        content.abstract = content_result["abstract"]
                        logger.debug(f"[DEBUG] 提取到摘要: {content.abstract[:100]}...")
                    
                    # 更新关键词
                    if content_result.get("keywords"):
                        content.keywords = content_result["keywords"]
                        logger.debug(f"[DEBUG] 提取到关键词: {content.keywords}")
                    
                    # 更新引用格式
                    if content_result.get("cite_format") != None:
                        if content_result["cite_format"]:
                            # 直接获取到引用格式
                            content.cite_format = content_result["cite_format"]
                            logger.debug(f"[DEBUG] 提取到引用格式: {content.cite_format[:100]}...")
                        else:
                            # 需要点击引用按钮
                            logger.debug("[DEBUG] 尝试点击引用按钮获取引用格式")
                            
                            try:
                                # 查找引用按钮
                                cite_button = await page.query_selector('button:has-text("引用"), [class*="cite"], [class*="quote"]')
                                if cite_button:
                                    await cite_button.click()
                                    await asyncio.sleep(1)  # 等待弹窗显示
                                    
                                    # 在弹窗中提取引用格式
                                    cite_text = await page.evaluate("""() => {
                                        const textarea = document.querySelector('.quote-r textarea.text, .quote-text, [class*="quote"] textarea');
                                        if (textarea) {
                                            return textarea.value.trim();
                                        }
                                        return "";
                                    }""")
                                    
                                    if cite_text:
                                        content.cite_format = cite_text
                                        logger.debug(f"[DEBUG] 从弹窗提取到引用格式: {content.cite_format[:100]}...")
                                    else:
                                        logger.debug("[DEBUG] 未从弹窗找到引用格式")
                                else:
                                    logger.debug("[DEBUG] 未找到引用按钮")
                            except Exception as e:
                                logger.debug(f"[DEBUG] 点击引用按钮时出错: {str(e)}")
            else:
                logger.warning("[WARNING] JavaScript提取内容返回空结果")
                
        except Exception as e:
            logger.debug(f"[DEBUG] 使用JavaScript提取内容时出错: {str(e)}")
            logger.debug(traceback.format_exc())
        
        # 如果JavaScript提取失败，回退到原来的提取方法
        if not content.title:
            # 尝试提取论文标题
            try:
                title_selectors = [
                    '.wx-tit h1', 
                    '.article-title', 
                    '.title', 
                    'h1', 
                    '.articleTitle',
                    'div.brief h2',
                    '.wxTitle',
                    'span.title'
                ]
                
                title_elem = None
                for selector in title_selectors:
                    title_elem = await page.query_selector(selector)
                    if title_elem:
                        logger.debug(f"[DEBUG] 找到标题元素: {selector}")
                        break
                        
                if title_elem:
                    content.title = await title_elem.text_content()
                    content.title = content.title.strip()
                    logger.debug(f"[DEBUG] 提取到标题: {content.title}")
            except Exception as e:
                logger.debug(f"[DEBUG] 提取标题时出错: {str(e)}")
        
        if not content.authors:
            # 尝试提取作者信息
            try:
                author_selectors = [
                    '.wx-tit .author', 
                    '.author', 
                    '.writers',
                    '.authorinfo',
                    'div.brief p:first-child',
                    'span.author'
                ]
                
                authors_elem = None
                for selector in author_selectors:
                    authors_elem = await page.query_selector(selector)
                    if authors_elem:
                        logger.debug(f"[DEBUG] 找到作者元素: {selector}")
                        break
                        
                if authors_elem:
                    authors_text = await authors_elem.text_content()
                    # 分割作者文本
                    authors = [a.strip() for a in re.split(r'[,，;；、\s]+', authors_text) if a.strip()]
                    content.authors = authors
                    logger.debug(f"[DEBUG] 提取到作者: {authors}")
            except Exception as e:
                logger.debug(f"[DEBUG] 提取作者时出错: {str(e)}")
        
        if not content.abstract:
            # 尝试提取摘要
            try:
                abstract_selectors = [
                    '#ChDivSummary', 
                    '.abstract', 
                    '.summary', 
                    '.Abstract',
                    'div.brief div.abstract',
                    'div.wxInfo span.abstract',
                    'div.wxInfo',
                    'span.abstract'
                ]
                
                abstract_elem = None
                for selector in abstract_selectors:
                    abstract_elem = await page.query_selector(selector)
                    if abstract_elem:
                        logger.debug(f"[DEBUG] 找到摘要元素: {selector}")
                        break
                        
                if abstract_elem:
                    content.abstract = await abstract_elem.text_content()
                    content.abstract = content.abstract.strip()
                    # 移除可能的"摘要:"前缀
                    content.abstract = re.sub(r'^摘要[：:]\s*', '', content.abstract)
                    logger.debug(f"[DEBUG] 提取到摘要: {content.abstract[:100]}...")
            except Exception as e:
                logger.debug(f"[DEBUG] 提取摘要时出错: {str(e)}")
        
        if not content.keywords:
            # 尝试提取关键词
            try:
                keyword_selectors = [
                    '.wx-tit-keys', 
                    '.keywords', 
                    '.Keyword',
                    'div.wxInfo span.keywords',
                    'span.keywords',
                    'div.brief span.keywords',
                    'p.keywords'
                ]
                
                keywords_elem = None
                for selector in keyword_selectors:
                    keywords_elem = await page.query_selector(selector)
                    if keywords_elem:
                        logger.debug(f"[DEBUG] 找到关键词元素: {selector}")
                        break
                        
                if keywords_elem:
                    keywords_text = await keywords_elem.text_content()
                    # 移除"关键词:"前缀
                    keywords_text = re.sub(r'^关键词[：:]\s*', '', keywords_text)
                    # 分割关键词
                    keywords = [k.strip() for k in re.split(r'[;；,，、\s]+', keywords_text) if k.strip()]
                    content.keywords = keywords
                    logger.debug(f"[DEBUG] 提取到关键词: {keywords}")
            except Exception as e:
                logger.debug(f"[DEBUG] 提取关键词时出错: {str(e)}")
        
        if not content.cite_format:
            # 尝试提取引用格式
            try:
                cite_selectors = [
                    '.quote-info', 
                    '.citation',
                    'div.cite',
                    'div.quoted',
                    'div.wxInfo div.quoted',
                    '.refer-info'
                ]
                
                cite_elem = None
                for selector in cite_selectors:
                    cite_elem = await page.query_selector(selector)
                    if cite_elem:
                        logger.debug(f"[DEBUG] 找到引用格式元素: {selector}")
                        break
                        
                if cite_elem:
                    content.cite_format = await cite_elem.text_content()
                    content.cite_format = content.cite_format.strip()
                    logger.debug(f"[DEBUG] 提取到引用格式: {content.cite_format[:100]}...")
                else:
                    # 如果没有找到引用格式，尝试点击引用按钮
                    cite_button = await page.query_selector('button:has-text("引用"), [class*="cite"], [class*="quote"]')
                    if cite_button:
                        await cite_button.click()
                        await asyncio.sleep(1)  # 等待弹窗显示
                        
                        # 在弹窗中提取引用格式
                        textarea = await page.query_selector('.quote-r textarea.text, .quote-text, [class*="quote"] textarea')
                        if textarea:
                            content.cite_format = await textarea.get_property('value')
                            content.cite_format = content.cite_format.strip()
                            logger.debug(f"[DEBUG] 从弹窗提取到引用格式: {content.cite_format[:100]}...")
            except Exception as e:
                logger.debug(f"[DEBUG] 提取引用格式时出错: {str(e)}")
        
        # 如果页面是自己创建的，需要关闭
        if should_close_page:
            await page.close()
            
        return content
    except Exception as e:
        logger.error(f"从URL提取内容时出错: {str(e)}")
        logger.error(traceback.format_exc())
        
        # 确保如果页面是自己创建的，出错时也能关闭
        if 'page' in locals() and page is not None and 'should_close_page' in locals() and should_close_page:
            try:
                await page.close()
            except:
                pass
                
        # 设置错误信息
        content.title = f"提取失败: {str(e)}"
        content.abstract = f"从URL提取内容时出错: {str(e)}"
        return content

async def batch_extract_contents(urls: List[str]) -> List[Dict]:
    """批量处理多个URL，提取内容并返回JSON格式"""
    results = []
    max_urls = min(50, len(urls))  # 限制最多处理50个URL
    
    logger.info(f"开始批量提取内容，共 {max_urls} 个URL")
    
    try:
        # 检查是否已初始化playwright
        global playwright_instance, browser_instance, context
        
        if playwright_instance is None or browser_instance is None or context is None:
            logger.info("Playwright未初始化，创建新实例")
            playwright_instance = await async_playwright().start()
            browser_instance = await playwright_instance.chromium.launch(headless=False)
            context = await browser_instance.new_context()
        
        # 一个一个处理URL
        for i, url in enumerate(urls[:max_urls]):
            logger.info(f"处理URL {i+1}/{max_urls}: {url}")
            
            # 创建一个新页面
            page = await context.new_page()
            
            try:
                # 提取内容
                result = await extract_content_from_url(url, page)
                results.append(result.dict())
                logger.info(f"成功处理URL: {url}")
            except Exception as e:
                logger.error(f"处理URL {url} 时出错: {str(e)}")
                results.append({
                    "url": url,
                    "error": str(e),
                    "title": "",
                    "authors": [],
                    "abstract": "",
                    "keywords": [],
                    "cite_format": ""
                })
            finally:
                # 关闭页面
                await page.close()
            
            # 添加短暂延迟，避免过快请求导致被封
            await asyncio.sleep(1)
        
        logger.info(f"批量处理完成，共处理 {len(results)} 个URL")
        return results
    except Exception as e:
        logger.error(f"批量处理过程中出错: {str(e)}")
        logger.error(traceback.format_exc())
        return [{"error": f"批量处理过程中出错: {str(e)}"}] + results

# 添加关闭函数，在程序结束时清理资源
async def cleanup_playwright():
    """清理playwright资源"""
    global playwright_instance, browser_instance, context
    
    if context:
        logger.debug("[DEBUG] 关闭playwright上下文")
        await context.close()
        context = None
    
    if browser_instance:
        logger.debug("[DEBUG] 关闭浏览器实例")
        await browser_instance.close()
        browser_instance = None
    
    if playwright_instance:
        logger.debug("[DEBUG] 关闭playwright实例")
        await playwright_instance.stop()
        playwright_instance = None

async def main():
    """主程序入口"""
    try:
        # 使用stdin/stdout流运行服务器
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="cnks",
                    server_version="0.3.0",
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )
    finally:
        # 确保playwright资源在程序结束时被清理
        await cleanup_playwright()

# 为符合README.md的要求，添加从FastMCP导出的接口
def create_fastmcp_server():
    """创建FastMCP服务器接口，符合README中的示例"""
    try:
        from mcp.server.fastmcp import FastMCP
        fast_mcp = FastMCP("知网搜索")
        
        # 只添加搜索并提取的工具
        if PLAYWRIGHT_AVAILABLE:
            @fast_mcp.tool()
            async def search_and_extract(keywords: str) -> dict:
                """搜索关键词并提取所有论文的详细内容"""
                logger.debug("[DEBUG] 正在使用FastMCP的search_and_extract函数")
                try:
                    # 第一步：执行搜索
                    logger.debug(f"[DEBUG] 开始搜索关键词: {keywords}")
                    
                    # 构建URL
                    url = f"https://kns.cnki.net/kns8s/search?q={quote(keywords)}"
                    logger.debug(f"[DEBUG] 搜索URL: {url}")
                    
                    # 如果playwright可用，使用playwright搜索
                    if PLAYWRIGHT_AVAILABLE:
                        logger.debug("[DEBUG] 使用playwright搜索")
                        result_count = await search_with_playwright(keywords)
                    else:
                        # 否则直接用open_chrome打开URL
                        logger.debug("[DEBUG] 直接使用open_chrome打开URL")
                        result = open_chrome(url)
                        
                        if isinstance(result, str):
                            # 如果是错误信息，返回错误
                            return {
                                "error": f"打开Chrome失败: {result}",
                                "keywords": keywords,
                                "count": 0,
                                "results": []
                            }
                        else:
                            # 成功打开但无法获取链接
                            return {
                                "keywords": keywords,
                                "count": 0,
                                "message": "已直接在Chrome中打开搜索页面，但无法自动获取搜索结果。请安装playwright以获取完整功能。",
                                "results": []
                            }
                    
                    # 检查搜索结果
                    if not isinstance(page_content, dict) or "links" not in page_content or not page_content["links"]:
                        # 如果没有找到链接，至少返回搜索页面作为结果
                        logger.debug("[DEBUG] 搜索未返回有效链接，返回搜索页面作为结果")
                        return {
                            "keywords": keywords,
                            "count": 1,
                            "results": [{
                                "title": f"搜索结果: {keywords}",
                                "authors": [],
                                "abstract": "请在浏览器中查看搜索结果",
                                "keywords": [],
                                "cite_format": "",
                                "url": url
                            }]
                        }
                    
                    # 提取链接
                    urls = [link["url"] for link in page_content["links"] if "url" in link]
                    if not urls:
                        logger.debug("[DEBUG] 没有找到有效链接，返回搜索页面")
                        return {
                            "keywords": keywords,
                            "count": 1,
                            "results": [{
                                "title": f"搜索结果: {keywords}",
                                "authors": [],
                                "abstract": "请在浏览器中查看搜索结果",
                                "keywords": [],
                                "cite_format": "",
                                "url": url
                            }]
                        }
                    
                    # 第二步：执行提取
                    results = await batch_extract_contents(urls)
                    
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
                    logger.error(traceback.format_exc())
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
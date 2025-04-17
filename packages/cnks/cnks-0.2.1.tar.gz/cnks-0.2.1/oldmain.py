from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import Optional, Dict, List
import logging
from datetime import datetime

from mcp.server.fastmcp import FastMCP, Context, Image
from mcp.server.fastmcp.prompts import base
from pydantic import BaseModel
from playwright.async_api import async_playwright, Browser, BrowserContext
import traceback

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建FastMCP服务器实例
mcp = FastMCP(
    "CNKI Content Extractor",
    dependencies=[
        "fastapi",
        "playwright",
        "python-dotenv",
        "pydantic",
        "bs4",
        "requests",
        "jinja2"
    ]
)

@dataclass
class AppContext:
    browser: Browser
    browser_context: BrowserContext

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """管理应用生命周期和浏览器实例"""
    logger.info("正在初始化浏览器...")
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(
                    headless=False,
                    args=[
                        '--start-maximized',
                        '--disable-gpu',
                        '--no-sandbox',
                        '--disable-setuid-sandbox',
                    ]
                )
    context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
    
    try:
        yield AppContext(
            browser=browser,
            browser_context=context
        )
    finally:
        logger.info("正在清理资源...")
        await context.close()
        await browser.close()
        await playwright.stop()

# 使用生命周期管理
mcp = FastMCP("CNKI Content Extractor", lifespan=app_lifespan)

# 定义数据模型
class CNKIContent(BaseModel):
    title: str = ""
    authors: List[str] = []
    abstract: str = ""
    keywords: List[str] = []
    cite_format: str = ""

@mcp.resource("capabilities://")
def get_capabilities() -> Dict:
    """获取服务器能力声明"""
    return {
        "version": "1.0.0",
        "features": {
            "resources": {
                "cnki_extraction": {
                    "description": "从CNKI知网提取论文信息",
                    "requires_auth": True,
                    "data_privacy": {
                        "user_data_access": True,
                        "data_retention": "session"
                    }
                }
            },
            "tools": {
                "extract": {
                    "description": "提取CNKI论文内容",
                    "requires_consent": True,
                    "execution_scope": "browser"
                }
            }
        }
    }

@mcp.tool()
async def extract_content(url: str, ctx: Context) -> CNKIContent:
    """从CNKI页面提取论文内容"""
    if not url.startswith('https://kns.cnki.net/'):
        raise ValueError('URL必须是CNKI知网的链接')

    browser_context = ctx.request_context.lifespan_context.browser_context
    content = CNKIContent()

    try:
        # 创建新页面
        page = await browser_context.new_page()
        ctx.info(f"正在访问页面: {url}")

        try:
            # 访问页面
            await page.goto(url, wait_until='networkidle', timeout=60000)
            await ctx.report_progress(0.2, "页面加载完成")

            # 等待并检查登录状态
            login_text = await page.evaluate('() => document.querySelector(".login-btn")?.textContent || ""')
            if "登录" in login_text:
                ctx.info("等待用户登录...")
                await ctx.report_progress(0.3, "等待用户登录")
                # 等待登录完成的逻辑...

            # 等待验证完成
            ctx.info("检查是否需要验证...")
            await ctx.report_progress(0.4, "验证检查")
            # 验证检查逻辑...

            # 提取内容
            ctx.info("正在提取内容...")
            await ctx.report_progress(0.6, "开始提取内容")

            # 提取标题
            content.title = await page.evaluate('''
                () => {
                    const selectors = ['h1.title', '.wx-tit h1', '.title', 'h1'];
                    for (const selector of selectors) {
                        const element = document.querySelector(selector);
                        if (element) {
                            const text = element.textContent.trim();
                            if (!text.includes('系统检测')) {
                                return text.split(/\s+/)[0];
                            }
                        }
                    }
                    return "";
                }
            ''')
            await ctx.report_progress(0.7, "标题提取完成")

            # 提取引用格式和作者
            cite_button = await page.wait_for_selector(
                'button:has-text("引用"), [class*="cite"], [class*="quote"]',
                timeout=15000
            )
            if cite_button:
                await cite_button.click()
                await ctx.report_progress(0.8, "获取引用格式")
                
                cite_result = await page.evaluate('''
                    () => {
                        const textarea = document.querySelector('.quote-r textarea.text');
                        if (textarea) {
                            const text = textarea.value.trim();
                            const cite_text = text.replace(/^\[1\]/, '').trim();
                            
                            const match = cite_text.match(/^([^\.]+)\./);
                            const authors = match ? match[1].split(',').map(a => a.trim()) : [];
                            
                            const titleMatch = cite_text.match(/\.([^\.]+?)\[/);
                            const title = titleMatch ? titleMatch[1].trim() : '';
                            
                            return {
                                cite_format: cite_text,
                                authors: authors,
                                title: title
                            };
                        }
                        return null;
                    }
                ''')
                
                if cite_result:
                    content.cite_format = cite_result["cite_format"]
                    content.authors = cite_result["authors"]
                    if cite_result["title"]:
                        content.title = cite_result["title"]

            # 提取摘要
            content.abstract = await page.evaluate('''
                () => {
                    const abstract = document.querySelector('.abstract-text, .abstract, .wx-tit + p');
                    return abstract ? abstract.textContent.trim() : "";
                }
            ''')

            # 提取关键词
            content.keywords = await page.evaluate('''
                () => {
                    const keywordElements = Array.from(document.querySelectorAll('.keywords a, .keywords-text, .keyword'));
                    if (keywordElements.length > 0) {
                        return keywordElements.map(k => k.textContent.trim());
                    }
                    
                    const paragraphs = Array.from(document.querySelectorAll('p'));
                    for (const p of paragraphs) {
                        if (p.textContent.includes('关键词')) {
                            const text = p.textContent.trim();
                            const keywordText = text.split(/关键词[:：]/)[1];
                            if (keywordText) {
                                return keywordText.split(/[,，;；]/)
                                    .map(k => k.trim())
                                    .filter(k => k);
                            }
                        }
                    }
                    return [];
                }
            ''')
            
            await ctx.report_progress(1.0, "内容提取完成")
            return content
            
        except Exception as e:
            logger.error(f"提取内容时出错: {str(e)}")
            await page.screenshot(path='extraction_error.png')
            raise Exception(f"提取内容失败: {str(e)}")

        finally:
            await page.close()

    except Exception as e:
        logger.error(f"处理请求时出错: {str(e)}")
        logger.error(f"错误堆栈: {traceback.format_exc()}")
        raise

@mcp.prompt()
def extract_prompt(url: str) -> list[base.Message]:
    """生成内容提取的提示模板"""
    return [
        base.UserMessage("我需要从以下CNKI链接提取论文信息："),
        base.UserMessage(url),
        base.AssistantMessage("我将帮您提取论文信息。请稍等片刻，这可能需要一些时间..."),
    ]

if __name__ == "__main__":
    import uvicorn
    logger.info("启动服务...")
    mcp.run(host="0.0.0.0", port=8000) 
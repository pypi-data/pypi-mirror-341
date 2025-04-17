from typing import Dict, List, Optional, Union
import logging
import traceback
import asyncio
import os
import subprocess
import time
from datetime import datetime
from pydantic import BaseModel
import platform
import json
from contextlib import asynccontextmanager

from playwright.async_api import async_playwright, Browser, BrowserContext, Page

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename="chrome_extractor.log",
    filemode="a"
)
logger = logging.getLogger("chrome_extractor")

# 定义数据模型
class CNKIContent(BaseModel):
    """CNKI论文内容模型"""
    title: str = ""
    authors: List[str] = []
    abstract: str = ""
    keywords: List[str] = []
    cite_format: str = ""
    url: str = ""  # 添加URL字段以记录来源

def find_chrome_executable():
    """查找Chrome可执行文件路径"""
    # 获取操作系统类型
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
        logger.error(f"不支持的操作系统: {system}")
        return None
    
    # 检查路径是否存在
    for path in chrome_paths:
        if os.path.exists(path):
            logger.info(f"找到Chrome: {path}")
            return path
    
    # 尝试从环境变量中查找
    chrome_env = os.environ.get("CHROME_PATH")
    if chrome_env and os.path.exists(chrome_env):
        logger.info(f"从环境变量找到Chrome: {chrome_env}")
        return chrome_env
    
    logger.error("未找到Chrome浏览器")
    return None

@asynccontextmanager
async def get_browser():
    """获取浏览器实例，使用上下文管理器确保资源释放"""
    playwright = None
    browser = None
    
    try:
        chrome_path = find_chrome_executable()
        if not chrome_path:
            raise ValueError("未找到Chrome浏览器，请设置CHROME_PATH环境变量指向Chrome位置")
        
        logger.info(f"正在启动Chrome浏览器: {chrome_path}")
        
        # 启动playwright
        playwright = await async_playwright().start()
        
        # 配置环境变量，告诉Playwright不要自动下载浏览器
        os.environ["PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD"] = "1"
        
        # 尝试不同的启动方式
        try:
            logger.info("尝试使用channel='chrome'启动")
            browser = await playwright.chromium.launch(
                headless=False,
                channel="chrome",
                executable_path=None  # 让Playwright自己查找Chrome
            )
        except Exception as e1:
            logger.info(f"channel='chrome'方式失败: {str(e1)}")
            try:
                logger.info(f"尝试使用executable_path启动: {chrome_path}")
                browser = await playwright.chromium.launch(
                    headless=False,
                    executable_path=chrome_path
                )
            except Exception as e2:
                logger.error(f"两种方式都失败了: {str(e2)}")
                # 最后尝试以非无头模式启动
                browser = await playwright.chromium.launch(
                    headless=False,
                    channel=None,
                    executable_path=chrome_path,
                    args=[
                        '--no-sandbox',
                        '--disable-setuid-sandbox',
                        '--disable-gpu',
                        '--start-maximized'
                    ]
                )
        
        # 创建新的浏览器上下文
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        
        try:
            yield browser, context
        finally:
            logger.info("关闭浏览器和上下文")
            await context.close()
            await browser.close()
    except Exception as e:
        logger.error(f"获取浏览器时出错: {str(e)}")
        logger.error(traceback.format_exc())
        raise
    finally:
        if playwright:
            logger.info("关闭Playwright")
            await playwright.stop()

async def extract_content_from_url(url: str) -> CNKIContent:
    """从CNKI页面提取论文内容"""
    if not url.startswith('https://kns.cnki.net/'):
        raise ValueError('URL必须是CNKI知网的链接')

    content = CNKIContent(url=url)
    
    async with get_browser() as (browser, context):
        # 创建新页面
        page = await context.new_page()
        logger.info(f"正在访问页面: {url}")

        try:
            # 访问页面
            await page.goto(url, wait_until='networkidle', timeout=60000)
            logger.info("页面加载完成")

            # 等待并检查登录状态
            login_text = await page.evaluate('() => document.querySelector(".login-btn")?.textContent || ""')
            if "登录" in login_text:
                logger.info("需要登录，请手动登录...")
                # 等待用户登录完成
                await asyncio.sleep(15)  # 给用户更多时间登录
            
            # 提取标题
            content.title = await page.evaluate('''
                () => {
                    const selectors = ['h1.title', '.wx-tit h1', '.title', 'h1'];
                    for (const selector of selectors) {
                        const element = document.querySelector(selector);
                        if (element) {
                            const text = element.textContent.trim();
                            if (!text.includes('系统检测')) {
                                return text.split(/\\s+/)[0];
                            }
                        }
                    }
                    return "";
                }
            ''')
            logger.info(f"提取到标题: {content.title}")

            # 提取引用格式和作者
            try:
                cite_button = await page.wait_for_selector(
                    'button:has-text("引用"), [class*="cite"], [class*="quote"]',
                    timeout=15000
                )
                if cite_button:
                    await cite_button.click()
                    logger.info("获取引用格式")
                    await asyncio.sleep(2)  # 等待引用框加载
                    
                    cite_result = await page.evaluate('''
                        () => {
                            const textarea = document.querySelector('.quote-r textarea.text');
                            if (textarea) {
                                const text = textarea.value.trim();
                                const cite_text = text.replace(/^\\[1\\]/, '').trim();
                                
                                const match = cite_text.match(/^([^\\.]+)\\./);
                                const authors = match ? match[1].split(',').map(a => a.trim()) : [];
                                
                                const titleMatch = cite_text.match(/\\.([^\\.]+?)\\[/);
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
                        logger.info(f"提取到作者: {content.authors}")
            except Exception as e:
                logger.error(f"提取引用格式时出错: {str(e)}")

            # 提取摘要
            content.abstract = await page.evaluate('''
                () => {
                    const abstract = document.querySelector('.abstract-text, .abstract, .wx-tit + p');
                    return abstract ? abstract.textContent.trim() : "";
                }
            ''')
            logger.info(f"提取到摘要长度: {len(content.abstract)} 字符")

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
            logger.info(f"提取到关键词: {content.keywords}")
            
            # 确保关闭页面
            await page.close()
            return content
            
        except Exception as e:
            logger.error(f"提取内容时出错: {str(e)}")
            try:
                # 尝试截图
                screenshot_path = f'extraction_error_{datetime.now().strftime("%Y%m%d%H%M%S")}.png'
                await page.screenshot(path=screenshot_path)
                logger.info(f"错误截图已保存至: {screenshot_path}")
            except:
                pass
            
            # 确保关闭页面
            await page.close()
            raise Exception(f"提取内容失败: {str(e)}")

async def batch_extract_contents(urls: List[str]) -> List[Dict]:
    """批量处理多个URL，提取内容并返回JSON格式"""
    results = []
    max_concurrent = 1  # 限制并发数，避免资源消耗过大
    
    # 创建任务分组
    for i in range(0, len(urls), max_concurrent):
        batch_urls = urls[i:i+max_concurrent]
        tasks = []
        
        for url in batch_urls:
            logger.info(f"添加任务: 处理URL {url}")
            tasks.append(extract_content_from_url(url))
        
        # 并发执行当前批次
        batch_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 处理结果
        for j, result in enumerate(batch_results):
            url_index = i + j
            url = urls[url_index] if url_index < len(urls) else "unknown"
            
            try:
                if isinstance(result, Exception):
                    # 处理异常情况
                    logger.error(f"处理URL {url} 时出错: {str(result)}")
                    results.append({
                        "url": url,
                        "error": str(result),
                        "title": "",
                        "authors": [],
                        "abstract": "",
                        "keywords": [],
                        "cite_format": ""
                    })
                else:
                    # 处理成功情况
                    results.append(result.dict())
                    logger.info(f"成功处理URL: {url}")
            except Exception as e:
                logger.error(f"处理结果时出错: {str(e)}")
                results.append({
                    "url": url,
                    "error": f"处理结果时出错: {str(e)}",
                    "title": "",
                    "authors": [],
                    "abstract": "",
                    "keywords": [],
                    "cite_format": ""
                })
        
        # 添加短暂延迟，避免过快请求导致被封
        await asyncio.sleep(2)
    
    logger.info(f"批量处理完成，共处理 {len(results)} 个URL")
    return results

# 直接搜索并提取内容
async def search_and_extract(keywords: str) -> Dict:
    """搜索关键词并提取所有论文的详细内容"""
    from . import server  # 导入server模块使用搜索功能
    
    try:
        logger.info(f"开始搜索关键词: {keywords}")
        # 使用server中的搜索功能
        links_count = await server.search_with_playwright(keywords)
        
        # 获取搜索结果
        page_content = server.page_content
        
        # 检查搜索结果
        if not isinstance(page_content, dict) or "links" not in page_content or not page_content["links"]:
            logger.error("搜索未返回有效链接")
            return {
                "error": "搜索未返回有效链接",
                "keywords": keywords,
                "count": 0,
                "results": []
            }
        
        # 提取链接
        urls = [link["url"] for link in page_content["links"] if "url" in link]
        if not urls:
            logger.error("搜索返回结果中没有有效链接")
            return {
                "error": "未找到有效链接",
                "keywords": keywords,
                "count": 0,
                "results": []
            }
        
        logger.info(f"搜索成功，找到 {len(urls)} 个链接，开始提取内容")
        
        # 提取内容
        results = await batch_extract_contents(urls)
        
        # 包装结果
        result_dict = {
            "keywords": keywords,
            "count": len(results),
            "results": results,
            "success_count": sum(1 for r in results if "error" not in r or not r["error"]),
            "error_count": sum(1 for r in results if "error" in r and r["error"])
        }
        
        return result_dict
    
    except Exception as e:
        logger.error(f"搜索并提取时出错: {str(e)}")
        logger.error(traceback.format_exc())
        return {
            "error": f"搜索并提取内容时出错: {str(e)}",
            "keywords": keywords,
            "count": 0,
            "results": []
        }

# 单元测试
async def test_extractor():
    """测试提取器功能"""
    test_url = "https://kns.cnki.net/kcms2/article/abstract?v=3uoqIhG8C44YLTlOAiTRKibYlV5Vjs7ioT0BO4yQ4m_wBGfVyh51O4GSy-IA63-FppCj3oNSHEUNzY35qnIKlFKtN6Av&uniplatform=NZKPT"
    try:
        content = await extract_content_from_url(test_url)
        print(f"提取成功:\n{content.json(indent=2, ensure_ascii=False)}")
        return True
    except Exception as e:
        print(f"测试失败: {str(e)}")
        return False

if __name__ == "__main__":
    # 运行测试
    asyncio.run(test_extractor()) 
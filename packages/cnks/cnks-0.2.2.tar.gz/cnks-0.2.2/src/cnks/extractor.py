from typing import Dict, List, Optional, Union
import logging
import traceback
import asyncio
from contextlib import asynccontextmanager
from datetime import datetime
from pydantic import BaseModel

from playwright.async_api import async_playwright, Browser, BrowserContext, Page

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename="cnki_extractor.log",
    filemode="a"
)
logger = logging.getLogger("cnki_extractor")

# 定义数据模型
class CNKIContent(BaseModel):
    """CNKI论文内容模型"""
    title: str = ""
    authors: List[str] = []
    abstract: str = ""
    keywords: List[str] = []
    cite_format: str = ""
    url: str = ""  # 添加URL字段以记录来源

async def get_browser():
    """获取浏览器实例"""
    from . import server  # 导入服务器模块以使用查找Chrome的函数
    
    playwright = await async_playwright().start()
    
    # 查找本地Chrome路径
    chrome_path = server.find_chrome_executable()
    
    if not chrome_path:
        raise ValueError('未找到Chrome可执行文件，请设置CHROME_PATH环境变量指向Chrome位置')
    
    logger.info(f"使用本地Chrome: {chrome_path}")
    
    try:
        # 尝试使用channel='chrome'模式
        browser = await playwright.chromium.launch(
            headless=False,
            channel="chrome"  # 优先使用Chrome通道
        )
    except Exception as e:
        logger.info(f"使用channel='chrome'失败: {str(e)}，尝试使用executable_path")
        # 如果失败，尝试使用executable_path指定Chrome路径
        browser = await playwright.chromium.launch(
            headless=False, 
            executable_path=chrome_path
        )
    
    context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
    
    return playwright, browser, context

async def extract_content_from_url(url: str) -> CNKIContent:
    """从CNKI页面提取论文内容"""
    if not url.startswith('https://kns.cnki.net/'):
        raise ValueError('URL必须是CNKI知网的链接')

    content = CNKIContent(url=url)
    playwright = None
    browser = None
    context = None
    page = None

    try:
        # 初始化浏览器
        playwright, browser, context = await get_browser()
        
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
                await asyncio.sleep(10)  # 给用户一些时间登录

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
            
            return content
            
        except Exception as e:
            logger.error(f"提取内容时出错: {str(e)}")
            if page:
                await page.screenshot(path=f'extraction_error_{datetime.now().strftime("%Y%m%d%H%M%S")}.png')
            raise Exception(f"提取内容失败: {str(e)}")

    except Exception as e:
        logger.error(f"处理请求时出错: {str(e)}")
        logger.error(f"错误堆栈: {traceback.format_exc()}")
        raise
    
    finally:
        # 关闭资源
        if page:
            await page.close()
        if context:
            await context.close()
        if browser:
            await browser.close()
        if playwright:
            await playwright.stop()

async def batch_extract_contents(urls: List[str]) -> List[Dict]:
    """批量处理多个URL，提取内容并返回JSON格式"""
    results = []
    
    for i, url in enumerate(urls):
        try:
            logger.info(f"正在处理第 {i+1}/{len(urls)} 个URL: {url}")
            content = await extract_content_from_url(url)
            results.append(content.dict())
            logger.info(f"成功提取第 {i+1} 个URL的内容")
            # 添加短暂延迟，避免过快请求导致被封
            await asyncio.sleep(2)
        except Exception as e:
            logger.error(f"处理URL {url} 时出错: {str(e)}")
            # 添加错误信息而不是跳过，这样可以知道哪些URL处理失败
            results.append({
                "url": url,
                "error": str(e),
                "title": "",
                "authors": [],
                "abstract": "",
                "keywords": [],
                "cite_format": ""
            })
    
    return results

# 单元测试
async def test_extractor():
    """测试提取器功能"""
    test_url = "https://kns.cnki.net/kcms2/article/abstract?v=3uoqIhG8C44YLTlOAiTRKibYlV5Vjs7ioT0BO4yQ4m_wBGfVyh51O4GSy-IA63-FppCj3oNSHEUNzY35qnIKlFKtN6Av&uniplatform=NZKPT"
    try:
        content = await extract_content_from_url(test_url)
        print(f"提取成功:\n{content.json(indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"测试失败: {str(e)}")

if __name__ == "__main__":
    # 运行测试
    asyncio.run(test_extractor()) 
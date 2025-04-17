import base64
import json
from mcp.server.fastmcp import FastMCP, Context
from mcp.types import TextContent, ImageContent
from playwright.async_api import Page
from browse_mcp.browse_manager import BrowserManager
from pydantic import BaseModel, Field
from browse_mcp.tools.playwright_tools import PlaywrightTools
import pathlib
from browse_mcp.tools.file_tools import FileTools

# from autogen_ext.agents.web_surfer._types import InteractiveRegion
from autogen_ext.agents.web_surfer.playwright_controller import PlaywrightController
from typing import (
    Any,
    AsyncGenerator,
    Dict,
    List,
    Optional,
    Sequence,
)


class SearchResult(BaseModel):
    """百度搜索结果的数据模型"""
    title: str = Field(description="搜索结果的标题")
    url: str = Field(description="搜索结果的URL链接")
    snippet: str = Field(description="搜索结果的简介摘要")
    source: Optional[str] = Field(None, description="来源网站")
    time: Optional[str] = Field(None, description="发布时间（如果有）")
    
    class Config:
        # 确保JSON序列化时不将中文转换为Unicode编码
        json_encoders = {
            str: lambda v: v
        }
        json_dumps_kwargs = {
            "ensure_ascii": False
        }
    
    def model_dump(self, **kwargs):
        """重写model_dump方法，确保返回的JSON不使用Unicode编码"""
        # 合并默认参数和传入的参数
        dump_kwargs = {"exclude_none": True}
        dump_kwargs.update(kwargs)
        # 调用父类的model_dump方法
        result = super().model_dump(**dump_kwargs)
        return result

class BrowserNavigationServer(FastMCP):
    def __init__(self, server_name="browser-operation-server"):
        super().__init__(server_name)
        self.mcp = self
        self.browser_manager = BrowserManager()
        # self.llm_config = get_default_llm_config()
        # self.llm_client = LLMClient(self.llm_config)

        self.search_results_cache = {}
        self.current_page = 1
        self.current_query = ""
        self.total_pages = 1
        
        self.screenshots = dict()
        self.register_tools()
        self.register_resources()
        self.register_prompts()
        self.file_tools = FileTools()

    def register_tools(self):
        @self.mcp.tool(description="Navigate to a URL and get makrdown content")
        async def playwright_navigate(url: str):
            """Navigate to a URL and return the page content in markdown format."""
            try:
                page: Page = await self.browser_manager.ensure_browser()
                await page.goto(url=url, wait_until="load", timeout=30000)
                
                # 获取页面标题
                page_title = await page.title()
                
                # 使用PlaywrightController获取页面内容的markdown格式
                playwright_controller = PlaywrightController()
                page_markdown = await playwright_controller.get_page_markdown(page)
                
                return {
                    "title": page_title,
                    "url": url,
                    "content": page_markdown
                }
            except Exception as e:
                raise ValueError(f"Navigation failed: {e}")
                
        @self.mcp.tool(description="在百度上搜索并获取结果")
        async def baidu_search(query: str, page: int = 1):
            """在百度上执行搜索查询并返回结果
            
            为了避免触发百度验证码，本方法会:
            1. 设置合理的User-Agent
            2. 模拟真实用户行为
            3. 控制请求频率
            4. 在需要时处理验证码
            5. 通过点击分页按钮获取每页结果
            
            参数:
                query: 搜索关键词
                page: 检索的页数
            """
            try:
                self.current_query = query
                self.current_page = page
                
                # 导航到百度首页
                search_url = f"https://www.baidu.com"
                
                # 导航到搜索页面
                browser_page: Page = await self.browser_manager.ensure_browser()

                # 设置合理的User-Agent和其他请求头，模拟真实浏览器
                # 使用常见的现代浏览器User-Agent
                user_agents = [
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15",
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55",
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0"
                ]
                import random
                
                # 随机选择一个User-Agent
                selected_user_agent = random.choice(user_agents)
                
                # 设置额外的请求头
                extra_headers = {
                    "User-Agent": selected_user_agent,
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Connection": "keep-alive",
                    "Upgrade-Insecure-Requests": "1",
                    "Cache-Control": "max-age=0"
                }
                
                # 设置请求头并导航到搜索页面
                await browser_page.set_extra_http_headers(extra_headers)
                await browser_page.goto(url=search_url, wait_until="domcontentloaded", timeout=30000)
                
                # 等待页面加载完成
                await browser_page.wait_for_load_state("networkidle")
                
                # 定位搜索框并输入关键词
                search_input_selector = "#kw"
                await browser_page.wait_for_selector(search_input_selector, timeout=5000)
                await browser_page.fill(search_input_selector, query)
                # 点击搜索按钮
                search_button_selector = "#su"
                await browser_page.wait_for_selector(search_button_selector, timeout=5000)
                await browser_page.click(search_button_selector)
                
                # 等待页面加载完成
                await browser_page.wait_for_load_state("networkidle")
                await browser_page.wait_for_selector(".result", timeout=5000)
                
                # 提取分页信息
                total_pages = await self._extract_pagination_info(browser_page)
                self.total_pages = total_pages
                # 如果需要获取所有页面的结果
                page_results = await self._extract_search_results(browser_page)
                if total_pages > 1 and page > 1:
                    self.current_page = 2
                    # 从当前页开始，获取后续所有页面的结果
                    while self.current_page <= page and self.current_page <= self.total_pages:
                        # 查找下一页按钮 - 尝试多种选择器
                        next_page_selector = "a.n:has-text('下一页')"
                        clicked = False
                        
                        # 等待下一页按钮出现
                        next_button = await browser_page.wait_for_selector(next_page_selector, timeout=15000)
                        if next_button:
                            # 确保按钮可见且可点击
                            await next_button.scroll_into_view_if_needed()
                            await browser_page.click(next_page_selector)
                            clicked = True
                            # 等待页面加载完成
                            await browser_page.wait_for_load_state("networkidle")
                            await browser_page.wait_for_selector(".result", timeout=15000)
            
                        
                        if not clicked:
                            print("无法找到下一页按钮")
                            break
                        
                        # 更新当前页码
                        self.current_page += 1
                        
                        # 添加随机延迟，避免触发验证码
                        delay_time = random.uniform(1.0, 2.0)
                        await browser_page.wait_for_timeout(delay_time * 1000)  # 转换为毫秒
                        current_page_results = await self._extract_search_results(browser_page)
                        # 合并结果
                        page_results.extend(current_page_results)
                # 缓存结果
                cache_key = f"{query}_{page}"
                self.search_results_cache[cache_key] = page_results
                
                # 构建返回信息
                # 使用json.dumps确保中文字符不会被转换为Unicode编码
                return {
                    "query": query,
                    "page": page,
                    "total_pages": total_pages,
                    "results": json.loads(json.dumps([result.model_dump(exclude_none=True) for result in page_results], ensure_ascii=False)),
                    "result_count": len(page_results)
                }
            except Exception as e:
                raise ValueError(f"搜索失败: {e}")
    async def _extract_pagination_info(self, page: Page) -> int:
        """提取分页信息"""
        try:
            # 尝试获取总页数
            total_pages = await page.evaluate("""
                () => {
                    const pageInfo = document.querySelector('.page-inner');
                    if (pageInfo) {
                        const lastPage = pageInfo.querySelector('a:last-of-type');
                        if (lastPage && lastPage.textContent) {
                            const pageNum = parseInt(lastPage.textContent.trim());
                            return isNaN(pageNum) ? 1 : pageNum;
                        }
                    }
                    return 1; // 默认为1页
                }
            """)
            return 10
        except Exception:
            return 1  # 如果无法提取，默认为1页
    async def _simulate_human_behavior(self, page: Page):
        """模拟真实用户行为，随机滚动和暂停"""
        import random
        import asyncio
        
        # 随机滚动页面
        for _ in range(random.randint(2, 5)):
            # 随机滚动距离
            scroll_distance = random.randint(300, 800)
            await page.evaluate(f"window.scrollBy(0, {scroll_distance})")
            
            # 随机暂停时间
            pause_time = random.uniform(0.5, 2.0)
            await asyncio.sleep(pause_time)
        
        # 有时候滚回顶部
        if random.random() > 0.7:
            await page.evaluate("window.scrollTo(0, 0)")
            await asyncio.sleep(random.uniform(0.3, 1.0))
            
    async def _check_and_handle_captcha(self, page: Page) -> bool:
        """检查是否出现验证码并尝试处理
        
        返回值:
            bool: 如果检测到并处理了验证码返回True，否则返回False
        """
        # 检查常见的百度验证码元素
        captcha_selectors = [
            "#verify_img",  # 图片验证码
            ".vcode-spin",  # 旋转验证码
            ".vcode-slide",  # 滑动验证码
            "#seccodeImage",  # 安全验证码图片
            ".vcode-body"  # 验证码容器
        ]
        
        for selector in captcha_selectors:
            if await page.query_selector(selector) is not None:
                print("检测到百度验证码，需要人工处理")
                
                # 在控制台记录验证码出现
                if hasattr(self, 'console_logs'):
                    self.console_logs.append("[警告] 检测到百度验证码，请手动处理")
                
                # 等待用户手动处理验证码
                # 这里我们等待30秒，假设用户会在这段时间内解决验证码
                # 在实际应用中，可能需要更复杂的机制来通知用户并等待验证码解决
                await page.wait_for_timeout(30000)  # 等待30秒
                
                # 检查验证码是否已解决
                if await page.query_selector(selector) is None:
                    return True  # 验证码已解决
                
                # 如果验证码仍然存在，可能需要更多时间或其他处理方式
                # 这里简单地再等待30秒
                await page.wait_for_timeout(30000)  # 再等待30秒
                return True  # 无论验证码是否解决，我们都返回True表示已尝试处理
        
        return False  # 没有检测到验证码
    
    async def _extract_search_results(self, page: Page) -> List[SearchResult]:
        """从百度搜索页面提取搜索结果"""
        results = []
        
        # 使用JavaScript提取搜索结果
        raw_results = await page.evaluate("""
            () => {
                const resultElements = document.querySelectorAll('.result');
                return Array.from(resultElements).map(el => {
                    // 提取标题和URL
                    const titleEl = el.querySelector('.t a, .c-title a');
                    const title = titleEl ? titleEl.textContent.trim() : '';
                    const url = titleEl ? titleEl.href : '';
                    
                    // 提取摘要
                    const snippetEl = el.querySelector('.c-abstract, .content-abstract');
                    const snippet = snippetEl ? snippetEl.textContent.trim() : '';
                    
                    // 提取来源和时间（如果有）
                    const sourceEl = el.querySelector('.c-author, .c-color-gray');
                    const source = sourceEl ? sourceEl.textContent.trim() : null;
                    
                    // 提取时间（通常包含在来源信息中）
                    let time = null;
                    if (source) {
                        const timeMatch = source.match(/\d{4}年\d{1,2}月\d{1,2}日|\d{1,2}天前|\d{1,2}小时前/);
                        time = timeMatch ? timeMatch[0] : null;
                    }
                    
                    return { title, url, snippet, source, time };
                });
            }
        """)
        
        # 将原始结果转换为SearchResult对象
        for item in raw_results:
            if item['title'] and item['url']:
                results.append(SearchResult(
                    title=item['title'],
                    url=item['url'],
                    snippet=item['snippet'] if item['snippet'] else "无摘要",
                    source=item['source'],
                    time=item['time']
                ))
        
        return results

        



    def register_resources(self):
        @self.mcp.resource("console://logs")
        async def get_console_logs() -> str:
            """Get a personalized greeting"""
            return TextContent(
                type="text", text="\n".join(self.browser_manager.console_logs)
            )

        @self.mcp.resource("screenshot://{name}")
        async def get_screenshot(name: str) -> str:
            """Get a screenshot by name"""
            screenshot_base64 = self.screenshots.get(name)
            if screenshot_base64:
                return ImageContent(
                    type="image",
                    data=screenshot_base64,
                    mimeType="image/png",
                    uri=f"screenshot://{name}",
                )
            else:
                raise ValueError(f"Screenshot {name} not found")

    def register_prompts(self):
        @self.mcp.prompt()
        async def hello_world(code: str) -> str:
            return f"Hello world:\n\n{code}"


""" 
When executing the MCP Inspector in a terminal, use the following command:

```bash
cmd> fastmcp dev ./server/browser_navigator_server.py:app
```

app = BrowserNavigationServer()

- `server/browser_navigator_server.py` specifies the file path.
- `app` refers to the server object created by `BrowserNavigationServer`.

After running the command, the following message will be displayed:

```
> Starting MCP Inspector...
> 🔍 MCP Inspector is up and running at http://localhost:5173 🚀
```

**Important:** Do not use `__main__` to launch the MCP Inspector. This will result in the following error:

    No server object found in **.py. Please either:
    1. Use a standard variable name (mcp, server, or app)
    2. Specify the object name with file:object syntax
"""

app = BrowserNavigationServer()
def main():
    app.run()

print("BrowserNavigationServer is running...")
# print all attributes of the mcp
# print(dir(app))


# if __name__ == "__main__":
#     app = BrowserNavigationServer()
#     app.run()
#     print("BrowserNavigationServer is running...")


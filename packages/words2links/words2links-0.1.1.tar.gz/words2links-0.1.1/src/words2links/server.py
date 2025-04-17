import asyncio
import os
import time
from typing import AsyncGenerator, Optional

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
from pydantic import AnyUrl
import mcp.server.stdio

from playwright.async_api import async_playwright
import urllib.parse

# Store notes as a simple key-value dict to demonstrate state management
notes: dict[str, str] = {}

server = Server("words2links")

@server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    """
    List available note resources.
    Each note is exposed as a resource with a custom note:// URI scheme.
    """
    return [
        types.Resource(
            uri=AnyUrl(f"note://internal/{name}"),
            name=f"Note: {name}",
            description=f"A simple note named {name}",
            mimeType="text/plain",
        )
        for name in notes
    ]

@server.read_resource()
async def handle_read_resource(uri: AnyUrl) -> str:
    """
    Read a specific note's content by its URI.
    The note name is extracted from the URI host component.
    """
    if uri.scheme != "note":
        raise ValueError(f"Unsupported URI scheme: {uri.scheme}")

    name = uri.path
    if name is not None:
        name = name.lstrip("/")
        return notes[name]
    raise ValueError(f"Note not found: {name}")

@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    """
    List available prompts.
    Each prompt can have optional arguments to customize its behavior.
    """
    return [
        types.Prompt(
            name="summarize-notes",
            description="Creates a summary of all notes",
            arguments=[
                types.PromptArgument(
                    name="style",
                    description="Style of the summary (brief/detailed)",
                    required=False,
                )
            ],
        )
    ]

@server.get_prompt()
async def handle_get_prompt(
    name: str, arguments: dict[str, str] | None
) -> types.GetPromptResult:
    """
    Generate a prompt by combining arguments with server state.
    The prompt includes all current notes and can be customized via arguments.
    """
    if name != "summarize-notes":
        raise ValueError(f"Unknown prompt: {name}")

    style = (arguments or {}).get("style", "brief")
    detail_prompt = " Give extensive details." if style == "detailed" else ""

    return types.GetPromptResult(
        description="Summarize the current notes",
        messages=[
            types.PromptMessage(
                role="user",
                content=types.TextContent(
                    type="text",
                    text=f"Here are the current notes to summarize:{detail_prompt}\n\n"
                    + "\n".join(
                        f"- {name}: {content}"
                        for name, content in notes.items()
                    ),
                ),
            )
        ],
    )

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    列出可用工具
    只提供搜索论文的工具
    """
    return [
        types.Tool(
            name="search_papers",
            description="使用关键词搜索CNKI知网CSSCI来源的论文",
            inputSchema={
                "type": "object",
                "properties": {
                    "keyword": {"type": "string"},
                },
                "required": ["keyword"],
            },
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> AsyncGenerator[types.TextContent | types.ImageContent | types.EmbeddedResource, None]:
    """
    实现工具执行逻辑
    search_papers工具用于搜索CNKI论文
    """
    if name != "search_papers":
        raise ValueError(f"未知工具: {name}")

    if not arguments:
        raise ValueError("缺少参数")

    keyword = arguments.get("keyword")
    if not keyword:
        raise ValueError("缺少关键词参数")

    yield types.TextContent(type="text", text=f"开始搜索关键词: {keyword}...")
    
    # 使用异步迭代器正确处理异步生成器
    search_generator = search_papers(keyword)
    async for result in search_generator:
        yield types.TextContent(type="text", text=result)
    
    yield types.TextContent(type="text", text=f"搜索完成.")

async def search_papers(keyword: str) -> AsyncGenerator[str, None]:
    """使用关键词搜索CNKI知网CSSCI来源的论文
    
    Args:
        keyword: 搜索关键词
        
    Yields:
        进度更新和结果
    """
    yield f"准备搜索: {keyword}"
    
    async with async_playwright() as p:
        yield "启动浏览器..."
        
        # 创建用户数据目录
        user_data_dir = os.path.join(os.path.expanduser("~"), ".playwright_user_data")
        os.makedirs(user_data_dir, exist_ok=True)
        
        browser = await p.chromium.launch(
            headless=True,  # 无头模式，实际使用时可改为True
            args=[
                "--disable-extensions",
                "--disable-gpu",
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-accelerated-2d-canvas",
                "--no-first-run",
                "--no-zygote",
                "--deterministic-fetch",
                "--disable-features=IsolateOrigins",
                "--disable-site-isolation-trials",
            ],
            user_data_dir=user_data_dir
        )
        
        try:
            # 创建上下文和页面
            yield "创建浏览器上下文..."
            context = await browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            )
            
            # 设置超时
            context.set_default_timeout(60000)  # 60秒
            
            # 测试网络连接
            yield "测试网络连接..."
            test_page = await context.new_page()
            try:
                await test_page.goto("https://www.baidu.com", wait_until="networkidle")
                yield "网络连接正常"
            except Exception as e:
                yield f"网络连接测试失败: {str(e)}"
                await test_page.close()
                raise Exception("网络连接测试失败，请检查网络设置")
            await test_page.close()
            
            # 主要搜索逻辑
            yield "打开知网搜索页面..."
            page = await context.new_page()
            
            try:
                # 构造搜索URL
                encoded_keyword = urllib.parse.quote(keyword)
                search_url = f"https://kns.cnki.net/kns8s/defaultresult/index?kw={encoded_keyword}"
                
                yield f"正在导航到搜索URL: {search_url}"
                try:
                    await page.goto(search_url, wait_until="domcontentloaded", timeout=90000)
                    yield "页面加载完成，等待结果..."
                except Exception as e:
                    yield f"导航到搜索页面失败: {str(e)}"
                    raise
                
                # 等待页面完全加载
                try:
                    await page.wait_for_load_state("networkidle", timeout=30000)
                    yield "网络加载完成"
                except Exception as e:
                    yield f"等待网络加载完成超时: {str(e)}"
                
                # 处理结果页面
                yield "处理搜索结果..."
                paper_links = await handle_results_page(page)
                
                if not paper_links:
                    yield "未找到论文，可能是搜索结果为空或网页结构发生变化"
                else:
                    yield f"找到 {len(paper_links)} 篇论文"
                    
                    # 格式化结果
                    results = [keyword]  # 第一行是关键词
                    for title, url in paper_links:
                        results.append(title)
                        results.append(f"@{url}")
                    
                    # 逐行返回结果
                    for line in results:
                        yield line
                
            except Exception as e:
                yield f"搜索过程中发生错误: {str(e)}"
                raise
            finally:
                await page.close()
        
        finally:
            await browser.close()
            yield "浏览器已关闭"

async def handle_results_page(page) -> list[tuple[str, str]]:
    """处理搜索结果页面，提取论文链接
    
    Args:
        page: Playwright页面对象
        
    Returns:
        论文标题和链接的列表 [(title, url), ...]
    """
    # 等待页面加载完成
    await asyncio.sleep(3)  # 等待3秒确保页面完全加载
    
    # 设置每页显示50条
    try:
        await page.evaluate("""() => {
            try {
                // 尝试点击页数选择器
                const pageSizeElements = document.querySelectorAll('.perpage-content a');
                if (pageSizeElements && pageSizeElements.length > 0) {
                    // 找到50条/页的元素并点击
                    for (let elem of pageSizeElements) {
                        if (elem.textContent.includes('50')) {
                            elem.click();
                            return true;
                        }
                    }
                }
                return false;
            } catch (e) {
                return false;
            }
        }""")
        await page.wait_for_load_state("networkidle", timeout=10000)
    except Exception as e:
        pass  # 忽略设置每页显示50条的错误，继续处理
    
    # 尝试选择CSSCI来源
    try:
        await page.evaluate("""() => {
            try {
                // 查找CSSCI选择框
                const cssciElements = Array.from(document.querySelectorAll('.list-setup'));
                const cssciElement = cssciElements.find(el => el.textContent.includes('CSSCI'));
                
                if (cssciElement) {
                    // 找到前一个兄弟节点中的复选框
                    const checkboxParent = cssciElement.parentElement.previousElementSibling;
                    if (checkboxParent) {
                        const checkbox = checkboxParent.querySelector('input[type="checkbox"]');
                        if (checkbox && !checkbox.checked) {
                            checkbox.click();
                            return true;
                        }
                    }
                }
                return false;
            } catch (e) {
                return false;
            }
        }""")
        await page.wait_for_load_state("networkidle", timeout=10000)
    except Exception as e:
        pass  # 忽略CSSCI选择错误，继续处理
    
    # 提取论文链接
    paper_links = []
    
    # 使用多种选择器尝试找到结果
    selectors = [
        ".result-table-list .result-table-item",
        ".search-result .search-result-item",
        "#gridTable .result-item"
    ]
    
    for selector in selectors:
        try:
            items = await page.query_selector_all(selector)
            if items and len(items) > 0:
                for item in items:
                    try:
                        # 提取标题和链接
                        title_selector = await item.query_selector(".title a, h1 a, .text a")
                        if title_selector:
                            title = await title_selector.text_content()
                            href = await title_selector.get_attribute("href")
                            
                            # 处理论文链接
                            if href and not href.startswith("http"):
                                base_url = page.url.split("/kns8")[0]
                                href = f"{base_url}{href}"
                            
                            if title and href:
                                paper_links.append((title.strip(), href.strip()))
                    except Exception:
                        continue
            
            if paper_links:
                break  # 如果找到结果，不再尝试其他选择器
        except Exception:
            continue
    
    # 如果上面的方法都没找到结果，尝试直接从页面提取链接
    if not paper_links:
        try:
            # 使用JavaScript从页面中提取所有论文链接
            urls_from_javascript = await page.evaluate("""() => {
                const links = Array.from(document.querySelectorAll('a'));
                return links
                    .filter(link => {
                        const href = link.getAttribute('href');
                        const text = link.textContent;
                        return href && 
                               (href.includes('/kcms') || href.includes('dbcode=CJFD')) && 
                               text && 
                               text.length > 5;
                    })
                    .map(link => ({
                        title: link.textContent.trim(),
                        url: link.getAttribute('href')
                    }));
            }""")
            
            if urls_from_javascript and len(urls_from_javascript) > 0:
                for item in urls_from_javascript:
                    title = item.get("title")
                    url = item.get("url")
                    
                    # 处理相对URL
                    if url and not url.startswith("http"):
                        base_url = page.url.split("/kns8")[0]
                        url = f"{base_url}{url}"
                    
                    if title and url:
                        paper_links.append((title, url))
        except Exception:
            pass
    
    return paper_links

async def main():
    # 使用标准输入/输出流运行服务器
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="words2links",
                server_version="0.1.1",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
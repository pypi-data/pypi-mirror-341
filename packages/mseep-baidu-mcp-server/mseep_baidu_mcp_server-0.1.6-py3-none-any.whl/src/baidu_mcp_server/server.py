import time
from mcp.server.fastmcp import FastMCP, Context
import httpx
from bs4 import BeautifulSoup
from typing import List
from dataclasses import dataclass
import sys
import traceback
import asyncio
from datetime import datetime, timedelta
import re
import readabilipy.simple_json
import markdownify
import logging


logging.getLogger("httpx").setLevel(logging.WARNING)

@dataclass
class SearchResult:
    title: str
    link: str
    snippet: str
    position: int


class RateLimiter:
    def __init__(self, requests_per_minute: int = 30):
        self.requests_per_minute = requests_per_minute
        self.requests = []

    async def acquire(self):
        now = datetime.now()
        # Remove requests older than 1 minute
        self.requests = [
            req for req in self.requests if now - req < timedelta(minutes=1)
        ]

        if len(self.requests) >= self.requests_per_minute:
            # Wait until we can make another request
            wait_time = 60 - (now - self.requests[0]).total_seconds()
            if wait_time > 0:
                await asyncio.sleep(wait_time)

        self.requests.append(now)


class BaiduSearcher:
    BASE_URL = "https://m.baidu.com/s"
    WEB_NORMAL = "1599"
    WEB_VIDEO_NORMAL = "48304"
    WEB_NOTE_NORMAL = "61570"
    WEB_KNOWLEDGE = "1529"
    WEB_WENKU = "1525"

    # WEB_VIDEO = "4295"
    # WEB_SHORT_VIDEO = "4660"
    # WEB_BAIKE = "1547"
    # WEB_REYI = "201"

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.59",
        "Referer": "https://m.baidu.com",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    }

    def __init__(self):
        self.rate_limiter = RateLimiter()

    async def process_result(self, result, fetcher):
        """
        处理单个结果，生成 content 并返回 SearchResult 对象。
        """
        content = ""
        abstract = result.get("abstract", "")
        labels = result.get("labels", [])
        url = result["url"]

        # 添加摘要部分
        if len(abstract) > 0:
            content += f"# Abstract\n{abstract}\n"
        
        # 添加标签部分
        if len(labels) > 0:
            content += f"# Labels\n{','.join(labels)}\n"

        try:
            text, url = await fetcher.fetch_and_parse(url)
            if len(text) > 0:
                content += f"# Content\n{text}"
        except Exception as e:
            pass

        return SearchResult(
            title=result.get("title", ""),
            link=url,
            snippet=content,
            position=None
        )
    
    def format_results_for_llm(self, results: List[SearchResult]) -> str:
        """Format results in a natural language style that's easier for LLMs to process"""
        if not results:
            return "No results were found for your search query. This could be due to Baidu's bot detection or the query returned no matches. Please try rephrasing your search or try again in a few minutes."

        output = []
        output.append(f"Found {len(results)} search results:\n")

        for result in results:
            output.append(f"{result.position}. {result.title}")
            output.append(f"   URL: {result.link}")
            output.append(f"   Summary: {result.snippet}")
            output.append("")  # Empty line between results

        return "\n".join(output)
    
    async def search(
        self, query: str, ctx: Context, max_results: int = 6, deep_mode: bool = False, max_retries: int = 5,
    ) -> List[SearchResult]:
       # Apply rate limiting
        await self.rate_limiter.acquire()

        # Create form data for POST request
        params = {
            "word": query,
        }

        await ctx.info(f"Searching Baidu for: {query}")

        search_results = []
        results = []
        pg = 0
        while len(results) < max_results:
            pg += 1
            pn = pg * 10
            try_cnt = 0
            while try_cnt < max_retries:
                try:
                    params["pn"] = pn
                    async with httpx.AsyncClient() as client:
                        response = await client.get(
                            self.BASE_URL, params=params, headers=self.HEADERS, timeout=30.0
                        )
                        response.raise_for_status()
                    break
                except:
                    try_cnt += 1
                    time.sleep(5)

            # Parse HTML response
            soup = BeautifulSoup(response.text, "html.parser")
            if not soup:
                await ctx.error("Failed to parse HTML response")
                return []
            res_normal_container = soup.findAll(
                "div", class_="c-result result", new_srcid=self.WEB_NORMAL
            )
            res_normal = []
            for res in res_normal_container:
                _ = res.find("div", class_="c-result-content").find("article")
                header = _.find("section").find("div")
                # 标签
                labels = []
                # 标题
                title = header.find(attrs={"data-module": "title"})
                if title:
                    title = title.find("span", class_="tts-b-hl").text
                # 链接
                try:
                    url = _["rl-link-href"]
                except Exception:
                    url = header.find("a")["href"]
                __ = header.find(attrs={"data-module": "title"})
                if __:
                    __ = __.find("span", class_="sc-tag")
                # “官方”标签
                if __:
                    labels.append(__.text)
                section = _.find("section")
                # 简介
                des = ""
                # 可能有多个`span`标签，需要依次解析
                ___ = _.find(attrs={"data-module": "abstract"})
                if ___:
                    for s in ___.findAll("div", role="text"):
                        for t in s.findAll("span"):
                            try:
                                if t.find("span").text:
                                    continue
                            except Exception:
                                pass
                            try:
                                if "c-color-gray" in t["class"]:
                                    continue
                            except Exception:
                                pass
                            des += t.text
                        des += "\n"
                des = des.strip("\n")
                # 来源（作者）
                origin = section.find("span", class_="cosc-source-text")
                if origin:
                    origin = origin.text
                else:
                    if __:
                        origin = __.find("div", class_="single-text")
                        if origin:
                            origin = origin.text
                
                
                res_normal.append(
                    {
                        "title": title,
                        "url": url,
                        "labels": labels,
                        "abstract": des,
                        "origin": origin,
                        "type": "web",
                    }
                )



            res_wenku_container = soup.findAll(
                "div", class_="c-result result", new_srcid=self.WEB_WENKU
            )
            res_wenku_normal = []
            for res in res_wenku_container:
                _ = res.find("div", class_="c-result-content").find("article")
                header = _.find("section").find("div")
                # 标签
                labels = []
                # 标题
                title = header.find(attrs={"data-module": "title"}).find("span", class_="tts-b-hl").text
                # 链接
                try:
                    url = _["rl-link-href"]
                except Exception:
                    url = header.find("a")["href"]
                
                __ = header.find(attrs={"data-module": "title"}).find("span", class_="sc-tag")
                # “官方”标签
                if __:
                    labels.append(__.text)
                section = _.find("section")
                # 简介
                des = ""
                # 可能有多个`span`标签，需要依次解析
                for s in _.find(attrs={"data-module": "abstract"}).findAll("div", role="text"):
                    for t in s.findAll("span"):
                        try:
                            if t.find("span").text:
                                continue
                        except Exception:
                            pass
                        try:
                            if "c-color-gray" in t["class"]:
                                continue
                        except Exception:
                            pass
                        des += t.text
                    des += "\n"
                des = des.strip("\n")
                # 来源（作者）
                origin = section.find("span", class_="cosc-source-text")
                if origin:
                    origin = origin.text
                else:
                    origin = __.find("div", class_="single-text")
                    if origin:
                        origin = origin.text
                
                

                res_wenku_normal.append(
                    {
                        "title": title,
                        "url": url,
                        "labels": labels,
                        "abstract": des,
                        "origin": origin,
                        "type": "doc",
                    }
                )

            res_video_normal_container = soup.findAll(
                "div", class_="c-result result", new_srcid=self.WEB_VIDEO_NORMAL
            )


            res_video_normal = []
            for res in res_video_normal_container:
                _ = res.find("div", class_="c-result-content").find("article")
                header = _.find("section").find("div")
                title = header.find("div", class_="title-container").find("p").find("span").text
                # 链接
                try:
                    url = _["rl-link-href"]
                except Exception:
                    url = header.find("a")["href"]
                __ = _.findAll("span", class_="cos-tag")
                labels = []
                for ___ in __:
                    labels.append(___.text)
            
                
                pattern = re.compile(r"^abstract-text_")  # 匹配以 "abstract-text_" 开头的类名
                des = ""
                text = _.find("span", class_=pattern)

                if text:
                    des = text.text.strip()
                    
            
                origin = res.find("span", class_="cosc-source-text")
                if origin:
                    origin = origin.text
                else:
                    origin = __.find("div", class_="single-text")
                    if origin:
                        origin = origin.text
                    
                res_video_normal.append(
                    {
                        "title": title,
                        "url": url,
                        "origin": origin,
                        "labels": labels,
                        "abstract": des,
                        "type": "video",
                    }
                )
            

            res_note_normal_container = soup.findAll(
                "div", class_="c-result result", new_srcid=self.WEB_NOTE_NORMAL
            )


            res_note_normal = []
            for res in res_note_normal_container:
                _ = res.find("div", class_="c-result-content").find("article")
                __ = _.find("section").find("div").find("div", attrs={"data-module": "sc_lk"})
                try:
                    url = __["rl-link-href"]
                except Exception:
                    url = __.find("a")["href"]
            
                title = __.find(attrs={"data-module": "title"}).find("span", class_="cosc-title-slot").text
                if not header:
                    continue
                des = ""
                labels = []

                source = __.find(attrs={"data-module": "source"})
                for label in source.findAll("div"):
                    if not label.find("div") and len(label.text) > 0:
                        labels.append(label.text)



                origin = __.find("div", class_=re.compile(r"^source-name"))
                if origin:
                    origin = origin.text
                else:
                    origin = __.find("div", class_="single-text")
                    if origin:
                        origin = origin.text
                

                res_note_normal.append(
                    {
                        "title": title,
                        "url": url,
                        "origin": origin,
                        "labels": labels,
                        "abstract": des,
                        "type": "note",
                    }
                )

            res_knowledge_normal_container = soup.findAll(
                "div", class_="c-result result", new_srcid=self.WEB_KNOWLEDGE
            )


            res_knowledge_normal = []

            for res in res_knowledge_normal_container:
                _ = res.find("div", class_="c-result-content").find("article")
                __ = _.find("section").find("div", attrs={"data-module": "lgtte"})
                try:
                    url = _["rl-link-href"]
                except Exception:
                    url = __.find("a")["href"]
            
                title = __.find("div", class_="c-title").text
                des = ""
                labels = []
                lgtt = _.find("section").find("div", attrs={"data-module": "lgtt"})
                ___ = lgtt.find("div", class_=re.compile(r"^c-line-"))
                if ___:
                    des = ___.text.strip()
                
                origin = _.find("div", class_="c-color-source")
                if origin:
                    origin = origin.text
                else:
                    origin = _.find("div", class_="single-text")
                    if origin:
                        origin = origin.text
                
                
                res_knowledge_normal.append(
                    {
                        "title": title,
                        "url": url,
                        "origin": origin,
                        "labels": labels,
                        "abstract": des,
                        "type": "knowledge",
                    }
                )
            results.extend(res_normal)
            results.extend(res_wenku_normal)
            results.extend(res_knowledge_normal)
            results.extend(res_note_normal)
            results.extend(res_video_normal)
        
        if deep_mode:
            tasks = [self.process_result(result, fetcher) for result in results]

            search_tasks = await asyncio.gather(*tasks, return_exceptions=True)

            for i, result in enumerate(search_tasks):
                if isinstance(result, Exception):
                    await ctx.error("Failed to processing result")
                    continue
                
                result.position = len(search_results) + 1
                search_results.append(result)

        else:
            for result in results:
                search_results.append(SearchResult(
                title=result.get("title", ""),
                link=result.get("url", ""),
                snippet=result.get("abstract", ""),
                position=len(search_results) + 1
            ))
        await ctx.info(f"Successfully found {len(search_results)} results")
        return search_results

class WebContentFetcher:
    def __init__(self):
        self.rate_limiter = RateLimiter(requests_per_minute=20)


    def extract_content_from_html(self, html: str) -> str:
        """Extract and convert HTML content to Markdown format.

        Args:
            html: Raw HTML content to process

        Returns:
            Simplified markdown version of the content
        """
        ret = readabilipy.simple_json.simple_json_from_html_string(
            html, use_readability=True
        )
        if not ret["content"]:
            # Parse the HTML
            soup = BeautifulSoup(html, "html.parser")

            # Remove script and style elements
            for element in soup(["script", "style", "nav", "header", "footer"]):
                element.decompose()

            # Get the text content
            text = soup.get_text()

            # Clean up the text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = " ".join(chunk for chunk in chunks if chunk)

            # Remove extra whitespace
            content= re.sub(r"\s+", " ", text).strip()
        else:
            content = markdownify.markdownify(
                ret["content"],
                heading_style=markdownify.ATX,
            )

        if len(content) > 150:
            content = content[:150] + "..."
        return content

    async def fetch_and_parse(self, url: str, max_redirects=5) -> tuple[str, str]:
        """Fetch and parse content from a webpage"""
        try:
            await self.rate_limiter.acquire()
            async with httpx.AsyncClient() as client:
                try_cnt = 0
                visited = set()
                while try_cnt < max_redirects:
                    if url in visited:
                        break
            
                    try:
                        response = await client.get(
                            url,
                            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
                            timeout=30.0,
                            follow_redirects=True
                        )
               
                        visited.add(url)

                        # 检查是否为客户端重定向（JavaScript 或 meta 标签）
                        if "text/html" in response.headers.get("Content-Type", ""):
                            soup = BeautifulSoup(response.text, "html.parser")
                            
                            # 尝试解析 JavaScript 重定向
                            script_tag = soup.find("script")
                            if script_tag and "window.location.replace" in script_tag.text:
                                # 提取 JavaScript 中的 URL
                                match = re.search(r'window\.location\.replace\("([^"]+)"\)', script_tag.text)
                                if match:
                                    url = match.group(1)
                                    continue
                            
                            # 尝试解析 meta 标签重定向
                            meta_tag = soup.find("meta", attrs={"http-equiv": "refresh"})
                            if meta_tag and "url=" in meta_tag.get("content", "").lower():
                                # 提取 meta 标签中的 URL
                                content = meta_tag["content"]
                                url = content.split("url=", 1)[-1].strip()
                                continue
                    except:
                        continue
                    finally:
                        try_cnt += 1
                    
            

            text = self.extract_content_from_html(response.text)
            return text, url

        except httpx.TimeoutException:
            return "Error: The request timed out while trying to fetch the webpage."
        except httpx.HTTPError as e:
            return f"Error: Could not access the webpage ({str(e)})"
        except Exception as e:
            return f"Error: An unexpected error occurred while fetching the webpage ({str(e)})"


# Initialize FastMCP server
mcp = FastMCP("baidu-search")
searcher = BaiduSearcher()
fetcher = WebContentFetcher()


@mcp.tool()
async def search(query: str, ctx: Context, max_results: int = 6, deep_mode: bool = False) -> str:
    """
    Search Baidu and return formatted results.

    Args:
        query: The search query string
        max_results: Maximum number of results to return (default: 6)
        deep_mode: Deep search the web content (default: False)
        ctx: MCP context for logging
    """
    try:
        results = await searcher.search(query, ctx, max_results, deep_mode)
        return searcher.format_results_for_llm(results)
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        return f"An error occurred while searching: {str(e)}"



def main():
    mcp.run()


if __name__ == "__main__":
    main()
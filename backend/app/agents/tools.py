from langchain.tools import BaseTool
from langchain.pydantic_v1 import BaseModel, Field
from duckduckgo_search import DDGS
import arxiv
import json

class SearchInput(BaseModel):
    query: str = Field(description="Search query to look up")

class WebSearchTool(BaseTool):
    name = "web_search"
    description = "Search the web for current information using DuckDuckGo"
    args_schema = SearchInput

    def _run(self, query: str) -> str:
        """Search the web for current information."""
        try:
            print(f"🔍 Web searching: {query}")
            ddgs = DDGS()
            results = []
            for result in ddgs.text(query, max_results=3):
                results.append({
                    "title": result.get('title', ''),
                    "url": result.get('href', ''),
                    "snippet": result.get('body', '')[:150] + "..."
                })
            return f"Web search results for '{query}':\n{json.dumps(results, indent=2)}"
        except Exception as e:
            return f"Error performing web search: {str(e)}"

class ArxivSearchTool(BaseTool):
    name = "arxiv_search"
    description = "Search arXiv for academic papers and research articles"
    args_schema = SearchInput

    def _run(self, query: str) -> str:
        """Search arXiv for academic papers."""
        try:
            print(f"📚 ArXiv searching: {query}")
            client = arxiv.Client()
            search = arxiv.Search(
                query=query,
                max_results=3,
                sort_by=arxiv.SortCriterion.Relevance
            )
            
            results = []
            for result in client.results(search):
                results.append({
                    "title": result.title,
                    "authors": [author.name for author in result.authors][:2],
                    "summary": result.summary[:200] + "...",
                    "published": result.published.strftime("%Y-%m-%d"),
                    "pdf_url": result.pdf_url,
                })
            return f"arXiv search results for '{query}':\n{json.dumps(results, indent=2)}"
        except Exception as e:
            return f"Error searching arXiv: {str(e)}"

class CalculatorTool(BaseTool):
    name = "calculator"
    description = "Evaluate mathematical expressions. Input should be a mathematical expression like '2 + 2' or '3 * 5'."

    def _run(self, expression: str) -> str:
        """Evaluate a mathematical expression."""
        try:
            # Safe evaluation
            allowed_chars = set('0123456789+-*/.() ')
            if not all(c in allowed_chars for c in expression):
                return "Error: Invalid characters in expression"
            
            result = eval(expression, {"__builtins__": {}}, {})
            return f"{expression} = {result}"
        except Exception as e:
            return f"Error evaluating expression: {str(e)}"

    def _arun(self, expression: str):
        """Async not implemented."""
        raise NotImplementedError("Calculator does not support async")
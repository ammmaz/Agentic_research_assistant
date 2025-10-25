import os
from typing import Dict, Any, List
from langchain.chat_models import ChatOpenAI

class FallbackResearchAgent:
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            openai_api_key=api_key
        )
    
    def research_topic(self, topic: str, research_questions: List[str]) -> Dict[str, Any]:
        """Fallback research using direct LLM when tools fail."""
        try:
            prompt = f"""
            Conduct comprehensive research on: {topic}
            
            Answer these research questions:
            {chr(10).join(f'- {q}' for q in research_questions)}
            
            Provide detailed information with key findings, trends, and insights.
            Include specific examples and mention important developments in this field.
            """
            
            result = self.llm.predict(prompt)
            
            return {
                "success": True,
                "research_output": result,
                "sources_used": ["AI-generated analysis"],
                "mode": "fallback"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Fallback research failed: {str(e)}",
                "research_output": None
            }
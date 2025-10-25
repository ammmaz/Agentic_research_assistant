import os
from typing import Dict, Any, List
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI

from app.agents.tools import WebSearchTool, ArxivSearchTool, CalculatorTool

class ResearchAgent:
    def __init__(self, advanced_mode=False):
        # Get API key from environment
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("❌ OPENAI_API_KEY not found in environment variables")
        
        print(f"🤖 ResearchAgent initialized ({'Advanced' if advanced_mode else 'Standard'} mode)")
        
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
            openai_api_key=api_key,
            streaming=False
        )
        
        self.tools = [
            WebSearchTool(),
            ArxivSearchTool(), 
            CalculatorTool(),
        ]
        
        # Use different agent types for standard vs advanced
        agent_type = AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION
        
        self.agent_executor = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=agent_type,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=5 if advanced_mode else 3,
            early_stopping_method="generate"
        )
        
        self.advanced_mode = advanced_mode
    
    def research_topic(self, topic: str, research_questions: List[str]) -> Dict[str, Any]:
        """Research a topic with fallback mechanism."""
        
        if self.advanced_mode:
            research_prompt = self._create_advanced_prompt(topic, research_questions)
        else:
            research_prompt = self._create_standard_prompt(topic, research_questions)
        
        try:
            print(f"🔍 Starting {'advanced' if self.advanced_mode else 'standard'} research: {topic}")
            result = self.agent_executor.run(research_prompt)
            print("✅ Research completed successfully")
            
            return {
                "success": True,
                "research_output": result,
                "sources_used": self._extract_sources(result),
                "mode": "advanced" if self.advanced_mode else "standard"
            }
            
        except Exception as e:
            print(f"❌ Agent research failed: {str(e)}")
            print("🔄 Attempting fallback research...")
            
            # Try fallback
            try:
                from .fallback_agent import FallbackResearchAgent
                fallback_agent = FallbackResearchAgent()
                fallback_result = fallback_agent.research_topic(topic, research_questions)
                return fallback_result
            except Exception as fallback_error:
                error_msg = f"Both agent and fallback research failed: {str(e)}"
                print(f"❌ {error_msg}")
                return {
                    "success": False,
                    "error": error_msg,
                    "research_output": None,
                    "mode": "advanced" if self.advanced_mode else "standard"
                }
    
    def _create_standard_prompt(self, topic: str, research_questions: List[str]) -> str:
        """Create prompt for standard research."""
        return f"""You are a research assistant. Research the following topic and answer the specific questions.

Topic: {topic}

Research Questions:
{chr(10).join(f"- {q}" for q in research_questions)}

Use the available tools to gather information:
- web_search: Search the web for current information
- arxiv_search: Search for academic papers
- calculator: Perform calculations if needed

Provide a comprehensive answer with sources when possible.
"""
    
    def _create_advanced_prompt(self, topic: str, research_questions: List[str]) -> str:
        """Create prompt for advanced research."""
        return f"""You are an expert research analyst conducting in-depth research.

TOPIC: {topic}

RESEARCH QUESTIONS:
{chr(10).join(f'- {q}' for q in research_questions)}

RESEARCH METHODOLOGY:
1. First, use web_search to find current information and recent developments
2. Then, use arxiv_search to find academic research and scientific papers
3. Analyze the information from both sources
4. Identify key trends, patterns, and insights
5. Provide detailed analysis with specific examples and data

REQUIREMENTS:
- Conduct thorough multi-source research
- Compare and contrast information from different sources
- Provide specific examples and evidence
- Include statistical data if available
- Identify any controversies or differing viewpoints
- Suggest areas for further research

TOOLS AVAILABLE:
- web_search: Search for current news, articles, and information
- arxiv_search: Search for academic papers and scientific research
- calculator: Perform any necessary calculations

Provide a comprehensive, well-structured analysis.
"""
    
    def _extract_sources(self, output: str) -> List[str]:
        """Extract sources from the agent's output."""
        sources = []
        if isinstance(output, str):
            lines = output.split('\n')
            for line in lines:
                if 'http' in line or 'arxiv' in line.lower():
                    sources.append(line.strip())
        return sources[:5]

class MultiStepResearchAgent:
    def __init__(self):
        # Use advanced mode for multi-step research
        self.research_agent = ResearchAgent(advanced_mode=True)
    
    def conduct_research(self, topic: str, research_questions: List[str]) -> Dict[str, Any]:
        """Conduct multi-step advanced research."""
        print("🚀 Starting multi-step advanced research...")
        return self.research_agent.research_topic(topic, research_questions)
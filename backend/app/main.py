from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
from pathlib import Path

# ABSOLUTE PATH to .env file - USE THE PATH FROM DEBUG
env_path = Path(r"C:\Users\wajiz.pk\Documents\agentic-research-rag\.env")
print(f"🔍 Loading .env from: {env_path}")

if env_path.exists():
    load_dotenv(env_path)
    print("✅ .env file loaded successfully")
else:
    print("❌ .env file not found")

# Get API key
api_key = os.getenv('OPENAI_API_KEY')
print(f"🔑 API Key: {'✅ FOUND' if api_key else '❌ MISSING'}")
if api_key:
    print(f"   Key starts with: {api_key[:10]}...")

app = FastAPI(
    title="Research Assistant API",
    description="AI-powered research system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResearchRequest(BaseModel):
    topic: str
    research_questions: List[str]
    detailed_report: bool = True

class ResearchResponse(BaseModel):
    success: bool
    topic: str
    research_output: Optional[str] = None
    report: Optional[str] = None
    sources: Optional[List[str]] = None
    error: Optional[str] = None

@app.get("/")
async def root():
    api_key = os.getenv('OPENAI_API_KEY')
    return {
        "message": "Research API is running", 
        "status": "healthy",
        "api_key_configured": bool(api_key)
    }

@app.get("/health")
async def health_check():
    api_key = os.getenv('OPENAI_API_KEY')
    return {
        "status": "healthy" if api_key else "missing_key",
        "api_key": "configured" if api_key else "missing",
        "message": "API is ready for research" if api_key else "API key not configured"
    }

@app.post("/research", response_model=ResearchResponse)
async def conduct_research(request: ResearchRequest):
    """Conduct standard research."""
    try:
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return ResearchResponse(
                success=False,
                topic=request.topic,
                error="OPENAI_API_KEY not found"
            )
        
        from app.agents.research_agent import ResearchAgent
        from app.chains.report_generator import ReportGenerator
        
        # Use standard mode
        research_agent = ResearchAgent(advanced_mode=False)
        report_generator = ReportGenerator()
        
        research_result = research_agent.research_topic(
            request.topic, 
            request.research_questions
        )
        
        if not research_result["success"]:
            return ResearchResponse(
                success=False,
                topic=request.topic,
                error=research_result["error"]
            )
        
        report = None
        if request.detailed_report:
            report = report_generator.generate_report(
                request.topic,
                research_result,
                request.research_questions
            )
        
        return ResearchResponse(
            success=True,
            topic=request.topic,
            research_output=research_result["research_output"],
            report=report,
            sources=research_result.get("sources_used", [])
        )
        
    except Exception as e:
        return ResearchResponse(
            success=False,
            topic=request.topic,
            error=str(e)
        )

@app.post("/advanced-research", response_model=ResearchResponse)
async def conduct_advanced_research(request: ResearchRequest):
    """Conduct advanced multi-step research."""
    try:
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return ResearchResponse(
                success=False,
                topic=request.topic,
                error="OPENAI_API_KEY not found"
            )
        
        from app.agents.research_agent import MultiStepResearchAgent
        from app.chains.report_generator import ReportGenerator
        
        multi_step_agent = MultiStepResearchAgent()
        report_generator = ReportGenerator()
        
        research_result = multi_step_agent.conduct_research(
            request.topic,
            request.research_questions
        )
        
        report = None
        if request.detailed_report:
            report = report_generator.generate_report(
                request.topic,
                research_result,
                request.research_questions
            )
        
        return ResearchResponse(
            success=True,
            topic=request.topic,
            research_output=research_result.get("research_output", ""),
            report=report,
            sources=research_result.get("sources_used", [])
        )
        
    except Exception as e:
        return ResearchResponse(
            success=False,
            topic=request.topic,
            error=str(e)
        )
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
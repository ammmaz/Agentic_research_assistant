from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('../../.env')

app = FastAPI(
    title="Research Assistant API",
    description="Working version with OpenAI integration",
    version="1.0.0"
)

# CORS middleware
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
    return {"message": "Research Assistant API is running!", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Backend server is working!"}

@app.post("/research", response_model=ResearchResponse)
async def conduct_research(request: ResearchRequest):
    """Conduct research using direct OpenAI API"""
    try:
        # Check if OpenAI API key is available
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if not openai_api_key:
            return ResearchResponse(
                success=False,
                topic=request.topic,
                error="OPENAI_API_KEY not found in .env file"
            )
        
        # Simple OpenAI integration without LangChain
        import openai
        
        research_prompt = f"""
        Research the following topic and answer the questions:
        
        Topic: {request.topic}
        
        Questions:
        {chr(10).join(f'- {q}' for q in request.research_questions)}
        
        Provide a comprehensive research summary with key findings.
        """
        
        client = openai.OpenAI(api_key=openai_api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a research assistant. Provide detailed, well-structured research findings."},
                {"role": "user", "content": research_prompt}
            ],
            max_tokens=1000
        )
        
        research_output = response.choices[0].message.content
        
        report = f"""
# Research Report: {request.topic}

## Executive Summary
{research_output}

## Research Questions
{chr(10).join(f'- {q}' for q in request.research_questions)}

## Methodology
Research conducted using AI-assisted analysis with OpenAI GPT-3.5-turbo.

## Key Findings
{research_output}

## Conclusion
This research provides comprehensive insights into the topic using AI-powered analysis.
"""
        
        return ResearchResponse(
            success=True,
            topic=request.topic,
            research_output=research_output,
            report=report if request.detailed_report else None,
            sources=["AI-generated research using OpenAI API"]
        )
        
    except ImportError:
        return ResearchResponse(
            success=False,
            topic=request.topic,
            error="OpenAI package not installed. Run: pip install openai"
        )
    except Exception as e:
        return ResearchResponse(
            success=False,
            topic=request.topic,
            error=f"Research failed: {str(e)}"
        )

@app.post("/advanced-research", response_model=ResearchResponse)
async def conduct_advanced_research(request: ResearchRequest):
    """Advanced research endpoint (mock version)"""
    return ResearchResponse(
        success=True,
        topic=request.topic,
        research_output=f"Advanced research completed for: {request.topic}\n\nQuestions addressed:\n{chr(10).join(f'- {q}' for q in request.research_questions)}",
        report=f"""# Advanced Research Report: {request.topic}

## Executive Summary
This is a demonstration of the advanced research functionality.

## Research Questions
{chr(10).join(f'- {q}' for q in request.research_questions)}

## Methodology
Advanced multi-step research analysis.

## Findings
- Research system is functioning correctly
- Backend API is properly connected
- Frontend can successfully make requests

## Next Steps
For full AI agent capabilities, ensure all LangChain dependencies are installed.
""",
        sources=["System demonstration", "Mock research data"]
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
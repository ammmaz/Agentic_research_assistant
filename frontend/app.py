import streamlit as st
import requests
import json
from typing import List
import time

# Page configuration
st.set_page_config(
    page_title="Agentic Research Assistant",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .research-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #1f77b4;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class ResearchAssistantFrontend:
    def __init__(self):
        self.api_url = "http://localhost:8000"  # Change in production
        
    def conduct_research(self, topic: str, questions: List[str], advanced: bool = False) -> dict:
        """Send research request to backend API."""
        endpoint = "/advanced-research" if advanced else "/research"
        
        payload = {
            "topic": topic,
            "research_questions": questions,
            "detailed_report": True
        }
        
        try:
            response = requests.post(f"{self.api_url}{endpoint}", json=payload)
            return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}

def main():
    st.markdown('<div class="main-header">🔍 Agentic Research Assistant</div>', unsafe_allow_html=True)
    
    # Initialize frontend
    frontend = ResearchAssistantFrontend()
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Research Configuration")
        
        research_mode = st.radio(
            "Research Mode",
            ["Standard", "Advanced"],
            help="Advanced mode uses multi-step research with deeper analysis"
        )
        
        st.markdown("---")
        st.markdown("### Example Research Topics")
        st.info("""
        - "Impact of AI on software development"
        - "Renewable energy trends in 2024"
        - "Quantum computing breakthroughs"
        - "Climate change mitigation strategies"
        """)
    
    # Main research interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Research Topic")
        topic = st.text_input(
            "Enter your research topic:",
            placeholder="e.g., Recent advancements in neural network architectures...",
            help="Be specific about what you want to research"
        )
    
    with col2:
        st.subheader("Research Questions")
        st.markdown("Add specific questions to guide the research:")
    
    # Dynamic research questions
    if 'research_questions' not in st.session_state:
        st.session_state.research_questions = [""]
    
    for i, question in enumerate(st.session_state.research_questions):
        col1, col2 = st.columns([5, 1])
        with col1:
            st.session_state.research_questions[i] = st.text_input(
                f"Question {i+1}",
                value=question,
                placeholder=f"What are the key aspects of...",
                key=f"question_{i}"
            )
        with col2:
            if i > 0:  # Don't remove the first question
                if st.button("❌", key=f"remove_{i}"):
                    st.session_state.research_questions.pop(i)
                    st.rerun()
    
    # Add new question button
    if st.button("➕ Add Another Question"):
        st.session_state.research_questions.append("")
        st.rerun()
    
    # Research execution
    if st.button("🚀 Conduct Research", type="primary", use_container_width=True):
        if not topic.strip():
            st.error("Please enter a research topic.")
            return
            
        # Filter out empty questions
        valid_questions = [q for q in st.session_state.research_questions if q.strip()]
        if not valid_questions:
            st.error("Please add at least one research question.")
            return
        
        with st.spinner("🤖 Research in progress... This may take a few minutes."):
            progress_bar = st.progress(0)
            
            for i in range(100):
                progress_bar.progress(i + 1)
                time.sleep(0.02)  # Simulate progress
            
            # Conduct research
            result = frontend.conduct_research(
                topic, 
                valid_questions, 
                advanced=(research_mode == "Advanced")
            )
        
        # Display results
        if result.get("success"):
            st.markdown('<div class="success-message">✅ Research completed successfully!</div>', unsafe_allow_html=True)
            
            # Create tabs for different sections
            tab1, tab2, tab3 = st.tabs(["Research Report", "Raw Findings", "Sources"])
            
            with tab1:
                if result.get("report"):
                    st.markdown("### 📊 Comprehensive Research Report")
                    st.markdown(result["report"])
                else:
                    st.info("No detailed report generated.")
            
            with tab2:
                if result.get("research_output"):
                    st.markdown("### 🔍 Raw Research Findings")
                    st.write(result["research_output"])
                else:
                    st.info("No research output available.")
            
            with tab3:
                if result.get("sources"):
                    st.markdown("### 📚 Research Sources")
                    for source in result["sources"]:
                        st.write(f"- {source}")
                else:
                    st.info("No sources extracted.")
        
        else:
            st.markdown(f'<div class="error-message">❌ Research failed: {result.get("error", "Unknown error")}</div>', unsafe_allow_html=True)

    # Example usage section
    with st.expander("💡 How to use this research assistant"):
        st.markdown("""
        **Best Practices:**
        
        1. **Be Specific**: Instead of "AI", research "Recent advancements in transformer architectures for natural language processing"
        2. **Ask Focused Questions**: 
           - "What are the current state-of-the-art models?"
           - "What are the main challenges in deployment?"
           - "What future developments are expected?"
        3. **Use Advanced Mode** for complex topics requiring deeper analysis
        
        **Capabilities:**
        - Web search for current information
        - Academic research via arXiv
        - Data analysis and calculations
        - Multi-step reasoning and synthesis
        - Comprehensive report generation
        """)

if __name__ == "__main__":
    main()
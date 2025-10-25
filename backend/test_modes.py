import os
import sys
from dotenv import load_dotenv
from pathlib import Path

# Add backend to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Load .env file
env_path = backend_dir.parent / '.env'
load_dotenv(env_path)

def test_research_modes():
    """Test both standard and advanced research modes."""
    
    api_key = os.getenv('OPENAI_API_KEY')
    print(f"🔑 API Key: {'✅ FOUND' if api_key else '❌ MISSING'}")
    
    if not api_key:
        print("Please set OPENAI_API_KEY in your .env file")
        return
    
    try:
        from app.agents.research_agent import ResearchAgent, MultiStepResearchAgent
        
        # Test topic and questions
        test_topic = "artificial intelligence in healthcare"
        test_questions = [
            "How is AI being used in medical diagnosis?",
            "What are the benefits of AI in healthcare?",
            "What are the main challenges and concerns?"
        ]
        
        print("=" * 60)
        print("🧪 TESTING RESEARCH AGENT MODES")
        print("=" * 60)
        
        # Test 1: Standard Mode
        print("\n1. 🧪 Testing STANDARD Mode...")
        print("-" * 40)
        standard_agent = ResearchAgent(advanced_mode=False)
        standard_result = standard_agent.research_topic(test_topic, test_questions)
        
        print(f"✅ Standard Mode Result: {standard_result['success']}")
        if standard_result['success']:
            print(f"   📝 Output length: {len(standard_result['research_output'])} characters")
            print(f"   📚 Sources found: {len(standard_result['sources_used'])}")
            print(f"   🎯 Mode: {standard_result.get('mode', 'standard')}")
            print(f"   📄 First 200 chars: {standard_result['research_output'][:200]}...")
        else:
            print(f"   ❌ Error: {standard_result['error']}")
        
        # Test 2: Advanced Mode
        print("\n2. 🚀 Testing ADVANCED Mode...")
        print("-" * 40)
        advanced_agent = ResearchAgent(advanced_mode=True)
        advanced_result = advanced_agent.research_topic(test_topic, test_questions)
        
        print(f"✅ Advanced Mode Result: {advanced_result['success']}")
        if advanced_result['success']:
            print(f"   📝 Output length: {len(advanced_result['research_output'])} characters")
            print(f"   📚 Sources found: {len(advanced_result['sources_used'])}")
            print(f"   🎯 Mode: {advanced_result.get('mode', 'advanced')}")
            print(f"   📄 First 200 chars: {advanced_result['research_output'][:200]}...")
        else:
            print(f"   ❌ Error: {advanced_result['error']}")
        
        # Test 3: Multi-Step Mode
        print("\n3. 🔬 Testing MULTI-STEP Mode...")
        print("-" * 40)
        multi_agent = MultiStepResearchAgent()
        multi_result = multi_agent.conduct_research(test_topic, test_questions)
        
        print(f"✅ Multi-Step Result: {multi_result['success']}")
        if multi_result['success']:
            print(f"   📝 Output length: {len(multi_result['research_output'])} characters")
            print(f"   📚 Sources found: {len(multi_result['sources_used'])}")
            print(f"   🎯 Mode: {multi_result.get('mode', 'multi-step')}")
            print(f"   📄 First 200 chars: {multi_result['research_output'][:200]}...")
        else:
            print(f"   ❌ Error: {multi_result['error']}")
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        tests = [
            ("Standard Mode", standard_result),
            ("Advanced Mode", advanced_result), 
            ("Multi-Step Mode", multi_result)
        ]
        
        for test_name, result in tests:
            status = "✅ PASS" if result['success'] else "❌ FAIL"
            print(f"{test_name}: {status}")
            
        print("\n🎉 Testing completed!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all required packages are installed and paths are correct")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def test_specific_topic(topic, questions):
    """Test a specific research topic."""
    print(f"\n🎯 Testing specific topic: {topic}")
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ API key not found")
        return
    
    try:
        from app.agents.research_agent import ResearchAgent
        
        # Test advanced mode for specific topic
        agent = ResearchAgent(advanced_mode=True)
        result = agent.research_topic(topic, questions)
        
        if result['success']:
            print(f"✅ Research successful!")
            print(f"📝 Output: {result['research_output']}")
            print(f"📚 Sources: {result['sources_used']}")
        else:
            print(f"❌ Research failed: {result['error']}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Run the main test
    test_research_modes()
    
    # Uncomment to test specific topics
    # print("\n" + "="*60)
    # print("🎯 ADDITIONAL TOPIC TESTS")
    # print("="*60)
    # 
    # # Test renewable energy
    # test_specific_topic(
    #     "renewable energy trends 2024",
    #     ["What are the latest solar power innovations?", "How is wind energy evolving?"]
    # )
    # 
    # # Test blockchain
    # test_specific_topic(
    #     "blockchain technology applications",
    #     ["What are real-world uses beyond cryptocurrency?", "How is blockchain used in supply chain?"]
    # )
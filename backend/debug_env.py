import os
from dotenv import load_dotenv
from pathlib import Path

print("🔍 Debugging .env file location...")

# Current directory
current_dir = Path(__file__).parent
print(f"Current directory: {current_dir}")

# Check multiple possible .env locations
possible_paths = [
    current_dir.parent / '.env',           # project root
    current_dir / '.env',                  # backend folder  
    current_dir / 'app' / '.env',          # app folder
]

for path in possible_paths:
    exists = path.exists()
    status = "✅ EXISTS" if exists else "❌ MISSING"
    print(f"{path} - {status}")
    
    if exists:
        # Try to load from this path
        load_dotenv(path)
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            print(f"   🎯 API KEY FOUND: {api_key[:10]}...")
        else:
            print(f"   ❌ No API key in this .env file")
            # Show what's actually in the file
            try:
                with open(path, 'r') as f:
                    content = f.read()
                    print(f"   File content: {content}")
            except Exception as e:
                print(f"   Could not read file: {e}")

# Also check environment variable directly
env_var = os.getenv('OPENAI_API_KEY')
print(f"\nEnvironment variable OPENAI_API_KEY: {'✅ SET' if env_var else '❌ NOT SET'}")
if env_var:
    print(f"Value: {env_var[:10]}...")
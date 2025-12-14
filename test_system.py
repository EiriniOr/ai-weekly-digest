#!/usr/bin/env python3
"""
System Test - Verify all components are working
"""

import sys
import os
from pathlib import Path

def test_dependencies():
    """Test that all required packages are installed"""
    print("Testing dependencies...")

    required = {
        'yaml': 'pyyaml',
        'feedparser': 'feedparser',
        'requests': 'requests',
        'anthropic': 'anthropic',
        'pptx': 'python-pptx',
    }

    missing = []
    for module, package in required.items():
        try:
            __import__(module)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} (missing)")
            missing.append(package)

    if missing:
        print(f"\nInstall missing packages:")
        print(f"  pip3 install {' '.join(missing)}")
        return False

    return True

def test_config():
    """Test that config file is valid"""
    print("\nTesting configuration...")

    import yaml
    config_file = Path(__file__).parent / "config.yaml"

    try:
        with open(config_file) as f:
            config = yaml.safe_load(f)

        print(f"  ✅ config.yaml exists and is valid")

        # Check required sections
        required_sections = ['sources', 'curation', 'presentation', 'schedule']
        for section in required_sections:
            if section in config:
                print(f"  ✅ {section} section present")
            else:
                print(f"  ❌ {section} section missing")
                return False

        return True
    except Exception as e:
        print(f"  ❌ Error reading config: {e}")
        return False

def test_api_key():
    """Test that Anthropic API key is set"""
    print("\nTesting API key...")

    api_key = os.environ.get('ANTHROPIC_API_KEY')

    if not api_key:
        print(f"  ❌ ANTHROPIC_API_KEY not set")
        print(f"     Set it with: export ANTHROPIC_API_KEY='your-key'")
        return False

    if api_key == "YOUR_API_KEY_HERE":
        print(f"  ❌ ANTHROPIC_API_KEY is still placeholder")
        print(f"     Replace with your actual key")
        return False

    print(f"  ✅ API key is set ({api_key[:8]}...)")
    return True

def test_mcp_server():
    """Test that PowerPoint MCP server is accessible"""
    print("\nTesting PowerPoint MCP Server...")

    mcp_path = Path("/Users/rena/mcp-powerpoint-server")

    if not mcp_path.exists():
        print(f"  ❌ MCP server not found at {mcp_path}")
        return False

    print(f"  ✅ MCP server directory exists")

    wrapper_file = mcp_path / "chatgpt_wrapper.py"
    if wrapper_file.exists():
        print(f"  ✅ chatgpt_wrapper.py found")
    else:
        print(f"  ❌ chatgpt_wrapper.py not found")
        return False

    # Try importing
    sys.path.insert(0, str(mcp_path))
    try:
        from chatgpt_wrapper import PowerPointAPI
        print(f"  ✅ PowerPointAPI can be imported")
        return True
    except Exception as e:
        print(f"  ❌ Error importing PowerPointAPI: {e}")
        return False

def test_directories():
    """Test that required directories exist"""
    print("\nTesting directories...")

    base_dir = Path(__file__).parent
    required_dirs = ['scripts', 'data', 'logs']

    for dir_name in required_dirs:
        dir_path = base_dir / dir_name
        if dir_path.exists():
            print(f"  ✅ {dir_name}/ exists")
        else:
            print(f"  ⚠️  {dir_name}/ missing (will be created)")
            dir_path.mkdir(exist_ok=True)

    return True

def test_scripts():
    """Test that all scripts exist and are executable"""
    print("\nTesting scripts...")

    base_dir = Path(__file__).parent
    scripts = [
        'generate_weekly_digest.py',
        'scripts/collect_news.py',
        'scripts/curate_content.py',
        'scripts/generate_presentation.py',
    ]

    all_ok = True
    for script in scripts:
        script_path = base_dir / script
        if script_path.exists():
            print(f"  ✅ {script}")
        else:
            print(f"  ❌ {script} missing")
            all_ok = False

    return all_ok

def test_internet():
    """Test internet connectivity"""
    print("\nTesting internet connectivity...")

    import requests

    try:
        response = requests.get('https://www.google.com', timeout=5)
        print(f"  ✅ Internet connection works")
        return True
    except Exception as e:
        print(f"  ❌ No internet connection: {e}")
        return False

def main():
    print("=" * 60)
    print("  AI WEEKLY DIGEST - SYSTEM TEST")
    print("=" * 60)
    print()

    tests = [
        ("Dependencies", test_dependencies),
        ("Configuration", test_config),
        ("API Key", test_api_key),
        ("MCP Server", test_mcp_server),
        ("Directories", test_directories),
        ("Scripts", test_scripts),
        ("Internet", test_internet),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"  ❌ Unexpected error: {e}")
            results.append((name, False))
        print()

    # Summary
    print("=" * 60)
    print("  TEST SUMMARY")
    print("=" * 60)
    print()

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}  {name}")

    print()
    print(f"  {passed}/{total} tests passed")
    print()

    if passed == total:
        print("  🎉 All tests passed! Your system is ready to use.")
        print()
        print("  Next steps:")
        print("    1. Run: python3 generate_weekly_digest.py")
        print("    2. Check: ~/Downloads/AI_Weekly_*.pptx")
        print("    3. Enable automation (see README.md)")
        print()
        return 0
    else:
        print("  ⚠️  Some tests failed. Please fix the issues above.")
        print()
        print("  Common fixes:")
        print("    • Install dependencies: pip3 install -r requirements.txt")
        print("    • Set API key: export ANTHROPIC_API_KEY='your-key'")
        print("    • Run setup: ./setup.sh")
        print()
        return 1

if __name__ == "__main__":
    sys.exit(main())

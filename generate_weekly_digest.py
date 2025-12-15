#!/usr/bin/env python3
"""
Weekly AI Digest Generator
Main orchestrator script that collects, curates, and generates the presentation
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

from collect_news import AINewsCollector
from curate_content import ContentCurator
from generate_webpage import WebpageGenerator
from deploy_github import deploy_to_github

async def generate_weekly_digest():
    """Run the complete weekly digest pipeline"""
    print("=" * 60)
    print("  🤖 AI WEEKLY DIGEST GENERATOR")
    print("=" * 60)
    print(f"  Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()

    try:
        # Step 1: Collect news
        print("STEP 1/5: Collecting AI news from multiple sources")
        print("-" * 60)
        collector = AINewsCollector()
        news_data = await collector.collect_all()
        print()

        # Step 2: Curate content
        print("STEP 2/5: Curating and filtering content with Claude")
        print("-" * 60)
        curator = ContentCurator()
        curated_data = await curator.curate()
        print()

        # Step 3: Generate webpage
        print("STEP 3/4: Generating beautiful webpage")
        print("-" * 60)
        generator = WebpageGenerator()
        filepath = await generator.generate()
        print()

        # Step 4: Deploy to GitHub Pages
        print("STEP 4/4: Deploying to GitHub Pages")
        print("-" * 60)
        github_deployed = await deploy_to_github(filepath)
        print()

        # Success summary
        print("=" * 60)
        print("  ✅ SUCCESS!")
        print("=" * 60)
        print(f"\n  Your weekly AI digest webpage is ready:")
        print(f"  📄 {filepath}")
        if github_deployed:
            print(f"  🌐 Live at: https://EiriniOr.github.io/ai-weekly-digest/")
        print(f"\n  View your futuristic AI digest online!")
        print()

        return filepath

    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("   Make sure to run the steps in order.")
        return None

    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return None

async def main():
    filepath = await generate_weekly_digest()

    if filepath:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())

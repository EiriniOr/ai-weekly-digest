#!/usr/bin/env python3
"""
Prepare video for manual YouTube upload
Since Google API libraries can't be installed locally, this script prepares
everything you need to manually upload the video to YouTube.
"""

from pathlib import Path
from datetime import datetime
import json

def prepare_upload():
    """Prepare video and metadata for manual upload"""
    print("📋 Preparing video for manual YouTube upload...\n")

    base_dir = Path(__file__).parent.parent
    video_dir = base_dir / "videos"

    # Find latest video
    video_files = sorted(video_dir.glob("ai_weekly_*.mp4"), reverse=True)

    if not video_files:
        print("❌ No video files found!")
        print(f"   Looking in: {video_dir}")
        return

    video_path = video_files[0]
    date_str = datetime.now().strftime('%Y-%m-%d')

    # Create metadata
    metadata = {
        "title": f"AI Weekly Digest - {datetime.now().strftime('%B %d, %Y')}",
        "description": f"""Your weekly curated AI news focusing on agentic AI, autonomous agents, and multi-agent systems.

📚 Topics covered this week:
• Research breakthroughs in agentic AI
• Industry updates and product launches
• New tools and frameworks
• Notable discussions from the AI community

🔗 Full digest: https://EiriniOr.github.io/ai-weekly-digest/

Created by Eirini Ornithopoulou
GitHub: https://github.com/EiriniOr/ai-weekly-digest

#AI #MachineLearning #AgenticAI #Agents #LLM #ArtificialIntelligence""",
        "tags": [
            "AI", "Machine Learning", "Agentic AI", "LLM",
            "Autonomous Agents", "Multi-Agent Systems",
            "OpenAI", "Claude", "Anthropic", "GPT",
            "AI News", "Tech News", "AI Research"
        ],
        "category": "28",  # Science & Technology
        "privacy": "public"
    }

    # Save metadata
    metadata_path = video_dir / f"upload_instructions_{date_str}.txt"

    instructions = f"""
═══════════════════════════════════════════════════════════
  MANUAL YOUTUBE UPLOAD INSTRUCTIONS
═══════════════════════════════════════════════════════════

Video File: {video_path.name}
Location: {video_path}

Channel: https://www.youtube.com/channel/UCUPSLoXvaMVbOIaXsOorHng

─────────────────────────────────────────────────────────────
UPLOAD STEPS:
─────────────────────────────────────────────────────────────

1. Go to: https://studio.youtube.com/
2. Click "CREATE" → "Upload videos"
3. Select file: {video_path}

4. Fill in details:

   TITLE:
   {metadata['title']}

   DESCRIPTION:
   {metadata['description']}

   TAGS (comma-separated):
   {', '.join(metadata['tags'])}

5. Select:
   - Category: Science & Technology
   - Visibility: Public
   - Made for kids: No

6. Click "PUBLISH"

─────────────────────────────────────────────────────────────
METADATA (for reference):
─────────────────────────────────────────────────────────────

{json.dumps(metadata, indent=2)}

═══════════════════════════════════════════════════════════
"""

    with open(metadata_path, 'w') as f:
        f.write(instructions)

    print(f"✅ Video ready for upload!")
    print(f"📁 Video: {video_path}")
    print(f"📄 Instructions: {metadata_path}")
    print(f"\n📺 Upload to: https://studio.youtube.com/\n")
    print("─" * 60)
    print(f"\n📋 Quick Copy - TITLE:\n{metadata['title']}\n")
    print("─" * 60)
    print(f"\n📋 Quick Copy - DESCRIPTION:\n{metadata['description']}\n")
    print("─" * 60)
    print(f"\n📋 Quick Copy - TAGS:\n{', '.join(metadata['tags'])}\n")
    print("═" * 60)

if __name__ == "__main__":
    prepare_upload()

#!/usr/bin/env python3
"""
YouTube Uploader
Uploads videos to YouTube channel
"""

import asyncio
from pathlib import Path
from datetime import datetime
import json

class YouTubeUploader:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.video_dir = self.base_dir / "videos"
        self.channel_id = "UCUPSLoXvaMVbOIaXsOorHng"  # Your channel

    def get_latest_video(self):
        """Find most recent video file"""
        video_files = sorted(self.video_dir.glob("ai_weekly_*.mp4"), reverse=True)

        if not video_files:
            return None

        return video_files[0]

    async def upload(self, video_path):
        """Upload video to YouTube"""
        print(f"📤 Uploading to YouTube...")

        try:
            # For now, save video metadata for manual upload
            # Full YouTube API integration can be added later
            date_str = datetime.now().strftime('%Y-%m-%d')

            metadata = {
                "title": f"AI Weekly Digest - {datetime.now().strftime('%B %d, %Y')}",
                "description": f"""Your weekly curated AI news focusing on agentic AI, autonomous agents, and multi-agent systems.

📚 Topics covered this week:
• Research breakthroughs
• Industry updates
• New tools & frameworks

🔗 Full digest: https://EiriniOr.github.io/ai-weekly-digest/

#AI #MachineLearning #AgenticAI #TechNews #ArtificialIntelligence""",
                "tags": [
                    "AI", "Machine Learning", "Agentic AI", "Autonomous Agents",
                    "Multi-Agent Systems", "Tech News", "Research", "Tools"
                ],
                "category": "28",  # Science & Technology
                "privacy": "public"
            }

            # Save metadata for reference
            metadata_path = video_path.parent / f"metadata_{date_str}.json"
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)

            print(f"  ✓ Video ready for upload: {video_path}")
            print(f"  ✓ Metadata saved: {metadata_path}")
            print(f"\n  📺 Channel: https://www.youtube.com/channel/{self.channel_id}")
            print(f"  ℹ️  YouTube API integration pending")
            print(f"     For now, manually upload {video_path.name}")

            return False  # No actual upload yet

        except Exception as e:
            print(f"  ❌ Upload preparation failed: {e}")
            return False

    async def upload_latest(self):
        """Upload most recent video"""
        video_path = self.get_latest_video()

        if not video_path:
            print("❌ No video found to upload")
            return False

        return await self.upload(video_path)

async def main():
    uploader = YouTubeUploader()
    success = await uploader.upload_latest()

    if success:
        print("\n✅ Upload complete!")
    else:
        print("\n⚠️  Video ready - manual upload required")

if __name__ == "__main__":
    asyncio.run(main())

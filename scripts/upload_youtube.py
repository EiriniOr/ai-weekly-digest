#!/usr/bin/env python3
"""
YouTube Uploader
Uploads videos to YouTube channel using YouTube Data API v3
"""

import asyncio
from pathlib import Path
from datetime import datetime
import json
import os
import base64

class YouTubeUploader:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.video_dir = self.base_dir / "videos"
        self.credentials_dir = self.base_dir / ".credentials"
        self.credentials_dir.mkdir(exist_ok=True)
        self.channel_id = "UCUPSLoXvaMVbOIaXsOorHng"

    def get_latest_video(self):
        """Find most recent video file"""
        video_files = sorted(self.video_dir.glob("ai_weekly_*.mp4"), reverse=True)

        if not video_files:
            return None

        return video_files[0]

    def _get_credentials(self):
        """Load OAuth2 credentials from environment or file"""
        try:
            # Try to get credentials from environment variable (GitHub Actions)
            creds_base64 = os.environ.get("YOUTUBE_CREDENTIALS_BASE64")
            if creds_base64:
                creds_json = base64.b64decode(creds_base64).decode('utf-8')
                return json.loads(creds_json)

            # Fallback to file (local development)
            creds_file = self.credentials_dir / "youtube_credentials.json"
            if creds_file.exists():
                with open(creds_file) as f:
                    return json.load(f)

            return None
        except Exception as e:
            print(f"  ⚠️  Error loading credentials: {e}")
            return None

    def _get_authenticated_service(self):
        """Get authenticated YouTube service"""
        try:
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            from google.auth.transport.requests import Request
            from googleapiclient.discovery import build

            SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

            creds = None
            token_file = self.credentials_dir / "youtube_token.json"

            # Load existing token
            if token_file.exists():
                creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)

            # Refresh or get new token
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    # Get client secrets from environment or file
                    client_secrets = self._get_credentials()
                    if not client_secrets:
                        print("  ⚠️  No OAuth2 credentials found")
                        return None

                    # Save client secrets temporarily for flow
                    temp_secrets = self.credentials_dir / "client_secrets_temp.json"
                    with open(temp_secrets, 'w') as f:
                        json.dump(client_secrets, f)

                    flow = InstalledAppFlow.from_client_secrets_file(
                        str(temp_secrets), SCOPES
                    )
                    creds = flow.run_local_server(port=0)

                    # Clean up temp file
                    temp_secrets.unlink()

                # Save token for future use
                with open(token_file, 'w') as f:
                    f.write(creds.to_json())

            return build('youtube', 'v3', credentials=creds)

        except ImportError:
            print("  ⚠️  Google API libraries not installed")
            print("     Run: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
            return None
        except Exception as e:
            print(f"  ⚠️  Authentication failed: {e}")
            return None

    async def upload(self, video_path):
        """Upload video to YouTube"""
        print(f"📤 Uploading to YouTube...")

        try:
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

            print(f"  ✓ Metadata saved: {metadata_path}")

            # Try YouTube API upload
            youtube = self._get_authenticated_service()

            if not youtube:
                print(f"  ⚠️  YouTube API not available - skipping upload")
                print(f"  📺 Channel: https://www.youtube.com/channel/{self.channel_id}")
                print(f"  ℹ️  To enable automatic uploads, set up OAuth2 credentials")
                return False

            # Upload video
            from googleapiclient.http import MediaFileUpload

            body = {
                'snippet': {
                    'title': metadata['title'],
                    'description': metadata['description'],
                    'tags': metadata['tags'],
                    'categoryId': metadata['category']
                },
                'status': {
                    'privacyStatus': metadata['privacy']
                }
            }

            print(f"  🎬 Uploading video: {video_path.name}")

            media = MediaFileUpload(
                str(video_path),
                chunksize=-1,
                resumable=True,
                mimetype='video/mp4'
            )

            request = youtube.videos().insert(
                part='snippet,status',
                body=body,
                media_body=media
            )

            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    progress = int(status.progress() * 100)
                    print(f"  📊 Upload progress: {progress}%")

            video_id = response['id']
            video_url = f"https://www.youtube.com/watch?v={video_id}"

            print(f"  ✅ Upload successful!")
            print(f"  🎥 Video ID: {video_id}")
            print(f"  🔗 URL: {video_url}")
            print(f"  📺 Channel: https://www.youtube.com/channel/{self.channel_id}")

            # Save video URL to metadata
            metadata['video_id'] = video_id
            metadata['video_url'] = video_url
            metadata['uploaded_at'] = datetime.now().isoformat()

            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)

            return True

        except Exception as e:
            print(f"  ❌ Upload failed: {e}")
            import traceback
            traceback.print_exc()
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

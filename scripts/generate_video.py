#!/usr/bin/env python3
"""
Video Generator
Creates YouTube videos from curated AI news with AI voice narration
"""

import asyncio
import json
import yaml
from datetime import datetime
from pathlib import Path
import anthropic
import os

class VideoGenerator:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        config_file = self.base_dir / "config.yaml"

        with open(config_file) as f:
            self.config = yaml.safe_load(f)

        self.data_dir = self.base_dir / "data"
        self.output_dir = self.base_dir / "output"
        self.video_dir = self.base_dir / "videos"
        self.video_dir.mkdir(exist_ok=True)

        self.claude_client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    def get_latest_curated_data(self):
        """Load most recent curated content"""
        data_files = sorted(self.data_dir.glob("curated_*.json"), reverse=True)

        if not data_files:
            raise FileNotFoundError("No curated data found")

        with open(data_files[0]) as f:
            return json.load(f)

    async def generate_script(self, curated_data):
        """Generate narration script using Claude"""
        print("📝 Generating video script with Claude...")

        prompt = f"""Create a natural, conversational 2-minute video script for a YouTube video about this week's AI news.

Style:
- Female narrator perspective
- Friendly, engaging tone (not too formal)
- Short, clear sentences that are easy to narrate
- Natural transitions between sections
- Time: approximately 2 minutes total

Content to cover:
Weekly Summary: {curated_data.get('weekly_summary', '')}

Research Papers ({len(curated_data['sections'].get('Key Research Papers', []))} items):
{json.dumps(curated_data['sections'].get('Key Research Papers', []), indent=2)}

Industry Updates ({len(curated_data['sections'].get('Industry Updates', []))} items):
{json.dumps(curated_data['sections'].get('Industry Updates', []), indent=2)}

Tools & Frameworks ({len(curated_data['sections'].get('Tools & Frameworks', []))} items):
{json.dumps(curated_data['sections'].get('Tools & Frameworks', []), indent=2)}

Output as JSON with sections for timing:
{{
  "intro": "Hook and welcome (5-10 seconds)",
  "summary": "Weekly overview (15-20 seconds)",
  "research": "Research highlights - mention top 2-3 papers (30-40 seconds)",
  "industry": "Industry news - mention top 2-3 updates (30-40 seconds)",
  "tools": "New tools - mention top 2-3 (20-30 seconds)",
  "outro": "Call to action and sign-off (10 seconds)"
}}

Keep each section concise and engaging. Focus on WHY each item matters, not just WHAT it is."""

        message = self.claude_client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        # Extract JSON from response
        response_text = message.content[0].text

        # Try to find JSON in the response
        try:
            # Look for JSON block
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()
            elif "```" in response_text:
                json_start = response_text.find("```") + 3
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()

            script = json.loads(response_text)
        except json.JSONDecodeError:
            # Fallback to simple script
            script = {
                "intro": f"Welcome to AI Weekly Digest for {datetime.now().strftime('%B %d, %Y')}.",
                "summary": curated_data.get('weekly_summary', ''),
                "research": f"This week we saw {len(curated_data['sections'].get('Key Research Papers', []))} major research papers in agentic AI.",
                "industry": f"In industry news, {len(curated_data['sections'].get('Industry Updates', []))} important updates.",
                "tools": f"And {len(curated_data['sections'].get('Tools & Frameworks', []))} new tools were released.",
                "outro": "Subscribe for weekly AI updates. See you next week!"
            }

        # Save script
        date_str = datetime.now().strftime('%Y%m%d')
        script_path = self.video_dir / f"script_{date_str}.json"
        with open(script_path, 'w') as f:
            json.dump(script, f, indent=2)

        print(f"  ✓ Script saved: {script_path}")
        return script

    async def generate_audio(self, script):
        """Generate audio narration using OpenAI TTS"""
        print("🎙️  Generating audio narration with OpenAI TTS...")

        try:
            from openai import OpenAI
            openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

            # Combine all script sections
            full_script = "\n\n".join([
                script.get('intro', ''),
                script.get('summary', ''),
                script.get('research', ''),
                script.get('industry', ''),
                script.get('tools', ''),
                script.get('outro', '')
            ])

            # Generate audio
            response = openai_client.audio.speech.create(
                model="tts-1-hd",
                voice="nova",  # Female voice
                input=full_script
            )

            # Save audio file
            date_str = datetime.now().strftime('%Y%m%d')
            audio_path = self.video_dir / f"narration_{date_str}.mp3"
            response.stream_to_file(str(audio_path))

            print(f"  ✓ Audio saved: {audio_path}")
            return audio_path

        except ImportError:
            print("  ⚠️  OpenAI package not installed - audio generation skipped")
            print("     (Will work in GitHub Actions)")
            return None
        except Exception as e:
            print(f"  ⚠️  Audio generation failed: {e}")
            return None

    async def create_video(self, script, audio_path, curated_data):
        """Generate video with moviepy"""
        print("🎬 Creating video...")

        try:
            from moviepy.editor import (
                ColorClip, TextClip, CompositeVideoClip,
                AudioFileClip, concatenate_videoclips
            )

            if not audio_path or not audio_path.exists():
                print("  ⚠️  No audio file - video creation skipped")
                return None

            # Load audio to get duration
            audio = AudioFileClip(str(audio_path))
            total_duration = audio.duration

            # Create gradient background
            background = ColorClip(
                size=(1920, 1080),
                color=(15, 12, 41),  # Your purple color
                duration=total_duration
            )

            clips = [background]

            # Intro (0-5 seconds)
            intro_text = TextClip(
                "🤖 AI Weekly Digest",
                fontsize=80,
                color='white',
                font='Arial-Bold',
                size=(1800, None),
                method='caption'
            ).set_duration(5).set_position('center').set_start(0)
            clips.append(intro_text)

            date_text = TextClip(
                datetime.now().strftime('%B %d, %Y'),
                fontsize=40,
                color='lightgray',
                font='Arial',
                size=(1800, None),
                method='caption'
            ).set_duration(5).set_position(('center', 700)).set_start(0)
            clips.append(date_text)

            # Summary section (5-20 seconds)
            summary_text = TextClip(
                "This Week's Highlights",
                fontsize=50,
                color='white',
                font='Arial-Bold',
                size=(1600, None),
                method='caption'
            ).set_duration(15).set_position(('center', 400)).set_start(5)
            clips.append(summary_text)

            # Research section indicator (20-25 seconds)
            research_header = TextClip(
                "🔬 Key Research Papers",
                fontsize=50,
                color='#9B59B6',
                font='Arial-Bold',
                size=(1600, None),
                method='caption'
            ).set_duration(5).set_position('center').set_start(20)
            clips.append(research_header)

            # Industry section indicator (50-55 seconds)
            industry_header = TextClip(
                "🏢 Industry Updates",
                fontsize=50,
                color='#3498DB',
                font='Arial-Bold',
                size=(1600, None),
                method='caption'
            ).set_duration(5).set_position('center').set_start(50)
            clips.append(industry_header)

            # Tools section indicator (90-95 seconds)
            tools_header = TextClip(
                "🛠️ Tools & Frameworks",
                fontsize=50,
                color='#1ABC9C',
                font='Arial-Bold',
                size=(1600, None),
                method='caption'
            ).set_duration(5).set_position('center').set_start(90)
            clips.append(tools_header)

            # Outro (last 5 seconds)
            outro_time = max(0, total_duration - 5)
            outro_text = TextClip(
                "Subscribe for Weekly AI Updates!",
                fontsize=60,
                color='white',
                font='Arial-Bold',
                size=(1600, None),
                method='caption'
            ).set_duration(5).set_position('center').set_start(outro_time)
            clips.append(outro_text)

            # Composite video
            video = CompositeVideoClip(clips)
            video = video.set_audio(audio)

            # Export
            date_str = datetime.now().strftime('%Y%m%d')
            output_path = self.video_dir / f"ai_weekly_{date_str}.mp4"

            video.write_videofile(
                str(output_path),
                fps=24,
                codec='libx264',
                audio_codec='aac',
                threads=4,
                preset='medium'
            )

            print(f"  ✓ Video created: {output_path}")
            return output_path

        except ImportError:
            print("  ⚠️  moviepy not installed - video creation skipped")
            print("     (Will work in GitHub Actions)")
            return None
        except Exception as e:
            print(f"  ⚠️  Video creation failed: {e}")
            return None

    async def generate(self):
        """Main video generation workflow"""
        print("🎥 Starting video generation...\n")

        try:
            # Load curated data
            curated_data = self.get_latest_curated_data()

            # Generate script
            script = await self.generate_script(curated_data)

            # Generate audio
            audio_path = await self.generate_audio(script)

            # Create video
            video_path = await self.create_video(script, audio_path, curated_data)

            if video_path:
                print(f"\n✅ Video generation complete: {video_path}")
            else:
                print("\n⚠️  Video generation skipped (packages not installed locally)")
                print("   Will work automatically in GitHub Actions")

            return video_path

        except Exception as e:
            print(f"\n❌ Video generation failed: {e}")
            return None

async def main():
    generator = VideoGenerator()
    video_path = await generator.generate()

    if video_path:
        print(f"\n🎉 Video ready: {video_path}")

if __name__ == "__main__":
    asyncio.run(main())

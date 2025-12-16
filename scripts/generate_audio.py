#!/usr/bin/env python3
"""
Audio Generator
Creates AI-narrated audio from curated AI news
"""

import asyncio
import json
import yaml
from datetime import datetime
from pathlib import Path
import anthropic
import os

class AudioGenerator:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        config_file = self.base_dir / "config.yaml"

        with open(config_file) as f:
            self.config = yaml.safe_load(f)

        self.data_dir = self.base_dir / "data"
        self.output_dir = self.base_dir / "output"
        self.audio_dir = self.base_dir / "audio"
        self.audio_dir.mkdir(exist_ok=True)

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
        print("📝 Generating narration script with Claude...")

        prompt = f"""Create a natural, conversational 2-minute audio script about this week's AI news.

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
                "outro": "Check out the full digest at the link below. See you next week!"
            }

        # Save script
        date_str = datetime.now().strftime('%Y%m%d')
        script_path = self.audio_dir / f"script_{date_str}.json"
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
            audio_path = self.audio_dir / f"narration_{date_str}.mp3"
            response.stream_to_file(str(audio_path))

            print(f"  ✓ Audio saved: {audio_path}")
            return audio_path

        except ImportError:
            print("  ⚠️  OpenAI package not installed - audio generation skipped")
            return None
        except Exception as e:
            print(f"  ⚠️  Audio generation failed: {e}")
            return None

    async def generate(self):
        """Main audio generation workflow"""
        print("🎙️  Starting audio generation...\n")

        try:
            # Load curated data
            curated_data = self.get_latest_curated_data()

            # Generate script
            script = await self.generate_script(curated_data)

            # Generate audio
            audio_path = await self.generate_audio(script)

            if audio_path:
                print(f"\n✅ Audio generation complete: {audio_path}")
            else:
                print("\n⚠️  Audio generation skipped")

            return audio_path

        except Exception as e:
            print(f"\n❌ Audio generation failed: {e}")
            return None

async def main():
    generator = AudioGenerator()
    audio_path = await generator.generate()

    if audio_path:
        print(f"\n🎉 Audio ready: {audio_path}")

if __name__ == "__main__":
    asyncio.run(main())

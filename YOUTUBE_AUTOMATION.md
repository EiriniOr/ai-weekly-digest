# 🎥 YouTube Automation - AI Weekly Digest Video Generator

## 🎯 Goal

Automatically create and upload weekly YouTube videos with:
- ✅ Female AI voice narration
- ✅ Animated visuals (text overlays, transitions)
- ✅ Based on your curated content
- ✅ Auto-upload to YouTube
- ✅ Fully automated (no manual work)

---

## 🏗️ Technical Architecture

### New Pipeline Step:

```
Current Flow:
Step 1: Collect → Step 2: Curate → Step 3: Webpage → Step 4: Deploy

New Flow:
Step 1: Collect → Step 2: Curate → Step 3: Webpage → Step 4: Deploy
                                   ↓
                            Step 5: Generate Video
                                   ↓
                            Step 6: Upload to YouTube
```

---

## 🎙️ AI Voice Options

### Option 1: OpenAI TTS (Recommended)

**Why it's best:**
- ✅ Natural-sounding female voices
- ✅ Good pricing ($15/1M characters)
- ✅ Simple API
- ✅ Multiple voice options

**Voices available:**
- `alloy` - Neutral, balanced
- `nova` - Warm, friendly (female)
- `shimmer` - Soft, gentle (female)

**Code example:**
```python
from openai import OpenAI
client = OpenAI()

speech = client.audio.speech.create(
    model="tts-1-hd",  # High quality
    voice="nova",      # Female voice
    input="This week in agentic AI..."
)

speech.stream_to_file("narration.mp3")
```

**Cost estimate:**
- ~2,000 characters per digest
- $0.03 per video (practically free)

### Option 2: ElevenLabs (Premium Quality)

**Why it's great:**
- ✅ Most realistic AI voices
- ✅ Custom voice cloning
- ✅ Emotional control
- ❌ More expensive

**Code example:**
```python
from elevenlabs import generate, save

audio = generate(
    text="This week in agentic AI...",
    voice="Bella",  # Female voice
    model="eleven_multilingual_v2"
)

save(audio, "narration.mp3")
```

**Cost estimate:**
- $5/month for 30,000 characters
- ~$0.30 per video

### Option 3: Google Cloud TTS (Budget)

**Why consider it:**
- ✅ Cheaper than ElevenLabs
- ✅ Good quality
- ❌ Less natural than OpenAI/ElevenLabs

**Code example:**
```python
from google.cloud import texttospeech

client = texttospeech.TextToSpeechClient()

synthesis_input = texttospeech.SynthesisInput(text="...")
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US",
    name="en-US-Neural2-F"  # Female voice
)

audio = client.synthesize_speech(
    input=synthesis_input,
    voice=voice,
    audio_config=audio_config
)
```

**Recommendation**: Start with OpenAI TTS (best balance of quality/price/simplicity)

---

## 🎬 Video Generation Options

### Option 1: moviepy (Python Library) - Recommended

**Why it's best:**
- ✅ Pure Python (integrates with your code)
- ✅ Free, open source
- ✅ Powerful editing capabilities
- ✅ No external dependencies (besides ffmpeg)

**What you can do:**
- Text animations
- Image overlays
- Transitions
- Audio sync
- Background music

**Installation:**
```bash
pip install moviepy
brew install ffmpeg  # macOS
```

**Example code:**
```python
from moviepy.editor import *

# Create text clips
intro = TextClip("AI Weekly Digest", fontsize=70, color='white')
intro = intro.set_duration(3).set_position('center')

summary = TextClip("This week: Multi-agent breakthroughs",
                   fontsize=40, color='white')
summary = summary.set_duration(5).set_position('center')

# Combine with background
background = ColorClip((1920, 1080), color=(15, 12, 41))  # Your purple gradient
background = background.set_duration(10)

# Add audio
audio = AudioFileClip("narration.mp3")

# Composite everything
video = CompositeVideoClip([background, intro, summary])
video = video.set_audio(audio)

# Export
video.write_videofile("weekly_digest.mp4", fps=24)
```

### Option 2: Remotion (React-based)

**Why consider it:**
- ✅ Beautiful animations (React/CSS)
- ✅ Template-based
- ❌ Requires Node.js setup
- ❌ More complex

**When to use:**
- If you want TV-quality animations
- If you're comfortable with React

### Option 3: Manim (Math animations)

**Why skip it:**
- ❌ Designed for math videos
- ❌ Overkill for your use case

**Recommendation**: Use moviepy (simple, powerful, integrates well)

---

## 📹 Video Structure

### Format:

```
┌─────────────────────────────────────────────────────────┐
│  Section 1: Intro (5 seconds)                           │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  Visual: Animated title + date                          │
│  Audio: "Welcome to AI Weekly Digest for December 15"   │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  Section 2: Summary (15 seconds)                        │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  Visual: Gradient background + text overlay             │
│  Audio: Claude's weekly_summary                         │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  Section 3: Key Research Papers (30 seconds)            │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  Visual: Title + insight for each paper                 │
│  Audio: "First, a breakthrough in multi-agent..."       │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  Section 4: Industry Updates (30 seconds)               │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  Visual: Company logos + headlines                      │
│  Audio: "In industry news, OpenAI announced..."         │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  Section 5: Tools & Frameworks (30 seconds)             │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  Visual: Tool names + descriptions                      │
│  Audio: "New tools released this week include..."       │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  Section 6: Outro (10 seconds)                          │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  Visual: Subscribe prompt + links                       │
│  Audio: "Subscribe for weekly AI updates..."            │
└─────────────────────────────────────────────────────────┘

Total: ~2 minutes (perfect for YouTube Shorts!)
```

---

## 🤖 Script Generation

### Use Claude to Create Video Script:

```python
# New module: scripts/generate_video_script.py

async def generate_script(curated_data):
    """Generate narration script optimized for video"""

    prompt = f"""Create a 2-minute video script for a YouTube video about this week's AI news.

Requirements:
- Conversational, friendly tone
- Female narrator perspective
- Short sentences (easy to narrate)
- Time each section (intro: 5s, summary: 15s, etc.)
- Include natural pauses
- End with call-to-action

Content:
{json.dumps(curated_data, indent=2)}

Format as JSON:
{{
  "intro": "Welcome to AI Weekly Digest...",
  "summary": "This week saw major breakthroughs...",
  "sections": {{
    "research": "Let's start with research. First, ...",
    "industry": "In industry news, ...",
    "tools": "And finally, new tools..."
  }},
  "outro": "Thanks for watching! Subscribe for..."
}}"""

    message = client.messages.create(
        model="claude-sonnet-4-5-20251029",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )

    return json.loads(message.content[0].text)
```

---

## 🎨 Visual Design

### Animated Text Overlays:

```python
from moviepy.editor import *

def create_text_clip(text, duration, fontsize=50):
    """Create animated text clip"""
    clip = TextClip(
        text,
        fontsize=fontsize,
        color='white',
        font='Arial-Bold',
        size=(1920, None),
        method='caption',
        align='center'
    )

    # Fade in/out
    clip = clip.set_duration(duration)
    clip = clip.fadein(0.5).fadeout(0.5)

    return clip


def create_gradient_background():
    """Create your signature gradient background"""
    # Use ImageMagick or create gradient image
    # Or use solid color and add overlay
    return ColorClip((1920, 1080), color=(15, 12, 41))
```

### Section Transitions:

```python
def slide_transition(clip1, clip2):
    """Slide transition between clips"""
    clip1 = clip1.set_start(0)
    clip2 = clip2.set_start(clip1.duration - 0.5)  # Overlap

    # Slide out / slide in effect
    clip1 = clip1.fx(vfx.slide_out, 0.5, 'left')
    clip2 = clip2.fx(vfx.slide_in, 0.5, 'right')

    return concatenate_videoclips([clip1, clip2])
```

---

## 📤 YouTube Upload Automation

### Using YouTube Data API v3:

**Setup:**
```bash
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

**Authentication:**
```python
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# OAuth 2.0 flow
flow = InstalledAppFlow.from_client_secrets_file(
    'client_secrets.json',
    scopes=['https://www.googleapis.com/auth/youtube.upload']
)

credentials = flow.run_local_server()
youtube = build('youtube', 'v3', credentials=credentials)
```

**Upload Video:**
```python
def upload_to_youtube(video_path, title, description, tags):
    """Upload video to YouTube"""

    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': '28'  # Science & Technology
        },
        'status': {
            'privacyStatus': 'public',  # or 'private', 'unlisted'
            'selfDeclaredMadeForKids': False
        }
    }

    media = MediaFileUpload(
        video_path,
        chunksize=-1,
        resumable=True,
        mimetype='video/mp4'
    )

    request = youtube.videos().insert(
        part='snippet,status',
        body=body,
        media_body=media
    )

    response = request.execute()
    video_id = response['id']

    print(f"Uploaded: https://youtube.com/watch?v={video_id}")
    return video_id
```

**Auto-generate metadata:**
```python
title = f"AI Weekly Digest - {datetime.now().strftime('%B %d, %Y')}"

description = f"""
{curated_data['weekly_summary']}

📚 Topics covered:
• {len(curated_data['sections']['Key Research Papers'])} research breakthroughs
• {len(curated_data['sections']['Industry Updates'])} industry updates
• {len(curated_data['sections']['Tools & Frameworks'])} new tools

🔗 Read the full digest: https://EiriniOr.github.io/ai-weekly-digest/

#AI #MachineLearning #AgenticAI #Technology
"""

tags = ['AI', 'Machine Learning', 'Agentic AI', 'Research', 'Tech News']
```

---

## 💻 Complete Implementation

### New Module: `scripts/generate_video.py`

```python
#!/usr/bin/env python3
"""
Video Generator
Creates YouTube videos from curated AI news
"""

import asyncio
import json
from pathlib import Path
from datetime import datetime
from openai import OpenAI
from moviepy.editor import *
import anthropic
import os

class VideoGenerator:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.data_dir = self.base_dir / "data"
        self.output_dir = self.base_dir / "output"
        self.video_dir = self.base_dir / "videos"
        self.video_dir.mkdir(exist_ok=True)

        self.openai_client = OpenAI()
        self.claude_client = anthropic.Anthropic()

    def get_latest_curated_data(self):
        """Load most recent curated content"""
        data_files = sorted(self.data_dir.glob("curated_*.json"), reverse=True)
        with open(data_files[0]) as f:
            return json.load(f)

    async def generate_script(self, curated_data):
        """Generate video narration script using Claude"""
        print("📝 Generating video script...")

        prompt = f"""Create a natural, conversational 2-minute video script for a YouTube video.

Style:
- Female narrator
- Friendly, engaging tone
- Short, clear sentences
- Natural pauses between sections

Content to cover:
{json.dumps(curated_data, indent=2)}

Output as JSON:
{{
  "intro": "...",
  "summary": "...",
  "research": "...",
  "industry": "...",
  "tools": "...",
  "outro": "..."
}}"""

        message = self.claude_client.messages.create(
            model="claude-sonnet-4-5-20251029",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        script = json.loads(message.content[0].text)
        print("  ✓ Script generated")
        return script

    async def generate_audio(self, script):
        """Generate audio narration using OpenAI TTS"""
        print("🎙️  Generating audio narration...")

        # Combine all script sections
        full_script = "\n\n".join([
            script['intro'],
            script['summary'],
            script['research'],
            script['industry'],
            script['tools'],
            script['outro']
        ])

        # Generate audio
        response = self.openai_client.audio.speech.create(
            model="tts-1-hd",
            voice="nova",  # Female voice
            input=full_script
        )

        # Save audio file
        audio_path = self.video_dir / "narration.mp3"
        response.stream_to_file(audio_path)

        print(f"  ✓ Audio saved: {audio_path}")
        return audio_path

    async def create_video(self, script, audio_path, curated_data):
        """Generate video with moviepy"""
        print("🎬 Creating video...")

        # Load audio to get duration
        audio = AudioFileClip(str(audio_path))
        total_duration = audio.duration

        # Create gradient background
        background = ColorClip(
            size=(1920, 1080),
            color=(15, 12, 41),  # Your purple color
            duration=total_duration
        )

        # Create text clips
        clips = []

        # Intro
        intro_text = TextClip(
            "🤖 AI Weekly Digest",
            fontsize=80,
            color='white',
            font='Arial-Bold'
        ).set_duration(5).set_position('center')
        clips.append(intro_text.set_start(0))

        date_text = TextClip(
            datetime.now().strftime('%B %d, %Y'),
            fontsize=40,
            color='lightgray',
            font='Arial'
        ).set_duration(5).set_position(('center', 700))
        clips.append(date_text.set_start(0))

        # Summary section (at 5 seconds)
        summary_text = TextClip(
            curated_data['weekly_summary'],
            fontsize=40,
            color='white',
            font='Arial',
            size=(1600, None),
            method='caption',
            align='center'
        ).set_duration(15).set_position('center')
        clips.append(summary_text.set_start(5))

        # Research papers section
        y_pos = 300
        for i, paper in enumerate(curated_data['sections']['Key Research Papers'][:3]):
            text = f"• {paper['title']}"
            paper_clip = TextClip(
                text,
                fontsize=30,
                color='white',
                font='Arial',
                size=(1600, None),
                method='caption'
            ).set_duration(10).set_position(('center', y_pos + i*150))
            clips.append(paper_clip.set_start(20 + i*10))

        # Outro
        outro_text = TextClip(
            "Subscribe for Weekly AI Updates!",
            fontsize=60,
            color='white',
            font='Arial-Bold'
        ).set_duration(5).set_position('center')
        clips.append(outro_text.set_start(total_duration - 5))

        # Composite video
        video = CompositeVideoClip([background] + clips)
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

    async def generate(self):
        """Main video generation workflow"""
        print("🎥 Starting video generation...\n")

        # Load curated data
        curated_data = self.get_latest_curated_data()

        # Generate script
        script = await self.generate_script(curated_data)

        # Generate audio
        audio_path = await self.generate_audio(script)

        # Create video
        video_path = await self.create_video(script, audio_path, curated_data)

        return video_path

async def main():
    generator = VideoGenerator()
    video_path = await generator.generate()
    print(f"\n✅ Video ready: {video_path}")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 📊 Cost Analysis

### Per Video:

| Service | Cost | Notes |
|---------|------|-------|
| OpenAI TTS | $0.03 | ~2,000 characters |
| Claude (script) | $0.01 | ~1,000 tokens |
| YouTube hosting | $0 | Free |
| **Total** | **$0.04** | Practically free! |

### Monthly (4 videos):
- **Total: $0.16/month**

**Compare to:**
- Hiring voice actor: $100-500 per video
- Video editor: $200-1000 per video
- Manual work: 4-8 hours per video

**Your system**: Fully automated, $0.04 per video 🎉

---

## 🚀 GitHub Actions Integration

### Update workflow to include video generation:

```yaml
# .github/workflows/weekly-digest.yml

- name: Generate video
  env:
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
  run: |
    python3 scripts/generate_video.py

- name: Upload to YouTube
  env:
    YOUTUBE_CLIENT_SECRETS: ${{ secrets.YOUTUBE_CLIENT_SECRETS }}
  run: |
    python3 scripts/upload_youtube.py
```

---

## 🎯 Next Steps

### Phase 1: Basic Setup (1 hour)
1. Install dependencies: `pip install openai moviepy`
2. Get OpenAI API key
3. Test TTS generation
4. Create simple video

### Phase 2: Automation (2 hours)
1. Create `generate_video.py` module
2. Integrate with existing pipeline
3. Test end-to-end

### Phase 3: YouTube (1 hour)
1. Set up YouTube channel
2. Get API credentials
3. Create `upload_youtube.py`
4. Test upload

### Phase 4: Polish (optional)
1. Better visuals (animations, transitions)
2. Background music
3. Thumbnail generation
4. YouTube Shorts format (vertical video)

---

## 💡 Creative Ideas

### YouTube Shorts Version:
- 60-second vertical video (1080x1920)
- Just weekly summary + top 3 highlights
- More viral potential

### Thumbnail Generation:
```python
from PIL import Image, ImageDraw, ImageFont

def generate_thumbnail(title):
    img = Image.new('RGB', (1280, 720), color=(15, 12, 41))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('Arial.ttf', 60)

    draw.text((640, 360), title, fill='white', font=font, anchor='mm')
    img.save('thumbnail.jpg')
```

### Background Music:
```python
# Add royalty-free music
music = AudioFileClip("background_music.mp3").volumex(0.1)
final_audio = CompositeAudioClip([narration, music])
video = video.set_audio(final_audio)
```

---

## 📚 Resources

### APIs & Libraries:
- OpenAI TTS: https://platform.openai.com/docs/guides/text-to-speech
- moviepy: https://zulko.github.io/moviepy/
- YouTube API: https://developers.google.com/youtube/v3

### Learning:
- moviepy tutorial: https://zulko.github.io/moviepy/getting_started/quick_start.html
- YouTube upload guide: https://developers.google.com/youtube/v3/guides/uploading_a_video

---

**Ready to build?** I can help you implement any of these components step-by-step!

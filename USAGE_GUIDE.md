# AI Weekly Digest - Usage Guide

## Quick Answers to Your Questions

### 1. How do I run the full flow manually to generate proper content?

Run this command from the project directory:

```bash
cd /Users/rena/ai-weekly-digest
python3 generate_weekly_digest.py
```

**What it does:**
1. Collects AI news from arXiv, Hacker News, and Reddit (last 7 days)
2. Curates content using Claude AI
3. Generates the webpage with your name in the footer
4. Creates AI-narrated video script
5. Generates audio narration (OpenAI TTS female voice)
6. Creates video (note: moviepy not installed locally, works in GitHub Actions)
7. Attempts YouTube upload (requires authentication)

### 2. Where does the video appear on the webpage?

**YES!** The video is automatically embedded on the webpage in two places:

1. **Main Page** ([https://EiriniOr.github.io/ai-weekly-digest/](https://EiriniOr.github.io/ai-weekly-digest/)):
   - Video player section appears between the weekly summary and content sections
   - Shows your latest YouTube uploads automatically via playlist embed
   - "Subscribe to our channel" link below the player

2. **Footer**: YouTube channel link at the bottom

The video player will automatically show your latest uploads once videos are published to YouTube!

### 3. How do I authenticate for YouTube uploads?

**The Challenge**: YouTube requires interactive browser authentication which can't happen automatically. Here's how to handle it:

#### Option A: Manual Upload (Easiest for now)
1. Video files are generated in: `/Users/rena/ai-weekly-digest/videos/`
2. Manually upload videos to your YouTube channel: [https://www.youtube.com/channel/UCUPSLoXvaMVbOIaXsOorHng](https://www.youtube.com/channel/UCUPSLoXvaMVbOIaXsOorHng)
3. The webpage will automatically show the latest videos via the embedded player

#### Option B: Set up OAuth2 for Automatic Uploads

**Prerequisites**:
- Google API libraries (can't install locally due to package conflicts)
- This will only work in GitHub Actions environment

**Steps** (documented in [YOUTUBE_API_SETUP.md](YOUTUBE_API_SETUP.md)):
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create OAuth2 credentials for YouTube Data API v3
3. Download credentials JSON
4. Convert to base64 and add to GitHub Secrets as `YOUTUBE_CREDENTIALS_BASE64`
5. First workflow run will require manual authentication
6. After that, uploads work automatically

**For Now**: Since packages can't be installed locally, the best approach is:
- Let GitHub Actions handle everything automatically each week
- OR manually upload videos from the `videos/` folder

### 4. Your Name on the Webpage

✅ **DONE!** Your name "Eirini Ornithopoulou" now appears in the footer of every page with a link to your GitHub profile.

The footer shows:
```
Created by Eirini Ornithopoulou
```

---

## File Locations

- **Generated Videos**: `/Users/rena/ai-weekly-digest/videos/`
  - `ai_weekly_YYYYMMDD.mp4` - Full video file
  - `narration_YYYYMMDD.mp3` - Audio narration
  - `script_YYYYMMDD.json` - AI-generated script

- **Generated Webpage**: `/Users/rena/ai-weekly-digest/output/index.html`
  - Also deployed to: [https://EiriniOr.github.io/ai-weekly-digest/](https://EiriniOr.github.io/ai-weekly-digest/)

- **Curated Data**: `/Users/rena/ai-weekly-digest/data/curated_YYYYMMDD.json`

---

## Automation Options

### GitHub Actions (Recommended - Works Automatically)
- Runs every Sunday at 6:00 PM UTC
- Installs all dependencies automatically
- Generates video with moviepy
- Deploys webpage to GitHub Pages
- Manual trigger option at: [https://github.com/EiriniOr/ai-weekly-digest/actions](https://github.com/EiriniOr/ai-weekly-digest/actions)

**Required GitHub Secrets** (already configured):
- `ANTHROPIC_API_KEY` ✅
- `OPENAI_API_KEY` ✅
- `YOUTUBE_CREDENTIALS_BASE64` (optional, for auto-upload)

### Local Testing
Run anytime:
```bash
cd /Users/rena/ai-weekly-digest
python3 generate_weekly_digest.py
```

**Note**: Local generation will skip video creation (moviepy not installed) but script and audio will be generated successfully.

---

## Current Status

✅ **Working Perfectly:**
- AI content curation with Claude
- Webpage generation with your name in footer
- AI script generation
- OpenAI TTS audio narration (female voice)
- Test video created with ffmpeg
- YouTube player embedded on webpage
- GitHub Actions fully configured

⚠️ **Needs Manual Step:**
- YouTube OAuth authentication (requires Google API libraries)
- Video creation locally (moviepy not installed)

**Solution**: Use GitHub Actions for full automation, or manually upload videos from the `videos/` folder.

---

## Quick Command Reference

```bash
# Generate full digest
python3 generate_weekly_digest.py

# Generate video only
python3 scripts/generate_video.py

# Upload to YouTube (requires authentication)
python3 scripts/upload_youtube.py

# Check what was generated
ls -lh videos/
ls -lh output/
ls -lh data/
```

---

## Questions?

- **Codebase**: [https://github.com/EiriniOr/ai-weekly-digest](https://github.com/EiriniOr/ai-weekly-digest)
- **Live Site**: [https://EiriniOr.github.io/ai-weekly-digest/](https://EiriniOr.github.io/ai-weekly-digest/)
- **YouTube**: [https://www.youtube.com/channel/UCUPSLoXvaMVbOIaXsOorHng](https://www.youtube.com/channel/UCUPSLoXvaMVbOIaXsOorHng)
- **Detailed YouTube Setup**: See [YOUTUBE_API_SETUP.md](YOUTUBE_API_SETUP.md)

# AI Weekly Digest Generator 🤖📺

Automatically generates a **beautiful webpage** and **AI-narrated YouTube videos** every week with the latest updates in **Agentic AI** - autonomous agents, multi-agent systems, tool use, planning, and reasoning.

🌐 **Live Site**: https://EiriniOr.github.io/ai-weekly-digest/
📺 **YouTube Channel**: https://www.youtube.com/channel/UCUPSLoXvaMVbOIaXsOorHng

## What It Does

Every Sunday at 6:00 PM UTC, this fully automated system:

1. **Collects** AI news from multiple sources (arXiv, Hacker News, Reddit)
2. **Curates** content using Claude to filter and categorize by relevance
3. **Generates** a futuristic animated webpage with the top updates
4. **Creates** AI-narrated YouTube videos with voice-over and animations
5. **Uploads** videos automatically to YouTube
6. **Deploys** everything to GitHub Pages

## Quick Start

### 1. Install Dependencies

```bash
cd /Users/rena/ai-weekly-digest
pip3 install anthropic pyyaml requests feedparser openai moviepy
pip3 install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

**Note**: On macOS with Homebrew Python, you may need to use a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Set Your API Keys

You need API keys for:
- **Anthropic Claude** (content curation)
- **OpenAI** (AI voice narration)
- **YouTube Data API** (video uploads) - See [YOUTUBE_API_SETUP.md](YOUTUBE_API_SETUP.md)

```bash
export ANTHROPIC_API_KEY="your-anthropic-key"
export OPENAI_API_KEY="your-openai-key"
```

Or add to your `~/.zshrc` or `~/.bash_profile`:

```bash
echo 'export ANTHROPIC_API_KEY="your-key"' >> ~/.zshrc
echo 'export OPENAI_API_KEY="your-key"' >> ~/.zshrc
source ~/.zshrc
```

For automated uploads, follow the [YouTube API Setup Guide](YOUTUBE_API_SETUP.md).

### 3. Test It Manually

Run the full pipeline once to make sure everything works:

```bash
python3 generate_weekly_digest.py
```

This will:
- Collect news from the past week
- Curate with Claude
- Generate a beautiful webpage
- Create AI-narrated video (if OpenAI key is set)
- Upload to YouTube (if credentials configured)
- Deploy to GitHub Pages

**Expected outputs**:
- Webpage: `output/index.html`
- Video: `videos/ai_weekly_YYYYMMDD.mp4`
- Live site: https://EiriniOr.github.io/ai-weekly-digest/

### 4. Set Up Automation

#### Option A: GitHub Actions (Recommended - Free & Cloud-based)

The system is already configured to run automatically via GitHub Actions!

**Setup steps:**

1. **Add GitHub Secrets** (required):
   Go to: https://github.com/EiriniOr/ai-weekly-digest/settings/secrets/actions

   Add these secrets:
   - `ANTHROPIC_API_KEY`: Your Claude API key
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `YOUTUBE_CREDENTIALS_BASE64`: YouTube OAuth credentials (see [YOUTUBE_API_SETUP.md](YOUTUBE_API_SETUP.md))

2. **That's it!** The workflow runs automatically every Sunday at 6:00 PM UTC.

3. **Manual trigger** (optional):
   - Go to: https://github.com/EiriniOr/ai-weekly-digest/actions
   - Click "Generate Weekly AI Digest"
   - Click "Run workflow"

**What happens:**
- Runs in GitHub's cloud (free for public repos)
- Generates webpage + video
- Uploads to YouTube automatically
- Deploys to GitHub Pages
- No local machine needed!

#### Option B: Local Automation (macOS launchd)

For running locally on your Mac:

```bash
# 1. Edit the plist file and add your API keys
nano com.aiweekly.digest.plist

# 2. Copy to LaunchAgents
cp com.aiweekly.digest.plist ~/Library/LaunchAgents/

# 3. Load the agent
launchctl load ~/Library/LaunchAgents/com.aiweekly.digest.plist

# 4. Verify it's loaded
launchctl list | grep aiweekly
```

#### Option C: Manual Run

If you prefer manual control, just run this command whenever you want your digest:

```bash
cd /Users/rena/ai-weekly-digest
python3 generate_weekly_digest.py
```

## Configuration

Edit `config.yaml` to customize:

### News Sources

```yaml
sources:
  arxiv:
    enabled: true
    categories:
      - cs.AI  # Artificial Intelligence
      - cs.LG  # Machine Learning
    max_papers: 10

  hackernews:
    enabled: true
    keywords:
      - "agentic ai"
      - "ai agents"
      - "llm"
    min_score: 50

  reddit:
    enabled: true
    subreddits:
      - MachineLearning
      - LocalLLaMA
    min_score: 100
```

### Focus Topics

```yaml
curation:
  focus_topics:
    - "autonomous agents"
    - "multi-agent systems"
    - "tool use"
    - "reasoning"
    - "planning"
```

### Presentation Settings

```yaml
presentation:
  title: "Weekly Agentic AI Digest"
  output_path: "/Users/rena/Downloads"
  sections:
    - name: "Key Research Papers"
      max_items: 5
    - name: "Industry Updates"
      max_items: 5
```

## How It Works

### Architecture

```
┌─────────────────┐
│ News Sources    │
│ • arXiv         │
│ • Hacker News   │
│ • Reddit        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ collect_news.py │  Aggregates all sources
│                 │  Saves: data/raw_news_*.json
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ curate_content  │  Claude filters & categorizes
│      .py        │  Saves: data/curated_*.json
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ generate_       │  Creates PowerPoint using
│ presentation.py │  MCP PowerPoint Server
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Downloads/     │  AI_Weekly_YYYY-MM-DD.pptx
│  📄 Presentation│
└─────────────────┘
```

### Data Flow

1. **Collection**: Pulls recent items from APIs and RSS feeds
2. **Storage**: Saves raw JSON data to `data/` directory
3. **Curation**: Claude analyzes all items and selects the most relevant
4. **Generation**: PowerPoint MCP server creates formatted slides
5. **Output**: Final `.pptx` file ready to open and learn from

## File Structure

```
ai-weekly-digest/
├── config.yaml                    # Configuration
├── generate_weekly_digest.py      # Main orchestrator
├── requirements.txt               # Python dependencies
├── README.md                      # This file
├── com.aiweekly.digest.plist      # launchd automation
│
├── scripts/
│   ├── collect_news.py            # News aggregation
│   ├── curate_content.py          # Claude curation
│   └── generate_presentation.py   # PowerPoint generation
│
├── data/
│   ├── raw_news_*.json            # Collected news
│   └── curated_*.json             # Curated content
│
├── output/                        # (unused, goes to Downloads)
└── logs/
    ├── stdout.log                 # Automation logs
    └── stderr.log                 # Error logs
```

## Commands Reference

### Run Full Pipeline

```bash
python3 generate_weekly_digest.py
```

### Run Individual Steps

```bash
# Step 1: Collect news
cd scripts && python3 collect_news.py

# Step 2: Curate content (requires Step 1)
cd scripts && python3 curate_content.py

# Step 3: Generate presentation (requires Step 2)
cd scripts && python3 generate_presentation.py
```

### Manage Automation

```bash
# Load (start) the automation
launchctl load ~/Library/LaunchAgents/com.aiweekly.digest.plist

# Unload (stop) the automation
launchctl unload ~/Library/LaunchAgents/com.aiweekly.digest.plist

# Check status
launchctl list | grep aiweekly

# View logs
tail -f logs/stdout.log
tail -f logs/stderr.log

# Test run immediately (for debugging)
launchctl start com.aiweekly.digest
```

## Customization Examples

### Change to Friday Digests

Edit `com.aiweekly.digest.plist`:

```xml
<key>Weekday</key>
<integer>5</integer>  <!-- 5 = Friday -->
```

### Focus on Different Topics

Edit `config.yaml`:

```yaml
curation:
  focus_topics:
    - "computer vision"
    - "nlp"
    - "transformers"
```

### Add More Sources

Extend `scripts/collect_news.py` with new collectors:

```python
async def collect_twitter(self):
    # Add Twitter/X API integration
    pass
```

### Change Presentation Style

Modify `scripts/generate_presentation.py` to use different MCP tools:

```python
# Add charts
await self.ppt.add_chart(...)

# Add images
await self.ppt.add_image(...)

# Change themes
await self.ppt.apply_theme(theme="modern")
```

## Troubleshooting

### "No curated data found"

Run the pipeline in order:

```bash
cd scripts
python3 collect_news.py
python3 curate_content.py
cd ..
python3 generate_weekly_digest.py
```

### API Key Not Found

Make sure `ANTHROPIC_API_KEY` is set:

```bash
echo $ANTHROPIC_API_KEY
```

If empty, set it:

```bash
export ANTHROPIC_API_KEY="your-key"
```

### Automation Not Running

Check launchd status:

```bash
launchctl list | grep aiweekly
```

View error logs:

```bash
cat logs/stderr.log
```

Verify API key in plist:

```bash
grep ANTHROPIC_API_KEY ~/Library/LaunchAgents/com.aiweekly.digest.plist
```

### No News Collected

- Check internet connection
- Verify source APIs are accessible
- Look at `logs/stdout.log` for errors
- Try running `collect_news.py` manually

## Future Enhancements

Possible additions:

- **Email delivery**: Automatically email the presentation
- **Slack integration**: Post summary to Slack channel
- **Web dashboard**: View curated news before generation
- **PDF export**: Generate PDF version alongside PPTX
- **Custom templates**: Design custom PowerPoint themes
- **More sources**: Twitter, LinkedIn, newsletters, podcasts
- **Trend analysis**: Track topics over time, highlight emerging trends

## FAQ

**Q: How much does this cost?**
A: Claude API costs ~$0.01-0.05 per week for curation (varies by content volume).

**Q: Can I run this on Windows/Linux?**
A: Yes! Replace launchd with Task Scheduler (Windows) or cron (Linux).

**Q: What if I miss a week?**
A: The system always looks at the past 7 days, so you can run it anytime.

**Q: Can I customize the presentation design?**
A: Yes! Edit `generate_presentation.py` and use the 36 MCP PowerPoint tools.

**Q: How do I change the schedule?**
A: Edit the `StartCalendarInterval` section in `com.aiweekly.digest.plist`.

## Support

- Check logs: `tail -f logs/stderr.log`
- Test components individually
- Verify API keys and dependencies
- Review config.yaml settings

## License

Personal use project. Modify as needed!

---

**Status**: ✅ Ready to use

**Next Steps**:
1. Install dependencies
2. Set API key
3. Run test generation
4. Enable automation

Enjoy your weekly AI learning! 🚀

# AI Weekly Digest Generator 🤖

Automatically generates a PowerPoint presentation every Sunday with the latest updates in **Agentic AI** - autonomous agents, multi-agent systems, tool use, planning, and reasoning.

## What It Does

Every Sunday at 9:00 AM, this system:

1. **Collects** AI news from multiple sources (arXiv, Hacker News, Reddit)
2. **Curates** content using Claude to filter and categorize by relevance
3. **Generates** a beautiful PowerPoint presentation with the top updates
4. **Delivers** the presentation to your Downloads folder

## Quick Start

### 1. Install Dependencies

```bash
cd /Users/rena/ai-weekly-digest
pip3 install -r requirements.txt
```

### 2. Set Your API Key

You need an Anthropic API key for content curation:

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

Or add it to your `~/.zshrc` or `~/.bash_profile`:

```bash
echo 'export ANTHROPIC_API_KEY="your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

### 3. Test It Manually

Run the full pipeline once to make sure everything works:

```bash
python3 generate_weekly_digest.py
```

This will:
- Collect news from the past week
- Curate with Claude
- Generate a PowerPoint presentation in your Downloads folder

**Expected output**: `~/Downloads/AI_Weekly_YYYY-MM-DD.pptx`

### 4. Set Up Sunday Automation

#### Option A: Using launchd (Recommended for macOS)

```bash
# 1. Create logs directory
mkdir -p logs

# 2. Edit the plist file and add your API key
nano com.aiweekly.digest.plist
# Replace YOUR_API_KEY_HERE with your actual Anthropic API key

# 3. Copy to LaunchAgents
cp com.aiweekly.digest.plist ~/Library/LaunchAgents/

# 4. Load the agent
launchctl load ~/Library/LaunchAgents/com.aiweekly.digest.plist

# 5. Verify it's loaded
launchctl list | grep aiweekly
```

The presentation will now be generated automatically every Sunday at 9:00 AM!

#### Option B: Manual Run

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

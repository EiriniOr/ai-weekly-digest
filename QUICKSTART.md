# Quick Start Guide 🚀

Get your weekly AI digest running in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- Anthropic API key ([get one here](https://console.anthropic.com/))

## Installation

```bash
# 1. Navigate to the directory
cd /Users/rena/ai-weekly-digest

# 2. Run setup
./setup.sh

# 3. Set your API key
export ANTHROPIC_API_KEY="your-api-key-here"
```

## First Run

```bash
# Generate your first digest
python3 generate_weekly_digest.py
```

This will:
1. Collect AI news from the past week (arXiv, Hacker News, Reddit)
2. Use Claude to curate the most relevant agentic AI content
3. Create a PowerPoint presentation in your Downloads folder

**Output**: `~/Downloads/AI_Weekly_YYYY-MM-DD.pptx`

## Enable Sunday Automation

```bash
# 1. Edit the plist and add your API key
nano com.aiweekly.digest.plist
# Replace YOUR_API_KEY_HERE with your actual key

# 2. Install the automation
cp com.aiweekly.digest.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.aiweekly.digest.plist

# 3. Verify it's running
launchctl list | grep aiweekly
```

Now every Sunday at 9:00 AM, you'll get a fresh presentation!

## Customization

Edit [config.yaml](config.yaml):

```yaml
# Change topics to focus on
curation:
  focus_topics:
    - "autonomous agents"
    - "tool use"
    - "reasoning"

# Change presentation title
presentation:
  title: "My Weekly AI Digest"

# Add/remove sources
sources:
  arxiv:
    enabled: true
  hackernews:
    enabled: true
```

## Troubleshooting

**No presentation created?**
- Check API key: `echo $ANTHROPIC_API_KEY`
- View logs: `cat logs/stderr.log`

**Automation not working?**
- Verify it's loaded: `launchctl list | grep aiweekly`
- Check the plist has your API key

**Need help?**
- See full documentation: [README.md](README.md)

## What's Next?

- Customize the topics in `config.yaml`
- Change the schedule in `com.aiweekly.digest.plist`
- Modify presentation style in `scripts/generate_presentation.py`

Enjoy your weekly learning! 📚

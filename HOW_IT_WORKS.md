# 🤖 How AI Weekly Digest Works

## 🎯 Overview

My AI Weekly Digest automatically curates agentic AI news every Sunday at 6 PM. Here's the complete workflow:

```
┌─────────────────────────────────────────────────────────────┐
│  GitHub Actions Trigger (Every Sunday at 6 PM UTC)         │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  STEP 1: Collect News (scripts/collect_news.py)            │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  • arXiv API → Recent AI research papers                   │
│  • Hacker News API → Top AI stories                        │
│  • Reddit JSON → Community discussions                      │
│                                                              │
│  Output: data/raw_news_YYYYMMDD.json                        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  STEP 2: Curate Content (scripts/curate_content.py)        │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  • Send all items to Claude Sonnet 4.5                     │
│  • Claude filters for agentic AI relevance                  │
│  • Categorizes into 4 sections                              │
│  • Generates one-sentence insights                          │
│  • Creates weekly summary                                    │
│                                                              │
│  Output: data/curated_YYYYMMDD.json                         │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  STEP 3: Generate Webpage (scripts/generate_webpage.py)    │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  • Creates index.html with futuristic design                │
│  • Animated gradient backgrounds                            │
│  • Section-colored content cards                            │
│  • Builds archive pages for past digests                    │
│                                                              │
│  Output: output/index.html + archive pages                  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  STEP 4: Deploy (scripts/deploy_github.py)                 │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  • Git init in output/ folder                               │
│  • Commit all HTML files                                    │
│  • Force push to gh-pages branch                            │
│                                                              │
│  Live: https://EiriniOr.github.io/ai-weekly-digest/        │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Step 1: News Collection (Parallel)

### Sources & APIs:

**1. arXiv (Research Papers)**
```python
# API: http://export.arxiv.org/api/query
# Categories: cs.AI, cs.MA, cs.LG
# Filters: Last 7 days, max 30 papers

Example output:
{
  "source": "arxiv",
  "title": "Multi-Agent Planning with LLM Coordination",
  "summary": "We propose a framework for...",
  "url": "https://arxiv.org/abs/2025.12345",
  "authors": ["Smith, J.", "Doe, A."],
  "published": "2025-12-10T00:00:00"
}
```

**2. Hacker News (Tech Stories)**
```python
# API: https://hacker-news.firebaseio.com/v0
# Keywords: "ai agent", "llm", "gpt", "claude", etc.
# Filters: Score ≥ 50 points

Example output:
{
  "source": "hackernews",
  "title": "New autonomous agent framework released",
  "url": "https://example.com",
  "score": 234,
  "comments": 89,
  "time": "2025-12-14T12:00:00"
}
```

**3. Reddit (Community Discussions)**
```python
# API: https://www.reddit.com/r/{subreddit}/top.json
# Subreddits: MachineLearning, artificial, LocalLLaMA
# Filters: Top posts this week, score ≥ 20

Example output:
{
  "source": "reddit",
  "subreddit": "MachineLearning",
  "title": "[D] Best practices for agent architectures",
  "url": "https://reddit.com/r/MachineLearning/comments/...",
  "score": 145,
  "comments": 42
}
```

**Result**: ~50-100 raw items saved to `data/raw_news_YYYYMMDD.json`

---

## 🧠 Step 2: AI Curation (The Magic!)

### How Claude Filters Content:

**Input**: All collected items (papers, stories, posts)

**Claude's Task**:
1. **Filter** for agentic AI relevance
   - Autonomous agents
   - Multi-agent systems
   - Tool use & function calling
   - Planning & reasoning
   - Agent frameworks

2. **Categorize** into 4 sections:
   - **Key Research Papers** (5 items max)
   - **Industry Updates** (5 items max)
   - **Tools & Frameworks** (4 items max)
   - **Notable Discussions** (4 items max) - excluded from output

3. **Generate insights**:
   - One sentence per item explaining why it matters
   - Example: *"Demonstrates how multi-agent competition leads to emergent coordination behaviors"*

4. **Create summary**:
   - 2-3 sentence overview of the week's themes
   - Example: *"This week saw major advances in multi-agent coordination..."*

**Output Structure**:
```json
{
  "sections": {
    "Key Research Papers": [
      {
        "title": "Multi-Agent Planning Framework",
        "url": "https://arxiv.org/abs/...",
        "meta": "arXiv • Smith, Doe",
        "insight": "Proposes novel coordination protocol...",
        "score": 9
      }
    ],
    "Industry Updates": [...],
    "Tools & Frameworks": [...]
  },
  "weekly_summary": "Major breakthroughs in agent coordination..."
}
```

**Saved to**: `data/curated_YYYYMMDD.json`

---

## 🎨 Step 3: Webpage Generation

### Main Page (index.html):

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>🤖 AI Weekly Digest</title>
    <style>
        /* Futuristic gradient background */
        body {
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        }

        /* Animated pattern overlay */
        body::before {
            animation: backgroundScroll 20s linear infinite;
        }

        /* Section-specific colors */
        .research { border-left: 4px solid #9B59B6; }  /* Purple */
        .industry { border-left: 4px solid #3498DB; }  /* Blue */
        .tools { border-left: 4px solid #1ABC9C; }     /* Turquoise */
    </style>
</head>
```

### Structure:
1. **Header** - Title, subtitle, current date
2. **Summary** - Claude's weekly summary
3. **Sections** - Colored cards with insights
4. **Archive** - Last 5 weeks (clickable)
5. **Footer** - Links to GitHub

### Archive Pages (digest-YYYYMMDD.html):

Each past week gets its own page:
- Same futuristic design
- "Back to Latest" link
- Full content from that week
- Automatically generated when new digest runs

---

## 🚀 Step 4: Deployment

### Git Workflow:
```bash
cd output/
git init
git checkout -B gh-pages
git add .
git commit -m "Update weekly digest - YYYY-MM-DD"
git push -f origin gh-pages
```

### GitHub Pages:
- **Branch**: `gh-pages`
- **Source**: Root directory
- **URL**: https://EiriniOr.github.io/ai-weekly-digest/

### Why gh-pages?
- Free hosting
- Auto-deploys from branch
- Custom domain support
- No server required

---

## ⚙️ Configuration (config.yaml)

```yaml
sources:
  arxiv:
    enabled: true
    categories: ["cs.AI", "cs.MA", "cs.LG"]
    max_papers: 30

  hackernews:
    enabled: true
    keywords: ["ai agent", "llm", "gpt", "claude"]
    min_score: 50

  reddit:
    enabled: true
    subreddits: ["MachineLearning", "artificial", "LocalLLaMA"]
    min_score: 20

curation:
  model: "claude-sonnet-4-5-20251029"
  focus_topics:
    - "Autonomous AI agents"
    - "Multi-agent systems"
    - "Tool use and function calling"

presentation:
  sections:
    - name: "Key Research Papers"
      max_items: 5
    - name: "Industry Updates"
      max_items: 5
    - name: "Tools & Frameworks"
      max_items: 4
```

---

## 🤖 Automation Methods

### Option 1: GitHub Actions (Cloud - Recommended)

**File**: `.github/workflows/weekly-digest.yml`

```yaml
name: Generate Weekly AI Digest

on:
  schedule:
    - cron: '0 18 * * 0'  # Every Sunday at 6 PM UTC
  workflow_dispatch:      # Manual trigger option

jobs:
  generate-digest:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install anthropic pyyaml requests feedparser

      - name: Generate digest
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: python3 generate_weekly_digest.py

      - name: Deploy to GitHub Pages
        run: |
          cd output
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git init
          git checkout -b gh-pages
          git add .
          git commit -m "Update digest - $(date +'%Y-%m-%d')"
          git push -f https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git gh-pages
```

**Advantages**:
- ✅ Runs in the cloud (laptop can be off)
- ✅ Free on GitHub
- ✅ Reliable scheduling
- ✅ Automatic deployment

**Setup Required**:
1. Add `ANTHROPIC_API_KEY` to GitHub Secrets
2. Enable GitHub Actions in repository settings

### Option 2: Local (macOS launchd)

**File**: `~/Library/LaunchAgents/com.aiweekly.digest.plist`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.aiweekly.digest</string>
    <key>ProgramArguments</key>
    <array>
        <string>/opt/homebrew/bin/python3</string>
        <string>/Users/rena/ai-weekly-digest/generate_weekly_digest.py</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Weekday</key>
        <integer>0</integer>  <!-- Sunday -->
        <key>Hour</key>
        <integer>18</integer> <!-- 6 PM -->
        <key>Minute</key>
        <integer>0</integer>
    </dict>
</dict>
</plist>
```

**Disadvantages**:
- ❌ Requires laptop to be on at 6 PM Sunday
- ❌ Doesn't run if sleeping
- ❌ Manual setup on each machine

---

## 📁 File Structure

```
ai-weekly-digest/
├── generate_weekly_digest.py      # Main orchestrator
├── config.yaml                     # Configuration
│
├── scripts/
│   ├── collect_news.py            # Step 1: News collection
│   ├── curate_content.py          # Step 2: AI curation
│   ├── generate_webpage.py        # Step 3: HTML generation
│   └── deploy_github.py           # Step 4: Deployment
│
├── data/                          # Generated data
│   ├── raw_news_YYYYMMDD.json    # Collected items
│   └── curated_YYYYMMDD.json     # Claude's curation
│
├── output/                        # Generated website
│   ├── index.html                # Current digest
│   └── digest-YYYYMMDD.html      # Archive pages
│
└── .github/
    └── workflows/
        └── weekly-digest.yml      # GitHub Actions
```

---

## 🔍 Data Flow Example

### Sunday, 6:00 PM:

**1. Collect (5 minutes)**
```
arXiv: 28 papers → raw_news_20251215.json
Hacker News: 12 stories → raw_news_20251215.json
Reddit: 15 posts → raw_news_20251215.json
Total: 55 items
```

**2. Curate (2 minutes)**
```
Claude receives 55 items
Filters for agentic AI relevance
Selects 18 best items
Categorizes into sections
Generates insights + summary
→ curated_20251215.json
```

**3. Generate (30 seconds)**
```
Creates index.html with:
- Header with date
- Weekly summary
- 3 colored sections
- 18 content cards
- Archive of last 5 weeks

Creates digest-20251215.html
→ output/
```

**4. Deploy (1 minute)**
```
Git operations in output/
Force push to gh-pages
→ Live at EiriniOr.github.io/ai-weekly-digest
```

**Total time**: ~8 minutes, fully automated

---

## 🎨 Design Elements

### Colors:
- **Background**: Purple-blue gradient (#0f0c29 → #302b63 → #24243e)
- **Research**: Purple (#9B59B6)
- **Industry**: Blue (#3498DB)
- **Tools**: Turquoise (#1ABC9C)
- **Text**: White/light gray on dark backgrounds

### Animations:
- Scrolling diagonal pattern (20s loop)
- Card hover effects (lift + glow)
- Archive item slide-right on hover

### Typography:
- **Headers**: 3rem gradient text
- **Content**: 1.1rem sans-serif
- **Insights**: 1rem with line spacing
- **Meta**: 0.9rem italic gray

---

## 🚀 Manual Run

To generate manually (for testing):

```bash
cd /Users/rena/ai-weekly-digest

# Set API key
export ANTHROPIC_API_KEY="your-key-here"

# Run the full pipeline
python3 generate_weekly_digest.py

# Or run steps individually:
python3 scripts/collect_news.py      # Step 1
python3 scripts/curate_content.py    # Step 2
python3 scripts/generate_webpage.py  # Step 3
python3 scripts/deploy_github.py     # Step 4
```

---

## 🔧 Customization

### Change Schedule:
Edit `.github/workflows/weekly-digest.yml`:
```yaml
cron: '0 18 * * 0'  # Sunday 6 PM
      '0 12 * * 1'  # Monday noon
      '0 9 * * 3'   # Wednesday 9 AM
```

### Change Content Focus:
Edit `config.yaml`:
```yaml
focus_topics:
  - "Your custom topic"
  - "Another focus area"
```

### Change Design:
Edit `scripts/generate_webpage.py`:
```python
section_colors = {
    "Key Research Papers": "#YOUR_COLOR",
    "Industry Updates": "#YOUR_COLOR"
}
```

---

## 🎯 Why This Works

**1. Automated Curation**
- No manual filtering needed
- Claude understands context
- Consistent quality

**2. Beautiful Design**
- Futuristic aesthetic
- Professional appearance
- Mobile-responsive

**3. Zero Maintenance**
- Runs automatically
- Self-deploying
- Scales indefinitely

**4. Full Control**
- All code on GitHub
- Easy to customize
- Complete ownership

---

**Last Updated**: December 15, 2025
**Live**: https://EiriniOr.github.io/ai-weekly-digest/
**GitHub**: https://github.com/EiriniOr/ai-weekly-digest

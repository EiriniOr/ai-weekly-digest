# AI Weekly Digest - Workflow

## Complete Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                     SUNDAY 9:00 AM                              │
│                  (Automated via launchd)                        │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 1: COLLECT NEWS                                           │
│  Script: scripts/collect_news.py                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📚 arXiv Research Papers                                       │
│     • cs.AI (Artificial Intelligence)                           │
│     • cs.LG (Machine Learning)                                  │
│     • cs.CL (Computation and Language)                          │
│     → Last 7 days, max 10 papers per category                  │
│                                                                 │
│  🔥 Hacker News                                                 │
│     • Keywords: "agentic ai", "ai agents", "llm"               │
│     • Min score: 50 points                                      │
│     → Top 100 stories, filter to max 15                        │
│                                                                 │
│  💬 Reddit                                                      │
│     • r/MachineLearning                                         │
│     • r/LocalLLaMA                                              │
│     • r/artificial                                              │
│     → Top posts from week, min 100 upvotes                     │
│                                                                 │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
                  ┌─────────────────┐
                  │  data/raw_news_ │
                  │  YYYYMMDD.json  │
                  └────────┬────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 2: CURATE CONTENT                                         │
│  Script: scripts/curate_content.py                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  🧠 Claude Sonnet 4.5 Analysis                                  │
│     • Filters for agentic AI relevance                          │
│     • Categorizes into sections:                                │
│       - Key Research Papers (5 items)                           │
│       - Industry Updates (5 items)                              │
│       - Tools & Frameworks (4 items)                            │
│       - Notable Discussions (4 items)                           │
│                                                                 │
│  Focus Topics:                                                  │
│     ✓ Autonomous agents                                         │
│     ✓ Multi-agent systems                                       │
│     ✓ Tool use & function calling                               │
│     ✓ Reasoning & planning                                      │
│     ✓ Memory systems                                            │
│     ✓ Agent frameworks                                          │
│                                                                 │
│  For each item:                                                 │
│     • Assigns to best section                                   │
│     • Generates insight summary                                 │
│     • Scores relevance (1-10)                                   │
│     • Selects top items per section                             │
│                                                                 │
│  Also creates:                                                  │
│     • Weekly summary (2-3 sentences)                            │
│     • Major themes identification                               │
│                                                                 │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
                  ┌─────────────────┐
                  │ data/curated_   │
                  │ YYYYMMDD.json   │
                  └────────┬────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 3: GENERATE PRESENTATION                                  │
│  Script: scripts/generate_presentation.py                       │
│  Uses: PowerPoint MCP Server (36 tools)                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Slide 1: Title Slide                                           │
│     • "Weekly Agentic AI Digest"                                │
│     • "Week of [date]"                                          │
│                                                                 │
│  Slide 2: Weekly Summary                                        │
│     • "This Week in Agentic AI"                                 │
│     • Major themes and trends                                   │
│     • Metadata (sources, date)                                  │
│                                                                 │
│  Slides 3-N: Content Sections                                   │
│     For each section:                                           │
│       → Section divider slide                                   │
│       → Individual item slides with:                            │
│          • Title                                                │
│          • Key insight                                          │
│          • Source metadata                                      │
│          • URL link                                             │
│                                                                 │
│  Final Slide: Keep Learning                                     │
│     • Sources summary                                           │
│     • Next digest date                                          │
│                                                                 │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
                  ┌─────────────────┐
                  │   Downloads/    │
                  │ AI_Weekly_      │
                  │ YYYY-MM-DD.pptx │
                  └─────────────────┘
                            │
                            ▼
                    📧 (Optional)
                   Email delivery
```

## Data Flow Details

### Collection Phase
- **Duration**: ~30-60 seconds
- **Output**: JSON file with all raw items
- **Size**: Typically 20-50 items total

### Curation Phase
- **Duration**: ~10-20 seconds (Claude API call)
- **Output**: JSON file with curated selections
- **Size**: Exactly 18 items (5+5+4+4 across sections)
- **Cost**: ~$0.01-0.05 per week

### Generation Phase
- **Duration**: ~5-10 seconds
- **Output**: PowerPoint presentation
- **Size**: 20-25 slides typically

## Customization Points

| Component | File | What to Change |
|-----------|------|----------------|
| News sources | `config.yaml` | Enable/disable sources, adjust limits |
| Focus topics | `config.yaml` | Topics for Claude to prioritize |
| Schedule | `com.aiweekly.digest.plist` | Day/time for automation |
| Presentation design | `scripts/generate_presentation.py` | Use different MCP tools |
| Content categories | `scripts/curate_content.py` | Section names and counts |

## Error Handling

Each step is independent and saves its output:

```
collect_news.py fails
   ↓
   ❌ No raw_news file created
   ⚠️  Can't run curate_content.py
   💡 Fix: Check internet, API access

curate_content.py fails
   ↓
   ❌ No curated file created
   ⚠️  Can't run generate_presentation.py
   💡 Fix: Check ANTHROPIC_API_KEY

generate_presentation.py fails
   ↓
   ❌ No presentation created
   ⚠️  But curated data exists
   💡 Fix: Check MCP server, retry generation
```

View detailed logs at: `logs/stdout.log` and `logs/stderr.log`

## Performance

**Total Runtime**: ~45-90 seconds end-to-end

- Collection: 30-60s (network I/O bound)
- Curation: 10-20s (Claude API call)
- Generation: 5-10s (local PowerPoint creation)

**Resource Usage**:
- CPU: Minimal (mostly I/O waiting)
- Memory: ~100-200 MB
- Disk: ~1-2 MB per week (JSON + PPTX)
- Network: ~5-10 MB download

**Cost**:
- Claude API: ~$0.01-0.05/week
- Storage: negligible
- Bandwidth: negligible

## Directory Structure After First Run

```
ai-weekly-digest/
├── data/
│   ├── raw_news_20251214.json      (collected items)
│   └── curated_20251214.json       (curated selections)
│
├── logs/
│   ├── stdout.log                  (automation output)
│   └── stderr.log                  (errors)
│
└── ~/Downloads/
    └── AI_Weekly_2025-12-14.pptx   (final presentation)
```

## Integration Options

### Email Delivery

Add to `generate_presentation.py`:

```python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

# After presentation generation
send_email(filepath)
```

### Slack Notification

Add webhook call:

```python
import requests

requests.post(webhook_url, json={
    'text': f'Your weekly AI digest is ready! {filepath}'
})
```

### Cloud Storage

Use `rclone` or cloud APIs:

```python
# Upload to Dropbox/Google Drive
upload_to_cloud(filepath)
```

## Monitoring

Check automation status:

```bash
# Is it running?
launchctl list | grep aiweekly

# Recent runs
cat logs/stdout.log

# Recent errors
cat logs/stderr.log

# Force run now (for testing)
launchctl start com.aiweekly.digest
```

## Weekly Workflow (User Perspective)

```
Saturday night
   ↓
   😴 Go to sleep

Sunday 9:00 AM
   ↓
   🤖 System runs automatically
   ↓
   (you're having breakfast)

Sunday 9:02 AM
   ↓
   ✅ Presentation ready in Downloads

Sunday morning
   ↓
   📖 Open presentation
   ↓
   🧠 Learn about agentic AI
   ↓
   🚀 Stay up to date!
```

Completely hands-off! 🎉

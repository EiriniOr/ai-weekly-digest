# 🏗️ Technical Architecture - AI Weekly Digest

## Where Does Everything Run?

### Two Execution Environments:

```
┌──────────────────────────────────────────────────────────────┐
│  OPTION 1: GitHub Actions (Cloud) - RECOMMENDED             │
├──────────────────────────────────────────────────────────────┤
│  • Runs on: GitHub's Ubuntu servers (free)                   │
│  • Triggered: Every Sunday at 6 PM UTC (cron)               │
│  • Your laptop: Can be OFF ✅                                │
│  • Cost: $0 (included in free tier)                         │
│  • Setup: Add ANTHROPIC_API_KEY to GitHub Secrets           │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  OPTION 2: Local Execution (Your Mac)                       │
├──────────────────────────────────────────────────────────────┤
│  • Runs on: Your MacBook Pro                                 │
│  • Triggered: macOS launchd (cron equivalent)               │
│  • Your laptop: Must be ON at 6 PM Sunday ❌                │
│  • Cost: $0                                                  │
│  • Setup: launchd plist file                                │
└──────────────────────────────────────────────────────────────┘
```

**You're currently using**: GitHub Actions (cloud-based) ✅

---

## 📦 Python Module Structure

### File Organization:

```python
ai-weekly-digest/
│
├── generate_weekly_digest.py      # MAIN ORCHESTRATOR
│   └── Imports and coordinates all modules
│
├── scripts/
│   ├── __init__.py               # (implicit) Makes it a Python package
│   ├── collect_news.py           # MODULE 1: News collection
│   ├── curate_content.py         # MODULE 2: AI curation
│   ├── generate_webpage.py       # MODULE 3: HTML generation
│   └── deploy_github.py          # MODULE 4: Git deployment
│
├── data/                         # DATA STORAGE (created at runtime)
│   ├── raw_news_YYYYMMDD.json   # Output from Module 1
│   └── curated_YYYYMMDD.json    # Output from Module 2
│
└── output/                       # WEB OUTPUT (created at runtime)
    ├── index.html               # Output from Module 3
    └── digest-*.html            # Archive pages from Module 3
```

---

## 🔗 How Modules Connect

### The Orchestrator Pattern:

```python
# generate_weekly_digest.py (Line 13-18)

# Step 1: Import path configuration
sys.path.insert(0, str(Path(__file__).parent / "scripts"))
#             └─> Adds /Users/rena/ai-weekly-digest/scripts to Python's search path

# Step 2: Import all modules
from collect_news import AINewsCollector      # Class from Module 1
from curate_content import ContentCurator     # Class from Module 2
from generate_webpage import WebpageGenerator # Class from Module 3
from deploy_github import deploy_to_github    # Function from Module 4
```

**What `sys.path.insert()` does**:
- Python normally can't find modules in subdirectories
- This tells Python: "Also look in the scripts/ folder for imports"
- Now we can do `from collect_news import ...` instead of `from scripts.collect_news import ...`

---

## 🔄 Data Flow Between Modules

### Step 1 → Step 2: File-based communication

```python
# MODULE 1: collect_news.py (saves data)
class AINewsCollector:
    async def collect_all(self):
        # Collect from APIs...
        all_news = {...}

        # Save to file
        output_file = self.data_dir / f"raw_news_{date}.json"
        with open(output_file, 'w') as f:
            json.dump(all_news, f, indent=2)

        return all_news  # Also returns in-memory


# MODULE 2: curate_content.py (reads data)
class ContentCurator:
    def get_latest_raw_data(self):
        # Find most recent file
        data_files = sorted(self.data_dir.glob("raw_news_*.json"), reverse=True)

        # Load it
        with open(data_files[0]) as f:
            return json.load(f)
```

**Why use files instead of passing data directly?**
- ✅ Persistence: Can re-run step 2 without re-running step 1
- ✅ Debugging: Can inspect raw data between steps
- ✅ Fault tolerance: If step 2 fails, step 1 data is saved
- ✅ Manual override: You can edit raw data before curation

---

## 🎭 Async/Await Pattern

### Why Everything is `async`?

```python
# Without async (blocking - SLOW):
def collect_all():
    papers = collect_arxiv()      # Wait 5 seconds
    stories = collect_hackernews() # Wait 5 seconds
    posts = collect_reddit()       # Wait 5 seconds
    # Total: 15 seconds (sequential)


# With async (concurrent - FAST):
async def collect_all():
    results = await asyncio.gather(
        self.collect_arxiv(),      # All run
        self.collect_hackernews(), # at the
        self.collect_reddit()      # same time!
    )
    # Total: 5 seconds (parallel)
```

**Technical details**:
- `async def` = This function can pause and resume
- `await` = Pause here until operation completes
- `asyncio.gather()` = Run multiple async operations concurrently
- Each API call runs in parallel while waiting for HTTP responses

---

## 🔌 API Integrations

### 1. arXiv API (No Auth Required)

```python
# collect_news.py (Line 41)
url = f"http://export.arxiv.org/api/query?search_query=cat:{category}&sortBy=submittedDate&sortOrder=descending&max_results={max_papers}"

feed = feedparser.parse(url)
# Uses feedparser library to parse RSS/Atom feeds
```

**Request**:
```http
GET http://export.arxiv.org/api/query?search_query=cat:cs.AI&max_results=30
```

**Response** (simplified):
```xml
<feed>
  <entry>
    <title>Multi-Agent Planning Framework</title>
    <summary>We propose a novel approach...</summary>
    <link href="https://arxiv.org/abs/2025.12345"/>
    <author><name>John Smith</name></author>
    <published>2025-12-10T00:00:00Z</published>
  </entry>
</feed>
```

### 2. Hacker News API (No Auth Required)

```python
# collect_news.py (Line 75-83)

# Step 1: Get top story IDs
top_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
response = requests.get(top_url)
story_ids = response.json()  # [34567, 34568, 34569, ...]

# Step 2: Fetch each story individually
for story_id in story_ids[:100]:
    story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
    story_data = requests.get(story_url).json()
```

**Request 1**:
```http
GET https://hacker-news.firebaseio.com/v0/topstories.json
```

**Response 1**:
```json
[34567890, 34567891, 34567892, ...]
```

**Request 2** (for each ID):
```http
GET https://hacker-news.firebaseio.com/v0/item/34567890.json
```

**Response 2**:
```json
{
  "by": "username",
  "descendants": 42,
  "id": 34567890,
  "score": 234,
  "time": 1702656000,
  "title": "New AI agent framework released",
  "type": "story",
  "url": "https://example.com"
}
```

### 3. Reddit JSON API (No Auth Required)

```python
# collect_news.py (Line 117-122)

url = f"https://www.reddit.com/r/{subreddit}/top.json?t=week&limit={max_items}"
headers = {'User-Agent': 'AIWeeklyDigest/1.0'}
# User-Agent is required by Reddit's API

response = requests.get(url, headers=headers)
data = response.json()
```

**Request**:
```http
GET https://www.reddit.com/r/MachineLearning/top.json?t=week&limit=10
User-Agent: AIWeeklyDigest/1.0
```

**Response**:
```json
{
  "data": {
    "children": [
      {
        "data": {
          "title": "[D] Best practices for agent architectures",
          "score": 145,
          "num_comments": 42,
          "permalink": "/r/MachineLearning/comments/abc123/...",
          "author": "ml_researcher",
          "created_utc": 1702656000
        }
      }
    ]
  }
}
```

### 4. Claude API (Requires API Key)

```python
# curate_content.py (Line 114-118)

self.client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

message = self.client.messages.create(
    model="claude-sonnet-4-5-20251029",
    max_tokens=4000,
    messages=[{"role": "user", "content": prompt}]
)

response_text = message.content[0].text
```

**Request** (SDK handles this):
```http
POST https://api.anthropic.com/v1/messages
Content-Type: application/json
x-api-key: sk-ant-api03-...

{
  "model": "claude-sonnet-4-5-20251029",
  "max_tokens": 4000,
  "messages": [
    {
      "role": "user",
      "content": "You are curating a weekly digest..."
    }
  ]
}
```

**Response**:
```json
{
  "id": "msg_...",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "{\"sections\": {...}, \"weekly_summary\": \"...\"}"
    }
  ],
  "model": "claude-sonnet-4-5-20251029",
  "usage": {
    "input_tokens": 2500,
    "output_tokens": 1200
  }
}
```

---

## 🎯 Class-Based Architecture

### Why Classes Instead of Functions?

```python
# BAD: Repeating configuration everywhere
def collect_arxiv():
    config = load_config()  # Load again
    data_dir = Path("data") # Repeat setup
    # ...

def collect_hackernews():
    config = load_config()  # Load again
    data_dir = Path("data") # Repeat setup
    # ...


# GOOD: Class stores shared state
class AINewsCollector:
    def __init__(self):
        self.config = load_config()      # Load once
        self.data_dir = Path("data")     # Setup once
        self.today = datetime.now()      # Shared

    async def collect_arxiv(self):
        # Use self.config, self.data_dir

    async def collect_hackernews(self):
        # Use self.config, self.data_dir
```

**Benefits**:
- **Shared state**: Config loaded once, used everywhere
- **Encapsulation**: All collection logic in one class
- **Testability**: Can mock the class in tests
- **Clarity**: Clear what belongs together

---

## 📝 Configuration Management

### YAML Configuration Pattern:

```python
# Every module follows this pattern:

class SomeModule:
    def __init__(self, config_path: str = "../config.yaml"):
        # 1. Find base directory (works from any location)
        self.base_dir = Path(__file__).parent.parent

        # 2. Build full path to config
        config_file = self.base_dir / "config.yaml"

        # 3. Load YAML
        with open(config_file) as f:
            self.config = yaml.safe_load(f)

        # 4. Access nested config
        self.model = self.config['curation']['model']
```

**Why this works**:
- `Path(__file__)` = Full path to current Python file
- `.parent` = Go up one directory
- `.parent.parent` = Go up two directories (to project root)
- Works whether you run from project root or scripts/ folder

**Example**:
```python
# If running: python3 scripts/collect_news.py
__file__ = "/Users/rena/ai-weekly-digest/scripts/collect_news.py"
Path(__file__).parent = "/Users/rena/ai-weekly-digest/scripts"
Path(__file__).parent.parent = "/Users/rena/ai-weekly-digest"
```

---

## 🚀 GitHub Actions Execution

### What Happens on GitHub's Servers:

```yaml
# .github/workflows/weekly-digest.yml

name: Generate Weekly AI Digest

on:
  schedule:
    - cron: '0 18 * * 0'  # Trigger: Sunday at 6 PM UTC

jobs:
  generate-digest:
    runs-on: ubuntu-latest  # GitHub provides this VM

    steps:
      # 1. Clone your repository
      - name: Checkout repository
        uses: actions/checkout@v3
        # Git clones https://github.com/EiriniOr/ai-weekly-digest
        # Into: /home/runner/work/ai-weekly-digest/ai-weekly-digest

      # 2. Install Python
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
        # Installs: Python 3.11 on the Ubuntu VM

      # 3. Install dependencies
      - name: Install dependencies
        run: |
          pip install --upgrade pip
          pip install anthropic pyyaml requests feedparser
        # Installs Python packages in VM

      # 4. Run your script
      - name: Generate weekly digest
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          # Injects secret from GitHub Secrets
        run: |
          python3 generate_weekly_digest.py
        # Executes: Your main orchestrator script

      # 5. Deploy to GitHub Pages
      - name: Deploy to GitHub Pages
        run: |
          cd output
          git config user.name "GitHub Actions Bot"
          git config user.email "actions@github.com"
          git init
          git checkout -b gh-pages
          git add .
          git commit -m "Update weekly digest - $(date +'%Y-%m-%d')"
          git push -f https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git gh-pages
        # Pushes output/ to gh-pages branch
```

### Step-by-Step Execution:

```
┌─────────────────────────────────────────────────────────────┐
│  GitHub's Server (Ubuntu VM)                                │
├─────────────────────────────────────────────────────────────┤
│  1. Cron trigger fires at Sunday 6 PM UTC                   │
│     └─> GitHub scheduler creates new job                    │
│                                                              │
│  2. Provision Ubuntu VM (fresh, clean environment)          │
│     └─> /home/runner/ directory                             │
│                                                              │
│  3. Clone repository                                         │
│     └─> git clone https://github.com/EiriniOr/...           │
│     └─> Into: /home/runner/work/ai-weekly-digest/           │
│                                                              │
│  4. Install Python 3.11                                      │
│     └─> apt-get install python3.11                          │
│                                                              │
│  5. Install pip packages                                     │
│     └─> pip install anthropic pyyaml requests feedparser    │
│                                                              │
│  6. Set environment variable                                 │
│     └─> export ANTHROPIC_API_KEY="sk-ant-..."               │
│                                                              │
│  7. Execute: python3 generate_weekly_digest.py              │
│     ├─> collect_news.py runs (API calls from VM)            │
│     ├─> curate_content.py runs (Claude API call)            │
│     ├─> generate_webpage.py runs (creates HTML)             │
│     └─> deploy_github.py runs (git push)                    │
│                                                              │
│  8. Git push to gh-pages branch                              │
│     └─> GitHub Pages auto-deploys                           │
│                                                              │
│  9. VM destroyed (cleanup)                                   │
└─────────────────────────────────────────────────────────────┘
```

**Total runtime**: ~8 minutes
**Cost**: $0 (free tier includes 2,000 minutes/month)

---

## 🌐 Deployment Mechanism

### How Git Deployment Works:

```python
# scripts/deploy_github.py (simplified)

async def deploy(self, html_path: str) -> bool:
    # 1. Initialize git in output/ folder
    subprocess.run(['git', 'init'], cwd=self.output_dir)

    # 2. Create/switch to gh-pages branch
    subprocess.run(['git', 'checkout', '-B', 'gh-pages'], cwd=self.output_dir)

    # 3. Stage all files
    subprocess.run(['git', 'add', '.'], cwd=self.output_dir)

    # 4. Commit
    date_str = datetime.now().strftime('%Y-%m-%d')
    subprocess.run(
        ['git', 'commit', '-m', f'Update weekly digest - {date_str}'],
        cwd=self.output_dir
    )

    # 5. Force push to remote
    repo_url = f"https://github.com/{repo}.git"
    subprocess.run(
        ['git', 'push', '-f', 'origin', 'gh-pages'],
        cwd=self.output_dir
    )
```

### What Happens in the output/ Directory:

```bash
# Before deploy:
output/
├── index.html
└── digest-20251215.html

# After git init:
output/
├── .git/              # Git repository created
├── index.html
└── digest-20251215.html

# After git push:
# Files are pushed to gh-pages branch on GitHub
# GitHub Pages serves files from this branch
```

### GitHub Pages Hosting:

```
┌─────────────────────────────────────────────────────────────┐
│  GitHub Repository                                          │
├─────────────────────────────────────────────────────────────┤
│  Branch: main                                                │
│  └─> Python scripts, config, etc.                           │
│                                                              │
│  Branch: gh-pages (special branch for GitHub Pages)         │
│  ├─> index.html                                             │
│  └─> digest-*.html                                          │
│      │                                                       │
│      └─> Automatically served at:                           │
│          https://EiriniOr.github.io/ai-weekly-digest/       │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔐 Environment Variables

### How API Keys Are Handled:

```python
# In your code:
api_key = os.environ.get("ANTHROPIC_API_KEY")

# os.environ is a dictionary of environment variables
# Example: os.environ = {
#   "HOME": "/Users/rena",
#   "USER": "rena",
#   "ANTHROPIC_API_KEY": "sk-ant-api03-..."
# }
```

### Local Execution:

```bash
# Option 1: Export in terminal
export ANTHROPIC_API_KEY="sk-ant-api03-..."
python3 generate_weekly_digest.py

# Option 2: Inline
ANTHROPIC_API_KEY="sk-ant-api03-..." python3 generate_weekly_digest.py

# Option 3: Load from .env file (if using python-dotenv)
# .env file:
# ANTHROPIC_API_KEY=sk-ant-api03-...
```

### GitHub Actions:

```yaml
# Workflow file:
env:
  ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
  # ${{ secrets.X }} fetches from GitHub Secrets

# GitHub Secrets are set in:
# Repository Settings → Secrets and variables → Actions
```

**Why this is secure**:
- ✅ Never committed to git
- ✅ Encrypted at rest in GitHub
- ✅ Only injected at runtime
- ✅ Not visible in logs

---

## 📊 Data Persistence

### File-Based State Management:

```python
# Directory structure after one run:

ai-weekly-digest/
├── data/
│   ├── raw_news_20251215.json      # Step 1 output
│   └── curated_20251215.json       # Step 2 output
│
└── output/
    ├── index.html                   # Step 3 output (current)
    └── digest-20251215.html         # Step 3 output (archive)
```

### Why This Design?

**Advantages**:
- ✅ **Resumable**: Can restart from any step
- ✅ **Debuggable**: Inspect intermediate outputs
- ✅ **Auditable**: Historical record of all runs
- ✅ **Fault-tolerant**: Step failures don't lose earlier work

**Example**:
```bash
# First attempt - fails at step 3
python3 generate_weekly_digest.py
# Steps 1 & 2 complete, data saved
# Step 3 fails due to HTML bug

# Fix the bug in generate_webpage.py

# Second attempt - skips step 1 & 2
python3 scripts/generate_webpage.py
# Uses existing curated_20251215.json
# No need to re-collect or re-curate
```

---

## 🔄 Error Handling

### Try-Except Pattern:

```python
# generate_weekly_digest.py (Line 70-79)

try:
    # Run all steps
    collector = AINewsCollector()
    news_data = await collector.collect_all()
    # ... more steps

except FileNotFoundError as e:
    # Specific error: missing file
    print(f"\n❌ Error: {e}")
    print("   Make sure to run the steps in order.")

except Exception as e:
    # Generic error: anything else
    print(f"\n❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()  # Print full stack trace
```

### Async Error Handling:

```python
# collect_news.py (Line 149-167)

# Run collectors concurrently
results = await asyncio.gather(
    self.collect_arxiv(),
    self.collect_hackernews(),
    self.collect_reddit(),
    return_exceptions=True  # Don't fail if one fails
)

# Handle exceptions individually
if isinstance(papers, Exception):
    print(f"arXiv error: {papers}")
    papers = []  # Continue with empty list
```

**Why `return_exceptions=True`?**
- Without it: If any collector fails, all fail
- With it: Failed collectors return Exception objects, successful ones return data
- Allows partial success (e.g., if Reddit is down, still use arXiv + HN)

---

## 🧵 Async Concurrency Model

### How `asyncio` Works Internally:

```python
# Simplified conceptual model:

# Single-threaded event loop
while True:
    # 1. Check which operations are ready
    ready_tasks = check_network_sockets()

    # 2. Resume ready tasks
    for task in ready_tasks:
        task.resume()

    # 3. Check if done
    if all_tasks_complete():
        break
```

### Visual Example:

```
Time →

Thread 1 (your code):
├─ Start collect_arxiv()      [Send HTTP request]
│  └─ await response          [Pause, wait for network]
│
├─ Start collect_hackernews() [Send HTTP request]
│  └─ await response          [Pause, wait for network]
│
├─ Start collect_reddit()     [Send HTTP request]
│  └─ await response          [Pause, wait for network]
│
│  [All three HTTP requests are now in flight]
│  [Event loop waits for any to complete]
│
├─ arXiv responds             [Resume collect_arxiv]
│  └─ Parse and return
│
├─ HN responds                [Resume collect_hackernews]
│  └─ Parse and return
│
└─ Reddit responds            [Resume collect_reddit]
   └─ Parse and return

Total time: ~5 seconds (overlapping)
```

**Key concepts**:
- **Single-threaded**: Still one Python thread
- **Non-blocking I/O**: Doesn't wait idly for network
- **Event loop**: Manages which coroutine to run next
- **Cooperative multitasking**: Code explicitly yields control with `await`

---

## 📦 Dependency Management

### Required Python Packages:

```bash
# Installed in GitHub Actions:
pip install anthropic pyyaml requests feedparser
```

### What Each Does:

```python
# 1. anthropic - Claude API client
from anthropic import Anthropic
client = Anthropic(api_key="...")
response = client.messages.create(...)

# 2. pyyaml - YAML configuration parser
import yaml
with open("config.yaml") as f:
    config = yaml.safe_load(f)

# 3. requests - HTTP requests
import requests
response = requests.get("https://api.example.com")
data = response.json()

# 4. feedparser - RSS/Atom feed parser
import feedparser
feed = feedparser.parse("https://export.arxiv.org/api/query?...")
for entry in feed.entries:
    print(entry.title)
```

### Standard Library (No Install):

```python
import asyncio      # Async/await support
import json         # JSON parsing
import subprocess   # Run shell commands
from pathlib import Path  # File path handling
from datetime import datetime  # Date/time
import os          # Environment variables
```

---

## 🎯 Summary: Complete Execution Flow

```python
# 1. GitHub Actions triggers at Sunday 6 PM UTC

# 2. VM provisions and clones repository

# 3. Python script starts:
async def generate_weekly_digest():

    # 4. Module 1: Collect (parallel API calls)
    collector = AINewsCollector()
    news_data = await collector.collect_all()
    # → Saves: data/raw_news_20251215.json

    # 5. Module 2: Curate (Claude API call)
    curator = ContentCurator()
    curated_data = await curator.curate()
    # → Reads: data/raw_news_20251215.json
    # → Saves: data/curated_20251215.json

    # 6. Module 3: Generate (HTML creation)
    generator = WebpageGenerator()
    filepath = await generator.generate()
    # → Reads: data/curated_20251215.json
    # → Saves: output/index.html + archive pages

    # 7. Module 4: Deploy (Git push)
    github_deployed = await deploy_to_github(filepath)
    # → Pushes output/ to gh-pages branch

# 8. GitHub Pages auto-deploys

# 9. Live at: https://EiriniOr.github.io/ai-weekly-digest/
```

---

## 🔍 Key Takeaways

### Design Principles:

1. **Modularity**: Each script has one job
2. **Persistence**: Save state between steps
3. **Fault tolerance**: Steps can be re-run independently
4. **Async**: Concurrent API calls for speed
5. **Configuration**: YAML file for easy changes
6. **Cloud execution**: GitHub Actions for automation
7. **File-based communication**: JSON between modules

### Technology Stack:

- **Language**: Python 3.11
- **Async**: asyncio for concurrency
- **APIs**: arXiv, Hacker News, Reddit, Claude
- **Storage**: File system (JSON)
- **Deployment**: Git + GitHub Pages
- **Automation**: GitHub Actions (cron)
- **Hosting**: GitHub Pages (free)

### Where Things Run:

- **Code execution**: GitHub's Ubuntu VM (cloud)
- **Website hosting**: GitHub Pages (CDN)
- **Data storage**: Git repository
- **API calls**: From GitHub's servers

---

**Questions to explore:**

1. Want to see how a specific API integration works?
2. Curious about async/await patterns?
3. Need help debugging a module?
4. Want to add a new data source?

Let me know what you'd like to dive deeper into!

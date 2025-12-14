#!/usr/bin/env python3
"""
Content Curator
Uses Claude to filter, categorize, and summarize AI news for the weekly digest
"""

import asyncio
import json
import yaml
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import anthropic
import os

class ContentCurator:
    def __init__(self, config_path: str = "../config.yaml"):
        self.base_dir = Path(__file__).parent.parent
        config_file = self.base_dir / "config.yaml"

        with open(config_file) as f:
            self.config = yaml.safe_load(f)

        self.data_dir = self.base_dir / "data"
        self.client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    def get_latest_raw_data(self) -> Dict[str, Any]:
        """Load the most recent raw news data"""
        data_files = sorted(self.data_dir.glob("raw_news_*.json"), reverse=True)

        if not data_files:
            raise FileNotFoundError("No raw news data found. Run collect_news.py first.")

        with open(data_files[0]) as f:
            return json.load(f)

    async def categorize_and_summarize(self, news_data: Dict[str, Any]) -> Dict[str, Any]:
        """Use Claude to intelligently categorize and summarize the news"""
        print("🧠 Using Claude to curate content...\n")

        focus_topics = self.config['curation']['focus_topics']
        sections = self.config['presentation']['sections']

        # Prepare the news items for Claude
        all_items = []

        # Add papers
        for paper in news_data['papers']:
            all_items.append({
                'type': 'paper',
                'title': paper['title'],
                'summary': paper['summary'][:200],
                'url': paper['url'],
                'meta': f"arXiv • {', '.join(paper['authors'])}"
            })

        # Add HN stories
        for story in news_data['hackernews']:
            all_items.append({
                'type': 'news',
                'title': story['title'],
                'url': story['url'],
                'meta': f"Hacker News • {story['score']} points • {story['comments']} comments"
            })

        # Add Reddit posts
        for post in news_data['reddit']:
            all_items.append({
                'type': 'discussion',
                'title': post['title'],
                'url': post['url'],
                'meta': f"r/{post['subreddit']} • {post['score']} upvotes • {post['comments']} comments"
            })

        # Create prompt for Claude
        prompt = f"""You are curating a weekly digest focused on **agentic AI** - autonomous AI agents, multi-agent systems, tool use, planning, and reasoning.

Focus topics: {', '.join(focus_topics)}

I have {len(all_items)} items from this week. Please:

1. Filter to the most relevant items about agentic AI and agent capabilities
2. Categorize them into these sections:
   - Key Research Papers (breakthroughs, novel architectures)
   - Industry Updates (product launches, company news)
   - Tools & Frameworks (new agent frameworks, libraries)
   - Notable Discussions (insights, debates, analyses)

3. For each selected item, provide:
   - Section assignment
   - One-sentence insight (what makes it important/interesting)
   - Relevance score (1-10)

4. Select the TOP items per section: {', '.join([f"{s['name']}: {s['max_items']}" for s in sections])}

Here are the items:

{json.dumps(all_items, indent=2)}

Return ONLY a valid JSON object with this structure:
{{
  "sections": {{
    "Key Research Papers": [
      {{"title": "...", "url": "...", "meta": "...", "insight": "...", "score": 9}}
    ],
    "Industry Updates": [...],
    "Tools & Frameworks": [...],
    "Notable Discussions": [...]
  }},
  "weekly_summary": "2-3 sentence summary of the week's major themes"
}}"""

        # Call Claude
        message = self.client.messages.create(
            model=self.config['curation']['model'],
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = message.content[0].text

        # Parse JSON response
        try:
            # Find JSON in response (in case Claude adds explanation)
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            json_str = response_text[json_start:json_end]

            curated = json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"Error parsing Claude response: {e}")
            print(f"Response: {response_text}")
            raise

        # Save curated content
        output_file = self.data_dir / f"curated_{datetime.now().strftime('%Y%m%d')}.json"
        with open(output_file, 'w') as f:
            json.dump(curated, f, indent=2)

        # Print summary
        print("✅ Content curated successfully!\n")
        print(f"Weekly theme: {curated['weekly_summary']}\n")

        for section_name, items in curated['sections'].items():
            print(f"  {section_name}: {len(items)} items")

        print(f"\n📁 Saved to: {output_file}")

        return curated

    async def curate(self) -> Dict[str, Any]:
        """Main curation workflow"""
        print("🎯 Starting content curation...\n")

        # Load raw data
        raw_data = self.get_latest_raw_data()
        print(f"📊 Loaded raw data with {len(raw_data['papers']) + len(raw_data['hackernews']) + len(raw_data['reddit'])} items\n")

        # Curate with Claude
        curated = await self.categorize_and_summarize(raw_data)

        return curated

async def main():
    curator = ContentCurator()
    await curator.curate()

if __name__ == "__main__":
    asyncio.run(main())

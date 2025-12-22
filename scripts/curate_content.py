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
        prompt = f"""Curate weekly digest on agentic AI - autonomous agents, multi-agent systems, tool use, planning, reasoning.

Focus topics: {', '.join(focus_topics)}

{len(all_items)} items from this week. Tasks:

1. Filter most relevant items about agentic AI and agent capabilities
2. Categorize into sections:
   - Key Research Papers (breakthroughs, novel architectures)
   - Industry Updates (product launches, company news)
   - Tools & Frameworks (agent frameworks, libraries)
   - Notable Discussions (insights, debates, analyses)

3. For each item provide:
   - Section assignment
   - One-sentence insight (what makes it important/interesting)
   - Relevance score (1-10)

4. Select TOP items per section: {', '.join([f"{s['name']}: {s['max_items']}" for s in sections])}

Items:

{json.dumps(all_items, indent=2)}

CRITICAL: Return ONLY valid JSON. No markdown, no code blocks, no explanatory text. Start with {{ and end with }}.

Structure:
{{
  "sections": {{
    "Key Research Papers": [
      {{"title": "...", "url": "...", "meta": "...", "insight": "...", "score": 9}}
    ],
    "Industry Updates": [],
    "Tools & Frameworks": [],
    "Notable Discussions": []
  }},
  "weekly_summary": "2-3 sentence summary of week's major themes"
}}"""

        # Call Claude with higher token limit for complete JSON
        message = self.client.messages.create(
            model=self.config['curation']['model'],
            max_tokens=16384,  # Increased for large JSON responses
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = message.content[0].text

        # Parse JSON response
        try:
            # Remove ALL markdown code blocks (multiple passes)
            json_str = response_text.strip()

            # Remove opening code fence
            for prefix in ['```json\n', '```json', '```\n', '```']:
                if json_str.startswith(prefix):
                    json_str = json_str[len(prefix):]
                    break

            # Remove closing code fence
            if '\n```' in json_str:
                json_str = json_str[:json_str.rfind('\n```')]
            elif json_str.endswith('```'):
                json_str = json_str[:-3]

            json_str = json_str.strip()

            # Validate we have JSON
            if not json_str.startswith('{'):
                raise ValueError(f"Response doesn't start with '{{': {json_str[:100]}")

            if not json_str.endswith('}'):
                raise ValueError(f"Response doesn't end with '}}': {json_str[-100:]}")

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

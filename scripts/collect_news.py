#!/usr/bin/env python3
"""
AI News Aggregator
Collects AI news from multiple sources for weekly digest
"""

import asyncio
import json
import yaml
from datetime import datetime, timedelta
from pathlib import Path
import feedparser
import requests
from typing import List, Dict, Any

class AINewsCollector:
    def __init__(self, config_path: str = "../config.yaml"):
        self.base_dir = Path(__file__).parent.parent
        config_file = self.base_dir / "config.yaml"

        with open(config_file) as f:
            self.config = yaml.safe_load(f)

        self.data_dir = self.base_dir / "data"
        self.data_dir.mkdir(exist_ok=True)

        self.today = datetime.now()
        self.week_ago = self.today - timedelta(days=7)

    async def collect_arxiv(self) -> List[Dict[str, Any]]:
        """Collect recent AI papers from arXiv"""
        if not self.config['sources']['arxiv']['enabled']:
            return []

        print("📚 Collecting from arXiv...")
        papers = []
        categories = self.config['sources']['arxiv']['categories']
        max_papers = self.config['sources']['arxiv']['max_papers']

        for category in categories:
            url = f"http://export.arxiv.org/api/query?search_query=cat:{category}&sortBy=submittedDate&sortOrder=descending&max_results={max_papers}"

            feed = feedparser.parse(url)

            for entry in feed.entries[:max_papers]:
                published = datetime(*entry.published_parsed[:6])

                if published >= self.week_ago:
                    papers.append({
                        'source': 'arxiv',
                        'title': entry.title,
                        'summary': entry.summary.replace('\n', ' ')[:300],
                        'url': entry.link,
                        'authors': [author.name for author in entry.authors[:3]],
                        'published': published.isoformat(),
                        'category': category
                    })

        print(f"  Found {len(papers)} recent papers")
        return papers

    async def collect_hackernews(self) -> List[Dict[str, Any]]:
        """Collect AI-related stories from Hacker News"""
        if not self.config['sources']['hackernews']['enabled']:
            return []

        print("🔥 Collecting from Hacker News...")
        stories = []
        keywords = self.config['sources']['hackernews']['keywords']
        min_score = self.config['sources']['hackernews']['min_score']
        max_items = self.config['sources']['hackernews']['max_items']

        # Get top stories
        top_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        response = requests.get(top_url, timeout=10)
        story_ids = response.json()[:100]  # Check top 100

        for story_id in story_ids:
            if len(stories) >= max_items:
                break

            story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
            story_data = requests.get(story_url, timeout=5).json()

            if not story_data or 'title' not in story_data:
                continue

            title_lower = story_data['title'].lower()

            # Check if story matches AI keywords
            if any(keyword in title_lower for keyword in keywords):
                if story_data.get('score', 0) >= min_score:
                    stories.append({
                        'source': 'hackernews',
                        'title': story_data['title'],
                        'url': story_data.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                        'score': story_data.get('score', 0),
                        'comments': story_data.get('descendants', 0),
                        'time': datetime.fromtimestamp(story_data['time']).isoformat()
                    })

        print(f"  Found {len(stories)} relevant stories")
        return stories

    async def collect_reddit(self) -> List[Dict[str, Any]]:
        """Collect AI discussions from Reddit"""
        if not self.config['sources']['reddit']['enabled']:
            return []

        print("💬 Collecting from Reddit...")
        posts = []
        subreddits = self.config['sources']['reddit']['subreddits']
        min_score = self.config['sources']['reddit']['min_score']
        max_items = self.config['sources']['reddit']['max_items']

        for subreddit in subreddits:
            url = f"https://www.reddit.com/r/{subreddit}/top.json?t=week&limit={max_items}"
            headers = {'User-Agent': 'AIWeeklyDigest/1.0'}

            try:
                response = requests.get(url, headers=headers, timeout=10)
                data = response.json()

                for post in data['data']['children'][:max_items]:
                    post_data = post['data']

                    if post_data['score'] >= min_score:
                        posts.append({
                            'source': 'reddit',
                            'subreddit': subreddit,
                            'title': post_data['title'],
                            'url': f"https://reddit.com{post_data['permalink']}",
                            'score': post_data['score'],
                            'comments': post_data['num_comments'],
                            'author': post_data['author'],
                            'created': datetime.fromtimestamp(post_data['created_utc']).isoformat()
                        })
            except Exception as e:
                print(f"  Error collecting from r/{subreddit}: {e}")

        print(f"  Found {len(posts)} relevant posts")
        return posts

    async def collect_all(self) -> Dict[str, List[Dict[str, Any]]]:
        """Collect from all enabled sources"""
        print("\n🤖 Starting AI news collection...\n")

        # Run all collectors concurrently
        results = await asyncio.gather(
            self.collect_arxiv(),
            self.collect_hackernews(),
            self.collect_reddit(),
            return_exceptions=True
        )

        papers, hn_stories, reddit_posts = results

        # Handle any exceptions
        if isinstance(papers, Exception):
            print(f"arXiv error: {papers}")
            papers = []
        if isinstance(hn_stories, Exception):
            print(f"HN error: {hn_stories}")
            hn_stories = []
        if isinstance(reddit_posts, Exception):
            print(f"Reddit error: {reddit_posts}")
            reddit_posts = []

        all_news = {
            'papers': papers,
            'hackernews': hn_stories,
            'reddit': reddit_posts,
            'collected_at': self.today.isoformat(),
            'week_start': self.week_ago.isoformat(),
            'week_end': self.today.isoformat()
        }

        # Save raw data
        output_file = self.data_dir / f"raw_news_{self.today.strftime('%Y%m%d')}.json"
        with open(output_file, 'w') as f:
            json.dump(all_news, f, indent=2)

        total = len(papers) + len(hn_stories) + len(reddit_posts)
        print(f"\n✅ Collection complete! Found {total} items")
        print(f"📁 Saved to: {output_file}")

        return all_news

async def main():
    collector = AINewsCollector()
    await collector.collect_all()

if __name__ == "__main__":
    asyncio.run(main())

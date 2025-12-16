#!/usr/bin/env python3
"""
Webpage Generator
Creates a beautiful futuristic webpage for AI Weekly Digest
"""

import asyncio
import json
import yaml
from datetime import datetime
from pathlib import Path
import sys

class WebpageGenerator:
    def __init__(self, config_path: str = "../config.yaml"):
        self.base_dir = Path(__file__).parent.parent
        config_file = self.base_dir / "config.yaml"

        with open(config_file) as f:
            self.config = yaml.safe_load(f)

        self.data_dir = self.base_dir / "data"
        self.output_dir = self.base_dir / "output"
        self.output_dir.mkdir(exist_ok=True)

    def get_latest_curated_data(self):
        """Load the most recent curated content"""
        data_files = sorted(self.data_dir.glob("curated_*.json"), reverse=True)

        if not data_files:
            raise FileNotFoundError("No curated data found. Run curate_content.py first.")

        with open(data_files[0]) as f:
            return json.load(f)

    def get_recent_digests(self, limit=5):
        """Get list of recent digest files"""
        data_files = sorted(self.data_dir.glob("curated_*.json"), reverse=True)
        return data_files[:limit]

    async def create_webpage(self, curated_data):
        """Generate beautiful futuristic webpage"""
        print("🎨 Creating webpage...\n")

        date_str = datetime.now().strftime('%Y-%m-%d')
        week_str = datetime.now().strftime('%B %d, %Y')

        # Get recent digests for archive
        recent_digests = self.get_recent_digests(5)
        archive_html = ""

        for idx, digest_file in enumerate(recent_digests):
            with open(digest_file) as f:
                digest_data = json.load(f)

            digest_date = digest_file.stem.replace('curated_', '')
            formatted_date = datetime.strptime(digest_date, '%Y%m%d').strftime('%B %d, %Y')

            total_items = sum(len(items) for items in digest_data.get('sections', {}).values())

            # Create individual archive page for older digests
            if idx > 0:  # Skip the current week (index 0)
                archive_filename = f"digest-{digest_date}.html"
                await self.create_archive_page(digest_data, digest_date, archive_filename)

                archive_html += f"""
                <a href="{archive_filename}" class="archive-link">
                    <div class="archive-item">
                        <div class="archive-date">{formatted_date}</div>
                        <div class="archive-summary">{digest_data.get('weekly_summary', '')[:150]}...</div>
                        <div class="archive-stats">{total_items} items</div>
                    </div>
                </a>
                """
            else:
                # Current week - not clickable
                archive_html += f"""
                <div class="archive-item current-week">
                    <div class="archive-date">{formatted_date} (Current)</div>
                    <div class="archive-summary">{digest_data.get('weekly_summary', '')[:150]}...</div>
                    <div class="archive-stats">{total_items} items</div>
                </div>
                """

        # Build sections HTML
        sections_html = ""
        sections = curated_data.get('sections', {})

        # Exclude Notable Discussions
        sections = {k: v for k, v in sections.items() if k != "Notable Discussions"}

        section_icons = {
            "Key Research Papers": "🔬",
            "Industry Updates": "🏢",
            "Tools & Frameworks": "🛠️"
        }

        section_colors = {
            "Key Research Papers": "#9B59B6",
            "Industry Updates": "#3498DB",
            "Tools & Frameworks": "#1ABC9C"
        }

        for section_name, items in sections.items():
            if not items:
                continue

            icon = section_icons.get(section_name, "📌")
            color = section_colors.get(section_name, "#5B9BD5")

            items_html = ""
            for item in items:
                title = item['title']
                insight = item.get('insight', '')
                meta = item.get('meta', 'Source unknown')
                url = item.get('url', '')

                url_html = f'<a href="{url}" target="_blank" class="item-link">🔗 Read more</a>' if url else ''

                items_html += f"""
                <div class="content-item">
                    <h3 class="item-title">{title}</h3>
                    <p class="item-insight">{insight}</p>
                    <div class="item-meta">
                        <span class="meta-source">📍 {meta}</span>
                        {url_html}
                    </div>
                </div>
                """

            sections_html += f"""
            <section class="content-section" style="border-left: 4px solid {color}">
                <h2 class="section-title">{icon} {section_name}</h2>
                <div class="section-items">
                    {items_html}
                </div>
            </section>
            """

        # Create HTML
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 AI Weekly Digest - Agentic AI Updates</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: #e0e0e0;
            line-height: 1.6;
            min-height: 100vh;
        }}

        /* Animated background pattern */
        body::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image:
                linear-gradient(45deg, rgba(102, 126, 234, 0.05) 25%, transparent 25%),
                linear-gradient(-45deg, rgba(118, 75, 162, 0.05) 25%, transparent 25%);
            background-size: 60px 60px;
            animation: backgroundScroll 20s linear infinite;
            pointer-events: none;
            z-index: -1;
        }}

        @keyframes backgroundScroll {{
            0% {{
                background-position: 0 0, 0 0;
            }}
            100% {{
                background-position: 60px 60px, -60px 60px;
            }}
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}

        /* Header */
        .header {{
            text-align: center;
            padding: 60px 20px;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.2));
            border-radius: 20px;
            margin-bottom: 40px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }}

        .header h1 {{
            font-size: 3rem;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }}

        .header .subtitle {{
            font-size: 1.2rem;
            color: #b0b0b0;
            margin-bottom: 20px;
        }}

        .header .date {{
            font-size: 1rem;
            color: #888;
        }}

        /* Summary Section */
        .summary {{
            background: rgba(74, 144, 226, 0.1);
            border-left: 4px solid #4A90E2;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 40px;
            backdrop-filter: blur(10px);
        }}

        .summary h2 {{
            color: #4A90E2;
            margin-bottom: 15px;
            font-size: 1.8rem;
        }}

        .summary p {{
            font-size: 1.1rem;
            line-height: 1.8;
            color: #d0d0d0;
        }}

        /* Content Sections */
        .content-section {{
            background: rgba(30, 30, 50, 0.6);
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        }}

        .section-title {{
            font-size: 1.8rem;
            margin-bottom: 25px;
            color: #fff;
        }}

        .section-items {{
            display: grid;
            gap: 20px;
        }}

        .content-item {{
            background: rgba(50, 50, 70, 0.5);
            padding: 20px;
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: transform 0.3s, box-shadow 0.3s;
        }}

        .content-item:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        }}

        .item-title {{
            color: #fff;
            margin-bottom: 10px;
            font-size: 1.2rem;
        }}

        .item-insight {{
            color: #c0c0c0;
            margin-bottom: 15px;
            font-size: 1rem;
        }}

        .item-meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
            font-size: 0.9rem;
        }}

        .meta-source {{
            color: #888;
        }}

        .item-link {{
            color: #4A90E2;
            text-decoration: none;
            transition: color 0.3s;
        }}

        .item-link:hover {{
            color: #667eea;
        }}

        /* Archive Section */
        .archive {{
            background: rgba(30, 30, 50, 0.6);
            padding: 30px;
            border-radius: 15px;
            margin-top: 40px;
            backdrop-filter: blur(10px);
        }}

        .archive h2 {{
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.8rem;
        }}

        .archive-link {{
            text-decoration: none;
            display: block;
            transition: transform 0.3s;
        }}

        .archive-link:hover {{
            transform: translateX(5px);
        }}

        .archive-item {{
            background: rgba(50, 50, 70, 0.5);
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
            border-left: 3px solid #667eea;
            cursor: pointer;
            transition: background 0.3s, box-shadow 0.3s;
        }}

        .archive-link .archive-item:hover {{
            background: rgba(70, 70, 90, 0.7);
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }}

        .archive-item.current-week {{
            border-left: 3px solid #4A90E2;
            cursor: default;
        }}

        .archive-date {{
            color: #4A90E2;
            font-weight: bold;
            margin-bottom: 5px;
        }}

        .archive-summary {{
            color: #b0b0b0;
            font-size: 0.95rem;
            margin-bottom: 8px;
        }}

        .archive-stats {{
            color: #888;
            font-size: 0.85rem;
        }}

        /* Footer */
        .footer {{
            text-align: center;
            padding: 40px 20px;
            color: #888;
            margin-top: 60px;
        }}

        .footer a {{
            color: #667eea;
            text-decoration: none;
        }}

        .footer a:hover {{
            color: #4A90E2;
        }}

        /* Responsive */
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 2rem;
            }}

            .content-item {{
                padding: 15px;
            }}

            .item-meta {{
                flex-direction: column;
                align-items: flex-start;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>🤖 AI Weekly Digest</h1>
            <p class="subtitle">Your curated agentic AI updates</p>
            <p class="date">Week of {week_str}</p>
        </div>

        <!-- Summary -->
        <div class="summary">
            <h2>📊 This Week's Highlights</h2>
            <p>{curated_data.get('weekly_summary', 'Your weekly AI digest')}</p>
        </div>

        <!-- YouTube Video -->
        <div class="video-container" style="margin: 40px 0; text-align: center;">
            <h2 style="margin-bottom: 20px;">📺 Watch This Week's Video</h2>
            <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 800px; margin: 0 auto; border-radius: 12px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);">
                <iframe
                    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; border-radius: 12px;"
                    src="https://www.youtube.com/embed?listType=playlist&list=UUUPSLoXvaMVbOIaXsOorHng"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowfullscreen>
                </iframe>
            </div>
            <p style="margin-top: 15px; font-size: 14px; opacity: 0.8;">
                <a href="https://www.youtube.com/channel/UCUPSLoXvaMVbOIaXsOorHng" target="_blank" style="color: #9B59B6; text-decoration: none;">
                    Subscribe to our channel →
                </a>
            </p>
        </div>

        <!-- Content Sections -->
        {sections_html}

        <!-- Archive -->
        <div class="archive">
            <h2>📅 Recent Editions</h2>
            {archive_html}
        </div>

        <!-- Footer -->
        <div class="footer">
            <p>🔬 Curated from arXiv, Hacker News, and Reddit</p>
            <p>Automatically generated every Sunday at 6:00 PM</p>
            <p style="margin-top: 20px;">
                <a href="https://www.youtube.com/channel/UCUPSLoXvaMVbOIaXsOorHng" target="_blank" style="margin-right: 20px;">📺 Watch on YouTube</a>
                <a href="https://github.com/EiriniOr/ai-weekly-digest" target="_blank">View on GitHub</a>
            </p>
            <p style="margin-top: 30px; opacity: 0.6; font-size: 14px;">
                Created by <a href="https://github.com/EiriniOr" target="_blank" style="color: #9B59B6; text-decoration: none;">Eirini Ornithopoulou</a>
            </p>
        </div>
    </div>
</body>
</html>
"""

        # Write HTML file
        output_path = self.output_dir / "index.html"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✅ Webpage created successfully!")
        print(f"📁 Location: {output_path}")

        return output_path

    async def create_archive_page(self, curated_data, date_str, filename):
        """Create an individual archive page for a past digest"""
        formatted_date = datetime.strptime(date_str, '%Y%m%d').strftime('%B %d, %Y')

        # Build sections HTML
        sections_html = ""
        sections = curated_data.get('sections', {})
        sections = {k: v for k, v in sections.items() if k != "Notable Discussions"}

        section_icons = {
            "Key Research Papers": "🔬",
            "Industry Updates": "🏢",
            "Tools & Frameworks": "🛠️"
        }

        section_colors = {
            "Key Research Papers": "#9B59B6",
            "Industry Updates": "#3498DB",
            "Tools & Frameworks": "#1ABC9C"
        }

        for section_name, items in sections.items():
            if not items:
                continue

            icon = section_icons.get(section_name, "📌")
            color = section_colors.get(section_name, "#5B9BD5")

            items_html = ""
            for item in items:
                title = item['title']
                insight = item.get('insight', '')
                meta = item.get('meta', 'Source unknown')
                url = item.get('url', '')

                url_html = f'<a href="{url}" target="_blank" class="item-link">🔗 Read more</a>' if url else ''

                items_html += f"""
                <div class="content-item">
                    <h3 class="item-title">{title}</h3>
                    <p class="item-insight">{insight}</p>
                    <div class="item-meta">
                        <span class="meta-source">📍 {meta}</span>
                        {url_html}
                    </div>
                </div>
                """

            sections_html += f"""
            <section class="content-section" style="border-left: 4px solid {color}">
                <h2 class="section-title">{icon} {section_name}</h2>
                <div class="section-items">
                    {items_html}
                </div>
            </section>
            """

        # Use same CSS as main page
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 AI Weekly Digest - {formatted_date}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: #e0e0e0;
            line-height: 1.6;
            min-height: 100vh;
        }}

        body::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image:
                linear-gradient(45deg, rgba(102, 126, 234, 0.05) 25%, transparent 25%),
                linear-gradient(-45deg, rgba(118, 75, 162, 0.05) 25%, transparent 25%);
            background-size: 60px 60px;
            animation: backgroundScroll 20s linear infinite;
            pointer-events: none;
            z-index: -1;
        }}

        @keyframes backgroundScroll {{
            0% {{
                background-position: 0 0, 0 0;
            }}
            100% {{
                background-position: 60px 60px, -60px 60px;
            }}
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}

        .header {{
            text-align: center;
            padding: 60px 20px;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.2));
            border-radius: 20px;
            margin-bottom: 40px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }}

        .header h1 {{
            font-size: 3rem;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }}

        .header .subtitle {{
            font-size: 1.2rem;
            color: #b0b0b0;
            margin-bottom: 20px;
        }}

        .header .date {{
            font-size: 1rem;
            color: #888;
        }}

        .back-link {{
            display: inline-block;
            margin-bottom: 20px;
            color: #667eea;
            text-decoration: none;
            font-size: 1.1rem;
            transition: color 0.3s;
        }}

        .back-link:hover {{
            color: #4A90E2;
        }}

        .summary {{
            background: rgba(74, 144, 226, 0.1);
            border-left: 4px solid #4A90E2;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 40px;
            backdrop-filter: blur(10px);
        }}

        .summary h2 {{
            color: #4A90E2;
            margin-bottom: 15px;
            font-size: 1.8rem;
        }}

        .summary p {{
            font-size: 1.1rem;
            line-height: 1.8;
            color: #d0d0d0;
        }}

        .content-section {{
            background: rgba(30, 30, 50, 0.6);
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        }}

        .section-title {{
            font-size: 1.8rem;
            margin-bottom: 25px;
            color: #fff;
        }}

        .section-items {{
            display: grid;
            gap: 20px;
        }}

        .content-item {{
            background: rgba(50, 50, 70, 0.5);
            padding: 20px;
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: transform 0.3s, box-shadow 0.3s;
        }}

        .content-item:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        }}

        .item-title {{
            color: #fff;
            margin-bottom: 10px;
            font-size: 1.2rem;
        }}

        .item-insight {{
            color: #c0c0c0;
            margin-bottom: 15px;
            font-size: 1rem;
        }}

        .item-meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
            font-size: 0.9rem;
        }}

        .meta-source {{
            color: #888;
        }}

        .item-link {{
            color: #4A90E2;
            text-decoration: none;
            transition: color 0.3s;
        }}

        .item-link:hover {{
            color: #667eea;
        }}

        .footer {{
            text-align: center;
            padding: 40px 20px;
            color: #888;
            margin-top: 60px;
        }}

        .footer a {{
            color: #667eea;
            text-decoration: none;
        }}

        .footer a:hover {{
            color: #4A90E2;
        }}

        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 2rem;
            }}

            .content-item {{
                padding: 15px;
            }}

            .item-meta {{
                flex-direction: column;
                align-items: flex-start;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <a href="index.html" class="back-link">← Back to Latest Digest</a>

        <div class="header">
            <h1>🤖 AI Weekly Digest</h1>
            <p class="subtitle">Archived Edition</p>
            <p class="date">{formatted_date}</p>
        </div>

        <div class="summary">
            <h2>📊 This Week's Highlights</h2>
            <p>{curated_data.get('weekly_summary', 'Your weekly AI digest')}</p>
        </div>

        {sections_html}

        <div class="footer">
            <p>🔬 Curated from arXiv, Hacker News, and Reddit</p>
            <p style="margin-top: 20px;">
                <a href="https://github.com/EiriniOr/ai-weekly-digest" target="_blank">View on GitHub</a>
            </p>
        </div>
    </div>
</body>
</html>
"""

        # Write archive HTML file
        archive_path = self.output_dir / filename
        with open(archive_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"  ✓ Created archive page: {filename}")

    async def generate(self):
        """Main generation workflow"""
        print("🎯 Starting webpage generation...\n")

        # Load curated data
        curated_data = self.get_latest_curated_data()

        total_items = sum(len(items) for items in curated_data.get('sections', {}).values())
        print(f"📊 Loaded curated content with {total_items} items\n")

        # Create webpage
        filepath = await self.create_webpage(curated_data)

        return filepath

async def main():
    generator = WebpageGenerator()
    filepath = await generator.generate()
    print(f"\n🎉 Done! Open your webpage:\n   {filepath}")

if __name__ == "__main__":
    asyncio.run(main())

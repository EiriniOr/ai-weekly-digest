#!/usr/bin/env python3
"""
Presentation Generator
Creates a clean PowerPoint presentation from curated AI news
Small fonts, no graphs, 10-15 slides
"""

import asyncio
import json
import yaml
from datetime import datetime
from pathlib import Path
import sys
import os

# Add MCP PowerPoint server to path
sys.path.insert(0, '/Users/rena/mcp-powerpoint-server')
from server import call_tool

class PresentationGenerator:
    def __init__(self, config_path: str = "../config.yaml"):
        self.base_dir = Path(__file__).parent.parent
        config_file = self.base_dir / "config.yaml"

        with open(config_file) as f:
            self.config = yaml.safe_load(f)

        self.data_dir = self.base_dir / "data"
        self.output_dir = Path(self.config['presentation']['output_path'])

    def get_latest_curated_data(self):
        """Load the most recent curated content"""
        data_files = sorted(self.data_dir.glob("curated_*.json"), reverse=True)

        if not data_files:
            raise FileNotFoundError("No curated data found. Run curate_content.py first.")

        with open(data_files[0]) as f:
            return json.load(f)

    async def create_presentation(self, curated_data):
        """Generate clean presentation with small fonts, no graphs, 10-15 slides"""
        print("🎨 Creating presentation...\n")

        # Generate filename
        date_str = datetime.now().strftime('%Y-%m-%d')
        filename_template = self.config['presentation']['filename_template']
        filename = filename_template.replace('{date}', date_str)
        filepath = str(self.output_dir / filename)

        # Create presentation with title slide
        title = self.config['presentation']['title']
        subtitle = self.config['presentation']['subtitle_template'].replace('{date}', date_str)

        await call_tool("create_presentation", {
            "title": title,
            "subtitle": subtitle,
            "filename": filepath
        })

        # Apply modern theme
        await call_tool("apply_theme", {
            "filename": filepath,
            "theme": "modern"
        })

        # Soft gradient background for title
        await call_tool("set_slide_background", {
            "filename": filepath,
            "color": "#667eea",
            "gradient": True
        })
        print(f"  ✓ Created title slide")

        # Add weekly summary slide - format as paragraph, not bullets
        weekly_summary = curated_data.get('weekly_summary', 'Your weekly AI digest')

        # Format as single paragraph text block with smaller font
        await call_tool("format_text", {
            "filename": filepath,
            "title": "🤖 This Week in Agentic AI",
            "text_blocks": [
                {
                    "text": "This Week's Highlights",
                    "font_size": 16,
                    "bold": True,
                    "color": "#FFFFFF"
                },
                {
                    "text": weekly_summary,
                    "font_size": 12,
                    "color": "#FFFFFF"
                },
                {
                    "text": "",
                    "font_size": 10
                },
                {
                    "text": "📚 arXiv • Hacker News • Reddit",
                    "font_size": 10,
                    "italic": True,
                    "color": "#CCCCCC"
                },
                {
                    "text": f"🗓️  {date_str}",
                    "font_size": 10,
                    "italic": True,
                    "color": "#CCCCCC"
                }
            ]
        })

        # Soft blue gradient background
        await call_tool("set_slide_background", {
            "filename": filepath,
            "color": "#4A90E2",
            "gradient": True
        })
        print(f"  ✓ Added summary slide")

        # Section colors with emojis - EXCLUDE Notable Discussions
        section_config = {
            "Key Research Papers": {
                "color": "#9B59B6",
                "emoji": "🔬"
            },
            "Industry Updates": {
                "color": "#3498DB",
                "emoji": "🏢"
            },
            "Tools & Frameworks": {
                "color": "#1ABC9C",
                "emoji": "🛠️"
            }
        }

        sections = curated_data.get('sections', {})

        # Filter out Notable Discussions
        sections = {k: v for k, v in sections.items() if k != "Notable Discussions"}

        for section_name, items in sections.items():
            if not items:
                continue

            print(f"  ✓ Adding section: {section_name} ({len(items)} items)")
            config = section_config.get(section_name, {"color": "#5B9BD5", "emoji": "📌"})

            # Section divider slide
            await call_tool("format_text", {
                "filename": filepath,
                "title": f"{config['emoji']} {section_name}",
                "text_blocks": [
                    {
                        "text": f"{len(items)} key updates this week",
                        "font_size": 18,
                        "bold": True,
                        "color": "#FFFFFF"
                    },
                    {
                        "text": "",
                        "font_size": 12
                    },
                    {
                        "text": "→ Swipe to explore",
                        "font_size": 14,
                        "italic": True,
                        "color": "#FFFFFF"
                    }
                ]
            })

            # Soft gradient background
            await call_tool("set_slide_background", {
                "filename": filepath,
                "color": config['color'],
                "gradient": True
            })

            # Add each item with small fonts, formatted as paragraph
            for idx, item in enumerate(items, 1):
                title_text = item['title']
                insight = item.get('insight', '')
                meta = item.get('meta', 'Source unknown')
                url = item.get('url', '')

                # Build text blocks with small fonts
                text_blocks = [
                    {
                        "text": insight,
                        "font_size": 11,
                        "color": "#333333"
                    },
                    {
                        "text": "",
                        "font_size": 8
                    },
                    {
                        "text": f"📍 {meta}",
                        "font_size": 9,
                        "italic": True,
                        "color": "#666666"
                    }
                ]

                if url:
                    # Shorten URL if too long
                    display_url = url if len(url) <= 60 else url[:57] + "..."
                    text_blocks.append({
                        "text": f"🔗 {display_url}",
                        "font_size": 8,
                        "color": "#3498DB"
                    })

                # Create slide with small title font
                await call_tool("format_text", {
                    "filename": filepath,
                    "title": f"{idx}. {title_text}",
                    "text_blocks": text_blocks
                })

                # Soft light background for readability
                await call_tool("set_slide_background", {
                    "filename": filepath,
                    "color": "#F5F7FA",
                    "gradient": False
                })

        # Closing slide
        await call_tool("format_text", {
            "filename": filepath,
            "title": "✨ Stay Curious",
            "text_blocks": [
                {
                    "text": "Your weekly AI digest",
                    "font_size": 16,
                    "bold": True,
                    "color": "#FFFFFF"
                },
                {
                    "text": "Automatically curated every Sunday at 6 PM",
                    "font_size": 12,
                    "italic": True,
                    "color": "#EEEEEE"
                },
                {
                    "text": "",
                    "font_size": 10
                },
                {
                    "text": "🔬 Data Sources:",
                    "font_size": 12,
                    "bold": True,
                    "color": "#FFFFFF"
                },
                {
                    "text": "arXiv Research Papers • Hacker News • Reddit ML Communities",
                    "font_size": 11,
                    "color": "#EEEEEE"
                },
                {
                    "text": "",
                    "font_size": 10
                },
                {
                    "text": f"📅 Next edition: {self._next_sunday()}",
                    "font_size": 11,
                    "italic": True,
                    "color": "#CCCCCC"
                }
            ]
        })

        # Soft purple gradient for closing
        await call_tool("set_slide_background", {
            "filename": filepath,
            "color": "#764ba2",
            "gradient": True
        })
        print(f"  ✓ Added closing slide")

        # Add footer to all slides
        await call_tool("add_footer", {
            "filename": filepath,
            "text": "🤖 AI Weekly Digest",
            "show_page_number": True
        })
        print(f"  ✓ Added footer with page numbers")

        # Save presentation
        await call_tool("save_presentation", {
            "filename": filepath
        })

        print(f"\n✅ Presentation created successfully!")
        print(f"📁 Location: {filepath}")

        return filepath

    def _next_sunday(self) -> str:
        """Calculate next Sunday's date"""
        from datetime import timedelta
        today = datetime.now()
        days_until_sunday = (6 - today.weekday()) % 7
        if days_until_sunday == 0:
            days_until_sunday = 7
        next_sunday = today + timedelta(days=days_until_sunday)
        return next_sunday.strftime('%B %d, %Y')

    async def generate(self) -> str:
        """Main generation workflow"""
        print("🎯 Starting presentation generation...\n")

        # Load curated data
        curated_data = self.get_latest_curated_data()

        # Filter to only 3 sections (no Notable Discussions)
        if 'sections' in curated_data:
            curated_data['sections'] = {
                k: v for k, v in curated_data['sections'].items()
                if k != "Notable Discussions"
            }

        total_items = sum(len(items) for items in curated_data.get('sections', {}).values())
        print(f"📊 Loaded curated content with {total_items} items (excluding discussions)\n")

        # Create presentation
        filepath = await self.create_presentation(curated_data)

        return filepath

async def main():
    generator = PresentationGenerator()
    filepath = await generator.generate()
    print(f"\n🎉 Done! Open your presentation:\n   {filepath}")

if __name__ == "__main__":
    asyncio.run(main())

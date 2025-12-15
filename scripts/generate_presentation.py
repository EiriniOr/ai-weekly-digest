#!/usr/bin/env python3
"""
Presentation Generator
Creates a beautiful PowerPoint presentation from curated AI news
Uses MCP server directly for advanced styling
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
        """Generate the weekly digest presentation with beautiful futuristic design"""
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
        print(f"  ✓ Created title slide")

        # Apply modern theme and add shapes to title
        await call_tool("apply_theme", {
            "filename": filepath,
            "theme": "modern"
        })

        # Add decorative shapes to title slide
        await call_tool("add_shape", {
            "filename": filepath,
            "shape_type": "rectangle",
            "left": 0.5,
            "top": 1.0,
            "width": 1.5,
            "height": 0.3,
            "fill_color": "#667eea"
        })

        await call_tool("add_shape", {
            "filename": filepath,
            "shape_type": "rectangle",
            "left": 8.0,
            "top": 6.0,
            "width": 1.5,
            "height": 0.3,
            "fill_color": "#764ba2"
        })
        print(f"  ✓ Applied futuristic theme with shapes")

        # Add weekly summary slide with emojis
        weekly_summary = curated_data.get('weekly_summary', 'Your weekly AI digest')

        # Break into readable lines
        summary_lines = self._break_into_lines(weekly_summary, 85)
        summary_content = [
            "📊 This Week's Highlights:",
            "",
            *summary_lines,
            "",
            "📚 Sources: arXiv • Hacker News • Reddit",
            f"🗓️  {date_str}"
        ]

        await call_tool("add_content_slide", {
            "filename": filepath,
            "title": "🤖 This Week in Agentic AI",
            "content": summary_content
        })

        # Add gradient background
        await call_tool("set_slide_background", {
            "filename": filepath,
            "color": "#3498DB",
            "gradient": True
        })

        # Add decorative circle
        await call_tool("add_shape", {
            "filename": filepath,
            "shape_type": "circle",
            "left": 8.5,
            "top": 5.5,
            "width": 1.0,
            "height": 1.0,
            "fill_color": "#FFFFFF",
            "line_color": "#3498DB"
        })
        print(f"  ✓ Added summary slide")

        # Count items per section for overview chart
        sections = curated_data.get('sections', {})
        section_names = list(sections.keys())
        section_counts = [len(items) for items in sections.values()]

        # Add overview chart
        if section_names and section_counts:
            await call_tool("add_chart_slide", {
                "filename": filepath,
                "title": "📈 Content Distribution",
                "chart_type": "column",
                "categories": section_names,
                "series": [{
                    "name": "Items",
                    "values": section_counts
                }]
            })

            # Colorful background
            await call_tool("set_slide_background", {
                "filename": filepath,
                "color": "#1ABC9C"
            })
            print(f"  ✓ Added overview chart")

        # Section colors with emojis
        section_config = {
            "Key Research Papers": {
                "color": "#9B59B6",
                "emoji": "🔬",
                "shape": "rectangle"
            },
            "Industry Updates": {
                "color": "#3498DB",
                "emoji": "🏢",
                "shape": "circle"
            },
            "Tools & Frameworks": {
                "color": "#1ABC9C",
                "emoji": "🛠️",
                "shape": "triangle"
            },
            "Notable Discussions": {
                "color": "#E74C3C",
                "emoji": "💬",
                "shape": "rectangle"
            }
        }

        for section_name, items in sections.items():
            if not items:
                continue

            print(f"  ✓ Adding section: {section_name} ({len(items)} items)")
            config = section_config.get(section_name, {"color": "#5B9BD5", "emoji": "📌", "shape": "rectangle"})

            # Section divider slide with emoji
            await call_tool("add_content_slide", {
                "filename": filepath,
                "title": f"{config['emoji']} {section_name}",
                "content": [
                    f"{len(items)} key updates this week",
                    "",
                    "→ Swipe to explore"
                ]
            })

            # Colored background
            await call_tool("set_slide_background", {
                "filename": filepath,
                "color": config['color'],
                "gradient": True
            })

            # Add decorative shape
            await call_tool("add_shape", {
                "filename": filepath,
                "shape_type": config['shape'],
                "left": 8.0,
                "top": 5.0,
                "width": 1.5,
                "height": 1.5,
                "fill_color": "#FFFFFF"
            })

            # Add each item with varied layouts
            for idx, item in enumerate(items, 1):
                title_text = item['title']
                if len(title_text) > 70:
                    title_text = title_text[:67] + "..."

                insight = item.get('insight', '')
                insight_lines = self._break_into_lines(insight, 85)

                meta = item.get('meta', 'Source unknown')
                if len(meta) > 80:
                    meta = meta[:77] + "..."

                url = item.get('url', '')
                if len(url) > 70:
                    url = url[:67] + "..."

                content_lines = [
                    *insight_lines,
                    "",
                    f"📍 {meta}",
                ]

                if url:
                    content_lines.append(f"🔗 {url}")

                # Alternate between regular slides and two-column slides
                if idx % 3 == 0:
                    # Two-column layout for variety
                    await call_tool("add_two_column_slide", {
                        "filename": filepath,
                        "title": f"{idx}. {title_text}",
                        "left_content": insight_lines[:len(insight_lines)//2] if len(insight_lines) > 1 else insight_lines,
                        "right_content": insight_lines[len(insight_lines)//2:] + ["", f"📍 {meta}"] + ([f"🔗 {url}"] if url else [])
                    })
                else:
                    # Regular content slide
                    await call_tool("add_content_slide", {
                        "filename": filepath,
                        "title": f"{idx}. {title_text}",
                        "content": content_lines
                    })

                # Light background for readability
                await call_tool("set_slide_background", {
                    "filename": filepath,
                    "color": "#F8F9FA"
                })

                # Add small emoji shape
                emoji_shape = "circle" if idx % 2 == 0 else "rectangle"
                await call_tool("add_shape", {
                    "filename": filepath,
                    "shape_type": emoji_shape,
                    "left": 0.3,
                    "top": 0.8,
                    "width": 0.4,
                    "height": 0.4,
                    "fill_color": config['color']
                })

        # Timeline slide showing next editions
        timeline_events = []
        from datetime import timedelta
        today = datetime.now()
        for i in range(4):
            days = 7 * (i + 1)
            future_date = today + timedelta(days=days)
            timeline_events.append({
                "date": future_date.strftime('%b %d'),
                "event": f"Week {i+1} Digest"
            })

        await call_tool("add_timeline_slide", {
            "filename": filepath,
            "title": "📅 Upcoming Editions",
            "events": timeline_events
        })

        await call_tool("set_slide_background", {
            "filename": filepath,
            "color": "#3498DB"
        })
        print(f"  ✓ Added timeline slide")

        # Closing slide with shapes and emojis
        await call_tool("add_content_slide", {
            "filename": filepath,
            "title": "✨ Stay Curious",
            "content": [
                "Your weekly AI digest",
                "Automatically curated every Sunday at 6 PM",
                "",
                "🔬 Data Sources:",
                "  • arXiv Research Papers",
                "  • Hacker News",
                "  • Reddit ML Communities",
                "",
                f"📅 Next edition: {self._next_sunday()}"
            ]
        })

        # Purple gradient for closing
        await call_tool("set_slide_background", {
            "filename": filepath,
            "color": "#764ba2",
            "gradient": True
        })

        # Add decorative shapes
        await call_tool("add_shape", {
            "filename": filepath,
            "shape_type": "circle",
            "left": 1.0,
            "top": 5.0,
            "width": 0.8,
            "height": 0.8,
            "fill_color": "#FFFFFF"
        })

        await call_tool("add_shape", {
            "filename": filepath,
            "shape_type": "rectangle",
            "left": 8.5,
            "top": 1.5,
            "width": 1.0,
            "height": 0.5,
            "fill_color": "#667eea"
        })
        print(f"  ✓ Added closing slide with shapes")

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

    def _break_into_lines(self, text: str, max_chars: int) -> list:
        """Break text into lines of maximum length"""
        if len(text) <= max_chars:
            return [text]

        words = text.split()
        lines = []
        current_line = []
        current_length = 0

        for word in words:
            word_len = len(word) + (1 if current_line else 0)
            if current_length + word_len <= max_chars:
                current_line.append(word)
                current_length += word_len
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
                current_length = len(word)

        if current_line:
            lines.append(' '.join(current_line))

        return lines

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

        total_items = sum(len(items) for items in curated_data.get('sections', {}).values())
        print(f"📊 Loaded curated content with {total_items} items\n")

        # Create presentation
        filepath = await self.create_presentation(curated_data)

        return filepath

async def main():
    generator = PresentationGenerator()
    filepath = await generator.generate()
    print(f"\n🎉 Done! Open your presentation:\n   {filepath}")

if __name__ == "__main__":
    asyncio.run(main())

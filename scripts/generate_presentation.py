#!/usr/bin/env python3
"""
Presentation Generator
Creates a beautiful PowerPoint presentation from curated AI news
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
from chatgpt_wrapper import PowerPointAPI

class PresentationGenerator:
    def __init__(self, config_path: str = "../config.yaml"):
        self.base_dir = Path(__file__).parent.parent
        config_file = self.base_dir / "config.yaml"

        with open(config_file) as f:
            self.config = yaml.safe_load(f)

        self.data_dir = self.base_dir / "data"
        self.output_dir = Path(self.config['presentation']['output_path'])
        self.ppt = PowerPointAPI()

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

        await self.ppt.create_presentation(
            title=title,
            subtitle=subtitle,
            filename=filepath
        )
        print(f"  ✓ Created title slide")

        # Apply futuristic gradient theme
        await self.ppt.apply_theme(
            filename=filepath,
            theme="modern"
        )

        # Add gradient background to title slide
        await self.ppt.set_slide_background(
            filename=filepath,
            color="#667eea",  # Purple gradient start
            gradient=True
        )
        print(f"  ✓ Applied futuristic gradient theme")

        # Add weekly summary slide with smaller text
        weekly_summary = curated_data.get('weekly_summary', 'Your weekly AI digest')

        # Break summary into smaller chunks for readability
        summary_lines = self._break_into_lines(weekly_summary, 100)

        text_blocks = []
        for line in summary_lines:
            text_blocks.append({
                "text": line,
                "font_size": 14,  # Smaller, readable font
                "color": "#FFFFFF"
            })

        # Add metadata in smaller font
        text_blocks.extend([
            {"text": "", "font_size": 12},
            {"text": "Curated from arXiv, Hacker News, and Reddit", "font_size": 11, "italic": True, "color": "#CCCCCC"},
            {"text": f"Generated: {date_str}", "font_size": 11, "italic": True, "color": "#CCCCCC"}
        ])

        await self.ppt.format_text_slide(
            filename=filepath,
            title="This Week in Agentic AI",
            text_blocks=text_blocks
        )

        # Set background gradient
        await self.ppt.set_slide_background(
            filename=filepath,
            color="#3498DB",
            gradient=True
        )
        print(f"  ✓ Added summary slide with gradient")

        # Add section slides with colorful backgrounds
        sections = curated_data.get('sections', {})
        section_colors = {
            "Key Research Papers": "#9B59B6",  # Purple
            "Industry Updates": "#3498DB",      # Blue
            "Tools & Frameworks": "#1ABC9C",    # Turquoise
            "Notable Discussions": "#E74C3C"    # Red
        }

        for section_name, items in sections.items():
            if not items:
                continue

            print(f"  ✓ Adding section: {section_name} ({len(items)} items)")
            section_color = section_colors.get(section_name, "#5B9BD5")

            # Section divider slide
            await self.ppt.format_text_slide(
                filename=filepath,
                title=section_name,
                text_blocks=[
                    {"text": f"{len(items)} key updates", "font_size": 20, "bold": True, "color": "#FFFFFF"},
                    {"text": "", "font_size": 12},
                    {"text": "Swipe to explore →", "font_size": 16, "italic": True, "color": "#FFFFFF"}
                ]
            )

            # Colored background for section divider
            await self.ppt.set_slide_background(
                filename=filepath,
                color=section_color,
                gradient=True
            )

            # Add each item with compact formatting and small fonts
            for idx, item in enumerate(items, 1):
                # Truncate title if too long
                title_text = item['title']
                if len(title_text) > 75:
                    title_text = title_text[:72] + "..."

                # Get insight and break into lines
                insight = item.get('insight', '')
                insight_lines = self._break_into_lines(insight, 90)

                # Build text blocks with small fonts
                text_blocks = []

                # Add insight lines
                for line in insight_lines:
                    text_blocks.append({
                        "text": line,
                        "font_size": 13,  # Small readable font
                        "color": "#333333"
                    })

                # Add spacing
                text_blocks.append({"text": "", "font_size": 10})

                # Add source info in smaller font
                meta = item.get('meta', 'Source unknown')
                if len(meta) > 70:
                    meta = meta[:67] + "..."
                text_blocks.append({
                    "text": f"Source: {meta}",
                    "font_size": 10,
                    "italic": True,
                    "color": "#666666"
                })

                # Add URL if available
                url = item.get('url', '')
                if url:
                    if len(url) > 60:
                        url = url[:57] + "..."
                    text_blocks.append({
                        "text": f"🔗 {url}",
                        "font_size": 9,
                        "color": "#3498DB"
                    })

                # Create slide with formatted text
                await self.ppt.format_text_slide(
                    filename=filepath,
                    title=f"{idx}. {title_text}",
                    text_blocks=text_blocks
                )

                # Light background for content slides
                await self.ppt.set_slide_background(
                    filename=filepath,
                    color="#F8F9FA"
                )

        # Add closing slide with gradient
        await self.ppt.format_text_slide(
            filename=filepath,
            title="Stay Curious",
            text_blocks=[
                {"text": "Your weekly AI digest", "font_size": 18, "bold": True, "color": "#FFFFFF"},
                {"text": "Automatically curated every Sunday", "font_size": 14, "italic": True, "color": "#EEEEEE"},
                {"text": "", "font_size": 12},
                {"text": "Data Sources:", "font_size": 14, "bold": True, "color": "#FFFFFF"},
                {"text": "  → arXiv Research Papers", "font_size": 12, "color": "#EEEEEE"},
                {"text": "  → Hacker News", "font_size": 12, "color": "#EEEEEE"},
                {"text": "  → Reddit ML Communities", "font_size": 12, "color": "#EEEEEE"},
                {"text": "", "font_size": 12},
                {"text": f"Next edition: {self._next_sunday()}", "font_size": 13, "italic": True, "color": "#CCCCCC"}
            ]
        )

        # Purple gradient for closing
        await self.ppt.set_slide_background(
            filename=filepath,
            color="#764ba2",
            gradient=True
        )
        print(f"  ✓ Added closing slide")

        # Add footer to all slides
        await self.ppt.add_footer(
            filename=filepath,
            text="AI Weekly Digest",
            show_page_number=True
        )
        print(f"  ✓ Added footer with page numbers")

        # Save presentation
        await self.ppt.save_presentation(filepath)

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

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

    def get_latest_curated_data(self) -> Dict[str, Any]:
        """Load the most recent curated content"""
        data_files = sorted(self.data_dir.glob("curated_*.json"), reverse=True)

        if not data_files:
            raise FileNotFoundError("No curated data found. Run curate_content.py first.")

        with open(data_files[0]) as f:
            return json.load(f)

    async def create_presentation(self, curated_data: Dict[str, Any]) -> str:
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

        # Apply futuristic purple/blue gradient theme
        await self.ppt.apply_theme(
            filename=filepath,
            theme="modern"  # Modern blue theme - clean and futuristic
        )
        print(f"  ✓ Applied futuristic theme")

        # Add gradient background to title slide
        await self.ppt.add_slide_background(
            filename=filepath,
            slide_index=0,
            color="#5B9BD5"  # Modern blue
        )

        # Add weekly summary slide with compact formatting
        weekly_summary = curated_data.get('weekly_summary', 'Your weekly AI digest')

        # Wrap summary text at 90 characters
        wrapped_summary = self._wrap_text(weekly_summary, 90)

        await self.ppt.add_content_slide(
            filename=filepath,
            title="This Week in Agentic AI",
            content=[
                wrapped_summary,
                "",
                "Curated from arXiv, Hacker News, and Reddit",
                f"Generated: {date_str}"
            ]
        )
        print(f"  ✓ Added summary slide")

        # Add section slides
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

            # Section divider slide with colored background
            current_slide = await self.ppt.add_content_slide(
                filename=filepath,
                title=section_name,
                content=[
                    f"{len(items)} key updates",
                    "",
                    "Swipe to explore →"
                ]
            )

            # Get the current slide index (approximate)
            slide_count = len(items) * 2 + 3  # Rough estimate

            # Add each item with compact formatting
            for idx, item in enumerate(items, 1):
                # Shorten title to fit (max 70 chars)
                title_text = item['title']
                if len(title_text) > 70:
                    title_text = title_text[:67] + "..."

                # Wrap insight text to fit nicely (max 80 chars per line)
                insight = item.get('insight', '')
                wrapped_insight = self._wrap_text(insight, 80)

                # Shorten meta info
                meta = item.get('meta', 'Source unknown')
                if len(meta) > 60:
                    meta = meta[:57] + "..."

                # Shorten URL
                url = item.get('url', '')
                if len(url) > 50:
                    url = url[:47] + "..."

                content_lines = [
                    wrapped_insight,
                    "",
                    f"Source: {meta}"
                ]

                if url:
                    content_lines.append(f"Link: {url}")

                await self.ppt.add_content_slide(
                    filename=filepath,
                    title=f"{idx}. {title_text}",
                    content=content_lines
                )

        # Add closing slide with gradient
        await self.ppt.add_content_slide(
            filename=filepath,
            title="Stay Curious",
            content=[
                "Your weekly AI digest",
                "Automatically curated every Sunday",
                "",
                "Data Sources:",
                "  → arXiv Research Papers",
                "  → Hacker News",
                "  → Reddit ML Communities",
                "",
                f"Next edition: {self._next_sunday()}"
            ]
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

    def _wrap_text(self, text: str, width: int) -> str:
        """Wrap text to specified width"""
        if len(text) <= width:
            return text

        words = text.split()
        lines = []
        current_line = []
        current_length = 0

        for word in words:
            if current_length + len(word) + 1 <= width:
                current_line.append(word)
                current_length += len(word) + 1
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
                current_length = len(word)

        if current_line:
            lines.append(' '.join(current_line))

        return '\n'.join(lines)

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

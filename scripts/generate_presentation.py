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
        """Generate the weekly digest presentation"""
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

        # Add weekly summary slide
        weekly_summary = curated_data.get('weekly_summary', 'Your weekly AI digest')
        await self.ppt.add_content_slide(
            filename=filepath,
            title="This Week in Agentic AI",
            content=[
                weekly_summary,
                "",
                f"📊 Curated from research papers, industry news, and community discussions",
                f"🗓️  {date_str}"
            ]
        )
        print(f"  ✓ Added summary slide")

        # Add section slides
        sections = curated_data.get('sections', {})

        for section_name, items in sections.items():
            if not items:
                continue

            print(f"  ✓ Adding section: {section_name} ({len(items)} items)")

            # Section divider slide
            await self.ppt.add_content_slide(
                filename=filepath,
                title=section_name,
                content=[f"{len(items)} key updates"]
            )

            # Add each item
            for idx, item in enumerate(items, 1):
                title_text = f"{idx}. {item['title'][:80]}"

                content_lines = [
                    item.get('insight', ''),
                    "",
                    f"📎 {item.get('meta', 'Source unknown')}",
                    ""
                ]

                # Add URL if available
                if 'url' in item:
                    content_lines.append(f"🔗 {item['url'][:60]}")

                await self.ppt.add_content_slide(
                    filename=filepath,
                    title=title_text,
                    content=content_lines
                )

        # Add closing slide
        await self.ppt.add_content_slide(
            filename=filepath,
            title="Keep Learning 🚀",
            content=[
                "This digest was automatically generated",
                "",
                "Sources:",
                "• arXiv research papers",
                "• Hacker News discussions",
                "• Reddit communities (r/MachineLearning, r/LocalLLaMA)",
                "",
                f"Next digest: {self._next_sunday()}"
            ]
        )
        print(f"  ✓ Added closing slide")

        # Save presentation
        await self.ppt.save_presentation(filepath)

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

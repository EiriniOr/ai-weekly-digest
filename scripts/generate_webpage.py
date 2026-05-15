#!/usr/bin/env python3
"""
Webpage Generator
Creates a futuristic galaxy-themed webpage for AI Weekly Digest
"""

import asyncio
import json
import yaml
from datetime import datetime
from pathlib import Path


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
            raise FileNotFoundError(
                "No curated data found. Run curate_content.py first."
            )

        with open(data_files[0]) as f:
            return json.load(f)

    async def create_webpage(self, curated_data):
        """Generate galaxy-themed futuristic webpage"""
        print("🎨 Creating webpage...\n")

        date_str = datetime.now().strftime("%Y%m%d")
        week_str = datetime.now().strftime("%B %d, %Y")

        # Build sections HTML
        sections_html = ""
        sections = curated_data.get("sections", {})
        sections = {k: v for k, v in sections.items() if k != "Notable Discussions"}

        section_meta = {
            "Key Research Papers": {
                "icon": "🔬",
                "color": "#b16cff",
                "glow": "rgba(177, 108, 255, 0.45)",
            },
            "Industry Updates": {
                "icon": "🏢",
                "color": "#22d3ee",
                "glow": "rgba(34, 211, 238, 0.45)",
            },
            "Tools & Frameworks": {
                "icon": "🛠️",
                "color": "#34d399",
                "glow": "rgba(52, 211, 153, 0.45)",
            },
        }

        for section_name, items in sections.items():
            if not items:
                continue

            meta = section_meta.get(
                section_name,
                {"icon": "📌", "color": "#7aa2ff", "glow": "rgba(122, 162, 255, 0.45)"},
            )
            icon = meta["icon"]
            color = meta["color"]
            glow = meta["glow"]

            items_html = ""
            for item in items:
                title = item["title"]
                insight = item.get("insight", "")
                src = item.get("meta", "Source unknown")
                url = item.get("url", "")

                url_html = (
                    f'<a href="{url}" target="_blank" class="item-link">read more →</a>'
                    if url
                    else ""
                )

                items_html += f"""
                <article class="content-item">
                    <h3 class="item-title">{title}</h3>
                    <p class="item-insight">{insight}</p>
                    <div class="item-meta">
                        <span class="meta-source">{src}</span>
                        {url_html}
                    </div>
                </article>
                """

            sections_html += f"""
            <section class="content-section" style="--accent: {color}; --accent-glow: {glow};">
                <h2 class="section-title"><span class="section-icon">{icon}</span>{section_name}</h2>
                <div class="section-items">
                    {items_html}
                </div>
            </section>
            """

        weekly_summary = curated_data.get("weekly_summary", "Your weekly AI digest")

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Weekly Digest — Agentic AI Updates</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-0: #050018;
            --bg-1: #0a0426;
            --bg-2: #120538;
            --neon-purple: #b16cff;
            --neon-magenta: #ff4dd2;
            --neon-cyan: #22d3ee;
            --neon-blue: #4a7dff;
            --text: #e7e6ff;
            --text-dim: #9a98c8;
            --text-muted: #6a679a;
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        html {{ scroll-behavior: smooth; }}

        body {{
            font-family: 'Space Grotesk', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-0);
            color: var(--text);
            line-height: 1.6;
            min-height: 100vh;
            overflow-x: hidden;
            position: relative;
        }}

        /* Galaxy background: layered radial nebulas */
        body::before {{
            content: '';
            position: fixed;
            inset: 0;
            background:
                radial-gradient(ellipse 80% 60% at 15% 10%, rgba(177, 108, 255, 0.22), transparent 60%),
                radial-gradient(ellipse 70% 50% at 85% 20%, rgba(255, 77, 210, 0.18), transparent 60%),
                radial-gradient(ellipse 90% 70% at 50% 90%, rgba(34, 211, 238, 0.16), transparent 65%),
                radial-gradient(ellipse 60% 60% at 80% 75%, rgba(74, 125, 255, 0.15), transparent 60%),
                linear-gradient(180deg, #050018 0%, #0a0426 50%, #120538 100%);
            z-index: -3;
            animation: nebulaShift 30s ease-in-out infinite alternate;
        }}

        @keyframes nebulaShift {{
            0%   {{ filter: hue-rotate(0deg) saturate(1); }}
            100% {{ filter: hue-rotate(25deg) saturate(1.15); }}
        }}

        /* Star field (twinkling stars) */
        .stars {{
            position: fixed;
            inset: 0;
            z-index: -2;
            pointer-events: none;
            overflow: hidden;
        }}

        .stars::before, .stars::after {{
            content: '';
            position: absolute;
            inset: -50%;
            background-image:
                radial-gradient(1px 1px at 20px 30px, #fff, transparent),
                radial-gradient(1px 1px at 60px 70px, #fff, transparent),
                radial-gradient(1px 1px at 110px 20px, #b16cff, transparent),
                radial-gradient(1.5px 1.5px at 160px 90px, #fff, transparent),
                radial-gradient(1px 1px at 200px 50px, #22d3ee, transparent),
                radial-gradient(1px 1px at 250px 10px, #fff, transparent),
                radial-gradient(1.5px 1.5px at 300px 110px, #fff, transparent),
                radial-gradient(1px 1px at 340px 60px, #ff4dd2, transparent),
                radial-gradient(1px 1px at 380px 130px, #fff, transparent);
            background-repeat: repeat;
            background-size: 400px 200px;
            animation: starDrift 120s linear infinite;
            opacity: 0.6;
        }}

        .stars::after {{
            background-size: 600px 300px;
            animation: starDrift 200s linear infinite, twinkle 4s ease-in-out infinite alternate;
            opacity: 0.4;
        }}

        @keyframes starDrift {{
            from {{ transform: translate(0, 0); }}
            to   {{ transform: translate(-400px, -200px); }}
        }}

        @keyframes twinkle {{
            from {{ opacity: 0.2; }}
            to   {{ opacity: 0.7; }}
        }}

        /* Cursor-following glow */
        .cursor-glow {{
            position: fixed;
            width: 500px;
            height: 500px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(177, 108, 255, 0.12), transparent 70%);
            pointer-events: none;
            z-index: -1;
            transform: translate(-50%, -50%);
            transition: opacity 0.3s;
            mix-blend-mode: screen;
        }}

        .container {{
            max-width: 1100px;
            margin: 0 auto;
            padding: 24px 24px 60px;
            position: relative;
        }}

        /* Compact header */
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 16px;
            padding: 18px 26px;
            background: linear-gradient(135deg, rgba(177, 108, 255, 0.08), rgba(34, 211, 238, 0.06));
            border: 1px solid rgba(177, 108, 255, 0.25);
            border-radius: 16px;
            margin-bottom: 28px;
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            box-shadow: 0 4px 30px rgba(177, 108, 255, 0.15);
            position: relative;
            overflow: hidden;
        }}

        .header::before {{
            content: '';
            position: absolute;
            top: 0; left: -100%;
            width: 100%; height: 2px;
            background: linear-gradient(90deg, transparent, var(--neon-cyan), var(--neon-magenta), transparent);
            animation: scanline 4s ease-in-out infinite;
        }}

        @keyframes scanline {{
            0%, 100% {{ left: -100%; }}
            50%      {{ left: 100%; }}
        }}

        .brand {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .brand-logo {{
            width: 38px; height: 38px;
            border-radius: 10px;
            background: linear-gradient(135deg, var(--neon-purple), var(--neon-magenta), var(--neon-cyan));
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
            box-shadow: 0 0 20px rgba(177, 108, 255, 0.5);
            animation: logoFloat 3s ease-in-out infinite;
        }}

        @keyframes logoFloat {{
            0%, 100% {{ transform: translateY(0); }}
            50%      {{ transform: translateY(-3px); }}
        }}

        .header h1 {{
            font-size: 1.35rem;
            font-weight: 700;
            background: linear-gradient(135deg, #fff 0%, var(--neon-purple) 50%, var(--neon-cyan) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: -0.01em;
        }}

        .header .tagline {{
            font-size: 0.78rem;
            color: var(--text-muted);
            font-family: 'JetBrains Mono', monospace;
            margin-top: 2px;
        }}

        .header .date-badge {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.78rem;
            color: var(--neon-cyan);
            padding: 6px 12px;
            border: 1px solid rgba(34, 211, 238, 0.35);
            border-radius: 999px;
            background: rgba(34, 211, 238, 0.06);
            white-space: nowrap;
        }}

        /* Podcast hero — the centerpiece */
        .podcast-hero {{
            position: relative;
            padding: 36px 32px;
            margin-bottom: 36px;
            border-radius: 24px;
            background:
                radial-gradient(ellipse at top left, rgba(177, 108, 255, 0.25), transparent 60%),
                radial-gradient(ellipse at bottom right, rgba(34, 211, 238, 0.2), transparent 60%),
                rgba(10, 4, 38, 0.6);
            border: 1px solid rgba(177, 108, 255, 0.3);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            box-shadow:
                0 8px 40px rgba(177, 108, 255, 0.2),
                inset 0 1px 0 rgba(255, 255, 255, 0.08);
            overflow: hidden;
        }}

        .podcast-hero::before {{
            content: '';
            position: absolute;
            inset: -2px;
            border-radius: 24px;
            padding: 2px;
            background: linear-gradient(135deg, var(--neon-purple), var(--neon-magenta), var(--neon-cyan));
            -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor;
                    mask-composite: exclude;
            opacity: 0.4;
            pointer-events: none;
            animation: borderPulse 6s ease-in-out infinite;
        }}

        @keyframes borderPulse {{
            0%, 100% {{ opacity: 0.35; }}
            50%      {{ opacity: 0.7; }}
        }}

        .podcast-label {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.72rem;
            color: var(--neon-magenta);
            letter-spacing: 0.18em;
            text-transform: uppercase;
            margin-bottom: 14px;
        }}

        .live-dot {{
            width: 8px; height: 8px;
            border-radius: 50%;
            background: var(--neon-magenta);
            box-shadow: 0 0 12px var(--neon-magenta);
            animation: pulse 2s ease-in-out infinite;
        }}

        @keyframes pulse {{
            0%, 100% {{ opacity: 1; transform: scale(1); }}
            50%      {{ opacity: 0.5; transform: scale(0.85); }}
        }}

        .podcast-title {{
            font-size: 2rem;
            font-weight: 700;
            line-height: 1.15;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #fff, var(--neon-purple));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        .podcast-sub {{
            color: var(--text-dim);
            margin-bottom: 24px;
            font-size: 1rem;
            max-width: 720px;
        }}

        .audio-shell {{
            display: flex;
            align-items: center;
            gap: 18px;
            padding: 14px 20px;
            background: rgba(5, 0, 24, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 14px;
            position: relative;
        }}

        .visualizer {{
            display: flex;
            align-items: center;
            gap: 3px;
            height: 32px;
            flex-shrink: 0;
        }}

        .visualizer span {{
            display: block;
            width: 3px;
            background: linear-gradient(180deg, var(--neon-cyan), var(--neon-purple));
            border-radius: 2px;
            animation: bars 1.2s ease-in-out infinite;
        }}

        .visualizer span:nth-child(1) {{ height: 50%; animation-delay: 0.0s; }}
        .visualizer span:nth-child(2) {{ height: 80%; animation-delay: 0.15s; }}
        .visualizer span:nth-child(3) {{ height: 35%; animation-delay: 0.3s; }}
        .visualizer span:nth-child(4) {{ height: 90%; animation-delay: 0.45s; }}
        .visualizer span:nth-child(5) {{ height: 60%; animation-delay: 0.6s; }}

        @keyframes bars {{
            0%, 100% {{ transform: scaleY(0.4); }}
            50%      {{ transform: scaleY(1); }}
        }}

        audio {{
            flex: 1;
            min-width: 0;
            height: 40px;
        }}

        audio::-webkit-media-controls-panel {{
            background: transparent;
        }}

        /* Weekly summary */
        .summary {{
            padding: 22px 26px;
            border-radius: 16px;
            margin-bottom: 32px;
            background: rgba(10, 4, 38, 0.5);
            border: 1px solid rgba(74, 125, 255, 0.25);
            border-left: 3px solid var(--neon-blue);
            backdrop-filter: blur(10px);
        }}

        .summary h2 {{
            font-size: 0.78rem;
            font-family: 'JetBrains Mono', monospace;
            color: var(--neon-blue);
            letter-spacing: 0.16em;
            text-transform: uppercase;
            margin-bottom: 10px;
        }}

        .summary p {{
            font-size: 1.02rem;
            color: var(--text);
            line-height: 1.7;
        }}

        /* Content sections */
        .content-section {{
            padding: 26px 28px;
            border-radius: 18px;
            margin-bottom: 24px;
            background: rgba(10, 4, 38, 0.55);
            border: 1px solid rgba(255, 255, 255, 0.06);
            backdrop-filter: blur(12px);
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.3);
            transition: border-color 0.4s, box-shadow 0.4s;
        }}

        .content-section:hover {{
            border-color: var(--accent);
            box-shadow: 0 8px 40px var(--accent-glow);
        }}

        .section-title {{
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 22px;
            color: #fff;
            letter-spacing: -0.01em;
        }}

        .section-icon {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 36px; height: 36px;
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid var(--accent);
            font-size: 1.15rem;
            box-shadow: 0 0 16px var(--accent-glow);
        }}

        .section-items {{
            display: grid;
            gap: 14px;
        }}

        .content-item {{
            position: relative;
            padding: 18px 20px;
            background: rgba(255, 255, 255, 0.025);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 12px;
            transition: transform 0.3s ease, background 0.3s, border-color 0.3s, box-shadow 0.3s;
            overflow: hidden;
        }}

        .content-item::before {{
            content: '';
            position: absolute;
            left: 0; top: 0; bottom: 0;
            width: 2px;
            background: var(--accent);
            opacity: 0;
            transition: opacity 0.3s;
        }}

        .content-item:hover {{
            transform: translateY(-3px);
            background: rgba(255, 255, 255, 0.04);
            border-color: var(--accent);
            box-shadow: 0 8px 28px var(--accent-glow);
        }}

        .content-item:hover::before {{
            opacity: 1;
        }}

        .item-title {{
            font-size: 1.05rem;
            font-weight: 600;
            color: #fff;
            margin-bottom: 8px;
            line-height: 1.4;
        }}

        .item-insight {{
            color: var(--text-dim);
            font-size: 0.95rem;
            margin-bottom: 12px;
            line-height: 1.6;
        }}

        .item-meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
            font-size: 0.82rem;
            font-family: 'JetBrains Mono', monospace;
        }}

        .meta-source {{
            color: var(--text-muted);
        }}

        .item-link {{
            color: var(--accent);
            text-decoration: none;
            transition: filter 0.2s, transform 0.2s;
        }}

        .item-link:hover {{
            filter: brightness(1.3);
            transform: translateX(3px);
        }}

        /* Footer */
        .footer {{
            text-align: center;
            padding: 40px 20px 10px;
            color: var(--text-muted);
            font-size: 0.85rem;
            font-family: 'JetBrains Mono', monospace;
        }}

        .footer a {{
            color: var(--neon-purple);
            text-decoration: none;
            transition: color 0.2s;
        }}

        .footer a:hover {{
            color: var(--neon-cyan);
        }}

        .footer p {{ margin-bottom: 6px; }}

        .footer .signature {{
            margin-top: 22px;
            opacity: 0.6;
            font-size: 0.78rem;
        }}

        /* Reveal on scroll */
        .reveal {{
            opacity: 0;
            transform: translateY(20px);
            transition: opacity 0.7s ease, transform 0.7s ease;
        }}

        .reveal.visible {{
            opacity: 1;
            transform: translateY(0);
        }}

        @media (max-width: 700px) {{
            .container {{ padding: 16px; }}
            .header {{ padding: 14px 18px; flex-wrap: wrap; }}
            .header h1 {{ font-size: 1.1rem; }}
            .podcast-hero {{ padding: 26px 22px; }}
            .podcast-title {{ font-size: 1.5rem; }}
            .audio-shell {{ flex-wrap: wrap; }}
            .cursor-glow {{ display: none; }}
        }}
    </style>
</head>
<body>
    <div class="stars"></div>
    <div class="cursor-glow"></div>

    <div class="container">
        <header class="header">
            <div class="brand">
                <div class="brand-logo">🤖</div>
                <div>
                    <h1>AI Weekly Digest</h1>
                    <div class="tagline">// agentic intelligence, every sunday</div>
                </div>
            </div>
            <div class="date-badge">{week_str}</div>
        </header>

        <section class="podcast-hero reveal">
            <div class="podcast-label"><span class="live-dot"></span>this week's broadcast</div>
            <h2 class="podcast-title">🎙️ Listen to the Digest</h2>
            <p class="podcast-sub">AI-narrated summary of the week's most important agentic AI developments — research, industry moves, and the tools shaping how machines reason.</p>
            <div class="audio-shell">
                <div class="visualizer" aria-hidden="true">
                    <span></span><span></span><span></span><span></span><span></span>
                </div>
                <audio controls preload="metadata">
                    <source src="audio/narration_{date_str}.mp3" type="audio/mpeg">
                    Your browser does not support the audio element.
                </audio>
            </div>
        </section>

        <section class="summary reveal">
            <h2>// this week's highlights</h2>
            <p>{weekly_summary}</p>
        </section>

        {sections_html}

        <footer class="footer">
            <p>// curated from arXiv · Hacker News · Reddit</p>
            <p>auto-generated every sunday at 18:00</p>
            <p style="margin-top: 16px;"><a href="https://github.com/EiriniOr/ai-weekly-digest" target="_blank">view on github</a></p>
            <p class="signature">crafted by <a href="https://github.com/EiriniOr" target="_blank">Eirini Ornithopoulou</a></p>
        </footer>
    </div>

    <script>
        // Cursor-following glow
        const glow = document.querySelector('.cursor-glow');
        let glowX = window.innerWidth / 2, glowY = window.innerHeight / 2;
        let targetX = glowX, targetY = glowY;

        document.addEventListener('mousemove', (e) => {{
            targetX = e.clientX;
            targetY = e.clientY;
        }});

        function animateGlow() {{
            glowX += (targetX - glowX) * 0.1;
            glowY += (targetY - glowY) * 0.1;
            glow.style.left = glowX + 'px';
            glow.style.top  = glowY + 'px';
            requestAnimationFrame(animateGlow);
        }}
        animateGlow();

        // Reveal on scroll
        const observer = new IntersectionObserver((entries) => {{
            entries.forEach((entry) => {{
                if (entry.isIntersecting) {{
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }}
            }});
        }}, {{ threshold: 0.1 }});

        document.querySelectorAll('.content-section, .summary, .podcast-hero').forEach((el) => {{
            el.classList.add('reveal');
            observer.observe(el);
        }});

        // Reveal first elements immediately
        setTimeout(() => {{
            document.querySelectorAll('.podcast-hero, .summary').forEach((el) => el.classList.add('visible'));
        }}, 100);
    </script>
</body>
</html>
"""

        output_path = self.output_dir / "index.html"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        print("✅ Webpage created successfully!")
        print(f"📁 Location: {output_path}")

        return output_path

    async def generate(self):
        """Main generation workflow"""
        print("🎯 Starting webpage generation...\n")

        curated_data = self.get_latest_curated_data()

        total_items = sum(
            len(items) for items in curated_data.get("sections", {}).values()
        )
        print(f"📊 Loaded curated content with {total_items} items\n")

        filepath = await self.create_webpage(curated_data)

        return filepath


async def main():
    generator = WebpageGenerator()
    filepath = await generator.generate()
    print(f"\n🎉 Done! Open your webpage:\n   {filepath}")


if __name__ == "__main__":
    asyncio.run(main())

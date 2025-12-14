#!/usr/bin/env python3
"""
GitHub Deployment
Deploys the latest presentation to GitHub Pages and updates portfolio
"""

import asyncio
import yaml
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

class GitHubDeployer:
    def __init__(self, config_path: str = "../config.yaml"):
        self.base_dir = Path(__file__).parent.parent
        config_file = self.base_dir / "config.yaml"

        with open(config_file) as f:
            self.config = yaml.safe_load(f)

        self.github_config = self.config.get('github', {})
        self.output_dir = self.base_dir / "output"
        self.output_dir.mkdir(exist_ok=True)

    def convert_to_pdf(self, pptx_path: str) -> str:
        """Convert PPTX to PDF for web viewing"""
        print("\n📄 Converting presentation to PDF...")

        pdf_path = pptx_path.replace('.pptx', '.pdf')

        # Try using LibreOffice (common on macOS via Homebrew)
        try:
            result = subprocess.run([
                'soffice',
                '--headless',
                '--convert-to', 'pdf',
                '--outdir', str(Path(pdf_path).parent),
                pptx_path
            ], capture_output=True, timeout=60)

            if result.returncode == 0 and Path(pdf_path).exists():
                print(f"  ✓ PDF created: {pdf_path}")
                return pdf_path
            else:
                print(f"  ⚠️  LibreOffice conversion failed")

        except FileNotFoundError:
            print(f"  ℹ️  LibreOffice not found (install with: brew install libreoffice)")
        except Exception as e:
            print(f"  ⚠️  PDF conversion error: {e}")

        # Fallback: Copy PPTX as-is for download
        print(f"  ℹ️  Using PPTX file directly (PDF conversion unavailable)")
        return pptx_path

    def create_github_pages_index(self, presentation_path: str, pdf_path: str = None):
        """Create index.html for GitHub Pages"""
        print("\n🌐 Creating GitHub Pages site...")

        date_str = datetime.now().strftime('%B %d, %Y')
        filename = Path(presentation_path).name
        pdf_filename = Path(pdf_path).name if pdf_path else filename

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Weekly Digest</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}
        .container {{
            background: white;
            border-radius: 20px;
            padding: 60px 40px;
            max-width: 600px;
            text-align: center;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        h1 {{
            font-size: 2.5rem;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        .subtitle {{
            color: #666;
            font-size: 1.1rem;
            margin-bottom: 40px;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin: 40px 0;
        }}
        .stat {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 12px;
        }}
        .stat-value {{
            font-size: 2rem;
            font-weight: bold;
            color: #667eea;
        }}
        .stat-label {{
            font-size: 0.9rem;
            color: #666;
            margin-top: 5px;
        }}
        .download-btn {{
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 18px 40px;
            border-radius: 12px;
            text-decoration: none;
            font-weight: 600;
            font-size: 1.1rem;
            transition: transform 0.2s, box-shadow 0.2s;
            margin: 10px;
        }}
        .download-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
        }}
        .secondary-btn {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }}
        .info {{
            margin-top: 40px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 12px;
            color: #666;
        }}
        .sources {{
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-top: 30px;
            flex-wrap: wrap;
        }}
        .source-tag {{
            background: #667eea;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9rem;
        }}
        .updated {{
            margin-top: 30px;
            color: #999;
            font-size: 0.9rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 AI Weekly Digest</h1>
        <div class="subtitle">Your automated agentic AI newsletter</div>

        <div class="stats">
            <div class="stat">
                <div class="stat-value">18</div>
                <div class="stat-label">Curated Items</div>
            </div>
            <div class="stat">
                <div class="stat-value">4</div>
                <div class="stat-label">Categories</div>
            </div>
            <div class="stat">
                <div class="stat-value">20+</div>
                <div class="stat-label">Slides</div>
            </div>
        </div>

        <a href="{pdf_filename}" class="download-btn" download>📥 Download Latest Digest</a>
        {f'<a href="{filename}" class="download-btn secondary-btn" download>📊 Download PowerPoint</a>' if pdf_path else ''}

        <div class="info">
            <strong>This week's digest includes:</strong><br><br>
            ✓ Key Research Papers from arXiv<br>
            ✓ Industry Updates from Hacker News<br>
            ✓ Tools & Frameworks<br>
            ✓ Notable Community Discussions<br>
        </div>

        <div class="sources">
            <span class="source-tag">arXiv</span>
            <span class="source-tag">Hacker News</span>
            <span class="source-tag">Reddit</span>
            <span class="source-tag">Claude AI</span>
        </div>

        <div class="updated">
            Last updated: {date_str}<br>
            Auto-generated every Sunday at 6:00 PM
        </div>
    </div>
</body>
</html>
"""

        # Write index.html
        index_path = self.output_dir / "index.html"
        with open(index_path, 'w') as f:
            f.write(html_content)

        print(f"  ✓ Created index.html")

        # Copy presentation files
        shutil.copy(presentation_path, self.output_dir / filename)
        print(f"  ✓ Copied {filename}")

        if pdf_path and pdf_path != presentation_path:
            shutil.copy(pdf_path, self.output_dir / pdf_filename)
            print(f"  ✓ Copied {pdf_filename}")

        return index_path

    def deploy_to_github(self) -> bool:
        """Deploy to GitHub Pages"""
        if not self.github_config.get('enabled', False):
            print("  ℹ️  GitHub deployment is disabled in config.yaml")
            return False

        print("\n🚀 Deploying to GitHub Pages...")

        repo = self.github_config.get('repo')
        branch = self.github_config.get('branch', 'gh-pages')

        if repo == "your-username/ai-weekly-digest":
            print("  ⚠️  Please configure github.repo in config.yaml")
            return False

        try:
            # Initialize output directory as git repo if needed
            if not (self.output_dir / ".git").exists():
                print(f"  ✓ Initializing git in output directory...")
                subprocess.run(['git', 'init'], cwd=self.output_dir, check=True)
                subprocess.run(['git', 'checkout', '-b', branch], cwd=self.output_dir, check=True)

            # Add all files
            subprocess.run(['git', 'add', '.'], cwd=self.output_dir, check=True)

            # Commit
            date_str = datetime.now().strftime('%Y-%m-%d')
            commit_msg = f"Update weekly digest - {date_str}"
            subprocess.run(['git', 'commit', '-m', commit_msg], cwd=self.output_dir, check=False)

            # Push to GitHub
            remote_url = f"https://github.com/{repo}.git"
            subprocess.run(['git', 'remote', 'remove', 'origin'], cwd=self.output_dir, check=False)
            subprocess.run(['git', 'remote', 'add', 'origin', remote_url], cwd=self.output_dir, check=True)
            subprocess.run(['git', 'push', '-f', 'origin', branch], cwd=self.output_dir, check=True)

            print(f"\n✅ Deployed to GitHub Pages!")
            print(f"  🌐 View at: https://{repo.split('/')[0]}.github.io/{repo.split('/')[1]}/")
            return True

        except subprocess.CalledProcessError as e:
            print(f"  ❌ Git command failed: {e}")
            print(f"  💡 Make sure you have push access to {repo}")
            return False
        except Exception as e:
            print(f"  ❌ Deployment error: {e}")
            return False

    async def deploy(self, presentation_path: str) -> bool:
        """Main deployment workflow"""
        print("🎯 Starting GitHub deployment...\n")

        # Convert to PDF if enabled
        pdf_path = None
        if self.github_config.get('pdf_export', True):
            pdf_path = self.convert_to_pdf(presentation_path)

        # Create GitHub Pages site
        self.create_github_pages_index(presentation_path, pdf_path)

        # Deploy to GitHub
        return self.deploy_to_github()

async def deploy_to_github(filepath: str) -> bool:
    """Async wrapper for GitHub deployment"""
    deployer = GitHubDeployer()
    return await deployer.deploy(filepath)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        deployer = GitHubDeployer()
        asyncio.run(deployer.deploy(sys.argv[1]))
    else:
        print("Usage: python deploy_github.py <path-to-presentation>")

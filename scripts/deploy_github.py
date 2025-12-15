#!/usr/bin/env python3
"""
GitHub Deployment
Deploys the latest webpage to GitHub Pages
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

    async def deploy(self, html_path: str) -> bool:
        """Deploy webpage to GitHub Pages"""
        if not self.github_config.get('enabled', False):
            print("  ℹ️  GitHub Pages deployment disabled")
            return False

        print("\n🚀 Deploying to GitHub Pages...")

        try:
            # Navigate to output directory
            subprocess.run(['git', 'init'], cwd=self.output_dir, check=True, capture_output=True)
            subprocess.run(['git', 'checkout', '-B', 'gh-pages'], cwd=self.output_dir, check=True, capture_output=True)

            # Add all files
            subprocess.run(['git', 'add', '.'], cwd=self.output_dir, check=True, capture_output=True)

            # Commit
            date_str = datetime.now().strftime('%Y-%m-%d')
            subprocess.run(
                ['git', 'commit', '-m', f'Update weekly digest - {date_str}'],
                cwd=self.output_dir,
                check=True,
                capture_output=True
            )

            # Get repo URL
            repo = self.github_config.get('repo', '')
            if repo:
                repo_url = f"https://github.com/{repo}.git"

                # Add remote if not exists
                subprocess.run(
                    ['git', 'remote', 'add', 'origin', repo_url],
                    cwd=self.output_dir,
                    capture_output=True
                )

                # Force push to gh-pages
                result = subprocess.run(
                    ['git', 'push', '-f', 'origin', 'gh-pages'],
                    cwd=self.output_dir,
                    capture_output=True,
                    text=True
                )

                if result.returncode == 0:
                    print(f"  ✓ Deployed to GitHub Pages!")
                    print(f"  🌐 View at: https://{repo.split('/')[0]}.github.io/{repo.split('/')[1]}/")
                    return True
                else:
                    print(f"  ⚠️  Deployment warning: {result.stderr}")
                    return False

        except subprocess.CalledProcessError as e:
            print(f"  ❌ Deployment error: {e}")
            return False
        except Exception as e:
            print(f"  ❌ Unexpected error: {e}")
            return False

async def deploy_to_github(html_path: str) -> bool:
    """Deploy webpage to GitHub Pages"""
    deployer = GitHubDeployer()
    return await deployer.deploy(html_path)

async def main():
    # Test deployment
    html_path = Path(__file__).parent.parent / "output" / "index.html"
    if html_path.exists():
        success = await deploy_to_github(str(html_path))
        if success:
            print("\n✅ Deployment successful!")
        else:
            print("\n❌ Deployment failed!")
    else:
        print(f"❌ HTML file not found: {html_path}")

if __name__ == "__main__":
    asyncio.run(main())

# GitHub Setup Guide

## Quick Setup (5 minutes)

### 1. Create GitHub Repository

Go to [GitHub](https://github.com/new) and create a new repository:
- **Name**: `ai-weekly-digest`
- **Description**: "Automated weekly AI digest with presentations"
- **Visibility**: Public (required for free GitHub Pages)
- **Do NOT** initialize with README (we already have one)

### 2. Push to GitHub

```bash
cd /Users/rena/ai-weekly-digest

# Add remote
git remote add origin https://github.com/YOUR-USERNAME/ai-weekly-digest.git

# Push
git push -u origin main
```

Replace `YOUR-USERNAME` with your actual GitHub username.

### 3. Configure Settings in config.yaml

Edit `config.yaml` and update these sections:

```yaml
# Email Delivery
email:
  enabled: true
  recipient: "your-email@example.com"  # Your email
  sender_email: "your-email@example.com"  # Your email
  sender_password: "your-app-password"  # Gmail app password

# GitHub Pages Deployment
github:
  enabled: true
  repo: "YOUR-USERNAME/ai-weekly-digest"  # Your repo
  branch: "gh-pages"
  pdf_export: true
```

### 4. Set Up Gmail App Password (for email)

If using Gmail:

1. Go to [Google Account](https://myaccount.google.com/)
2. Security → 2-Step Verification (enable if not already)
3. Security → App passwords
4. Create app password for "Mail"
5. Copy the 16-character password
6. Paste it into `config.yaml` as `sender_password`

### 5. Enable GitHub Pages

After your first presentation is generated and pushed:

1. Go to your repository on GitHub
2. Settings → Pages
3. Source: Select `gh-pages` branch
4. Click Save

Your digest will be available at:
`https://YOUR-USERNAME.github.io/ai-weekly-digest/`

### 6. Update Portfolio Configuration

Edit `config.yaml` to match your actual details:

```yaml
github:
  repo: "YOUR-USERNAME/ai-weekly-digest"  # ← Change this
```

Then the system will automatically:
- Create presentations every Sunday at 6 PM
- Email you the presentation
- Deploy to GitHub Pages
- Update your portfolio link

## Testing Before Automation

Test each component individually:

```bash
# 1. Test the full pipeline
python3 generate_weekly_digest.py

# 2. Check email was sent (check your inbox)

# 3. Verify GitHub Pages deployment
# Visit: https://YOUR-USERNAME.github.io/ai-weekly-digest/
```

## Environment Variables for launchd

Update `com.aiweekly.digest.plist` with your actual API key:

```xml
<key>EnvironmentVariables</key>
<dict>
    <key>ANTHROPIC_API_KEY</key>
    <string>YOUR_ACTUAL_API_KEY</string>  <!-- Replace this -->
</dict>
```

## Git Authentication

If GitHub asks for credentials when pushing:

### Option 1: Personal Access Token (Recommended)

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token with `repo` permissions
3. Use token as password when pushing:
   ```bash
   Username: YOUR-USERNAME
   Password: ghp_xxxxxxxxxxxx  # Your token
   ```

### Option 2: SSH Key

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your-email@example.com"

# Copy public key
cat ~/.ssh/id_ed25519.pub

# Add to GitHub: Settings → SSH keys → New SSH key

# Change remote to SSH
git remote set-url origin git@github.com:YOUR-USERNAME/ai-weekly-digest.git
```

## Troubleshooting

### Push Rejected
```bash
git pull origin main --rebase
git push origin main
```

### Email Not Sending
- Check Gmail app password is correct
- Verify 2-step verification is enabled
- Check logs: `cat logs/stderr.log`

### GitHub Pages Not Showing
- Wait 2-3 minutes for deployment
- Check Settings → Pages is configured
- Verify `gh-pages` branch exists
- Check `output/` directory has files

### Automation Not Running
```bash
# Check if loaded
launchctl list | grep aiweekly

# Reload
launchctl unload ~/Library/LaunchAgents/com.aiweekly.digest.plist
launchctl load ~/Library/LaunchAgents/com.aiweekly.digest.plist

# Check logs
tail -f logs/stdout.log
```

## Complete Workflow After Setup

Once everything is configured:

1. **Sunday 6:00 PM** - System runs automatically
2. **Sunday 6:02 PM** - Presentation generated
3. **Sunday 6:02 PM** - Email sent to your inbox
4. **Sunday 6:02 PM** - GitHub Pages updated
5. **Sunday evening** - You review the digest!

## Portfolio Integration

The presentation will be automatically available at:
- **Download**: `https://YOUR-USERNAME.github.io/ai-weekly-digest/AI_Weekly_YYYY-MM-DD.pptx`
- **PDF**: `https://YOUR-USERNAME.github.io/ai-weekly-digest/AI_Weekly_YYYY-MM-DD.pdf`
- **Landing page**: `https://YOUR-USERNAME.github.io/ai-weekly-digest/`

You can link to this from your portfolio!

## Next Steps

After setup is complete:
1. Test everything manually first
2. Verify email delivery
3. Check GitHub Pages deployment
4. Enable launchd automation
5. Wait for Sunday 6 PM
6. Enjoy automated learning! 🎉

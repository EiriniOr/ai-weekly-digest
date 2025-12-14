# Complete Setup Instructions

## What You Now Have

✅ **Automated AI Weekly Digest System** that:
- Runs every **Sunday at 6:00 PM (18:00)**
- Collects AI news from arXiv, Hacker News, Reddit
- Uses Claude to curate and filter content
- Generates PowerPoint presentation
- **Emails you the presentation**
- **Deploys to GitHub Pages automatically**
- **Updates your portfolio with latest digest**

## Setup Steps

### 1. Create GitHub Repository

```bash
# Go to https://github.com/new
# Create repository named: ai-weekly-digest
# Make it Public (required for free GitHub Pages)
# Don't initialize with README

# Then push your code:
cd /Users/rena/ai-weekly-digest
git remote add origin https://github.com/YOUR-USERNAME/ai-weekly-digest.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Configure Email Settings

Edit `/Users/rena/ai-weekly-digest/config.yaml`:

```yaml
email:
  enabled: true
  recipient: "your-actual-email@gmail.com"  # ← Your email
  smtp_server: "smtp.gmail.com"
  smtp_port: 587
  sender_email: "your-actual-email@gmail.com"  # ← Your email
  sender_password: "your-app-password-here"  # ← Get this from Google
```

**Get Gmail App Password:**
1. Go to https://myaccount.google.com/security
2. Enable 2-Step Verification
3. Go to App Passwords
4. Create password for "Mail"
5. Copy the 16-character password
6. Paste into config.yaml

### 3. Configure GitHub Deployment

Edit `/Users/rena/ai-weekly-digest/config.yaml`:

```yaml
github:
  enabled: true
  repo: "YOUR-USERNAME/ai-weekly-digest"  # ← Your GitHub repo
  branch: "gh-pages"
  pdf_export: true
```

### 4. Set Anthropic API Key

Edit `/Users/rena/ai-weekly-digest/com.aiweekly.digest.plist`:

```xml
<key>ANTHROPIC_API_KEY</key>
<string>YOUR_ACTUAL_ANTHROPIC_API_KEY</string>  <!-- Replace this -->
```

Or for testing, set environment variable:
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

### 5. Install Dependencies

```bash
cd /Users/rena/ai-weekly-digest
./setup.sh
```

### 6. Test the System

```bash
# Test full pipeline
python3 generate_weekly_digest.py
```

This should:
- ✅ Collect news (30-60 seconds)
- ✅ Curate with Claude (10-20 seconds)
- ✅ Generate presentation (5-10 seconds)
- ✅ Send email to your inbox
- ✅ Deploy to GitHub Pages

**Check:**
- Presentation in `~/Downloads/AI_Weekly_*.pptx`
- Email in your inbox
- GitHub Pages at `https://YOUR-USERNAME.github.io/ai-weekly-digest/`

### 7. Enable GitHub Pages

After first successful deployment:

1. Go to https://github.com/YOUR-USERNAME/ai-weekly-digest
2. Settings → Pages
3. Source: **gh-pages** branch
4. Click Save

Your digest will be live at:
`https://YOUR-USERNAME.github.io/ai-weekly-digest/`

### 8. Enable Sunday Automation

```bash
# Copy launchd plist
cp /Users/rena/ai-weekly-digest/com.aiweekly.digest.plist ~/Library/LaunchAgents/

# Load it
launchctl load ~/Library/LaunchAgents/com.aiweekly.digest.plist

# Verify it's running
launchctl list | grep aiweekly
```

You should see: `com.aiweekly.digest`

### 9. Update Portfolio

The portfolio at `/Users/rena/eirini-portfolio` has been updated to include:
- New project title: "PowerPoint MCP Server + AI Weekly Digest Automation"
- Link to live digest: `https://EiriniOr.github.io/ai-weekly-digest/`
- Updated highlights showing automation features

**Deploy portfolio changes:**
```bash
cd /Users/rena/eirini-portfolio
git add src/App.jsx
git commit -m "Update portfolio with AI Weekly Digest automation features"
git push origin main
```

## What Happens Next

### Every Sunday at 6:00 PM:

```
18:00:00 - System starts
18:00:30 - News collected from APIs
18:00:50 - Claude curates content
18:01:00 - Presentation generated
18:01:10 - Email sent to your inbox ✉️
18:01:20 - Deployed to GitHub Pages 🌐
18:01:30 - Done! ✅
```

### You'll receive:
1. **Email** with presentation attached
2. **GitHub Pages** updated with latest digest
3. **Portfolio** automatically shows current week's digest

## Customization

### Change Topics

Edit `config.yaml`:
```yaml
curation:
  focus_topics:
    - "autonomous agents"  # Add your topics
    - "reinforcement learning"
    - "computer vision"
```

### Change Schedule

Edit `com.aiweekly.digest.plist`:
```xml
<key>Weekday</key>
<integer>5</integer>  <!-- 5 = Friday -->
<key>Hour</key>
<integer>9</integer>  <!-- 9 AM -->
```

Then reload:
```bash
launchctl unload ~/Library/LaunchAgents/com.aiweekly.digest.plist
launchctl load ~/Library/LaunchAgents/com.aiweekly.digest.plist
```

### Disable Email/GitHub

Edit `config.yaml`:
```yaml
email:
  enabled: false  # No email

github:
  enabled: false  # No GitHub deployment
```

## Monitoring

### View Logs
```bash
# Output log
tail -f /Users/rena/ai-weekly-digest/logs/stdout.log

# Error log
tail -f /Users/rena/ai-weekly-digest/logs/stderr.log
```

### Check Status
```bash
# Is automation running?
launchctl list | grep aiweekly

# Force run now (for testing)
launchctl start com.aiweekly.digest
```

## Troubleshooting

### Email not sending
- Verify Gmail app password in `config.yaml`
- Check 2-step verification is enabled
- Look at logs: `cat logs/stderr.log`

### GitHub deployment failing
- Verify repo name in `config.yaml`
- Check GitHub credentials
- Make sure repository is public
- Check push permissions

### Automation not running
```bash
# Reload launchd
launchctl unload ~/Library/LaunchAgents/com.aiweekly.digest.plist
launchctl load ~/Library/LaunchAgents/com.aiweekly.digest.plist

# Check API key in plist
grep ANTHROPIC_API_KEY ~/Library/LaunchAgents/com.aiweekly.digest.plist
```

### No presentations generated
- Check `logs/stderr.log` for errors
- Verify internet connection
- Test manually: `python3 generate_weekly_digest.py`
- Check API key is valid

## File Locations

- **Main script**: `/Users/rena/ai-weekly-digest/generate_weekly_digest.py`
- **Config**: `/Users/rena/ai-weekly-digest/config.yaml`
- **Automation**: `~/Library/LaunchAgents/com.aiweekly.digest.plist`
- **Logs**: `/Users/rena/ai-weekly-digest/logs/`
- **Output**: `~/Downloads/AI_Weekly_*.pptx`
- **GitHub Pages**: `https://YOUR-USERNAME.github.io/ai-weekly-digest/`

## Cost

- **Claude API**: ~$0.01-0.05 per week
- **GitHub Pages**: Free
- **Email**: Free (Gmail)
- **Total**: ~$2-3 per year

## Support

- Check logs first
- Test components individually
- See `README.md` for detailed documentation
- See `GITHUB_SETUP.md` for GitHub-specific help

## Next Steps

1. ✅ Complete steps 1-9 above
2. ✅ Test everything manually
3. ✅ Verify email and GitHub Pages work
4. ✅ Enable automation
5. ✅ Wait for Sunday 6 PM
6. 🎉 Enjoy automated learning!

---

**You're all set!** Every Sunday you'll get a fresh AI digest in your inbox and on GitHub Pages. 🚀

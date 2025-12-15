# YouTube API Setup Guide

This guide will help you set up automatic YouTube video uploads for your AI Weekly Digest.

## Prerequisites

- A Google account
- A YouTube channel (you already have: https://www.youtube.com/channel/UCUPSLoXvaMVbOIaXsOorHng)
- Access to Google Cloud Console

## Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Name it "AI Weekly Digest" (or any name you prefer)
4. Click "Create"

## Step 2: Enable YouTube Data API v3

1. In your project, go to "APIs & Services" → "Library"
2. Search for "YouTube Data API v3"
3. Click on it and then click "Enable"

## Step 3: Create OAuth 2.0 Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted to configure OAuth consent screen:
   - Click "Configure consent screen"
   - Choose "External" (unless you have a Google Workspace)
   - Fill in the required fields:
     - App name: "AI Weekly Digest"
     - User support email: your email
     - Developer contact information: your email
   - Click "Save and Continue"
   - Skip "Scopes" for now
   - Add your email as a test user
   - Click "Save and Continue"

4. Back to "Create OAuth client ID":
   - Application type: "Desktop app"
   - Name: "AI Weekly Digest Uploader"
   - Click "Create"

5. **Download the credentials**:
   - Click "Download JSON" on the credential you just created
   - Save it as `client_secrets.json`

## Step 4: Add Credentials to GitHub Secrets

### For GitHub Actions (Automated Uploads)

You need to convert your OAuth credentials to base64 and add them as a GitHub secret.

1. Open Terminal and run:
   ```bash
   # Navigate to where you saved client_secrets.json
   cd ~/Downloads  # or wherever you saved it

   # Convert to base64
   base64 -i client_secrets.json | pbcopy
   ```
   (This copies the base64 string to your clipboard)

2. Go to your GitHub repository: https://github.com/EiriniOr/ai-weekly-digest/settings/secrets/actions

3. Click "New repository secret"

4. Add the secret:
   - Name: `YOUTUBE_CREDENTIALS_BASE64`
   - Value: Paste the base64 string from your clipboard
   - Click "Add secret"

### Important: Initial Authentication

The first time the system tries to upload, it needs to authenticate interactively. You have two options:

#### Option A: Authenticate Locally First (Recommended)

1. Move the `client_secrets.json` to your project:
   ```bash
   mkdir -p /Users/rena/ai-weekly-digest/.credentials
   mv ~/Downloads/client_secrets.json /Users/rena/ai-weekly-digest/.credentials/youtube_credentials.json
   ```

2. Run a test upload locally (after generating a video):
   ```bash
   cd /Users/rena/ai-weekly-digest
   python3 scripts/upload_youtube.py
   ```

3. A browser window will open asking you to authorize the app
4. Sign in with your Google account and grant permissions
5. This creates a `youtube_token.json` file in `.credentials/`

6. Convert the token to base64 and add as another GitHub secret:
   ```bash
   cd .credentials
   base64 -i youtube_token.json | pbcopy
   ```

7. In GitHub Secrets, add:
   - Name: `YOUTUBE_TOKEN_BASE64`
   - Value: Paste the token

8. Update `.github/workflows/weekly-digest.yml` to restore the token file before running

#### Option B: Use Service Account (More Complex)

For fully automated uploads without manual authentication, you can use a service account with domain-wide delegation. This is more complex but doesn't require initial manual authentication.

## Step 5: Security Best Practices

1. **Never commit credentials to Git**:
   - The `.credentials/` directory is already in `.gitignore`
   - Always use environment variables or secrets for credentials

2. **Restrict API Scopes**:
   - The app only requests `youtube.upload` scope (minimal permissions)

3. **Monitor API Usage**:
   - YouTube API has quotas (10,000 units/day free)
   - Uploading one video uses ~1,600 units
   - You can upload ~6 videos per day within free quota

## Step 6: Test the Integration

After setting up credentials:

1. **Add the OPENAI_API_KEY secret** (if not already done):
   - Go to: https://github.com/EiriniOr/ai-weekly-digest/settings/secrets/actions
   - Add secret:
     - Name: `OPENAI_API_KEY`
     - Value: `your-openai-api-key-here`

2. **Manually trigger the workflow**:
   - Go to: https://github.com/EiriniOr/ai-weekly-digest/actions
   - Click "Generate Weekly AI Digest"
   - Click "Run workflow"
   - Watch the logs to see if video uploads successfully

3. **Check your YouTube channel**:
   - Videos may be in "Processing" status for a few minutes
   - Check: https://studio.youtube.com/channel/UCUPSLoXvaMVbOIaXsOorHng/videos

## Troubleshooting

### "The OAuth client was not found"
- Make sure you enabled YouTube Data API v3 in the correct project
- Verify the client_secrets.json is from the correct project

### "Access Not Configured"
- Enable YouTube Data API v3 in Google Cloud Console
- Wait a few minutes for changes to propagate

### "Invalid Credentials"
- Check that your base64 encoding is correct
- Make sure there are no extra spaces or newlines
- Try re-downloading the credentials

### "Quota Exceeded"
- YouTube API has a daily quota of 10,000 units
- Each upload uses ~1,600 units
- Wait 24 hours for quota to reset
- Or request quota increase in Google Cloud Console

## Cost

- YouTube Data API: **FREE** (within quota limits)
- OpenAI TTS: ~$0.04 per video
- Total: ~$0.04 per week ($2.08/year)

## What Happens Now

Once set up:

1. Every Sunday at 6:00 PM UTC:
   - GitHub Actions collects AI news
   - Claude curates the content
   - OpenAI generates voice narration
   - moviepy creates the video
   - **Video automatically uploads to YouTube**
   - Webpage deploys to GitHub Pages

2. Your channel will automatically get weekly videos!

3. You can still manually trigger anytime from GitHub Actions

## Further Customization

Edit `/Users/rena/ai-weekly-digest/scripts/upload_youtube.py` to customize:
- Video title format
- Description template
- Tags and categories
- Privacy settings (public/unlisted/private)
- Playlist assignment

Enjoy your automated YouTube channel! 🎉

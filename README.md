# news-cron-job

Automated scheduler for the [NewsMonitor](https://github.com/MSNYC/NewsMonitor) email digest system. Uses GitHub Actions to trigger news email delivery twice daily.

## Overview

This repository contains a small Python script that triggers the NewsMonitor serverless function on Vercel. It runs on a cron schedule via GitHub Actions, sending GET requests to the Vercel endpoint at 8 AM and 8 PM ET.

## Architecture

```
┌─────────────────┐
│ GitHub Actions  │  Cron: 8 AM & 8 PM ET
│  (cron.yml)     │
└────────┬────────┘
         │ HTTP GET + API Key Header
         ▼
┌─────────────────┐
│ Vercel Function │  https://news-monitor-five.vercel.app
│ (NewsMonitor)   │  Fetches RSS feeds & sends email
└─────────────────┘
```

## Prerequisites

- GitHub account (for running cron jobs)
- Deployed [NewsMonitor](https://github.com/MSNYC/NewsMonitor) instance on Vercel
- API key from your Vercel environment variables

## Setup

### 1. Fork or Clone This Repository

```bash
git clone https://github.com/YOUR_USERNAME/news-cron-job.git
cd news-cron-job
```

### 2. Add GitHub Secret

1. Go to your repository **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Name: `MY_SECRET_API_KEY`
4. Value: Copy the API key from your Vercel environment variables (must match the `MY_SECRET_API_KEY` in your NewsMonitor Vercel deployment)
5. Click **Add secret**

### 3. Update Vercel URL (if needed)

If your NewsMonitor deployment URL is different, edit `run_cron.py` or set a `VERCEL_URL` environment variable:

```python
VERCEL_URL = "https://your-deployment-url.vercel.app/api/send-news"
```

### 4. Enable GitHub Actions

1. Go to the **Actions** tab in your repository
2. If prompted, click **"I understand my workflows, go ahead and enable them"**
3. The cron job will now run automatically at 8 AM and 8 PM ET

## How It Works

### Cron Schedule

The workflow triggers twice daily:
- **8:00 AM ET** (1:00 PM UTC) - `cron: '0 13 * * *'`
- **8:00 PM ET** (1:00 AM UTC) - `cron: '0 1 * * *'`

### Retry Logic

The script includes robust error handling:
- **3 retry attempts** with 30-second delays
- **120-second timeout** per request (allows Vercel cold starts)
- Handles connection errors, timeouts, and HTTP failures
- Exits with proper status codes for GitHub Actions monitoring
- Avoids printing response bodies to public Actions logs

### Manual Testing

You can manually trigger the workflow:
1. Go to **Actions** tab
2. Select **"Send News Email Cron Job"**
3. Click **"Run workflow"**
4. Select branch and click **"Run workflow"**

## Files

- **`run_cron.py`** - Main script that sends HTTP request to Vercel
- **`.github/workflows/cron.yml`** - GitHub Actions workflow configuration
- No third-party Python dependencies required

## Customization

### Change Schedule

Edit `.github/workflows/cron.yml`:

```yaml
schedule:
  - cron: '0 9,21 * * *'  # 9 AM & 9 PM UTC (adjust for your timezone)
```

**Cron syntax:** `minute hour day month day-of-week`

### Adjust Retry Settings

Edit `run_cron.py`:

```python
max_retries = 5  # Increase retry attempts
timeout = 180    # Increase timeout to 3 minutes
```

## Monitoring

### Check Workflow Status

1. Go to **Actions** tab
2. View recent workflow runs
3. Click on any run to see detailed logs

### Successful Run

```
Attempt 1/3: Sending request to https://news-monitor-five.vercel.app/api/send-news
News email triggered successfully!
```

### Failed Run

If all retries fail, the workflow will exit with status code 1, and GitHub will mark the run as failed. Check:
- Vercel function logs for errors
- API key matches between GitHub Secrets and Vercel environment variables
- Vercel deployment is active and responding

## Cost

For standard GitHub-hosted runners, GitHub Actions usage is free in public repositories. Private repositories use the account plan's monthly Actions quota. This cron job should use very little time either way, but public visibility is the clearest way to keep runner cost at $0.

## Troubleshooting

### Workflow not running automatically?

- Ensure GitHub Actions is enabled in repository settings
- Check that the cron schedule is correct for your timezone
- GitHub Actions may have up to 10-minute delays during high load
- Public repository scheduled workflows are automatically disabled after 60 days with no repository activity

### Getting 403 Forbidden errors?

- API key mismatch - verify `MY_SECRET_API_KEY` matches in both:
  - GitHub Secrets (this repo)
  - Vercel environment variables (NewsMonitor)

### Timeout errors?

- Vercel cold starts can take 10-20 seconds
- Script already has 120-second timeout
- Check Vercel function logs for issues

### Manual trigger not working?

- Ensure you have write permissions to the repository
- Check that the workflow file has no YAML syntax errors

## Security

- ✅ API key stored as GitHub Secret (encrypted)
- ✅ No credentials in code
- ✅ `.env` files ignored by git
- ✅ Uses environment variables exclusively
- ✅ Workflow runs with read-only repository permissions
- ✅ Checkout credentials are not persisted
- ✅ Failure logs do not print response bodies from the remote endpoint

## Related Projects

- [NewsMonitor](https://github.com/MSNYC/NewsMonitor) - Main news aggregation and email delivery system

## License

MIT License - feel free to use for personal or commercial projects.

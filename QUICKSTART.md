# 🚀 MyFlixVault - Quick Start Guide

Get up and running in 5 minutes!

## Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install flask requests pillow
```

## Step 2: Get API Key

Choose one:

### Option A: TMDB (Recommended)
1. Go to https://www.themoviedb.org/signup
2. Create free account
3. Go to Settings → API
4. Request API key (instant approval)

### Option B: OMDB
1. Go to http://www.omdbapi.com/apikey.aspx
2. Enter email for free key
3. Check email for activation

## Step 3: Run Application

```bash
python main.py
```

You should see:
```
* Running on http://0.0.0.0:8080
```

## Step 4: Initial Setup

1. Open browser to: `http://localhost:8080`
2. Click **Settings** (gear icon)
3. Enter your API key
4. Set local media path (if you have local videos)
5. Click **Save Settings**

## Step 5: Add Your First Entry

### Method 1: Manual Entry
1. Click **+ Add** button
2. Fill in:
   - Category: Movie or Series
   - Name: "Inception"
   - Year: "2010"
   - Type: "Sci-Fi"
3. Click **Save Entry**
4. Poster auto-loads!

### Method 2: From Local Files
1. Set local media path in Settings
2. Go to **Local Videos**
3. Browse your files
4. Click **+** on any item to add to collection

## You're Done! 🎉

### Quick Tips:

**Search**: Press `Ctrl+K` or use search bar

**Filter Series**: Click status buttons (Watching, Finished, etc.)

**Watch Video**: Click on any card → Select file → Enjoy!
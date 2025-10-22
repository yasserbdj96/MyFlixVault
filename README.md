# 🎬 MyFlixVault

<div align="center">

![MyFlixVault Logo](https://raw.githubusercontent.com/yasserbdj96/MyFlixVault/main/static/logo.png)

**A Professional Personal Media Collection Manager with Netflix-Inspired UI**

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](CONTRIBUTING.md)

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Screenshots](#-screenshots) • [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Configuration](#-configuration)
- [Usage Guide](#-usage-guide)
- [Keyboard Shortcuts](#%EF%B8%8F-keyboard-shortcuts)
- [API Integration](#-api-integration)
- [Screenshots](#-screenshots)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [Roadmap](#-roadmap)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

---

## 🌟 Overview

MyFlixVault is a feature-rich, self-hosted personal media collection manager designed for movie and TV series enthusiasts. With a modern Netflix-inspired interface, it helps you organize, track, and manage your entire media library with ease.

### Why MyFlixVault?

- 🎨 **Modern UI/UX** - Beautiful, responsive interface inspired by Netflix
- 📱 **Cross-Platform** - Works seamlessly on desktop, tablet, and mobile
- 🎥 **Local Media Support** - Stream videos directly from your hard drive
- 📊 **Rich Statistics** - Track your watching habits and collection insights
- 🔒 **Privacy-Focused** - All data stored locally, no cloud dependencies
- ⚡ **Fast & Lightweight** - Built with performance in mind

---

## ✨ Features

### 🎬 Core Features

- **Collection Management**
  - Add, edit, and delete movies and TV series
  - Automatic poster fetching from TMDB/OMDB
  - Support for multiple API providers
  - Duplicate detection to prevent redundant entries
  - Rating system (0-10 scale)
  - Personal notes for each entry

- **Local Media Integration**
  - Browse and play videos from your local storage
  - Automatic metadata extraction from filenames
  - Support for MP4, MKV, AVI, MOV formats
  - Series episode detection and organization
  - Smart file scanning and categorization

- **Enhanced Video Player**
  - Custom HTML5 video player with modern controls
  - Playback speed control (0.25x - 2x)
  - Picture-in-Picture (PiP) mode
  - Subtitle support (.srt, .vtt, .ass)
  - Keyboard shortcuts for seamless control
  - Progress saving and resume playback
  - Quality detection (SD/HD/FHD/4K)

### 🔍 Smart Features

- **Advanced Search & Filter**
  - Real-time search with debouncing
  - Filter by status (Watching, Finished, Awaiting, Stopped)
  - Sort by name, year, or date added
  - Search persistence across sessions

- **Watch History**
  - Automatic tracking of watched content
  - Timestamp logging
  - Last 50 entries preserved
  - Quick access sidebar

- **Statistics Dashboard**
  - Total movies and series count
  - Series by completion status
  - Content by year and country
  - Visual analytics

### 🎨 Customization

- **Theme Support**
  - Dark mode (default)
  - Light mode
  - Instant theme switching
  - CSS variable-based theming

- **Settings & Configuration**
  - Multiple API providers (TMDB, OMDB, Custom)
  - Poster quality selection (185px - Original)
  - Automatic backup system
  - Duplicate checking toggle
  - Custom local media paths

### 💾 Data Management

- **Backup & Export**
  - Automatic backups on every change (optional)
  - Manual export to JSON format
  - Import from backup files
  - Timestamped backup files
  - Metadata preservation

- **Poster Management**
  - Scan for empty posters
  - Bulk poster regeneration
  - Local poster caching
  - Automatic fallback images

---

## 🛠️ Tech Stack

### Backend
- **Flask 3.0.0** - Python web framework
- **Pillow 10.1.0** - Image processing
- **Requests 2.31.0** - HTTP library

### Frontend
- **HTML5 & CSS3** - Modern web standards
- **Vanilla JavaScript** - No framework dependencies
- **Font Awesome 6.4.0** - Icon library

### APIs
- **TMDB API** - The Movie Database (recommended)
- **OMDB API** - Open Movie Database
- **Custom API** - Support for custom endpoints

---

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (for cloning the repository)

### Step 1: Clone Repository

```bash
git clone https://github.com/yasserbdj96/MyFlixVault.git
cd MyFlixVault
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install Flask==3.0.0 requests==2.31.0 Pillow==10.1.0 Werkzeug==3.0.1
```

### Step 3: Get API Key

Choose one of the following:

#### Option A: TMDB (Recommended)
1. Visit [The Movie Database](https://www.themoviedb.org/signup)
2. Create a free account
3. Go to Settings → API
4. Request an API key (instant approval)

#### Option B: OMDB
1. Visit [OMDb API](http://www.omdbapi.com/apikey.aspx)
2. Enter your email
3. Check email for activation link
4. Copy your API key

### Step 4: Run Application

```bash
python main.py
```

The application will start on `http://localhost:8080`

---

## 🚀 Quick Start

### First Time Setup

1. **Open Browser**
   ```
   http://localhost:8080
   ```

2. **Configure Settings**
   - Click the ⚙️ Settings icon
   - Select API provider (TMDB/OMDB)
   - Enter your API key
   - Set local media path (optional)
   - Choose theme (Dark/Light)
   - Save settings

3. **Add Your First Entry**
   - Click **+ Add** button
   - Select category (Movie/Series)
   - Enter details:
     - Name: "Inception"
     - Year: "2010"
     - Country: "US"
     - Type: "Sci-Fi"
   - Click **Save Entry**
   - Poster loads automatically!

4. **Browse Local Media** (Optional)
   - Set local media path in Settings
   - Click 📁 Local Videos
   - Browse and play your videos
   - Add items to collection with one click

---

## ⚙️ Configuration

### Settings Overview

| Setting | Description | Default |
|---------|-------------|---------|
| **API Provider** | Movie database source | TMDB |
| **API Key** | Authentication key | - |
| **Local Media Path** | Path to video files | - |
| **Theme** | UI color scheme | Dark |
| **Poster Quality** | Image resolution | w500 (High) |
| **Auto Backup** | Backup on changes | Disabled |
| **Check Duplicates** | Prevent duplicate names | Enabled |

### Setting Local Media Path

#### Windows
```
D:\Media
or
D:\\Videos\\Movies
```

#### Linux/Mac
```
/home/username/Videos
or
/mnt/media/Movies
```

### Poster Quality Options

| Quality | Resolution | File Size | Recommended For |
|---------|-----------|-----------|-----------------|
| Low | 185px | ~20KB | Slow connections |
| Medium | 342px | ~50KB | Balanced |
| High | 500px | ~100KB | Most users ✓ |
| Very High | 780px | ~200KB | Large screens |
| Original | Full | ~500KB+ | Archival |

---

## 📖 Usage Guide

### Managing Your Collection

#### Adding Content

**Manual Entry:**
1. Click **+ Add**
2. Fill in details
3. Poster auto-fetches
4. Click **Save**

**From Local Files:**
1. Go to **Local Videos**
2. Click **+** on any item
3. Metadata pre-filled
4. Verify and save

#### Editing Entries

1. Click ✏️ edit icon on card
2. Update information
3. Optional: Check "Regenerate Poster"
4. Click **Save Entry**

#### Deleting Entries

1. Click 🗑️ delete icon
2. Confirm deletion
3. Entry removed permanently

### Playing Videos

#### From Collection
1. Click on any card
2. Modal shows available files
3. Select version/episode
4. Video player opens

#### From Local Videos
1. Browse **Local Videos** page
2. Click on card
3. For series: select episode
4. Click **Play**

### Video Player Controls

#### Mouse Controls
- **Click video** - Play/Pause
- **Hover** - Show controls
- **Progress bar** - Seek to position
- **Volume** - Hover and adjust

#### Touch Controls
- **Tap video** - Play/Pause
- **Tap controls** - Show/Hide
- **Swipe progress** - Seek
- **Pinch** - Zoom (if supported)

---

## ⌨️ Keyboard Shortcuts

### Main Interface

| Key | Action |
|-----|--------|
| `Ctrl/Cmd + K` | Focus search |
| `Escape` | Clear search |
| `1` | Switch to Series tab |
| `2` | Switch to Movies tab |

### Video Player

| Key | Action |
|-----|--------|
| `Space` or `K` | Play/Pause |
| `←` | Rewind 5 seconds |
| `→` | Forward 5 seconds |
| `↑` | Increase volume |
| `↓` | Decrease volume |
| `M` | Mute/Unmute |
| `F` | Toggle fullscreen |
| `P` | Picture-in-Picture |
| `J` | Rewind 10 seconds |
| `L` | Forward 10 seconds |
| `C` | Toggle subtitles |
| `0-9` | Jump to 0%-90% |
| `<` or `,` | Decrease speed |
| `>` or `.` | Increase speed |

---

## 🔌 API Integration

### TMDB API

**Endpoints Used:**
- `/search/movie` - Search movies
- `/search/tv` - Search TV series
- `/movie/{id}/videos` - Get movie trailers
- `/tv/{id}/videos` - Get series trailers

**Example Request:**
```python
params = {
    'api_key': 'YOUR_API_KEY',
    'query': 'Inception',
    'year': '2010'
}
response = requests.get('https://api.themoviedb.org/3/search/movie', params=params)
```

### OMDB API

**Example Request:**
```python
params = {
    'apikey': 'YOUR_API_KEY',
    't': 'Inception',
    'y': '2010',
    'type': 'movie'
}
response = requests.get('http://www.omdbapi.com/', params=params)
```

### Custom API

Configure custom endpoints in Settings:
- Poster API URL
- Trailer API URL

Format expected:
```json
{
  "poster_url": "https://...",
  "trailer_url": "https://..."
}
```

---

## 📸 Screenshots

### Main Collection View
*Beautiful Netflix-inspired interface with cards and smooth animations*
<div align="center">
    <a href="https://raw.githubusercontent.com/yasserbdj96/MyFlixVault/main/screenshot/interface-1.png">
        <img height="100" src="https://raw.githubusercontent.com/yasserbdj96/MyFlixVault/main/screenshot/interface-1.png" alt="Beautiful Netflix-inspired interface with cards and smooth animations">
    </a>
    <a href="https://raw.githubusercontent.com/yasserbdj96/MyFlixVault/main/screenshot/interface-2.png">
        <img height="100" src="https://raw.githubusercontent.com/yasserbdj96/MyFlixVault/main/screenshot/interface-2.png" alt="Beautiful Netflix-inspired interface with cards and smooth animations">
    </a>
    <a href="https://raw.githubusercontent.com/yasserbdj96/MyFlixVault/main/screenshot/interface-3.png">
        <img height="100" src="https://raw.githubusercontent.com/yasserbdj96/MyFlixVault/main/screenshot/interface-3.png" alt="Beautiful Netflix-inspired interface with cards and smooth animations">
    </a>
    <a href="https://raw.githubusercontent.com/yasserbdj96/MyFlixVault/main/screenshot/interface-4.png">
        <img height="100" src="https://raw.githubusercontent.com/yasserbdj96/MyFlixVault/main/screenshot/interface-4.png" alt="Beautiful Netflix-inspired interface with cards and smooth animations">
    </a>
    <a href="https://raw.githubusercontent.com/yasserbdj96/MyFlixVault/main/screenshot/interface-5.png">
        <img height="100" src="https://raw.githubusercontent.com/yasserbdj96/MyFlixVault/main/screenshot/interface-5.png" alt="Beautiful Netflix-inspired interface with cards and smooth animations">
    </a>
    <a href="https://raw.githubusercontent.com/yasserbdj96/MyFlixVault/main/screenshot/interface-6.png">
        <img height="100" src="https://raw.githubusercontent.com/yasserbdj96/MyFlixVault/main/screenshot/interface-6.png" alt="Beautiful Netflix-inspired interface with cards and smooth animations">
    </a>
    <a href="https://raw.githubusercontent.com/yasserbdj96/MyFlixVault/main/screenshot/interface-7.png">
        <img height="100" src="https://raw.githubusercontent.com/yasserbdj96/MyFlixVault/main/screenshot/interface-7.png" alt="Beautiful Netflix-inspired interface with cards and smooth animations">
    </a>
</div>

### Video Player
*Professional HTML5 player with custom controls and subtitle support*
<div align="center">
    <a href="https://raw.githubusercontent.com/yasserbdj96/MyFlixVault/main/screenshot/player.png">
        <img height="100" src="https://raw.githubusercontent.com/yasserbdj96/MyFlixVault/main/screenshot/player.png" alt="Professional HTML5 player with custom controls and subtitle support">
    </a>
</div>


### Local Media Browser
*Browse and organize your local video files*
<div align="center">
    <a href="https://raw.githubusercontent.com/yasserbdj96/MyFlixVault/main/screenshot/local-1.png">
        <img height="100" src="https://raw.githubusercontent.com/yasserbdj96/MyFlixVault/main/screenshot/local-1.png" alt="Browse and organize your local video files">
    </a>
    <a href="https://raw.githubusercontent.com/yasserbdj96/MyFlixVault/main/screenshot/local-2.png">
        <img height="100" src="https://raw.githubusercontent.com/yasserbdj96/MyFlixVault/main/screenshot/local-2.png" alt="Browse and organize your local video files">
    </a>
</div>

### Statistics Dashboard
*Track your collection and watching habits*
<div align="center">
    <a href="https://raw.githubusercontent.com/yasserbdj96/MyFlixVault/main/screenshot/Dashboard-1.png">
        <img height="100" src="https://raw.githubusercontent.com/yasserbdj96/MyFlixVault/main/screenshot/Dashboard-1.png" alt="Track your collection and watching habits">
    </a>
    <a href="https://raw.githubusercontent.com/yasserbdj96/MyFlixVault/main/screenshot/Dashboard-2.png">
        <img height="100" src="https://raw.githubusercontent.com/yasserbdj96/MyFlixVault/main/screenshot/Dashboard-2.png" alt="Track your collection and watching habits">
    </a>
    <a href="https://raw.githubusercontent.com/yasserbdj96/MyFlixVault/main/screenshot/Dashboard-3.png">
        <img height="100" src="https://raw.githubusercontent.com/yasserbdj96/MyFlixVault/main/screenshot/Dashboard-3.png" alt="Track your collection and watching habits">
    </a>
</div>

---

## 🐛 Troubleshooting

### Common Issues

#### Posters Not Loading
**Problem:** Images show placeholder icons

**Solutions:**
1. Verify API key in Settings
2. Check internet connection
3. Try regenerating poster (Edit → Regenerate)
4. Check temp folder permissions

#### Local Videos Not Found
**Problem:** "No files found" message

**Solutions:**
1. Verify local media path format:
   - Windows: `D:\Media` or `D:\\Media`
   - Linux/Mac: `/home/user/Videos`
2. Check folder read permissions
3. Ensure video formats are supported (MP4, MKV, AVI, MOV)
4. Try absolute path instead of relative

#### Video Won't Play
**Problem:** Player shows error or black screen

**Solutions:**
1. Check video codec compatibility (H.264/MP4 recommended)
2. Try different browser (Chrome/Edge recommended)
3. Verify file path is accessible
4. Check file isn't corrupted
5. Ensure local media path is correct

#### Search Not Working
**Problem:** Search returns no results

**Solutions:**
1. Clear browser cache (Ctrl+F5)
2. Check JavaScript console for errors (F12)
3. Try refreshing page
4. Verify JSON file isn't corrupted

### Database Issues

#### Reset Collection
```bash
# Backup first!
cp my_list.json my_list.json.backup

# Start fresh
rm my_list.json
python main.py
```

#### Restore from Backup
1. Go to Settings
2. Click "Import Collection"
3. Select backup file
4. Confirm restore

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Reporting Bugs

1. Check existing issues
2. Create detailed bug report
3. Include:
   - OS and Python version
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable

### Suggesting Features

1. Open feature request issue
2. Describe use case
3. Explain expected behavior
4. Consider implementation approach

### Pull Requests

1. Fork repository
2. Create feature branch
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. Make changes
4. Test thoroughly
5. Commit with clear messages
6. Push to branch
7. Open Pull Request

### Code Style

- Follow PEP 8 for Python
- Use meaningful variable names
- Comment complex logic
- Update documentation

---

## 🗺️ Roadmap

### Version 2.1 (Planned)
- [ ] Multi-user support with authentication
- [ ] Cloud sync (Google Drive, Dropbox)
- [ ] Advanced filtering (genre, rating, decade)
- [ ] Watchlist and favorites
- [ ] IMDb integration
- [ ] Batch import from folder

### Version 2.2 (Future)
- [ ] Mobile app (React Native)
- [ ] Recommendation engine
- [ ] Social features (share collections)
- [ ] Plex/Jellyfin integration
- [ ] Subtitle download automation
- [ ] Poster customization

### Version 3.0 (Vision)
- [ ] AI-powered metadata extraction
- [ ] Torrent integration
- [ ] Streaming service tracking
- [ ] Advanced analytics dashboard
- [ ] Plugin system
- [ ] Docker container support

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 MyFlixVault

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

---

## 🙏 Acknowledgments

### APIs & Services
- [The Movie Database (TMDB)](https://www.themoviedb.org/) - Movie and TV data
- [OMDb API](http://www.omdbapi.com/) - Alternative movie database
- [Font Awesome](https://fontawesome.com/) - Icon library

### Technologies
- [Flask](https://flask.palletsprojects.com/) - Python web framework
- [Pillow](https://python-pillow.org/) - Image processing
- [Requests](https://requests.readthedocs.io/) - HTTP library

### Inspiration
- Netflix - UI/UX design inspiration
- Plex - Media organization concepts
- Jellyfin - Open-source media server ideas

---

## 📞 Support

### Get Help
- 📖 [Documentation](docs/)
- 💬 [Discussions](https://github.com/yasserbdj96/MyFlixVault/discussions)
- 🐛 [Issue Tracker](https://github.com/yasserbdj96/MyFlixVault/issues)

### Community
- ⭐ Star this repository
- 🍴 Fork and contribute
- 📢 Share with friends

---

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/yasserbdj96/MyFlixVault?style=social)
![GitHub forks](https://img.shields.io/github/forks/yasserbdj96/MyFlixVault?style=social)
![GitHub issues](https://img.shields.io/github/issues/yasserbdj96/MyFlixVault)
![GitHub pull requests](https://img.shields.io/github/issues-pr/yasserbdj96/MyFlixVault)

---

<div align="center">

**Made with ❤️ by movie and TV enthusiasts, for enthusiasts**

[⬆ Back to Top](#-MyFlixVault)

</div>
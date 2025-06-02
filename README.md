  <p align="center">
  <img src="static/logo.png" alt="MyFlixVault Logo" width="200"/>
</p>

  # MyFlixVault - Media Collection Manager

  MyFlixVault is a self-hosted media collection manager that helps you organize and access your movie and TV show collection. It features automatic metadata fetching, local media playback, and a clean web interface.

  ## Features

  - 🎬 **Media Organization**: Manage movies and TV series with posters, metadata, and viewing status
  - 🖼️ **Automatic Poster Fetching**: Integrates with TMDB/OMDB APIs to get posters
  - 📺 **Trailer Integration**: Watch trailers directly in the app
  - 💾 **Local Media Playback**: Stream videos from your local storage
  - 🔍 **Smart Search**: Find media quickly with powerful search
  - 📊 **Episode Tracking**: Track watched episodes for TV series
  - ⚙️ **Customizable Settings**: Configure API keys and media paths

  ## Installation

  1. Clone the repository:
  ```bash
  git clone https://github.com/yourusername/myflixvault.git
  cd myflixvault
  ```
  2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

  3. Run the application:
  ```bash
  python main.py
```

  4. Access the web interface at: http://localhost:8080

  # Configuration
  Configure your settings via the Settings page:
  - API Provider: Choose between TMDB (default) or OMDB
  - API Key: Add your TMDB/OMDB API key
  - Local Media Path: Set your media storage location (e.g., D:\Media)

  # Usage
  - Add Media: Click "+ Add" to manually add movies/series
  - Edit Entries: Click "Edit" on any media card
  - Play Local Media: Click any media card to access local files
  - Watch Trailers: Click media cards to view trailers
  - Browse Local Videos: Access via "Local Videos" in header

  # Project Structure
  ```bash
  myflixvault/
├── main.py            # Main application logic
├── my_list.json       # Database of media entries
├── settings.json      # Application configuration
├── temp/              # Cached poster images
├── templates/         # HTML templates
│   ├── index.html
│   ├── add_edit.html
│   ├── settings.html
│   ├── local_videos.html
│   └── video_player.html
├── static/            # Static assets
│   ├── css/
│   ├── js/
│   └── logo.png
└── requirements.txt   # Python dependencies
```

  # Requirements
  - Python 3.7+
  - Flask
  - Requests
  - Pillow

  # Screenshots

<div align="center">
    <a href="https://raw.githubusercontent.com/yasserbdj96/MyFlixVault/main/Screenshot/Screenshot_1.png">
        <img height="100" src="https://raw.githubusercontent.com/yasserbdj96/MyFlixVault/main/Screenshot/Screenshot_1.png" alt="">
    </a>
    <a href="https://raw.githubusercontent.com/yasserbdj96/MyFlixVault/main/Screenshot/Screenshot_2.png">
        <img height="100" src="https://raw.githubusercontent.com/yasserbdj96/MyFlixVault/main/Screenshot/Screenshot_2.png" alt="">
    </a>
    <a href="https://raw.githubusercontent.com/yasserbdj96/MyFlixVault/main/Screenshot/Screenshot_3.png">
        <img height="100" src="https://raw.githubusercontent.com/yasserbdj96/MyFlixVault/main/Screenshot/Screenshot_3.png" alt="">
    </a>
    <a href="https://raw.githubusercontent.com/yasserbdj96/MyFlixVault/main/Screenshot/Screenshot_4.png">
        <img height="100" src="https://raw.githubusercontent.com/yasserbdj96/MyFlixVault/main/Screenshot/Screenshot_4.png" alt="">
    </a>
    <a href="https://raw.githubusercontent.com/yasserbdj96/MyFlixVault/main/Screenshot/Screenshot_5.png">
        <img height="100" src="https://raw.githubusercontent.com/yasserbdj96/MyFlixVault/main/Screenshot/Screenshot_5.png" alt="">
    </a>
    <a href="https://raw.githubusercontent.com/yasserbdj96/MyFlixVault/main/Screenshot/Screenshot_6.png">
        <img height="100" src="https://raw.githubusercontent.com/yasserbdj96/MyFlixVault/main/Screenshot/Screenshot_6.png" alt="">
    </a>
    <a href="https://raw.githubusercontent.com/yasserbdj96/MyFlixVault/main/Screenshot/Screenshot_7.png">
        <img height="100" src="https://raw.githubusercontent.com/yasserbdj96/MyFlixVault/main/Screenshot/Screenshot_7.png" alt="">
    </a>
    <a href="https://raw.githubusercontent.com/yasserbdj96/MyFlixVault/main/Screenshot/Screenshot_8.png">
        <img height="100" src="https://raw.githubusercontent.com/yasserbdj96/MyFlixVault/main/Screenshot/Screenshot_8.png" alt="">
    </a>
</div>

  # License
  MIT License - Free for personal and commercial use
  ```bash
This YAML file contains a comprehensive README with:
1. Project title and description
2. Key features list
3. Installation instructions
4. Configuration guide
5. Usage documentation
6. Project structure overview
7. Requirements
8. License information

The YAML uses the `|` character to preserve markdown formatting in a multi-line string. To use this:
1. Save as `readme.yml`
2. Convert to README.md using:
```
  
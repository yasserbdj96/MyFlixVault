import json
import os
import hashlib
import requests
import re  # Add this import
import urllib.parse
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify, send_file  # Add jsonify, send_file
from PIL import Image
from io import BytesIO
import base64
from collections import defaultdict

SETTINGS_FILE = "settings.json"

class Settings:
    def __init__(self):
        self.api_provider = ""
        self.api_key = ""  # Default key
        self.poster_api_url = ""
        self.trailer_api_url = ""
        self.local_media_path = ""
        
        # Load settings if exists
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                data = json.load(f)
                for key, value in data.items():
                    if key == "local_media_path" and value:
                        # Use path normalization instead of string replacement
                        value = os.path.normpath(value)
                    setattr(self, key, value)

    def save(self):
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(self.__dict__, f, indent=4)

# Initialize settings
app_settings = Settings()

app = Flask(__name__)
JSON_FILE = "my_list.json"
TEMP_FOLDER = "temp"

# Ensure temp directory exists
os.makedirs(TEMP_FOLDER, exist_ok=True)

import os
import re

def extract_media_info(filename):
    name = os.path.splitext(filename)[0]
    original_name = name

    # Replace separators with space
    name = re.sub(r'[_\-.]+', ' ', name)

    # Convert to lowercase for uniform processing
    name = name.lower()

    # Initialize info
    info = {'name': name.strip(), 'type': 'movie'}

    # Try to extract year
    year_match = re.search(r'\b(19\d{2}|20\d{2}|202\d)\b', name)
    if year_match:
        info['year'] = year_match.group(1)
        name = name.replace(info['year'], '')

    # Detect episode formats
    ep_match = re.search(r'\bs(\d{1,2})e(\d{1,2})\b', name) or re.search(r'\b(\d{1,2})x(\d{1,2})\b', name)
    if ep_match:
        info['type'] = 'series'
        info['season'] = int(ep_match.group(1))
        info['episode'] = int(ep_match.group(2))
        info['episode_str'] = f"S{info['season']:02d}E{info['episode']:02d}"
        name = name.replace(ep_match.group(0), '')

    # Remove any standalone episode-like numbers (e.g., One Piece 1015)
    name = re.sub(r'\b\d{3,5}\b', '', name)

    # Remove known junk tags
    junk_tags = [
        r'\b(web[-_. ]?dl|nf|hdtv|mycima|wecima|show|tube|autos|ink|world|ar|weciima|mp4|ova|web)\b',
        r'\b(1080p|720p|4k|bluray|webrip|hdrip)\b',
        r'\bsp\b',
    ]
    for pattern in junk_tags:
        name = re.sub(pattern, '', name, flags=re.IGNORECASE)

    # Clean up extra spaces
    name = re.sub(r'\s+', ' ', name).strip()

    # Final display name
    info['name'] = name.title()

    return info




# Modify get_movie_poster function
def get_movie_poster(movie_name, typeis, year=None, region=None):
    settings = app_settings

    if settings.api_provider == "omdb":
        # OMDB implementation
        base_url = 'http://www.omdbapi.com/'
        params = {
            'apikey': settings.api_key,
            't': movie_name,
            'type': 'movie' if typeis.lower() == 'movie' else 'series',
            'y': year
        }
        response = requests.get(base_url, params=params)
        data = response.json()
        return data.get('Poster') if 'Poster' in data else None

    elif settings.api_provider == "custom" and settings.poster_api_url:
        # Custom API implementation
        base_url = settings.poster_api_url
        # Example: response = requests.get(base_url, params={...})
        # return response.json().get('poster_url')
        return None

    else:  # Default to TMDB
        typeis = typeis.lower().split()[0]
        base_url = f'https://api.themoviedb.org/3/search/{typeis}'
        params = {
            'api_key': settings.api_key,
            'query': movie_name,
        }
        if year:
            if typeis == 'movie':
                params['year'] = year
            elif typeis == 'tv':
                params['first_air_date_year'] = year
        if region:
            params['region'] = region.upper()

        response = requests.get(base_url, params=params)
        response.raise_for_status()
        results = response.json().get('results', [])

        if results:
            title_key = 'title' if typeis == 'movie' else 'name'
            for result in results:
                title = result.get(title_key, '').lower()
                result_year = (result.get('release_date') or result.get('first_air_date') or '')[:4]
                if title == movie_name.lower() and (not year or result_year == str(year)):
                    poster_path = result.get('poster_path')
                    if poster_path:
                        return f'https://image.tmdb.org/t/p/w500{poster_path}'
            poster_path = results[0].get('poster_path')
            if poster_path:
                return f'https://image.tmdb.org/t/p/w500{poster_path}'
        print(f"[WARN] Poster not found for: {movie_name}")
        return None

def get_cached_poster(url, fallback_info=None):
    os.makedirs(TEMP_FOLDER, exist_ok=True)
    filename = hashlib.md5(url.encode()).hexdigest() + ".jpg"
    filepath = os.path.join(TEMP_FOLDER, filename)

    # Serve from cache if file exists
    if os.path.exists(filepath):
        return url_for('poster_file', filename=filename)

    try:
        # Try downloading and resizing the poster
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        img = Image.open(BytesIO(response.content))
        img.thumbnail((200, 300))  # Resize to small
        img.save(filepath, format="JPEG")
        return url_for('poster_file', filename=filename)

    except Exception as e:
        print(f"[ERROR] Failed to fetch/save poster: {e}")

        # If fallback_info is available, try to regenerate poster
        if fallback_info:
            name = fallback_info.get('name')
            media_type = fallback_info.get('type')
            year = fallback_info.get('year')
            country = fallback_info.get('country')

            new_url = get_movie_poster(name, media_type, year=year, region=country)
            if new_url and new_url != url:
                print(f"[INFO] Regenerating poster for '{name}'")
                return get_cached_poster(new_url, fallback_info=fallback_info)

    # Final fallback to original URL
    return url

@app.route('/temp/<path:filename>')
def poster_file(filename):
    return send_from_directory(TEMP_FOLDER, filename)

@app.context_processor
def inject_helpers():
    def get_poster_safe(item):
        return get_cached_poster(item['poster_url'], fallback_info=item)
    return {'get_poster': get_poster_safe}

def load_data():
    if not os.path.exists(JSON_FILE):
        return {"series": [], "movies": []}
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

@app.route('/')
def index():
    active_tab = request.args.get('tab', 'series')
    query = request.args.get('q', '').lower()
    data = load_data()
    if active_tab == 'series':
        items = data.get('series', [])
    else:
        items = data.get('movies', [])
    if query:
        query = query.lower()
        filtered_items = [item for item in items if query in item['name'].lower()]
    else:
        filtered_items = items
    return render_template('index.html', 
                          items=filtered_items,
                          active_tab=active_tab,
                          query=query,
                          show_local_videos=True)

@app.route('/add', methods=['GET', 'POST'])
def add_entry():
    if request.method == 'POST':
        data = load_data()
        category = request.form['category']
        tab = request.form.get('tab', 'series')
        query = request.form.get('q', '')

        name = request.form['name']
        year = request.form['year']
        country = request.form['country']
        media_type = request.form['type']
        ep = request.form.get('ep', '') if category == 'series' else ''
        condition = request.form.get('condition', '') if category == 'series' else ''

        query_str = f"{name}"
        poster_url = request.form.get('poster_url') or get_movie_poster(query_str, media_type, year, region=country)

        new_entry = {
            "name": name,
            "year": year,
            "country": country,
            "type": media_type,
            "poster_url": poster_url
        }

        if category == 'series':
            new_entry["ep"] = ep
            new_entry["condition"] = condition

        data[category].append(new_entry)
        save_data(data)
        return redirect(url_for('index', tab=tab, q=query))

    tab = request.args.get('tab', 'series')
    query = request.args.get('q', '')
    return render_template('add_edit.html', action='Add', tab=tab, q=query, item={})

@app.route('/edit/<category>/<int:index>', methods=['GET', 'POST'])
def edit_entry(category, index):
    data = load_data()
    items = data.get(category, [])

    if index >= len(items):
        return redirect(url_for('index'))

    item = items[index]

    if request.method == 'POST':
        tab = request.form.get('tab', 'series')
        query = request.form.get('q', '')

        item['name'] = request.form['name']
        item['year'] = request.form['year']
        item['country'] = request.form['country']
        item['type'] = request.form['type']
        item['poster_url'] = request.form.get('poster_url', '')

        if category == 'series':
            item['ep'] = request.form.get('ep', '')
            item['condition'] = request.form.get('condition', '')

        if 'regenerate_poster' in request.form:
            query_str = f"{item['name']}"
            item['poster_url'] = get_movie_poster(query_str, item['type'], item['year'], region=item['country']) or item['poster_url']

        save_data(data)
        return redirect(url_for('index', tab=tab, q=query))

    tab = request.args.get('tab', 'series')
    query = request.args.get('q', '')
    return render_template('add_edit.html', action='Edit', item=item, tab=tab, q=query)

@app.route('/delete/<category>/<int:index>')
def delete_entry(category, index):
    data = load_data()
    items = data.get(category, [])

    if index < len(items):
        del items[index]
        save_data(data)

    tab = request.args.get('tab', 'series')
    query = request.args.get('q', '')
    return redirect(url_for('index', tab=tab, q=query))

# Modify get_trailer function similarly
@app.route('/trailer')
def get_trailer():
    settings = app_settings
    name = request.args.get('name')
    media_type = request.args.get('type')
    year = request.args.get('year')
    country = request.args.get('country')

    if settings.api_provider == "custom" and settings.trailer_api_url:
        # Custom trailer API implementation
        # Example: response = requests.get(settings.trailer_api_url, params={...})
        # return {'trailer_url': response.json().get('trailer_url')}
        return {'trailer_url': None}
    else:
        # Original TMDB implementation
        API_KEY = settings.api_key
        search_type = media_type.lower().split()[0]
        search_url = f'https://api.themoviedb.org/3/search/{search_type}'
        video_url_template = 'https://api.themoviedb.org/3/{type}/{id}/videos'

        search_params = {
            'api_key': API_KEY,
            'query': name,
            'include_adult': False
        }
        if year:
            if search_type == 'movie':
                search_params['year'] = year
            elif search_type == 'tv':
                search_params['first_air_date_year'] = year
        if country:
            search_params['region'] = country.upper()

        try:
            search_res = requests.get(search_url, params=search_params).json()
            results = search_res.get('results', [])
            if not results:
                print(f"[INFO] No results found for: {name}")
                # Try without region/year if initial search fails
                new_params = {k: v for k, v in search_params.items() if k not in ['region', 'year', 'first_air_date_year']}
                search_res = requests.get(search_url, params=new_params).json()
                results = search_res.get('results', [])
                if not results:
                    return {'trailer_url': None}

            # Improved exact matching
            title_key = 'name' if search_type == 'tv' else 'title'
            clean_name = re.sub(r'[^\w\s]', '', name.lower())

            exact_match = None
            for item in results:
                item_title = re.sub(r'[^\w\s]', '', item.get(title_key, '').lower())
                if item_title == clean_name:
                    exact_match = item
                    break

            # Fallback to partial match if no exact match
            item_id = None
            if exact_match:
                item_id = exact_match['id']
            else:
                for item in results:
                    item_title = item.get(title_key, '').lower()
                    if name.lower() in item_title:
                        item_id = item['id']
                        break

            if not item_id:
                item_id = results[0]['id'] if results else None

            if not item_id:
                return {'trailer_url': None}

            video_url = video_url_template.format(type=search_type, id=item_id)
            video_res = requests.get(video_url, params={'api_key': API_KEY}).json()
            videos = video_res.get('results', [])

            for vid in videos:
                if vid['type'] == 'Trailer' and vid['site'] == 'YouTube':
                    return {'trailer_url': f"https://www.youtube.com/embed/{vid['key']}"}

        except Exception as e:
            print(f"[ERROR] Fetching trailer failed: {e}")

        return {'trailer_url': None}

# Add this route
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    global app_settings
    
    if request.method == 'POST':
        app_settings.api_provider = request.form['api_provider']
        app_settings.api_key = request.form['api_key']
        if app_settings.api_provider == 'custom':
            app_settings.poster_api_url = request.form['poster_api_url']
            app_settings.trailer_api_url = request.form['trailer_api_url']
        app_settings.local_media_path = request.form['local_media_path']  # Add this line
        app_settings.save()
        return redirect(url_for('index'))
    
    return render_template('settings.html', settings=app_settings)

# Add new endpoint for local media
@app.route('/local_media')
def local_media():
    name = request.args.get('name')
    media_type = request.args.get('type')
    base_path = app_settings.local_media_path

    if not base_path or not os.path.exists(base_path):
        return jsonify({"error": "Local media path not set or does not exist"})

    results = []
    normalized_name = re.sub(r'[^a-z0-9]', '', name.lower())

    try:
        base_path = os.path.normpath(base_path)
        
        if media_type == 'movie':
            # Movie search remains unchanged
            for root, _, files in os.walk(base_path):
                for file in files:
                    if file.lower().endswith(('.mp4', '.mkv', '.avi', '.mov')):
                        file_path = os.path.join(root, file)
                        file_name = os.path.splitext(file)[0]
                        normalized_file = re.sub(r'[^a-z0-9]', '', file_name.lower())
                        if normalized_name in normalized_file:
                            results.append({
                                "name": file,
                                "path": file_path
                            })
                            
        elif media_type == 'series':
            # NEW: Search all video files recursively
            for root, _, files in os.walk(base_path):
                for file in files:
                    if file.lower().endswith(('.mp4', '.mkv', '.avi', '.mov')):
                        file_path = os.path.join(root, file)
                        file_name = os.path.splitext(file)[0]
                        normalized_file = re.sub(r'[^a-z0-9]', '', file_name.lower())
                        
                        # Check if series name appears in filename
                        if normalized_name in normalized_file:
                            # Extract episode number directly from filename
                            ep_match = re.search(r'(\d{3,4}(?:\.\d+)?)', file)
                            ep_num = ep_match.group(1) if ep_match else "Unknown"

                            results.append({
                                "name": file,
                                "episode": ep_num,
                                "path": file_path
                            })
    except Exception as e:
        print(f"Error scanning media: {e}")
        return jsonify({"error": "Error scanning media files"})

    # Sort episodes by episode number if series
    if media_type == 'series':
        def extract_ep_num(item):
            try:
                return float(item.get("episode", "0"))
            except Exception:
                return 0
        results.sort(key=extract_ep_num)

    return jsonify({"results": results})

# Add endpoint to serve local media
@app.route('/play_local')
def play_local():
    file_path = request.args.get('path')
    if not file_path:
        return "File path not provided", 400

    file_path = urllib.parse.unquote(file_path)
    file_path = os.path.normpath(file_path)
    base_path = os.path.abspath(app_settings.local_media_path)
    full_path = os.path.abspath(file_path)

    # Security checks (same as before)
    if not os.path.exists(full_path):
        dir_path, filename = os.path.split(full_path)
        if os.path.exists(dir_path):
            for f in os.listdir(dir_path):
                if f.lower() == filename.lower():
                    full_path = os.path.join(dir_path, f)
                    break
    if not os.path.exists(full_path):
        return f"File not found: {full_path}", 404
    if not full_path.startswith(base_path):
        return f"Forbidden: File not in media directory {base_path}", 403

    # Pass the filename as title
    return render_template('video_player.html', title=os.path.basename(full_path), path=file_path)

# Serve the video file itself (for <video src="...">)
@app.route('/video_file')
def serve_video_file():
    path = request.args.get('path')
    if not path:
        return "File path not provided", 400
    path = os.path.normpath(urllib.parse.unquote(path))
    base_path = os.path.abspath(app_settings.local_media_path)
    full_path = os.path.abspath(path)
    if not full_path.startswith(base_path):
        return "Forbidden", 403
    if not os.path.exists(full_path):
        return "File not found", 404
    return send_file(full_path)

@app.route('/local_videos')
def local_videos():
    base_path = app_settings.local_media_path
    if not base_path or not os.path.exists(base_path):
        return render_template('local_videos.html', error="Local media path not set or does not exist")

    media_items = {'movies': [], 'series': defaultdict(list)}
    
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.lower().endswith(('.mp4', '.mkv', '.avi', '.mov')):
                file_path = os.path.join(root, file)
                file_info = extract_media_info(file)
                
                if file_info['type'] == 'movie':
                    existing = next((m for m in media_items['movies'] if m['name'] == file_info['name']), None)
                    if existing:
                        existing['files'].append(file_path)
                    else:
                        media_items['movies'].append({
                            'name': file_info['name'],
                            'year': file_info.get('year'),
                            'files': [file_path],
                            'poster_url': get_movie_poster(file_info['name'], 'movie', file_info.get('year'))
                        })
                else:
                    media_items['series'][file_info['name']].append({
                        'file_path': file_path,
                        'season': file_info.get('season'),
                        'episode': file_info.get('episode'),
                        'episode_str': file_info.get('episode_str')
                    })
    # Prepare series for template
    series_list = []
    for name, episodes in media_items['series'].items():
        poster_url = get_movie_poster(name, 'tv')
        series_list.append({
            'name': name,
            'poster_url': poster_url,
            'episodes': episodes
        })
    
    return render_template('local_videos.html', 
                           movies=media_items['movies'], 
                           series=series_list)

if __name__ == '__main__':
    port = 8080
    app.run(host='0.0.0.0', port=port, debug=True)

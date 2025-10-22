import json
import os
import hashlib
import requests
import re
import urllib.parse
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify, send_file
from PIL import Image
from io import BytesIO
import base64
from collections import defaultdict
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SETTINGS_FILE = "settings.json"
WATCH_HISTORY_FILE = "watch_history.json"

class Settings:
    def __init__(self):
        self.api_provider = "tmdb"
        self.api_key = ""
        self.poster_api_url = ""
        self.trailer_api_url = ""
        self.local_media_path = ""
        self.theme = "dark"
        self.poster_quality = "w500"
        self.enable_auto_backup = False
        self.check_duplicates = True
        
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                data = json.load(f)
                for key, value in data.items():
                    if key == "local_media_path" and value:
                        value = os.path.normpath(value)
                    setattr(self, key, value)

    def save(self):
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(self.__dict__, f, indent=4)

class WatchHistory:
    def __init__(self):
        self.history = []
        if os.path.exists(WATCH_HISTORY_FILE):
            with open(WATCH_HISTORY_FILE, 'r') as f:
                self.history = json.load(f)
    
    def add_entry(self, name, media_type, episode=None):
        entry = {
            "name": name,
            "type": media_type,
            "episode": episode,
            "timestamp": datetime.now().isoformat()
        }
        self.history.insert(0, entry)
        self.history = self.history[:50]  # Keep last 50 entries
        self.save()
    
    def save(self):
        with open(WATCH_HISTORY_FILE, 'w') as f:
            json.dump(self.history, f, indent=4)

app_settings = Settings()
watch_history = WatchHistory()

app = Flask(__name__)
JSON_FILE = "my_list.json"
TEMP_FOLDER = "temp"
BACKUP_FOLDER = "backups"

os.makedirs(TEMP_FOLDER, exist_ok=True)
os.makedirs(BACKUP_FOLDER, exist_ok=True)

def extract_media_info(filename):
    name = os.path.splitext(filename)[0]
    name = re.sub(r'[_\-.]+', ' ', name)
    name = name.lower()

    info = {'name': name.strip(), 'type': 'movie'}

    # First extract year
    year_match = re.search(r'\b(19\d{2}|20\d{2}|202\d)\b', name)
    if year_match:
        info['year'] = year_match.group(1)
        name = name.replace(info['year'], '')

    # Try S01E02 or 1x02 patterns first
    ep_match = re.search(r'\bs(\d{1,2})e(\d{1,2})\b', name) or re.search(r'\b(\d{1,2})x(\d{1,2})\b', name)
    if ep_match:
        info['type'] = 'series'
        info['season'] = int(ep_match.group(1))
        info['episode'] = int(ep_match.group(2))
        info['episode_str'] = f"S{info['season']:02d}E{info['episode']:02d}"
        name = name.replace(ep_match.group(0), '')
    else:
        # Look for standalone episode numbers (like 1004)
        standalone_ep_match = re.search(r'\b(\d{3,4})\b', name)
        if standalone_ep_match:
            episode_num = standalone_ep_match.group(1)
            # Make sure it's not a year
            if not (1900 <= int(episode_num) <= 2030):
                info['type'] = 'series'
                info['episode'] = int(episode_num)
                info['episode_str'] = f"Episode {episode_num}"
                name = name.replace(episode_num, '')

    # Remove junk tags
    junk_tags = [
        r'\b(web[-_. ]?dl|nf|hdtv|mycima|wecima|show|tube|autos|ink|world|ar|weciima|mp4|ova|web)\b',
        r'\b(1080p|720p|4k|bluray|webrip|hdrip)\b',
        r'\bsp\b',
        r'\b(HDTV|WEBRip|BluRay|WEB-DL|HDRip|BRRip|DVDRip|HDCAM|DVD|BDRip|4K|Abyss|HDTS|TVRip|HC|FHDRip|DVDSCR|CAM|PreDVD|TS)\b'
    ]

    for pattern in junk_tags:
        name = re.sub(pattern, '', name, flags=re.IGNORECASE)

    # Clean up extra spaces
    name = re.sub(r'\s+', ' ', name).strip()
    info['name'] = name.title()

    return info

def get_movie_poster(movie_name, typeis, year=None, region=None):
    settings = app_settings

    if settings.api_provider == "omdb":
        base_url = 'http://www.omdbapi.com/'
        params = {
            'apikey': settings.api_key,
            't': movie_name,
            'type': 'movie' if typeis.lower() == 'movie' else 'series',
            'y': year
        }
        try:
            response = requests.get(base_url, params=params, timeout=5)
            data = response.json()
            return data.get('Poster') if 'Poster' in data else None
        except Exception as e:
            logger.error(f"OMDB API error: {e}")
            return None

    elif settings.api_provider == "custom" and settings.poster_api_url:
        return None

    else:  # TMDB
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

        try:
            response = requests.get(base_url, params=params, timeout=5)
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
                            return f'https://image.tmdb.org/t/p/{settings.poster_quality}{poster_path}'
                poster_path = results[0].get('poster_path')
                if poster_path:
                    return f'https://image.tmdb.org/t/p/{settings.poster_quality}{poster_path}'
            logger.warning(f"Poster not found for: {movie_name}")
        except Exception as e:
            logger.error(f"TMDB API error: {e}")
        return None

def get_cached_poster(url, fallback_info=None):
    if not url:
        return url_for('static', filename='images/no-poster.png')
    
    os.makedirs(TEMP_FOLDER, exist_ok=True)
    filename = hashlib.md5(url.encode()).hexdigest() + ".jpg"
    filepath = os.path.join(TEMP_FOLDER, filename)

    if os.path.exists(filepath):
        return url_for('poster_file', filename=filename)

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        img = Image.open(BytesIO(response.content))
        img.thumbnail((300, 450))
        img.save(filepath, format="JPEG", quality=85)
        return url_for('poster_file', filename=filename)

    except Exception as e:
        logger.error(f"Failed to fetch/save poster: {e}")

        if fallback_info:
            name = fallback_info.get('name')
            media_type = fallback_info.get('type')
            year = fallback_info.get('year')
            country = fallback_info.get('country')

            new_url = get_movie_poster(name, media_type, year=year, region=country)
            if new_url and new_url != url:
                logger.info(f"Regenerating poster for '{name}'")
                return get_cached_poster(new_url, fallback_info=fallback_info)

    return url_for('static', filename='images/no-poster.png')

@app.route('/temp/<path:filename>')
def poster_file(filename):
    return send_from_directory(TEMP_FOLDER, filename)

@app.context_processor
def inject_helpers():
    def get_poster_safe(item):
        return get_cached_poster(item.get('poster_url'), fallback_info=item)
    return {'get_poster': get_poster_safe, 'settings': app_settings}

def load_data():
    if not os.path.exists(JSON_FILE):
        return {"series": [], "movies": []}
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    if app_settings.enable_auto_backup:
        backup_file = os.path.join(BACKUP_FOLDER, f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

@app.route('/')
def index():
    active_tab = request.args.get('tab', 'series')
    query = request.args.get('q', '').lower()
    sort_by = request.args.get('sort', 'name')
    
    data = load_data()
    all_items = data.get('series' if active_tab == 'series' else 'movies', [])
    
    # Add original index to each item for proper edit/delete links
    items_with_index = []
    for idx, item in enumerate(all_items):
        item_copy = item.copy()
        item_copy['original_index'] = idx
        items_with_index.append(item_copy)
    
    # Filter items
    if query:
        filtered_items = [item for item in items_with_index if query in item['name'].lower()]
    else:
        filtered_items = items_with_index
    
    # Sort items
    if sort_by == 'name':
        filtered_items.sort(key=lambda x: x['name'].lower())
    elif sort_by == 'year':
        filtered_items.sort(key=lambda x: x.get('year', '0'), reverse=True)
    elif sort_by == 'date_added':
        filtered_items.reverse()
    
    return render_template('index.html', 
                          items=filtered_items,
                          active_tab=active_tab,
                          query=query,
                          sort_by=sort_by,
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
        rating = request.form.get('rating', '')
        notes = request.form.get('notes', '')

        query_str = f"{name}"
        poster_url = request.form.get('poster_url') or get_movie_poster(query_str, media_type, year, region=country)

        new_entry = {
            "name": name,
            "year": year,
            "country": country,
            "type": media_type,
            "poster_url": poster_url,
            "rating": rating,
            "notes": notes,
            "date_added": datetime.now().isoformat()
        }

        if category == 'series':
            new_entry["ep"] = ep
            new_entry["condition"] = condition

        if app_settings.check_duplicates:
            duplicates = [i for i in data[category] if i['name'].strip().lower() == name.strip().lower()]
            if duplicates:
                return f"Duplicate {category[:-1]} '{name}' already exists!", 400

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
        item['rating'] = request.form.get('rating', '')
        item['notes'] = request.form.get('notes', '')

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

@app.route('/trailer')
def get_trailer():
    settings = app_settings
    name = request.args.get('name')
    media_type = request.args.get('type')
    year = request.args.get('year')
    country = request.args.get('country')

    if settings.api_provider == "custom" and settings.trailer_api_url:
        return {'trailer_url': None}
    else:
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
            search_res = requests.get(search_url, params=search_params, timeout=5).json()
            results = search_res.get('results', [])
            if not results:
                new_params = {k: v for k, v in search_params.items() if k not in ['region', 'year', 'first_air_date_year']}
                search_res = requests.get(search_url, params=new_params, timeout=5).json()
                results = search_res.get('results', [])
                if not results:
                    return {'trailer_url': None}

            title_key = 'name' if search_type == 'tv' else 'title'
            clean_name = re.sub(r'[^\w\s]', '', name.lower())

            exact_match = None
            for item in results:
                item_title = re.sub(r'[^\w\s]', '', item.get(title_key, '').lower())
                if item_title == clean_name:
                    exact_match = item
                    break

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
            video_res = requests.get(video_url, params={'api_key': API_KEY}, timeout=5).json()
            videos = video_res.get('results', [])

            for vid in videos:
                if vid['type'] == 'Trailer' and vid['site'] == 'YouTube':
                    return {'trailer_url': f"https://www.youtube.com/embed/{vid['key']}"}

        except Exception as e:
            logger.error(f"Fetching trailer failed: {e}")

        return {'trailer_url': None}

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    global app_settings
    
    if request.method == 'POST':
        app_settings.api_provider = request.form['api_provider']
        app_settings.api_key = request.form['api_key']
        if app_settings.api_provider == 'custom':
            app_settings.poster_api_url = request.form['poster_api_url']
            app_settings.trailer_api_url = request.form['trailer_api_url']
        app_settings.local_media_path = request.form['local_media_path']
        app_settings.theme = request.form.get('theme', 'dark')
        app_settings.poster_quality = request.form.get('poster_quality', 'w500')
        app_settings.enable_auto_backup = 'enable_auto_backup' in request.form
        app_settings.check_duplicates = 'check_duplicates' in request.form
        app_settings.save()
        return redirect(url_for('index'))
    
    return render_template('settings.html', settings=app_settings)

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
            for root, _, files in os.walk(base_path):
                for file in files:
                    if file.lower().endswith(('.mp4', '.mkv', '.avi', '.mov')):
                        file_path = os.path.join(root, file)
                        file_name = os.path.splitext(file)[0]
                        normalized_file = re.sub(r'[^a-z0-9]', '', file_name.lower())
                        
                        if normalized_name in normalized_file:
                            ep_match = re.search(r'(\d{3,4}(?:\.\d+)?)', file)
                            ep_num = ep_match.group(1) if ep_match else "Unknown"

                            results.append({
                                "name": file,
                                "episode": ep_num,
                                "path": file_path
                            })
    except Exception as e:
        logger.error(f"Error scanning media: {e}")
        return jsonify({"error": "Error scanning media files"})

    if media_type == 'series':
        def extract_ep_num(item):
            try:
                return float(item.get("episode", "0"))
            except Exception:
                return 0
        results.sort(key=extract_ep_num)

    return jsonify({"results": results})

@app.route('/play_local')
def play_local():
    file_path = request.args.get('path')
    if not file_path:
        return "File path not provided", 400

    file_path = urllib.parse.unquote(file_path)
    file_path = os.path.normpath(file_path)
    base_path = os.path.abspath(app_settings.local_media_path)
    full_path = os.path.abspath(file_path)

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
        return f"Forbidden: File not in media directory", 403

    # Add to watch history
    file_info = extract_media_info(os.path.basename(full_path))
    watch_history.add_entry(
        file_info['name'], 
        file_info['type'],
        file_info.get('episode_str')
    )

    return render_template('video_player.html', title=os.path.basename(full_path), path=file_path)

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

@app.route('/watch_history')
def get_watch_history():
    return jsonify(watch_history.history)

@app.route('/statistics')
def statistics():
    data = load_data()
    stats = {
        'total_series': len(data.get('series', [])),
        'total_movies': len(data.get('movies', [])),
        'series_by_condition': {},
        'items_by_year': {},
        'items_by_country': {}
    }
    
    for series in data.get('series', []):
        condition = series.get('condition', 'Unknown')
        stats['series_by_condition'][condition] = stats['series_by_condition'].get(condition, 0) + 1
    
    for item in data.get('series', []) + data.get('movies', []):
        year = item.get('year', 'Unknown')
        country = item.get('country', 'Unknown')
        stats['items_by_year'][year] = stats['items_by_year'].get(year, 0) + 1
        stats['items_by_country'][country] = stats['items_by_country'].get(country, 0) + 1
    
    return jsonify(stats)

@app.route('/scan_empty_posters')
def scan_empty_posters():
    """Scan for items with empty poster URLs"""
    try:
        data = load_data()
        empty_items = {
            'series': [],
            'movies': []
        }
        
        # Scan series with empty poster URLs
        for item in data.get('series', []):
            if not item.get('poster_url'):
                empty_items['series'].append(item)
        
        # Scan movies with empty poster URLs
        for item in data.get('movies', []):
            if not item.get('poster_url'):
                empty_items['movies'].append(item)
        
        return jsonify(empty_items)
    
    except Exception as e:
        logger.error(f"Error scanning empty posters: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/regenerate_empty_posters', methods=['POST'])
def regenerate_empty_posters():
    """Regenerate posters for all items with empty poster URLs"""
    try:
        data = load_data()
        regenerated = 0
        failed = 0
        
        # Regenerate series posters
        for item in data.get('series', []):
            if not item.get('poster_url'):
                try:
                    query_str = f"{item['name']}"
                    new_poster = get_movie_poster(
                        query_str, 
                        item.get('type', 'tv'), 
                        item.get('year'), 
                        region=item.get('country')
                    )
                    if new_poster:
                        item['poster_url'] = new_poster
                        regenerated += 1
                    else:
                        failed += 1
                except Exception as e:
                    logger.error(f"Failed to regenerate poster for series {item['name']}: {e}")
                    failed += 1
        
        # Regenerate movie posters
        for item in data.get('movies', []):
            if not item.get('poster_url'):
                try:
                    query_str = f"{item['name']}"
                    new_poster = get_movie_poster(
                        query_str, 
                        item.get('type', 'movie'), 
                        item.get('year'), 
                        region=item.get('country')
                    )
                    if new_poster:
                        item['poster_url'] = new_poster
                        regenerated += 1
                    else:
                        failed += 1
                except Exception as e:
                    logger.error(f"Failed to regenerate poster for movie {item['name']}: {e}")
                    failed += 1
        
        # Save the updated data
        save_data(data)
        
        return jsonify({
            'regenerated': regenerated,
            'failed': failed,
            'message': f'Successfully regenerated {regenerated} posters. {failed} failed.'
        })
    
    except Exception as e:
        logger.error(f"Error regenerating empty posters: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/scan_duplicates')
def scan_duplicates():
    """Scan for duplicate movie and series names (same name + same year + same country)"""
    try:
        data = load_data()
        duplicates = {
            'series': [],
            'movies': []
        }

        # Helper function to find duplicates by name + year + country
        def find_duplicates(items):
            seen = {}
            dups = []
            for item in items:
                name = item.get('name', '').strip().lower()
                year = str(item.get('year', '')).strip().lower()
                country = str(item.get('country', '')).strip().lower()
                if not name:
                    continue

                key = f"{name}|{year}|{country}"
                if key in seen:
                    # Only add the first occurrence once
                    if seen[key] is not None:
                        dups.append(seen[key])
                        seen[key] = None
                    dups.append(item)
                else:
                    seen[key] = item
            return dups

        duplicates['series'] = find_duplicates(data.get('series', []))
        duplicates['movies'] = find_duplicates(data.get('movies', []))

        return jsonify(duplicates)

    except Exception as e:
        logger.error(f"Error scanning duplicates: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/export_backup')
def export_backup():
    """Export a complete backup of the collection"""
    try:
        data = load_data()
        
        # Add metadata
        backup_data = {
            "metadata": {
                "export_date": datetime.now().isoformat(),
                "version": "1.0",
                "total_movies": len(data.get('movies', [])),
                "total_series": len(data.get('series', []))
            },
            "collection": data
        }
        
        # Create JSON response
        response = jsonify(backup_data)
        response.headers['Content-Disposition'] = f'attachment; filename=myflixvault_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        response.headers['Content-Type'] = 'application/json'
        
        return response
        
    except Exception as e:
        logger.error(f"Error exporting backup: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/import_backup', methods=['POST'])
def import_backup():
    """Import a backup file"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if file and file.filename.endswith('.json'):
            data = json.load(file)
            
            # Validate backup structure
            if 'collection' not in data:
                return jsonify({"error": "Invalid backup file format"}), 400
            
            # Save the imported data
            save_data(data['collection'])
            
            return jsonify({
                "message": f"Successfully imported {len(data['collection'].get('movies', []))} movies and {len(data['collection'].get('series', []))} series"
            })
        
        return jsonify({"error": "Invalid file type. Please upload a JSON file"}), 400
        
    except Exception as e:
        logger.error(f"Error importing backup: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = 8080
    app.run(host='0.0.0.0', port=port, debug=True)
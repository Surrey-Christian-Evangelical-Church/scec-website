import json
import csv
import urllib.parse

# Load custom server files and wp media
with open('/home/harry/.gemini/antigravity/brain/a24fb83d-db4b-4084-9c15-f6201d4cf2c0/scratch/custom_server_files.json') as f:
    custom_files = json.load(f)

with open('/home/harry/.gemini/antigravity/brain/a24fb83d-db4b-4084-9c15-f6201d4cf2c0/scratch/wp_media_manifest.json') as f:
    wp_media = json.load(f)

rows = []

# Process custom server files (mostly videos and documents)
for item in custom_files:
    url = item if item.startswith('http') else f"https://scecchinese.com{item}"
    decoded_name = urllib.parse.unquote(url.split('/')[-1])
    ext = decoded_name.split('.')[-1].lower() if '.' in decoded_name else 'unknown'
    
    # Categorize suggested Google Drive folder
    if '/worship-songs/' in url:
        category = "Google Drive: 诗歌敬拜视频 (Worship Songs)"
    elif '/mp4/' in url or '/christmas/' in url or '/party/' in url:
        category = "Google Drive: 活动与聚会视频 (Event Videos)"
    elif '/books/' in url or ext == 'pdf':
        category = "Google Drive: 属灵书籍与教材 (Documents & Books)"
    else:
        category = "Google Drive: 网站图片素材 (Site Media)"

    rows.append({
        'Source_Location': 'Server Directory (FTP/Webroot)',
        'File_Name': decoded_name,
        'File_Type': ext.upper(),
        'Suggested_Google_Drive_Folder': category,
        'Original_URL': url
    })

# Process WP Media uploads
for m in wp_media['items']:
    url = m['url']
    decoded_name = urllib.parse.unquote(url.split('/')[-1])
    ext = decoded_name.split('.')[-1].lower() if '.' in decoded_name else 'unknown'
    rows.append({
        'Source_Location': 'WordPress Media Library',
        'File_Name': decoded_name,
        'File_Type': ext.upper(),
        'Suggested_Google_Drive_Folder': 'Google Drive / Google Photos: 活动相册与图库 (Photo Albums)',
        'Original_URL': url
    })

csv_path = '/home/harry/git/scec-site/media_migration_manifest.csv'
with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f, fieldnames=['Source_Location', 'File_Name', 'File_Type', 'Suggested_Google_Drive_Folder', 'Original_URL'])
    writer.writeheader()
    writer.writerows(rows)

print(f"Generated {csv_path} with {len(rows)} entries!")

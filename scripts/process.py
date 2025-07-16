import requests
import csv
from collections import defaultdict

# Source of MIME type definitions
MIME_TYPES_URL = 'https://raw.githubusercontent.com/apache/httpd/refs/heads/trunk/docs/conf/mime.types'

# Dictionary mapping extension to MIME type(s)
extension_to_mime = defaultdict(list)

def fetch_mime_types():
    print("Fetching MIME types from Apache HTTPD repository...")
    response = requests.get(MIME_TYPES_URL)
    if response.status_code != 200:
        raise Exception("Failed to fetch MIME types data.")
    return response.text

def parse_mime_types(data):
    print("Parsing MIME types...")
    for line in data.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        parts = line.split()
        if len(parts) < 2:
            continue

        mime_type = parts[0]
        extensions = parts[1:]

        for ext in extensions:
            ext = ext.strip()
            if mime_type not in extension_to_mime[ext]:
                extension_to_mime[ext].append(mime_type)

def save_to_csv(output_file='data/extension-to-mimetype.csv'):
    print("Writing results to CSV...")
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Extension', 'MIME Types'])  # Header
        for ext in sorted(extension_to_mime):
            mimes = '; '.join(extension_to_mime[ext])
            writer.writerow([ext, mimes])
    print(f"CSV saved as {output_file}")

if __name__ == '__main__':
    mime_text = fetch_mime_types()
    parse_mime_types(mime_text)
    save_to_csv()

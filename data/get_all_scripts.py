import os
import requests
import zipfile
from bs4 import BeautifulSoup
from io import BytesIO
import tempfile

# Create base images directory
base_image_dir = "images"
os.makedirs(base_image_dir, exist_ok=True)

# Base URL with script parameter placeholder
base_url = "https://ociana.osu.edu/inscriptions?per_page=1500&search%5Bscript%5D={}"

# Iterate over script values from 1 to 35
for script_id in range(1, 36):
    url = base_url.format(script_id)
    print(f"Fetching script ID {script_id}...")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all <a> tags within <div class="card-footer">
    card_footers = soup.find_all('div', class_='card-footer')
    for footer in card_footers:
        links = footer.find_all('a')
        for link in links:
            href = link.get('href')
            if href:
                full_url = f"https://ociana.osu.edu{href}"
                detail_response = requests.get(full_url)
                detail_soup = BeautifulSoup(detail_response.text, 'html.parser')

                # Extract the "Language and Script" value
                script_name = "unknown_script"
                for dt in detail_soup.find_all('dt'):
                    dt_text = dt.get_text(strip=True)
                    if dt_text == "Language and Script":
                        dd = dt.find_next_sibling('dd')
                        if dd:
                            for div in dd.find_all('div', class_='fst-italic small'):
                                div.decompose()
                            script_name = dd.get_text(strip=True).lower().replace(" ", "_")

                # Create script-specific directory
                script_dir = os.path.join(base_image_dir, script_name)
                os.makedirs(script_dir, exist_ok=True)

                # Find the "Download Images" link
                # Find the "Download Image(s)" link (handle both singular and plural)
                download_link = None
                for a_tag in detail_soup.find_all('a'):
                    if a_tag.string and a_tag.string.strip().lower() in ["download image", "download images"]:
                        download_link = a_tag
                        break
                if download_link and download_link.get('href'):
                    zip_url = f"https://ociana.osu.edu{download_link.get('href')}"
                    print(f"Downloading images from: {zip_url}")
                    zip_response = requests.get(zip_url)
                    if zip_response.status_code == 200:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp_zip:
                            tmp_zip.write(zip_response.content)
                            tmp_zip_path = tmp_zip.name

                        with zipfile.ZipFile(tmp_zip_path, 'r') as z:
                            for file_info in z.infolist():
                                if not file_info.filename.lower().endswith('.csv') and not file_info.is_dir():
                                    file_name = os.path.basename(file_info.filename)
                                    target_path = os.path.join(script_dir, file_name)
                                    with z.open(file_info) as source, open(target_path, 'wb') as target:
                                        target.write(source.read())

                        os.remove(tmp_zip_path)

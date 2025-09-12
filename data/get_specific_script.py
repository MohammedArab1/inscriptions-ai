import requests
from bs4 import BeautifulSoup
import csv
import os

# List of URLs to scrape (update this list manually)
urls = [
    "https://ociana.osu.edu/inscriptions/16797",
    "https://ociana.osu.edu/inscriptions/16799",
    "https://ociana.osu.edu/inscriptions/16800",
    "https://ociana.osu.edu/inscriptions/16801",
    "https://ociana.osu.edu/inscriptions/16802",
    "https://ociana.osu.edu/inscriptions/16803",
    "https://ociana.osu.edu/inscriptions/16804",
    "https://ociana.osu.edu/inscriptions/16805",
    "https://ociana.osu.edu/inscriptions/16806",
    "https://ociana.osu.edu/inscriptions/16807",
    "https://ociana.osu.edu/inscriptions/16808",
    "https://ociana.osu.edu/inscriptions/16809",
    "https://ociana.osu.edu/inscriptions/16810",
    "https://ociana.osu.edu/inscriptions/16811",
    "https://ociana.osu.edu/inscriptions/16812",
    "https://ociana.osu.edu/inscriptions/16813",
    "https://ociana.osu.edu/inscriptions/16815",
    "https://ociana.osu.edu/inscriptions/16817",
    "https://ociana.osu.edu/inscriptions/16818",
    "https://ociana.osu.edu/inscriptions/16819",
    "https://ociana.osu.edu/inscriptions/16820",
    "https://ociana.osu.edu/inscriptions/16821",
    "https://ociana.osu.edu/inscriptions/16822",
    "https://ociana.osu.edu/inscriptions/16824",
    "https://ociana.osu.edu/inscriptions/16825",
    "https://ociana.osu.edu/inscriptions/16826",
    "https://ociana.osu.edu/inscriptions/16827",
    "https://ociana.osu.edu/inscriptions/16831",
    "https://ociana.osu.edu/inscriptions/16833",
    "https://ociana.osu.edu/inscriptions/16834",
    "https://ociana.osu.edu/inscriptions/16836",
    "https://ociana.osu.edu/inscriptions/16840",
    "https://ociana.osu.edu/inscriptions/16846",
    "https://ociana.osu.edu/inscriptions/16847",
    "https://ociana.osu.edu/inscriptions/16850",
    "https://ociana.osu.edu/inscriptions/16851",
    "https://ociana.osu.edu/inscriptions/16852",
    "https://ociana.osu.edu/inscriptions/16854",
    "https://ociana.osu.edu/inscriptions/16856",
    "https://ociana.osu.edu/inscriptions/16857",
    "https://ociana.osu.edu/inscriptions/16862",
    "https://ociana.osu.edu/inscriptions/16864",
    "https://ociana.osu.edu/inscriptions/16869",
    "https://ociana.osu.edu/inscriptions/16878"
]

# Output CSV file name
output_file = "scraped_data.csv"
image_folder = "./safaiticImages"

# Create images directory if it doesn't exist
os.makedirs(image_folder, exist_ok=True)

# Open CSV file for writing
with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Image Path", "Translation Text"])

    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            # Get the image src
            img_tag = soup.find('img', class_='card-img-top')
            image_src = img_tag['src'] if img_tag else ''
            image_name = image_src.split('/')[-1] if image_src else ''
            local_image_path = os.path.join(image_folder, image_name)

            # Download the image
            if image_src:
                img_response = requests.get("https://ociana.osu.edu"+image_src)
                img_response.raise_for_status()
                with open(local_image_path, 'wb') as img_file:
                    img_file.write(img_response.content)

            # Find the <dt> with text "Translation" and get the corresponding <dd>
            translation_text = ''
            for dt in soup.find_all('dt'):
                if dt.get_text(strip=True) == "Translation":
                    dd = dt.find_next_sibling('dd')
                    if dd:
                        # Remove the final <div class="fst-italic small"> if present
                        div_to_remove = dd.find('div', class_='fst-italic small')
                        if div_to_remove:
                            div_to_remove.decompose()
                        translation_text = dd.get_text(strip=True)
                    break

            # Write the data to CSV
            writer.writerow([local_image_path, translation_text])

        except Exception as e:
            print(f"Error processing {url}: {e}")

print(f"Scraping completed. Data saved to {output_file}. Images saved to {image_folder}.")

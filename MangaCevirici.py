import requests
import easyocr
import os

print("""
  __  __                      _______                  _       _             
 |  \/  |                    |__   __|                | |     | |            
 | \  / | __ _ _ __   __ _  __ _| |_ __ __ _ _ __  ___| | __ _| |_ ___  _ __ 
 | |\/| |/ _` | '_ \ / _` |/ _` | | '__/ _` | '_ \/ __| |/ _` | __/ _ \| '__|
 | |  | | (_| | | | | (_| | (_| | | | | (_| | | | \__ \ | (_| | || (_) | |   
 |_|  |_|\__,_|_| |_|\__, |\__,_|_|_|  \__,_|_| |_|___/_|\__,_|\__\___/|_|   
                      __/ |                                                  
                     |___/                                                   

            By BadiCo | ig: badico.py
--------------------------------------------------------------------------------
""")
print("For example: https://i.imgur.com/QNIuolw.png")
manga_chapter_id = input("Input a manga chapterId from MangaDex.org: ")
manga_pages = list()

response = requests.get(f"https://api.mangadex.org/at-home/server/{manga_chapter_id}")
response_json = response.json()

def process_image(image_path):
    manga_reader = easyocr.Reader(['en'])
    results = manga_reader.readtext(image_path)
    return results

def download_images(image_url, save_path):
    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
    else:
        raise Exception(f"Page cant be installed. HTTP result: {response.status_code}")

if (response_json["result"] == "error"):
    print("An error occured while trying to accessing chapter infos. Are you sure that you entered right chapterId? (r'u retarded)")
else:
    manga_text_and_dialogues = list()

    manga_pages.extend(response_json["chapter"]["data"])

    for i, page in enumerate(manga_pages, start=0):
        download_images(f"{response_json['baseUrl']}/data/{response_json['chapter']['hash']}/{response_json['chapter']['data'][i]}", f"temp_page{i}")
        print(f"temp_page{i} file downloaded to your computer. (Because EasyOCR needs downloaded images. You can research about it.)")

        ocr_result = process_image(f"temp_page{i}")
        ocr_result.reverse()

        print(f"Text and dialogues in page {i + 1} (in reverse): ")
        for (bbox, text, prob) in ocr_result:
            print(f"Text - {text} | Probablity: {prob}")

        if os.path.exists(f"temp_page{i}"):
            os.remove(f"temp_page{i}")
            print(f"temp_page{i} removed. (for your security of course!)")

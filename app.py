from flask import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from proxy import get_chromedriver
import os
import time
import requests



from telegraph import Telegraph

telegraph = Telegraph()
telegraph.create_account(short_name='anonymous')

def create_telegraph_post(text):

    response = telegraph.create_page(
            "Images", 
            html_content=text
        )

    link = response['url']

    return link



def get_postimage_link(file_path):
    
    driver = get_chromedriver(use_proxy=False, user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15')
        
    driver.get("https://postimages.org/")

    driver.find_element(By.CLASS_NAME, "dz-hidden-input").send_keys(file_path)
    # time.sleep(3)

    postimage_link = ''
    
    while postimage_link == '':
        try:
            postimage_link = driver.find_element(By.XPATH, r'/html/body/div[1]/div/div[3]/div/form/div[1]/div[2]/div/input').get_attribute("value")
        except:
            pass
    
    driver.close()
    driver.quit()

    print("[+] Postimage success")

    return postimage_link

def get_anopic_link(file_path):

    driver = get_chromedriver(use_proxy=True, user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15')

    driver.get("https://anopic.net/")
    
    driver.find_element(By.CLASS_NAME, "dz-hidden-input").send_keys(file_path)
    # time.sleep(5)
    driver.find_element(By.XPATH, r'/html/body/main/div/div/div').click()
    # time.sleep(3)

    anopic_link = ''

    while anopic_link == '':
        try:
            anopic_link = driver.find_element(By.XPATH, r'/html/body/div[2]/div/div/div[2]/p').text
        except:
            pass

    driver.close()
    driver.quit()

    print("[+] Anopic success")
    
    return anopic_link


def get_telegraph_link(file_path):

    with open(file_path, 'rb') as f:
        telegraph_src = requests.post('https://telegra.ph/upload',
            files={'file': ('file', f, 'image/jpg')}
        ).json()[0]['src']

        response = None

        while response == None:
            response = telegraph.create_page(
                "Anonymous image", 
                html_content=f'<img src="{telegraph_src}">'
            )

        telegraph_link = response['url']

        print("[+] Telegraph success")

        return telegraph_link



app = Flask(__name__, static_url_path = "", static_folder = "static")

app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':

        files = request.files.getlist("file")

        print("[+] File uploaded")

        photos_links = []
  
        for file in files:

            postimage_link = ''
            telegraph_link = ''
            anopic_link = ''

            file.save('static/temp_files/' + file.filename)

            file_path = os.getcwd()+f"/static/temp_files/{file.filename}"

            postimage_link = get_postimage_link(file_path)

            anopic_link = get_anopic_link(file_path)

            telegraph_link = get_telegraph_link(file_path)
            
            photos_links.append([file.filename, postimage_link, telegraph_link, anopic_link])
        
        
        photos_telegraph_posts = []
        telegraph_links = []

        for photo in photos_links:

            photo_text = f'<a href="{photo[1]}">{photo[1]}</a><br><a href="{photo[2]}">{photo[2]}</a><br><a href="{photo[3]}">{photo[3]}</a><br><br>'

            photos_telegraph_posts.append([photo[3], create_telegraph_post(photo_text)])
            telegraph_links.append(create_telegraph_post(photo_text))

            # os.remove('static/temp_files/'+i[0])


        return render_template("upload.html", photos_links=photos_telegraph_posts, telegraph_links=telegraph_links)

# librerías
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from flask import Flask, request

app = Flask(__name__)


@app.route('/GetAmazonWishlist', methods=['GET'])
def get_wishlist():
    # obtenemos url desde la request
    url = request.args.get('wishlist_url')

    # seteamos user-agent falso
    ua = UserAgent()
    user_agent = ua.random

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument(f'user-agent={user_agent}')

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    # hacemos scroll down hasta el final para que se carguen todos los items
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    items_wishlist = driver.find_elements(By.CSS_SELECTOR, 'li[data-itemid]')

    items = []

    for item in items_wishlist:
        item_id = item.get_attribute('data-itemid')

        item_element_id = item.find_element(By.ID, 'itemName_' + item_id)

        item_url = item_element_id.get_attribute('href')
        item_name = item_element_id.get_attribute('title')
        item_image = item.find_element(By.TAG_NAME, 'img').get_attribute('src')

        item_obj = {
            'item_id': item_id,
            'name': item_name,
            'url': item_url,
            'image': item_image
        }  

        # print(item_obj)
        items.append(item_obj)

    # print(items)
    if items:
        return {'items': items,
                'num_items': len(items),
                'status': 200}
    else:
        return {'items': items,
                'num_items': len(items),
                'status': 400}   
    
if __name__ == '__main__':
    app.run() # Run the application
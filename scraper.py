
# scraper.py

import requests
import traceback
from flask_cors import CORS 
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from requests.exceptions import RequestException
import time
from retry import retry
from selenium import webdriver
# from selenium.webdriver.edge.webdriver import EdgeDriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)
CORS(app)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.48'
}

try:
    @retry(RequestException, tries=3, delay=2, backoff=2)
    @app.route('/amazon')
    def get_amazon_results():
        search_term = request.args.get('term') 
        url = f"https://www.amazon.in/s?k={search_term}"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            # Initialize results
            results = []

            # Extract data from search results
            for item in soup.select('div[data-asin][data-component-type="s-search-result"]'):
                
                brand_element = item.select_one('span.a-size-base-plus.a-color-base') 

                title_element = item.select_one('span.a-size-base-plus.a-color-base.a-text-normal')
                if title_element is None:
                    title_element = item.select_one('span.a-size-medium.a-color-base.a-text-normal')
                
                price_element = item.select_one('span.a-price > span.a-offscreen')
                url_element = item.select_one('a.a-link-normal.s-no-outline')['href']
                if url_element is None:
                    url_element = item.select_one('a.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal')['href']

                image_element = item.select_one('img.s-image')
                image_url = image_element['src'] if image_element else None
            

                if title_element and price_element and url_element:
                    title = title_element.text if hasattr(title_element, 'text') else ""
                    if brand_element:
                        brand = brand_element.text if hasattr(brand_element, 'text') else ""
                        title = f'{brand} - {title}'
                    price = price_element.text if hasattr(price_element, 'text') else ""
                    url = url_element

                    # Construct product object
                    product = {
                        "title": title,
                        "price": price, 
                        "url": f'https://www.amazon.in{url}',
                        "image_url": image_url
                    }   

                    # Append to results
                    results.append(product)
                else:
                    print("Skipping incomplete result")

            return jsonify(results)
    
        else:
            print('Amazon request failed')
            return []
        
    @retry(RequestException, tries=3, delay=2, backoff=2)
    @app.route('/myntra')
    def get_myntra_results():
        search_term = request.args.get('term')

        # options = Options()
        # options.add_argument('--headless')

        service = Service(r"C:\Users\sarth\Downloads\edgedriver_win64\msedgedriver.exe")
        driver = webdriver.Edge(service=service)
        link=f"https://www.myntra.com/{search_term}"
        driver.get(link)
        driver.maximize_window()
        time.sleep(1)
        response = driver.execute_script("return document.readyState")
        print(response)

        try:
            for i in range(1, 6):
                scroll_position = i * (driver.execute_script("return document.body.scrollHeight") / 8)
                driver.execute_script(f"window.scrollTo(0, {scroll_position});")
                time.sleep(1)

            response = driver.execute_script("return document.readyState")
            print(response)
            if response == "complete":
                # Parse HTML
                soup = BeautifulSoup(driver.page_source, 'html.parser')  
                results = []
                print('hello')

                # Extract data from search results on Myntra
                for item in soup.select('li.product-base'):
                    brand_element = item.select_one('h3.product-brand')
                    product_element = item.select_one('h4.product-product')

                    price_element = item.select_one('span.product-discountedPrice')
                    if price_element:
                        pass
                    else:
                        price_element = item.select_one('div.product-price')


                    image_element = item.select_one('picture.img-responsive')
                    if image_element:
                        image_urls=item.select_one('img')
                        image_url=image_urls['src']
                    else:
                        image_url = None


                    url_element = item.select_one('a')
                    # print(brand_element,url_element['href'],image_element)


                    if brand_element and product_element and price_element and url_element and image_url:
                        brand = brand_element.text.strip()
                        title = f"{brand} - {product_element.text.strip()}"
                        price = price_element.text.strip()
                        url =url_element['href']

                        product = {
                            "title": title,
                            "price": price,
                             "url": f'https://www.myntra.com/{url}',
                            "image_url": image_url
                        }
                        results.append(product)
                    else:
                        print("Skipping incomplete result")

                return jsonify(results)

        except Exception as e:
            print("Error parsing page: ", e)
            return []

        finally:
            driver.quit()

     

            # return jsonify(results)

        # else:
        #     print('Myntra request failedd')
        #     driver.quit()
        #     return []

    
    @retry(RequestException, tries=3, delay=2, backoff=2)
    @app.route('/flipkart')
    def get_flipkart_results():
        search_term = request.args.get('term') 
        url = f"https://www.flipkart.com/search?q={search_term}"
        headers_flipkart = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.48',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.flipkart.com/',
        }
        response = requests.get(url, headers=headers_flipkart)

        if response.status_code == 200:
            
            soup = BeautifulSoup(response.content, 'html.parser')
            results = []
            for item in soup.select('div._1AtVbE'):   

                brand_element = item.select_one('div._2WkVRV')


                product_element = item.select_one('a.IRpwTa _2-ICcC')
                if product_element:
                    pass
                else:
                    product_element = item.select_one('a.IRpwTa')



                title_element = item.select_one('a.s1Q9rs')
                if title_element:
                    pass
                else:
                    title_element = item.select_one('div._4rR01T')



                price_element = item.select_one('div._30jeq3')
                if price_element :
                    pass
                else:
                    price_element = item.select_one('div._30jeq3._1_WHN1')
                if price_element:
                    pass
                else:
                    price_element = item.select_one('div._1_WHN1')
                   


                url_element = item.select_one('a._1fQZEK')
                if url_element :
                    pass
                else:
                    url_element = item.select_one('a.s1Q9rs')
                if url_element:
                    pass
                else:
                    url_element = item.select_one('a._2rpwqI')
                if url_element:
                    pass
                else:
                    url_element = item.select_one('a._8VNy32')
                if url_element:
                    pass
                else:
                    url_element = item.select_one('a.IRpwTa _2-ICcC')
                if url_element:
                    pass
                else:
                    url_element = item.select_one('a.IRpwTa')
                 


                image_element = item.select_one('img._396cs4') 
                if image_element:
                    image_url = image_element['src'] 
                else:
                    image_element = item.select_one('img._2r_T1I')
                    if image_element:
                        image_url = image_element['src'] 
                    else:
                        image_url = None



                if brand_element and product_element and price_element and url_element and image_url:
                    brand = brand_element.text.strip()
                    title = f"{brand} - {product_element.text.strip()}"
                    price = price_element.text.strip()
                    url = url_element['href']

                    # Construct product object
                    product = {
                        "title": title,
                        "price": price,
                        "url": f'https://www.flipkart.com{url}',
                        "image_url": image_url
                    }

                    # Append to results
                    results.append(product)

                
                # Check if all elements are present
                elif title_element and price_element and url_element:
                    title = title_element.text
                    price = price_element.text
                    url = url_element['href']

                    # Construct product object
                    product = {
                        "title": title,
                        "price": price,
                        "url": f'https://www.flipkart.com{url}',
                        "image_url": image_url
                    }

                    # Append to results
                    results.append(product)


                else:
                    print("Skipping incomplete result")

            return jsonify(results)

        else:
            print('Flipkart request failed')
            return []

except Exception as e:
    # Print the traceback
    traceback.print_exc()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)  # Run on a different port than the Node.js app







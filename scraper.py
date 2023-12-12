
# scraper.py
import requests
import traceback
from flask_cors import CORS 
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from requests.exceptions import RequestException
from retry import retry

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
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            # Initialize results
            results = []

            # Extract data from search results 
            for item in soup.select('div._1AtVbE'):    
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
                 


                image_element = item.select_one('img._396cs4')
                image_url = image_element['src'] if image_element else None

                # Check if all elements are present
                if title_element and price_element and url_element:
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







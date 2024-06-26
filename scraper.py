
# scraper.py

import requests
import traceback
from flask_cors import CORS 
from flask_cors import cross_origin
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from requests.exceptions import RequestException
import time
from retry import retry
from selenium import webdriver
# from selenium.webdriver.edge.webdriver import EdgeDriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)
CORS(app)

# try:
    # @retry(RequestException, tries=3, delay=3, backoff=2)
    # @app.route('/amazon')
    # def get_amazon_results():
    #     search_term = request.args.get('term') 
    #     url = f"https://www.amazon.in/s?k={search_term}"
    #     header = {"User-Agent": "Edg/123.0.2420.81"}
    #     response = requests.get(url, headers=header)
    #     print(response.status_code)

    #     if response.status_code == 200:
    #         # Parse HTML
    #         soup = BeautifulSoup(response.content, 'html.parser')
    #         # Initialize results
    #         results = []

    #         # Extract data from search results
    #         for item in soup.select('div[data-asin][data-component-type="s-search-result"]'):
                
    #             brand_element = item.select_one('span.a-size-base-plus.a-color-base') 

    #             title_element = item.select_one('span.a-size-base-plus.a-color-base.a-text-normal')
    #             if title_element is None:
    #                 title_element = item.select_one('span.a-size-medium.a-color-base.a-text-normal')
                
    #             # print(title_element)
    #             # print("1")
    #             price_element = item.select_one('span.a-price > span.a-offscreen')
    #             if price_element is None:
    #                 price_element = item.select_one('spam.a-price-whole')
               
    #             # print(title_element)
    #             url_element = item.select_one('a.a-link-normal.s-no-outline')['href']
    #             if url_element is None:
    #                 url_element = item.select_one('a.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal')['href']
               
    #             # print(url_element)
    #             image_element = item.select_one('img.s-image')
    #             image_url = image_element['src'] if image_element else None

    #             # print(image_url)
    #             # print("4")

    #             if title_element and price_element and url_element:
    #                 title = title_element.text if hasattr(title_element, 'text') else ""
    #                 if brand_element:
    #                     brand = brand_element.text if hasattr(brand_element, 'text') else ""
    #                     title = f'{brand} - {title}'
    #                 price = price_element.text if hasattr(price_element, 'text') else ""
    #                 url = url_element

    #                 # Construct product object
    #                 product = {
    #                     "title": title,
    #                     "price": price, 
    #                     "url": f'https://www.amazon.in{url}',
    #                     "image_url": image_url
    #                 }   

    #                 # Append to results
    #                 results.append(product)
    #             else:
    #                 print("Skipping incomplete result")

    #         return jsonify(results)
    
    #     else:
    #         print('Amazon request failed')
    #         return []

headers = {
    # 'User-Agent': 'Edg/123.0.2420.81'
    'User-Agent': 'Edg/125.0.2535.51'
}

try:
    @retry(RequestException, tries=3, delay=2, backoff=2)
    @app.route('/amazon')
    @cross_origin()
    def get_amazon_results():

        search_term = request.args.get('term')
        service = Service(r"C:\Users\sarth\Downloads\edgedriver_win64 (4)\msedgedriver.exe")
        # service = Service(r"C:\Users\sarth\Downloads\edgedriver_win64 (2)\msedgedriver.exe")
        # service = Service(r"C:\Users\sarth\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe")
        options = Options()
        options.add_argument('--headless')
        options.add_argument("user-agent=Edg/124.0.2478.80")  # Run in headless mode
        driver = webdriver.Edge(service=service,options=options)
        link=f"https://www.amazon.in/s?k={search_term}"
        driver.get(link)
        time.sleep(5)
        response = driver.execute_script("return document.readyState")
        # print(response) 
        try:
            response = driver.execute_script("return document.readyState")
            print(response)
            if response == "complete":
                # driver.quit()
            # if (1):
            # if response.status_code == 200:
                # Parse HTML
                soup = BeautifulSoup(driver.page_source, 'html.parser')  
                results = []
                # print('hello')
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
            
        except Exception as e:
            print("Error parsing page: ", e)
            return jsonify([])

        finally:
            driver.quit()
    
        # else:
        #     print('Amazon request failed')
        #     return []
        
    @retry(RequestException, tries=3, delay=2, backoff=2)
    @app.route('/myntra')
    @cross_origin()
    def get_myntra_results():
        search_term = request.args.get('term')

        options = Options()
        options.add_argument('--headless')
        # options.add_argument("user-agent=Edg/124.0.2478.80")
        options.add_argument("user-agent=Edg/125.0.2535.51")
        service = Service(r"C:\Users\sarth\Downloads\edgedriver_win64 (4)\msedgedriver.exe")
        # service = Service(r"C:\Users\sarth\Downloads\edgedriver_win64 (2)\msedgedriver.exe")
        # service = Service(r"C:\Users\sarth\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe")

        # service = Service(r"C:\Users\sarth\Downloads\edgedriver_win64(3)\msedgedriver.exe")
        driver = webdriver.Edge(service=service,options=options)
        link=f"https://www.myntra.com/{search_term}"
        driver.get(link)
        driver.maximize_window()
        # time.sleep(1)
        response = driver.execute_script("return document.readyState")
        print(response)

        try:
            for i in range(1, 6):
                scroll_position = i * (driver.execute_script("return document.body.scrollHeight") / 8)
                driver.execute_script(f"window.scrollTo(0, {scroll_position});")
                time.sleep(0.3)

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
            return jsonify([])

        finally:
            driver.quit()

     

            # return jsonify(results)

        # else:
        #     print('Myntra request failedd')
        #     driver.quit()
        #     return []
# url = f"https://www.flipkart.com/search?q={search_term}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"

#         headers_flipkart = {
#             'User-Agent': 'Edg/123.0.2420.81',
#             'Accept-Language': 'en-US,en;q=0.9',
#             'Accept-Encoding': 'gzip, deflate, br',
#             'Referer': 'https://www.flipkart.com/',
#         }
    
    @retry(RequestException, tries=3, delay=2, backoff=2)
#     @app.route('/flipkart')
#     def get_flipkart_results():
#         search_term = request.args.get('term')
#         url = f"https://www.flipkart.com/search?q={search_term}"

#         # Setup Selenium WebDriver
#         service = Service(r"C:\Users\sarth\Downloads\edgedriver_win64(3)\msedgedriver.exe")
#         options = Options()
#         options.add_argument('--headless')  # Run in headless mode
#         driver = webdriver.Edge(service=service, options=options)

#         try:
#             driver.get(url)
#             # time.sleep(2)  # Wait for the page to load

#             # Now using Selenium's page source for BeautifulSoup
#             soup = BeautifulSoup(driver.page_source, 'html.parser')
#             results = []

#             for item in soup.select('div._75nlfW'):
#                 brand_element = item.select_one('div.syl9yP')

#                 product_element = item.select_one('a.IRpwTa _2-ICcC')
#                 if product_element:
#                     pass
#                 else:
#                     product_element = item.select_one('a.IRpwTa')
#                 if product_element:
#                     pass
#                 else:
#                     product_element = item.select_one('a.WKTcLC.BwBZTg')
#                 if product_element:
#                     pass
#                 else:
#                     product_element = item.select_one('a.WKTcLC')
# #                 print(product_element)



#                 title_element = item.select_one('a.s1Q9rs')
#                 if title_element:
#                     pass
#                 else:
#                     title_element = item.select_one('div._4rR01T')
#                 if title_element:
#                     pass
#                 else:
#                     title_element = item.select_one('a.wjcEIp')
#                 if title_element:
#                     pass
#                 else:
#                     title_element = item.select_one('div.KzDlHZ')
# #                 print(title_element)





#                 price_element = item.select_one('div._30jeq3')
#                 if price_element :
#                     pass
#                 else:
#                     price_element = item.select_one('div._30jeq3._1_WHN1')
#                 if price_element:
#                     pass
#                 else:
#                     price_element = item.select_one('div._1_WHN1')
#                 if price_element :
#                     pass
#                 else:
#                     price_element = item.select_one('div.Nx9bqj')
#                 if price_element :
#                     pass
#                 else:
#                     price_element = item.select_one('div.Nx9bqj._4b5DiR')
# #                 print(price_element)
                   


#                 url_element = item.select_one('a._1fQZEK')
#                 if url_element :
#                     pass
#                 else:
#                     url_element = item.select_one('a.s1Q9rs')
#                 if url_element:
#                     pass
#                 else:
#                     url_element = item.select_one('a._2rpwqI')
#                 if url_element:
#                     pass
#                 else:
#                     url_element = item.select_one('a._8VNy32')
#                 if url_element:
#                     pass
#                 else:
#                     url_element = item.select_one('a.IRpwTa _2-ICcC')
#                 if url_element:
#                     pass
#                 else:
#                     url_element = item.select_one('a.IRpwTa')
#                 if url_element:
#                     pass
#                 else:
#                     url_element = item.select_one('a.WKTcLC.BwBZTg')
#                 if url_element:
#                     pass
#                 else:
#                     url_element = item.select_one('a.WKTcLC')
#                 if url_element:
#                     pass
#                 else:
#                     url_element = item.select_one('a.wjcEIp')
#                 if url_element:
#                     pass
#                 else:
#                     url_element = item.select_one('a.CGtC98')
# #                 print(url_element)
                    
                 


#                 image_element = item.select_one('img._396cs4') 
#                 if image_element:
#                     image_url = image_element['src'] 
#                 else:
#                     image_element = item.select_one('img._2r_T1I')
#                 if image_element:
#                     image_url = image_element['src'] 
#                 else:
#                     image_element = item.select_one('img._53J4C-')
#                 if image_element:
#                     image_url = image_element['src'] 
#                 else:
#                     image_element = item.select_one('img.DByuf4')
#                     if image_element:
#                         image_url = image_element['src'] 
#                     else:
#                         image_url = None
# #                 print(image_element)
                

#                 if brand_element and product_element and price_element and url_element and image_url:
#                     brand = brand_element.text.strip()
#                     title = f"{brand} - {product_element.text.strip()}"
#                     price = price_element.text.strip()
#                     url = url_element['href']

#                     # Construct product object
#                     product = {
#                         "title": title,
#                         "price": price,
#                         "url": f'https://www.flipkart.com{url}',
#                         "image_url": image_url
#                     }

#                     # Append to results
#                     results.append(product)
#                     # print(results)

                
#                 # Check if all elements are present
#                 elif title_element and price_element and url_element:
#                     title = title_element.text
#                     price = price_element.text
#                     url = url_element['href']

#                     # Construct product object
#                     product = {
#                         "title": title,
#                         "price": price,
#                         "url": f'https://www.flipkart.com{url}',
#                         "image_url": image_url
#                     }

#                     # Append to results
#                     results.append(product)
#                 else:
#                     print("Skipping incomplete result")

#             return jsonify(results)
#         except Exception as e:
#             print(f"Error scraping Flipkart: {e}")
#             return jsonify({"error": "Failed to scrape Flipkart"})
#         finally:
#             driver.quit()
    @app.route('/flipkart')
    @cross_origin()
    def get_flipkart_results():
        search_term = request.args.get('term') 
        url = f"https://www.flipkart.com/search?q={search_term}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"

        headers_flipkart = {
            # 'User-Agent': ' Edg/123.0.2420.81',
            # 'User-Agent': 'Edg/124.0.2478.80',
            'User-Agent': 'Edg/125.0.2535.51',
            # 'User-Agent': 'Chrome/124.0.6367.91',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.flipkart.com/',
        }
        response = requests.get(url, headers=headers_flipkart)

        if response.status_code == 200:
            
            time.sleep(2)
            soup = BeautifulSoup(response.content, 'html.parser')
            results = []
            for item in soup.select('div._75nlfW'):
                brand_element = item.select_one('div.syl9yP')

                product_element = item.select_one('a.IRpwTa _2-ICcC')
                if product_element:
                    pass
                else:
                    product_element = item.select_one('a.IRpwTa')
                if product_element:
                    pass
                else:
                    product_element = item.select_one('a.WKTcLC.BwBZTg')
                if product_element:
                    pass
                else:
                    product_element = item.select_one('a.WKTcLC')
#                 print(product_element)

                title_element = item.select_one('a.s1Q9rs')
                if title_element:
                    pass
                else:
                    title_element = item.select_one('div._4rR01T')
                if title_element:
                    pass
                else:
                    title_element = item.select_one('a.wjcEIp')
                if title_element:
                    pass
                else:
                    title_element = item.select_one('div.KzDlHZ')
#                 print(title_element)

                price_element = item.select_one('div._30jeq3')
                if price_element :
                    pass
                else:
                    price_element = item.select_one('div._30jeq3._1_WHN1')
                if price_element:
                    pass
                else:
                    price_element = item.select_one('div._1_WHN1')
                if price_element :
                    pass
                else:
                    price_element = item.select_one('div.Nx9bqj')
                if price_element :
                    pass
                else:
                    price_element = item.select_one('div.Nx9bqj._4b5DiR')
#                 print(price_element)
                   
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
                if url_element:
                    pass
                else:
                    url_element = item.select_one('a.WKTcLC.BwBZTg')
                if url_element:
                    pass
                else:
                    url_element = item.select_one('a.WKTcLC')
                if url_element:
                    pass
                else:
                    url_element = item.select_one('a.wjcEIp')
                if url_element:
                    pass
                else:
                    url_element = item.select_one('a.CGtC98')
#                 print(url_element)
                    
                image_element = item.select_one('img._396cs4') 
                if image_element:
                    image_url = image_element['src'] 
                else:
                    image_element = item.select_one('img._2r_T1I')
                if image_element:
                    image_url = image_element['src'] 
                else:
                    image_element = item.select_one('img._53J4C-')
                if image_element:
                    image_url = image_element['src'] 
                else:
                    image_element = item.select_one('img.DByuf4')
                    if image_element:
                        image_url = image_element['src'] 
                    else:
                        image_url = None
#                 print(image_element)
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
                    # print(results)
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
            print(response.status_code)
            return []
    

    city_codes = {
    "Agartala": "IXA", "Agatti": "AGX", "Agra": "AGR", "Akola": "AKD",
    "Allahabad": "IXD", "Along": "IXV", "Ambala": "IXD", "Aurangabad": "IXU",
    "Siliguri": "IXB", "Bareilly": "BEK", "Hyderabad": "BPM", "Belgaum": "IXG",
    "Bellary": "BEP", "Bathinda": "BUP", "Bhavnagar": "BHU", "Bhuj": "BHJ",
    "Bidar": "BDR", "Bhubaneswar": "BBI", "Bilaspur": "PAB", "Ranchi": "IXR",
    "Calicut": "CCJ", "Car Nicobar": "CBD", "Chandigarh": "IXC", "Lucknow": "LKO",
    "Chennai": "MAA", "Mumbai": "BOM", "Kochi": "COK", "Coimbatore": "CJB",
    "Vasco da Gama": "GOI", "Daman": "NMB", "Dehradun": "DED", "Indore": "IDR",
    "Dhanbad": "DBD", "Dibrugarh": "DIB", "Dimapur": "DMU", "Nagpur": "NAG",
    "Gaya": "GAY", "Gorakhpur": "GOP", "Gwalior": "GWL",
    "Bangalore": "BLR", "Jalpaiguri": "IXB", "Hisar": "HSS", "Hubli": "HBX",
    "Imphal": "IMF", "New Delhi": "DEL", "Jabalpur": "JLR", "Jaipur": "JAI",
    "Jaisalmer": "JSA", "Bengaluru": "BLR", "Jammu": "IXJ", "Jamnagar": "JGA",
    "Jodhpur": "JDH", "Jorhat": "JRH", "Kadapa": "CDP", "Bhutan": "BHU",
    "Leh": "IXL", "Aizawl": "AJL", "Patna": "PAT", "Guwahati": "GAU",
    "Ludhiana": "LUH", "Madurai": "IXM", "Udaipur": "UDR", "Mangalore": "IXE",
    "Latur": "LTU", "Varanasi": "VNS", "Aizawl": "AJL",
    "Patna": "PAT", "Guwahati": "GAU", "Ludhiana": "LUH", "Madurai": "IXM",
    "Udaipur": "UDR", "Mangalore": "IXE", "Pune": "PNQ", "Bhopal": "BHO",
    "Rajahmundry": "RJA", "Hyderabad": "HYD", "Rajkot": "RAJ", "Ratnagiri": "RTC",
    "Rewa": "REW", "Rourkela": "RRK", "Salem": "SXV",
    "Ahmedabad": "AMD", "Srinagar": "SXR", "Shillong": "SHL", "Shirdi": "SAG",
    "Silchar": "IXS", "Solapur": "SSE", "Jamshedpur": "IXW",
    "Amritsar": "ATQ", "Puttaparthi": "PUT", "Surat": "STV", "Tezpur": "TEZ",
    "Tiruchirappally": "TRZ", "Thiruvananthapuram": "TRV",
    "Vijayawada": "VGA", "Port Blair": "IXZ", "Ziro": "ZER",
    "Kolkata": "CCU",
    }



    @retry(RequestException, tries=3, delay=2, backoff=2)
    @app.route('/paytmflights')
    @cross_origin()
    def get_paytmflights_results():
         origin = request.args.get('origin')
         destination = request.args.get('destination')
         departureDate = request.args.get('formattedDepartureDate')

         # Get city codes from the dictionary
         origin_code = city_codes.get(origin)
         destination_code = city_codes.get(destination)
         if not origin_code or not destination_code:
            return jsonify({"error": "City code not found in the dictionary."})

         try:


             # Adjust URL with city codes
             url = f"https://flight.easemytrip.com/FlightList/Index?srch={origin_code}-{origin}-India|{destination_code}-{destination}-India|{departureDate}&px=1-0-0&cbn=0&ar=undefined&isow=true&isdm=true&lang=en-us&_gl=1*1ctplya*_ga*NjU5NDM4ODc1LjE3MTI3NjgzMzk.*_ga_328ZMQHY8M*MTcxMjc2ODMzOS4xLjEuMTcxMjc2ODQ1Mi42MC4wLjA.&IsDoubleSeat=false&CCODE=IN&curr=INR&apptype=B2C"

             # Set up Edge options
             options = Options()
             options.add_argument("--headless")  # Run Edge in headless mode

             # Create a new instance of the Edge driver
             driver_path = (r"C:\Users\sarth\Downloads\edgedriver_win64 (4)\msedgedriver.exe")
            #  driver_path = (r"C:\Users\sarth\Downloads\edgedriver_win64 (2)\msedgedriver.exe")
            #  driver_path="C:\\Users\\sarth\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"

             service = Service(executable_path=driver_path)

             # Create a new instance of the Edge driver
             driver = webdriver.Edge(service=service, options=options)

             # Navigate to the URL
             driver.get(url)

             # Wait for the page to load (adjust the delay if needed)
             time.sleep(4)

             # Get the page source after JavaScript rendering
             html = driver.page_source

             # Parse the HTML with BeautifulSoup
             soup = BeautifulSoup(html, "html.parser")

             # Extract flight details using the updated CSS selectors
             results = []
             flight_data = soup.find_all("div", {"class": "row no-margn fltResult ng-scope"})
             if flight_data:
                 print(1)
             for flight in flight_data:
                 print(2)
                  # Note: Replace 'button.book-btn' with the actual selector for the booking button
                #  booking_button = flight.find_element_by_css_selector('button.btn.book-bt-n.ng-scope')
                
                # # Click the booking button
                #  booking_button.click()
                
                # # Wait for the new page to load. Adjust the timeout as necessary.
                #  WebDriverWait(driver,0.2).until(EC.url_changes)
                
                # # Extract the current URL, which is now the booking page URL
                #  booking_url = driver.current_url if driver.current_url else None
                
                # # Navigate back to the original page with the list of flights
                #  driver.back()
                
                # # Wait for the original page to load. Adjust the selector as necessary.
                #  WebDriverWait(driver,0.2).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.row.no-margn.fltResult.ng-scope')))
                
                 airline_element = flight.select_one("div.col-md-7.col-sm-7.padd-lft.airl-txt-n > span.txt-r4.ng-binding")
                 airline = airline_element.text if hasattr(airline_element, 'text') else ""

                 departure_time_element = flight.select_one("div.col-md-2.col-sm-2.col-xs-4.top5 > span.txt-r2-n.ng-binding")
                 departure_time = departure_time_element.text if hasattr(departure_time_element, 'text') else ""

                 arrival_time_element = flight.select_one("div.col-md-2.col-sm-2.col-xs-3.top5.txdir > span.txt-r2-n.ng-binding")
                 arrival_time = arrival_time_element.text if hasattr(arrival_time_element, 'text') else ""

                 duration_element = flight.select_one("div.col-md-2.col-sm-2.col-xs-5.non-st > span.dura_md.ng-binding")
                 duration = duration_element.text if hasattr(duration_element, 'text') else ""

                 price_element = flight.select_one("div.col-md-2.col-sm-2.col-xs-5.mr5.cle > div.fareflex > div.ng-scope > div.txt-r6-n.ng-scope > span.ng-binding")
                 if price_element:
                    price = price_element.text if hasattr(price_element, 'text') else ""
                 else:
                     price_element = flight.select_one("div.col-md-10.col-sm-8.col-xs-9.txt-r6-n.exPrc > span.ng-binding")
                     price = price_element.text if hasattr(price_element, 'text') else ""

                 print(airline)
                #  if booking_url is None:
                 booking_url = url

                 flight_details = {
                     "airline": airline,
                     "origin": origin,
                     "destination": destination,
                     "departureTime": departure_time,
                     "arrivalTime": arrival_time,
                     "duration": duration,
                     "price": price,
                     "bookingUrl": booking_url
                    }

                 results.append(flight_details)
                 print(results)
             return jsonify(results)

         except Exception as e:
            print("Error occurred during scraping: ", e)
            return jsonify([])

         finally:
            driver.quit()



    @retry(RequestException, tries=3, delay=2, backoff=2)
    # MakeMyTrip scraping route
    @app.route('/makemytrip')
    @cross_origin()
    def get_makemytripflights_results():
        origin = request.args.get('origin')
        destination = request.args.get('destination')
        deDate = request.args.get('formattedDepartureDate')
        day,month,year=deDate.split('/')
        day = day.zfill(2)
        month = month.zfill(2)
        departureDate = f"{day}/{month}/{year}"
        print (departureDate)



        # Get city codes from the dictionary
        origin_code = city_codes.get(origin)
        destination_code = city_codes.get(destination)
        if not origin_code or not destination_code:
            return jsonify({"error": "City code not found in the dictionary."})

        try:
            # Adjust URL with city codes"
            url = f"https://www.makemytrip.com/flight/search?itinerary={origin_code}-{destination_code}-{departureDate}&tripType=O&paxType=A-1_C-0_I-0&intl=false&cabinClass=E&ccde=IN&lang=eng"
            # Set up Chrome options
            options = Options()
            # options.add_argument("user-agent=Edg/124.0.2478.80")
            options.add_argument("user-agent=Edg/125.0.2535.51")
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--allow-running-insecure-content")
            options.add_argument("--disable-extensions")
            options.add_argument("--profile.default_content_settings.cookies=1")  # Run Chrome in headless mode

            # Create a new instance of the Chrome driver
            driver_path = (r"C:\Users\sarth\Downloads\edgedriver_win64 (4)\msedgedriver.exe")
            # driver_path=(r"C:\Users\sarth\Downloads\edgedriver_win64 (2)\msedgedriver.exe")
    #         driver_path="C:\\Users\\sarth\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"
            service = Service(executable_path=driver_path)
            driver = webdriver.Edge(service=service, options=options)

            # Navigate to the URL
            driver.get(url)

            # Wait for the page to load (adjust the delay if needed)
            time.sleep(4)
            # Get the page source after JavaScript rendering
            html = driver.page_source

            # Parse the HTML with BeautifulSoup
            soup = BeautifulSoup(html, "html.parser")
            # Extract flight details using the updated CSS selectors
            results = []
            flight_data = soup.find_all("div", class_="fli-list-body-section")
            for flight in flight_data:
                airline = flight.find("span", class_="airways-name font12").text.strip()
                departure_time = flight.find("p", class_="dept-time append_bottom3").text.strip()
                departure_city = flight.find("p", class_="dept-city").find("font").text.strip()
                duration_info = flight.find("div", class_="fli-stops make_relative")
                duration = duration_info.find("p", class_="append_bottom5").text.strip() if duration_info else ""

    #             duration = flight.find("p", class_="app").text.strip()
    #             duration_info = flight.find("p", class_="append_bottom5")
    #             hours = duration_info.find("p").contents[0].strip() if duration_info else ""
    #             minutes = duration_info.find("p").contents[2].strip() if duration_info else ""
    #             duration = f"{hours}h {minutes}m"
                arrival_time = flight.find("p", class_="reaching-time append_bottom3").text.strip()
                arrival_city = flight.find("p", class_="arrival-city").find("font").text.strip()
                price = flight.find("span", class_="actual-price").text.strip()

    #         flight_data = soup.find_all("div", class_="fli-list-body-section ")
    #         print(flight_data)
    #         for flight in flight_data:
    #             airline = flight.find("p", class_="boldFont blackText airlineName").text.strip()
    #             departure_info = flight.find("div", class_="flexOne timeInfoLeft")
    #             departure_time = departure_info.find("span").text.strip() if departure_info else ""
    #             arrival_info = flight.find("div", class_="flexOne timeInfoRight")
    #             arrival_time = departure_info.find("span").text.strip() if departure_info else ""
    #             duration_info = flight.find("div", class_="stop-info flexOne")
    #             hours = duration_info.find("p").contents[0].strip() if duration_info else ""
    #             minutes = duration_info.find("p").contents[2].strip() if duration_info else ""
    #             duration = f"{hours}h {minutes}m"
    #             price = flight.find("div", class_="blackText fontSize18 blackFont white-space-no-wrap clusterViewPrice").text.strip()
                booking_url = url
                flight_details = {
                    "airline": airline,
                    "origin": origin,
                    "destination": destination,
                    "departureTime": departure_time,
                    "arrivalTime": arrival_time,
                    "duration": duration,
                    "price": price,
                    "bookingUrl":booking_url
                }
                results.append(flight_details)

            return jsonify(results)

        except Exception as e:
            print("Error occurred during scraping: ", e)
            return jsonify([])

        finally:
            driver.quit()
  

except Exception as e:
    # Print the traceback
    traceback.print_exc()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)  # Run on a different port than the Node.js app








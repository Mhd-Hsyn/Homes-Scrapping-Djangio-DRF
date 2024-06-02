import re
from PIL import Image
import re, time, json
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webApi.models import(
    Property_Type,
    Home,
    Home_Images,
    Price_History,
    Mortgage_History,
    Deed_History
)
from . import helper as hp

def requireKeys(reqArray,requestData):
    try:
        for j in reqArray:
            if not j in requestData:
                return False
            
        return True

    except:
        return False


def allfieldsRequired(reqArray,requestData):
    try:
        for j in reqArray:
            if len(requestData[j]) == 0:
                return False

        
        return True

    except:
        return False


def checkemailforamt(email):
    emailregix = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if(re.match(emailregix, email)):

        return True

    else:
       return False



def passwordLengthValidator(passwd):
    if len(passwd) >= 8 and len(passwd) <= 20:
        return True

    else:
        return False



##both keys and required field validation

def keyValidation(keyStatus,reqStatus,requestData,requireFields):


    ##keys validation
    if keyStatus:
        keysStataus = requireKeys(requireFields,requestData)
        if not keysStataus:
            return {'status':False,'message':f'{requireFields} all keys are required'}



    ##Required field validation
    if reqStatus:
        requiredStatus = allfieldsRequired(requireFields,requestData)
        if not requiredStatus:
            return {'status':False,'message':'All Fields are Required'}





def imageValidator(img,ignoredimension = True,formatcheck = False):

    try:

        if img.name[-3:] == "svg":
            return True
        im = Image.open(img)
        width, height = im.size
        if ignoredimension:
            if width > 330 and height > 330:
                return False

            else:
                return True

        if formatcheck:
            if im.format == "PNG":
                
                return True

            else:
                
                return False
            
        return True
    
    except:
        return False




def execptionhandler(val):
    if 'error' in val.errors:
        error = val.errors["error"][0]
    else:
        key = next(iter(val.errors))
        error = key + ", "+val.errors[key][0]

    return error




def makedict(obj,key,imgkey=False):
    dictobj = {}
    
    for j in range(len(key)):
        keydata = getattr(obj,key[j])
        if keydata:
            dictobj[key[j]] = keydata
    
    if imgkey:
        imgUrl = getattr(obj,key[-1])
        if imgUrl:
            dictobj[key[-1]] = imgUrl.url
        else:
             dictobj[key[-1]] = ""

    return dictobj





def generate_homes_url(
        city,
        state,
        min_price :int = None,
        max_price :int = None,
        min_bedrooms :int = None,
        max_bedrooms :int = None,
        min_baths :int = None,
        max_baths :int = None,
        min_sqft : int = None,
        max_sqft : int = None,
        min_lotsize : str = None,
        max_lotsize : str = None,
        min_yearbuilt : int = None,
        max_yearbuilt : int = None,
        min_dom : str = None,
        max_dom : str = None,
        property_type : str = None
        ):

    base_url = "https://www.homes.com/"
    city = city.replace(" ", "-")
    url = f"{base_url}{city.lower()}-{state.lower()}/"
    # Handling bedrooms parameter
    if min_bedrooms is not None and max_bedrooms is not None:
        url += f"{min_bedrooms}-to-{max_bedrooms}-bedroom/"
    elif min_bedrooms is not None:
        url += f"{min_bedrooms}-bedroom/"
    elif max_bedrooms is not None:
        url += f"{max_bedrooms}-bedroom/"

    
    # Handling baths parameter
    if min_baths is not None and max_baths is not None:
        url += "?" if "?" not in url else "&"
        url += f"bath-min={min_baths}&bath-max={max_baths}"
    elif min_baths is not None:
        url += "?" if "?" not in url else "&"
        url += f"bath-min={min_baths}&bath-max={min_baths}"
    elif max_baths is not None:
        url += "?" if "?" not in url else "&"
        url += f"bath-min={max_baths}&bath-max={max_baths}"

    # Handling price parameter
    if min_price is not None and max_price is not None:
        url += "?" if "?" not in url else "&"
        url += f"price-min={min_price}&price-max={max_price}"

    elif min_price is not None:
        url += "?" if "?" not in url else "&"
        url += f"price-min={min_price}"
    
    elif max_price is not None:
        url += "?" if "?" not in url else "&"
        url += f"price-max={max_price}"

    # Handling sqft parameter
    if min_sqft is not None and max_sqft is not None:
        url += "?" if "?" not in url else "&"
        url += f"sfmin={min_sqft}&sfmax={max_sqft}"
    elif min_sqft is not None:
        url += "?" if "?" not in url else "&"
        url += f"sfmin={min_sqft}"
    elif max_sqft is not None:
        url += "?" if "?" not in url else "&"
        url += f"sfmax={max_sqft}"

    # Handling lot_size parameter
    if min_lotsize is not None and max_lotsize is not None:
        url += "?" if "?" not in url else "&"
        url += f"ls-min={min_lotsize}&ls-max={max_lotsize}"
    elif min_lotsize is not None:
        url += "?" if "?" not in url else "&"
        url += f"ls-min={min_lotsize}"
    elif max_lotsize is not None:
        url += "?" if "?" not in url else "&"
        url += f"ls-max={max_lotsize}"

    # Handling year-built parameter
    if min_yearbuilt is not None and max_yearbuilt is not None:
        url += "?" if "?" not in url else "&"
        url += f"yb-min={min_yearbuilt}&yb-max={max_yearbuilt}"
    elif min_yearbuilt is not None:
        url += "?" if "?" not in url else "&"
        url += f"yb-min={min_yearbuilt}"
    elif max_yearbuilt is not None:
        url += "?" if "?" not in url else "&"
        url += f"yb-max={max_yearbuilt}"

    # Handling days-on-market parameter
    if min_dom is not None:
        url += "?" if "?" not in url else "&"
        url += f"dom-min={min_dom}"
    if max_dom is not None:
        url += "?" if "?" not in url else "&"
        url += f"dom-max={max_dom}"

    # Handling property-type
    if property_type is not None:
        url += "?" if "?" not in url else "&"
        url += f"property_type={property_type}"

    return url




def get_all_links(html):
    """
    This function is responsible for get all links after search
    """
    count = 0

    soup = BeautifulSoup(html, 'html.parser')
    ul_tag = soup.find('ul', class_='placards-list')
    all_links_list = []
    if ul_tag:
        for li_tag in ul_tag.find_all('li', class_='placard-container'):
            # Find the div tag within the li tag with class 'for-sale-content-container'
            div_tag = li_tag.find('div', class_='for-sale-content-container')
            # Find the a tag within the div tag
            a_tag = div_tag.find('a') if div_tag else None
            
            # Extract the href attribute from the a tag
            link = a_tag['href'] if a_tag else None
            # missing   https://www.homes.com/
            link = f"https://www.homes.com{link}"
            count += 1
            print(f"{count} {link}")
            # Append the link to the list
            all_links_list.append(link)
        return all_links_list




def extract_currency(value):
    if value:
        # Use regular expression to extract currency
        match = re.search(r'(?P<currency>[^\d,]+)?', value)
        if match:
            return match.group('currency')
    return ''

def convert_to_number(value):
    if value:
        # Remove commas and dollar signs from the value
        cleaned_value = value.replace(',', '')
        # Use regular expression to extract numeric part
        match = re.search(r'\b\d+(\.\d+)?\b', cleaned_value)
        if match:
            return float(match.group())
    return ''







def scrap_inner_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    data = {
        "id": "",
        "homelink": "",
        "images" : [],
        "price": "",
        "price_currency": "",
        "address_main": "",
        "city": "",
        "state_zip": "",
        "estimated_payment": "",
        "about": "",
        "beds": "",
        "baths": "",
        "sq_ft": "",
        "price_per_sq_ft": "",
        "days_on_market": "",
        # agent details
        "agent_type": "",
        "agent_name":"",
        "agent_email": "",
        "agent_phone": "",
        "agent_agency_name": "",
        # home type
        "home_type": "",
        "est_annual_taxes" : "",
        "year_built": "",
        "hoa_fees": "",
        "lot_detail": "",
        "price_history" : [],
        "deed_history": [],
        "mortgage_history": []   
    }

    city = ''
    address_main = ''
    city = ''
    state_zip = ''
    price = ''

    # for images
    carousel_divs = soup.find_all('div', class_ = "primary-carousel-slide")
    if carousel_divs:
        all_images = []
        for div in carousel_divs:
            image_elements = div.find_all('img', class_ = "primary-carousel-slide-img")
            all_images.extend(img['data-src'] for img in image_elements)
    
        data['images'] = all_images

    # for price
    price_element = soup.find('span', id = 'price')
    price_value = price_element.text.strip() if price_element else ''
    price = convert_to_number(price_value)
    data['price'] =price
    price_currency = extract_currency(price_value)
    data['price_currency'] = price_currency

    # for address
    address_element = soup.find('div', class_ = "property-info-address") if soup.find('div', class_ = "property-info-address") else None
    if address_element is not None:
        address_main_ele = address_element.find('span', class_ = "property-info-address-main")
        address_main = address_main_ele.text.strip() if address_main_ele else ''
        data['address_main'] = address_main
        city_state_elements = address_element.find_all('a', class_=['standard-link', 'text-only']) # b/c of space
        city = city_state_elements[0].text.strip() if city_state_elements and len(city_state_elements) > 0 else ''
        state_zip = city_state_elements[1].text.strip() if city_state_elements and len(city_state_elements) > 0 else ''
        data['city'] = city
        data['state_zip'] = state_zip

    estimated_payment_element = soup.find('p', class_ = ['property-estimated-info' , 'text-only'])
    estimated_payment = estimated_payment_element.text.strip() if estimated_payment_element else ''
    data['estimated_payment'] = convert_to_number(estimated_payment) if estimated_payment else ''

    about_home_element = soup.find('p', class_ = 'ldp-description-text')
    about_home = about_home_element.text.strip() if about_home_element else ''
    data['about'] = about_home if about_home else ''

    # For Beds / Baths / SqFt / price per SqFt
    # Find the main div with class 'property-info-features'
    main_div = soup.find('div', class_='property-info-features')
    if main_div:
        all_spans = main_div.find_all('span', class_='property-info-feature-detail') 
        if all_spans:
            # Extract data from each pair of spans inside the main div  ( FOR BED AND BATHS )
            for span in all_spans:
                key = span.find_next('span').get_text(strip=True)
                value = span.get_text(strip=True)
                if key == "Beds" or key == "Bed":
                    data["beds"] = convert_to_number(value)
                elif key == "Baths" or key == "Bath":
                    data['baths'] = convert_to_number(value)
                elif key == "Sq Ft":
                    data['sq_ft'] = convert_to_number(value)
                elif key == "Price per Sq Ft":
                    data['price_per_sq_ft'] = convert_to_number(value)
                else :
                    # If key doesn't match any condition, move on to the next iteration
                    continue

    # for days on market 
    days_on_market_value = ""

    main_div_for_estimate_price = soup.find("div", class_="search-activity-grid")
    if main_div_for_estimate_price:
        # Locate all activity cards within the main div
        activity_cards = main_div_for_estimate_price.find_all("div", class_="search-activity-card")

        # Loop through the activity cards to find "Days On Market"
        for activity_card in activity_cards:
            title_tag = activity_card.find("p", class_="search-activity-card-title")
            text_tag = activity_card.find("p", class_="search-activity-card-text")

            if title_tag and text_tag:
                title = title_tag.get_text(strip=True)
                if title == "Days On Market":
                    days_on_market_value = text_tag.get_text(strip=True)
                    data['days_on_market'] = days_on_market_value
                    break  # Stop searching once "Days On Market" is found

    # For Lisrening Agents 
    agent_name = ''
    agent_phone = ''
    agent_type = ''
    agent_email = ''
    agent_agency_name = ''
    agent_element = soup.find("div", class_="agent-information-mls-info")
    if agent_element:
        agent_type_element = agent_element.find("p" , class_="listing-agent-title")
        agent_type = agent_type_element.get_text(strip=True) if agent_type_element else ''

        agent_name_element = agent_element.select_one(".agent-information-fullname")
        agent_name = agent_name_element.get_text(strip=True) if agent_name_element else ''

        agent_agency_name_element = agent_element.find("span", class_="agent-information-agency-name")
        agent_agency_name = agent_agency_name_element.get_text(strip=True) if agent_agency_name_element else ''

        agent_phone_ele = agent_element.find("a", class_="agent-information-phone-number")
        agent_phone = agent_phone_ele.get_text(strip=True) if agent_phone_ele else ''
        
        agent_email_ele = agent_element.find("span", class_="agent-information-email")
        agent_email = agent_email_ele.get_text(strip=True) if agent_email_ele else ''

        data['agent_type'] = agent_type
        data['agent_name'] = agent_name
        data['agent_email'] = agent_email
        data['agent_phone'] = agent_phone
        data['agent_agency_name'] = agent_agency_name


    if not agent_name and not agent_phone:
        agent_element = soup.find('div', class_= 'info-wrapper')
        if agent_element:
            agent_type_ele = agent_element.find('div', class_ = 'listing-agent-label') if agent_element else ''
            agent_type = agent_type_ele.text.strip() if agent_type_ele else ''
            data['agent_type'] = agent_type
            agent_name = agent_element.find('div', class_= 'agent-name').text.strip() if agent_element else ''
            data['agent_name'] = agent_name
            agent_phone_element = soup.find('div', class_ ='agent-phone')
            if agent_phone_element:
                agent_phone = agent_phone_element.find('a', class_ = ['standard-link' , 'text-only']).text.strip() if agent_phone_element else ''
                data['agent_phone'] = agent_phone


    home_detail_element = soup.find("div", class_="category")
    if home_detail_element:
        # Locate all subcategory containers within the main category
        sub_categories = home_detail_element.find_all("div", class_="subcategory-container")

        for cat in sub_categories:
            title = cat.find("p", class_="amenity-name").get_text(strip=True)

            if title == "Property Type":
                value = cat.find("li", class_="amenities-detail").get_text(strip=True)
                data['home_type'] = value

            if title == "Home Type":
                value = cat.find("li", class_="amenities-detail").get_text(strip=True)
                data['home_type'] = value

            elif title == "Est. Annual Taxes":
                value = cat.find("li", class_="amenities-detail").get_text(strip=True)
                data['est_annual_taxes'] = convert_to_number(value)

            elif title == "Year Built":
                value = cat.find("li", class_="amenities-detail").get_text(strip=True)
                data['year_built'] = value
            
            elif title == "Year Built | Renovated":
                value = cat.find("li", class_="amenities-detail").get_text(strip=True)
                value = value.split("|")[0].strip() if "|" in value else value.strip()
                data['year_built'] = value

            elif title == "HOA Fees":
                value = cat.find("li", class_="amenities-detail").get_text(strip=True)
                data['hoa_fees'] = convert_to_number(value)

            elif title == "Lot Details" or title == "Unit Details":
                value = cat.find_all("li", class_="amenities-detail")
                val = value[0].get_text(strip=True) if value else ''
                data['lot_detail'] = val
            else:
                continue


    price_table = soup.find('table', class_ = "price-table")
    if price_table:
        # Extract table headers
        headers = [th.text.strip() for th in price_table.find('thead').find_all('th')]

        # Extract table rows
        price_detail_data = []
        for row in price_table.find('tbody').find_all('tr'):
            # Extract the "long-date" span from the "Date" column
            date_span = row.find('th', class_='price-year').find('span', class_='long-date')
            
            # Use the extracted date_span or an empty string if not found
            date = date_span.text.strip() if date_span else ''

            # Extract other columns
            row_data = [date] + [td.text.strip() for td in row.find_all('td')]
            price_detail_data.append(row_data)

        # Create a Pandas DataFrame
        price_df = pd.DataFrame(price_detail_data, columns=headers)
        price_dict = price_df.to_dict(orient='records')
        for entry in price_dict:
            entry['Price'] = convert_to_number(entry.get('Price', None))
            entry['Sq Ft Price'] = convert_to_number(entry.get('Sq Ft Price', None))

        data['price_history'] = price_dict

    # Go for Deed History and Mortage History
    deed_data = []
    deed_table = soup.find('table', class_ = "deed-table")
    if deed_table:
        headers = deed_table.find('thead').find_all('th')
        headers = [th.text.strip() for th in headers]
        rows = deed_table.find('tbody').find_all('tr')
        
        for row in rows:
            date = row.find('span', class_ = "shorter-date").text.strip()
            deed_type = row.find('td', class_ = 'deed-type').text.strip()
            sale_price = row.find('td', class_='deed-sale-price').text.strip()
            title_company = row.find('td', class_='deed-title-company').text.strip()

            # Append data to the list
            deed_data.append([date, deed_type, sale_price, title_company])

        deed_df = pd.DataFrame(columns=headers, data= deed_data)
        deed_dict = deed_df.to_dict(orient='records')
        for entry in deed_dict:
            entry['Sale Price'] = convert_to_number(entry.get('Sale Price', None))

        data['deed_history'] = deed_dict


    mortage_history_table = soup.find('table', class_= "mortgage-table")
    if mortage_history_table:
        headers = [th.text.strip() for th in mortage_history_table.find("thead").find_all("th")]
        rows = [tr for tr in mortage_history_table.find("tbody").find_all("tr")]
        
        mortage_history_data = []
        for row in rows:
            date = row.find('span', class_ = "shorter-date").text.strip()
            status = row.find('td', class_="mortgage-status").text.strip()
            loan_amount = row.find('td', class_="mortgage-amount").text.strip()
            loan_type = row.find('td', class_="mortgage-type").text.strip()
            mortage_history_data.append([date, status, loan_amount, loan_type])
        
        mortage_history_df = pd.DataFrame(data=mortage_history_data, columns=headers)
        mortage_dict = mortage_history_df.to_dict(orient='records')
        for entry in mortage_dict:
            entry['Loan Amount'] = convert_to_number(entry.get('Loan Amount', None))

        data['mortgage_history'] = mortage_dict

    return data






#############################################################################################




def sysInit(options, url):
    # Start virtual display
    display = Display(visible=0, size=(800, 600))
    display.start()
    web_driver = None

    try:
        print("Starting........")
        # Initialize the Chrome WebDriver
        web_driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

        # Navigate to the target URL
        web_driver.get(url)
        html = web_driver.page_source
        links_list = get_all_links(html)
        if not links_list:
            print ("NO links _____")
            return {"status": False,"data":[]}
        
        button_enabled = True
        while button_enabled:
            try:
                # Wait for the button with the text "Next" to be clickable
                next_button = WebDriverWait(web_driver, 20).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.next.text-only'))
                )

                # Scroll into view
                web_driver.execute_script("arguments[0].scrollIntoView(true);", next_button)

                # Click using JavaScript
                web_driver.execute_script("arguments[0].click();", next_button)
                print("CLICKED SUCCESFULLY_____________")

                # Wait for the button to become stale (i.e., replaced with a new one)
                WebDriverWait(web_driver, 10).until(
                    EC.staleness_of(next_button)
                )

                # Wait for the new "Next" button to be clickable
                next_button = WebDriverWait(web_driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.next.text-only'))
                )

                html = web_driver.page_source
                links = get_all_links(html)
                links_list.extend(links) if links is not None else None

            except TimeoutException:
                # Catch TimeoutException and break the loop if the button is not found
                break

            # Check if the button is disabled
            button_enabled = 'disabled' not in next_button.get_attribute('class')

        print("COMPLETEDDD LINKS _________")
        print(json.dumps(links_list))

        data = []
        count = 1

        for link in links_list:
            print("************************************************************")
            print(f"{count} LINK IS START______________________________________________ ", link)

            web_driver.get(link)
            html = web_driver.page_source
            web_driver.execute_script("window.scrollTo(0, 600);")
            web_driver.implicitly_wait(20)
            time.sleep(2)
            html = web_driver.page_source
            web_driver.execute_script("window.scrollTo(0, 700);")
            web_driver.implicitly_wait(20)
            time.sleep(2)
            html = web_driver.page_source
            web_driver.execute_script("window.scrollTo(0, 7500);")
            web_driver.implicitly_wait(20)
            time.sleep(2)
            html = web_driver.page_source
            web_driver.execute_script("window.scrollTo(0, 1500);")
            web_driver.implicitly_wait(20)
            time.sleep(2)
            html = web_driver.page_source

            link_data = scrap_inner_data(html)
            uid = link.split("/")
            uid = uid[-1] if uid[-1] else uid[-2]
            link_data['id'] = uid
            link_data['homelink'] = link
            data.append(link_data)
            # print(html)
            print(f"\n\n\nLink No {count} HTML ************************ COMPLETE  *******************************\n\n\n\n\n\n\n")
            
            count += 1
        print(json.dumps(data))

        return {"status": True, "data" : data}

    finally:
        print("QUIT WEB DRIVER ______________")
        # Stop virtual display regardless of success or failure
        display.stop()

        # Quit the WebDriver
        if web_driver:
            web_driver.quit()




#############################################################################



def add_data(my_data):
    print("____________________________\n\n\n")
    for home_data in my_data['homes']:
        property_type, created = Property_Type.objects.get_or_create(name=home_data['home_type'].lower())

        gethome = Home.objects.filter(homeid= home_data['id'], homelink= home_data['homelink']).first()

        if not gethome:
            print(property_type)
            price = hp.to_decimal(home_data['price'])
            print(price)
            print(type(price))
            price_currency = home_data['price_currency']
            
            city = home_data['city'].split(',')[0].strip()
            state = home_data['city'].split(',')[1].strip()
            
            zip_code = hp.convert_positive_integer(home_data['state_zip'])
            print(zip_code)
            print(type(zip_code))

            address = home_data['address_main']
            estimated_payment =  hp.to_decimal(home_data['estimated_payment'])
            about = home_data['about']
            beds =  hp.to_decimal(home_data['beds'])
            print(beds)
            print(type(beds))

            baths =  hp.to_decimal(home_data['baths'])
            print(baths)
            print(type(baths))
            
            sqft =  hp.to_decimal(home_data['sq_ft'])
            print(sqft)
            print(type(sqft))
            
            price_per_sqft =  hp.to_decimal(home_data['price_per_sq_ft'])
            print(price_per_sqft)
            print(type(price_per_sqft))
            
            lot_size = hp.convert_lot_size(home_data['lot_detail'])
            print("LOT SIZE IS ",lot_size)
            print("LOT SIZE TYPE IS ___ ",type(lot_size))

            days_on_market = hp.convert_days_on_market(home_data['days_on_market'])
            print("DOM IS ",days_on_market)
            print("DOM TYPE IS ___ ",type(days_on_market))

            year_built = hp.convert_positive_integer(home_data['year_built'])
            print("Year built IS ",year_built)
            print("Year-buikt TYPE IS ___ ",type(year_built))

            est_annual_tax = hp.convert_positive_integer(home_data['est_annual_taxes'])
            print("Est Annual Tax IS ",est_annual_tax)
            print("Est Annual Tax TYPE IS ___ ",type(est_annual_tax))

            hoa_fees = hp.convert_positive_integer(home_data['hoa_fees'])
            print("hoa_fees IS ",hoa_fees)
            print("hoa_fees TYPE IS ___ ",type(hoa_fees))

            agent_type = home_data['agent_type']
            agent_name =home_data['agent_name']
            agent_email = home_data['agent_email']
            agent_phone = home_data['agent_phone']
            agent_agency_name = home_data['agent_agency_name']

            print("\n\n\n")
            

            home = Home.objects.create(
                property_type = property_type,
                homeid = home_data['id'],
                homelink = home_data['homelink'], 
                price = price,
                price_currency = price_currency,
                city = city,
                state = state,
                zip_code = zip_code,
                address = address,
                estimated_payment =estimated_payment,
                about = about,
                beds = beds,
                baths = baths,
                sqft = sqft,
                price_per_sqft = price_per_sqft,
                lot_size_sqft = lot_size,
                days_on_market = days_on_market,
                year_built = year_built,
                est_annual_tax = est_annual_tax,
                hoa_fees = hoa_fees,
                # agent detail
                agent_type = agent_type,
                agent_name = agent_name,
                agent_email =agent_email,
                agent_phone =agent_phone,
                agent_agency_name = agent_agency_name
            )
            for image_url in home_data['images']:
                Home_Images.objects.create(
                    home = home,
                    image = image_url
                )
            
            for price_history_data in home_data['price_history']:
                Price_History.objects.create(
                    date=hp.convert_to_common_date_format(price_history_data['Date']),
                    event=price_history_data['Event'],
                    price=hp.to_decimal(price_history_data['Price']),
                    change=price_history_data['Change'],
                    sqft_price=hp.to_decimal(price_history_data['Sq Ft Price']),
                    home=home
                )
            
            for deed_history_data in home_data['deed_history']:
                Deed_History.objects.create(
                    date = hp.convert_to_common_date_format(deed_history_data['Date']),
                    type = deed_history_data['Type'],
                    sale_price = hp.to_decimal(deed_history_data['Sale Price']),
                    title_company = deed_history_data['Title Company'],
                    home = home
                )
            
            for mortgage_data in home_data['mortgage_history']:
                loan_amount =hp.to_decimal(mortgage_data['Loan Amount'])
                date = hp.convert_to_common_date_format(mortgage_data['Date'])

                Mortgage_History.objects.create(
                    date = date,
                    status = mortgage_data['Status'],
                    loan_amount= loan_amount,
                    loan_type = mortgage_data['Loan Type'],
                    home = home
                )
        else:
            print("Home is exists in database, you can't add again")
    return True




##############################################################################################





def get_and_add(options, url):
    # Start virtual display
    display = Display(visible=0, size=(800, 600))
    display.start()
    web_driver = None

    try:
        print("Starting........")
        # Initialize the Chrome WebDriver
        web_driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

        # Navigate to the target URL
        web_driver.get(url)
        html = web_driver.page_source
        links_list = get_all_links(html)
        if not links_list:
            print ("NO links _____")
            return {"status": False,"data":[]}
        
        button_enabled = True
        while button_enabled:
            try:
                # Wait for the button with the text "Next" to be clickable
                next_button = WebDriverWait(web_driver, 20).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.next.text-only'))
                )

                # Scroll into view
                web_driver.execute_script("arguments[0].scrollIntoView(true);", next_button)

                # Click using JavaScript
                web_driver.execute_script("arguments[0].click();", next_button)
                print("CLICKED SUCCESFULLY_____________")

                # Wait for the button to become stale (i.e., replaced with a new one)
                WebDriverWait(web_driver, 10).until(
                    EC.staleness_of(next_button)
                )

                # Wait for the new "Next" button to be clickable
                next_button = WebDriverWait(web_driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.next.text-only'))
                )

                html = web_driver.page_source
                links = get_all_links(html)
                links_list.extend(links) if links is not None else None

            except TimeoutException:
                # Catch TimeoutException and break the loop if the button is not found
                break

            # Check if the button is disabled
            button_enabled = 'disabled' not in next_button.get_attribute('class')

        print("COMPLETEDDD LINKS _________")
        # print(json.dumps(links_list))


        # remove links which already scrap and added in DB
        existing_links = Home.objects.values_list('homelink', flat=True)
        filtered_link = [link for link in links_list if link not in existing_links]
        data = []

        for index, link in enumerate(filtered_link):
            print("************************************************************")
            print(f"{index+1} LINK IS START______________________________________________ ", link)

            web_driver.get(link)
            html = web_driver.page_source
            web_driver.execute_script("window.scrollTo(0, 600);")
            web_driver.implicitly_wait(20)
            time.sleep(2)
            html = web_driver.page_source
            web_driver.execute_script("window.scrollTo(0, 700);")
            web_driver.implicitly_wait(20)
            time.sleep(2)
            html = web_driver.page_source
            web_driver.execute_script("window.scrollTo(0, 7500);")
            web_driver.implicitly_wait(20)
            time.sleep(2)
            html = web_driver.page_source
            web_driver.execute_script("window.scrollTo(0, 1500);")
            web_driver.implicitly_wait(20)
            time.sleep(2)
            html = web_driver.page_source

            link_data = scrap_inner_data(html)
            uid = link.split("/")
            uid = uid[-1] if uid[-1] else uid[-2]
            link_data['id'] = uid
            link_data['homelink'] = link
            # after fetching add the single home data in Database
            add_data({"homes":[link_data]})
            data.append(link_data)
            
            # print(html)
            print(f"\n\n\nLink No {index+1} HTML ************************ COMPLETE  *******************************\n\n\n\n\n\n\n")
            
        print(json.dumps(data))

        return {"status": True, "data" : data}

    finally:
        print("QUIT WEB DRIVER ______________")
        # Stop virtual display regardless of success or failure
        display.stop()

        # Quit the WebDriver
        if web_driver:
            web_driver.quit()

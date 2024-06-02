import os, json, time
from decimal import Decimal
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from selenium.webdriver.chrome.options import Options
from .models import (
    Property_Type,
    Home,
    Home_Images,
    Price_History,
    Mortgage_History,
    Deed_History
)
from .serializers import *
from webApi.Useable import helper as hp
from webApi.Useable import useable as uc

# Set Chrome options
options = Options()
# options.headless = False
options.add_argument('--enable-logging')
options.add_argument('--log-level=0')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
options.add_argument('--no-sandbox')




class HomesDataScraperViewset(ModelViewSet):
    """
    This Class has method getjson
    """
    @action (detail= False, methods= ['GET'])
    def get_homes_data(self, request):
        """
        Fetch homes data from homes.com based on provided parameters.

        Parameters:
        - city (str): The city name. (mendatory)
        - state (str): The state code. (mendatory)
        - min_price (int): Minimum price filter (optional).
        - max_price (int): Maximum price filter (optional).
        - min_bedrooms (int): Minimum number of bedrooms (optional).
        - max_bedrooms (int): Maximum number of bedrooms (optional).
        - min_baths (int): Minimum number of bathrooms (optional).
        - max_baths (int): Maximum number of bathrooms (optional).

        Returns:
        - JSON: A JSON-formatted response containing the scraped homes data.

        Usage:
        - Call this method with appropriate parameters to get homes data in JSON format.
        """
        try:
            require_field = ['city', 'state']
            validator = uc.keyValidation(True, True, request.GET, require_field)
            if validator:
                return Response( validator, status= status.HTTP_400_BAD_REQUEST)

            homes_url = uc.generate_homes_url(**request.GET.dict())
            print("created a link ")
            print("url ____", homes_url)

            fetch_data = uc.sysInit(options, homes_url)
            if fetch_data['status']:
                my_data = {"status": True,"homes" : fetch_data['data']}
                file_name = 'homes_data.json'
                file_path = os.path.join(os.getcwd(), file_name)
                with open(file_path, 'w') as json_file:
                    json.dump(my_data, json_file, indent=4)

                return Response({"status": True,"homes" : fetch_data['data']}, status= status.HTTP_200_OK)
            
            elif not fetch_data['status']:
                return Response({"status": False, "error": "block by homes.com", "homes" : fetch_data['data']}, status= status.HTTP_200_OK)

            else:
                return Response({"status": False, "error": "Something wents Wrong "}, status= status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            message = f"somethings wents wrong _____ error : {e}"
            return Response({"status": False, "error": message}, status= status.HTTP_400_BAD_REQUEST)



    @action(detail= False, methods= ['POST'])
    def add_homes_data(self, request):
        try:
            file = request.FILES.get('file', None)
            if file is None:
                return Response({"status": False, "error": "Please upload the file"}, status= status.HTTP_400_BAD_REQUEST)
            json_data =JSONParser().parse(file)
            add_data = uc.add_data(json_data)
            if add_data:
                return Response({"status": True, "message": "Data Inserted succssfully"}, status= status.HTTP_200_OK)

        except Exception as e:
            message = f"somethings wents wrong _____ error : {e}"
            return Response({"status": False, "error": message}, status= status.HTTP_400_BAD_REQUEST)



    @action (detail= False, methods= ['GET'])
    def get_and_add_homes_data(self, request):
        try:
            require_field = ['city', 'state']
            validator = uc.keyValidation(True, True, request.GET, require_field)
            if validator:
                return Response( validator, status= status.HTTP_400_BAD_REQUEST)

            homes_url = uc.generate_homes_url(**request.GET.dict())
            print("created a link ")
            print("url ____", homes_url)

            fetch_data = uc.get_and_add(options, homes_url)
            if fetch_data['status']:
                return Response({"status": True, "message": "Data Inserted succssfully" ,"homes" : fetch_data['data']}, status= status.HTTP_200_OK)

            elif not fetch_data['status']:
                return Response({"status": False,"error": "block by homes.com","homes" : fetch_data['data']}, status= status.HTTP_200_OK)

            else:
                return Response({"status": False, "error": "Something wents Wrong "}, status= status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            message = f"somethings wents wrong _____ error : {e}"
            return Response({"status": False, "error": message}, status= status.HTTP_400_BAD_REQUEST)


    
    @action(detail= False, methods=['GET'])
    def get_homes_by_filters(self, request):
        try:
            filters={}
            city = request.GET.get('city', None)
            state = request.GET.get('state', None)
            price_min = request.GET.get('price_min', None)
            price_max = request.GET.get('price_max', None)
            beds_min = request.GET.get('beds_min', None)
            beds_max = request.GET.get('beds_max', None)
            baths_min = request.GET.get('baths_min', None)
            baths_max = request.GET.get('baths_max', None)
            sqft_max = request.GET.get('sqft_max', None)
            sqft_min = request.GET.get('sqft_min', None)
            yb_max = request.GET.get('yb_max', None)
            yb_min = request.GET.get('yb_min', None)
            dob_max = request.GET.get('dob_max', None)
            dob_min = request.GET.get('dob_min', None)
            lot_max = request.GET.get('lot_max', None)
            lot_min = request.GET.get('lot_min', None)
            property_type = request.GET.get('property_type', None)

            if not city and not state:
                return Response({"status": False, "error": "city and state name is required"}, status= status.HTTP_400_BAD_REQUEST)

            filters['city'] =city
            filters['state'] =state

            if price_min:
                filters['price__gte'] = price_min
            if price_max:
                filters['price__lte'] = price_max
            if beds_min:
                filters['beds__gte'] = beds_min
            if beds_max:
                filters['beds__lte'] = beds_max
            if baths_min:
                filters['baths__gte'] = baths_min
            if baths_max:
                filters['baths__lte'] = baths_max
            if sqft_min:
                filters['sqft__gte'] = sqft_min
            if sqft_max:
                filters['sqft__lte'] = sqft_max
            if yb_min:
                filters['year_built__gte'] = yb_min
            if yb_max:
                filters['year_built__lte'] = yb_max
            if dob_max:
                filters['days_on_market__lte'] = dob_max
            if dob_min:
                filters['days_on_market__gte'] = dob_min
            if lot_max:
                if "sf" not in lot_max:
                    lot_max = hp.extract_numeric_value(lot_max)
                    lot_max = Decimal(lot_max) * Decimal('43560')
                else:
                    lot_max = hp.extract_numeric_value(lot_max)
                filters['lot_size_sqft__lte'] = lot_max
            if lot_min:
                if "sf" not in lot_min:
                    lot_min = hp.extract_numeric_value(lot_min)
                    lot_min = lot_min * Decimal('43560')
                else:
                    lot_min = hp.extract_numeric_value(lot_min)
                filters['lot_size_sqft__gte'] = lot_min
            if property_type:
                property_types = [ptype.strip() for ptype in property_type.split(',')]
                filters['property_type__name__in'] = property_types

            # query_set = Home.objects.filter(**filters).order_by('price')
            query_set = Home.objects.filter(**filters)
            serializer = HomesSerializer(query_set, many=True)
            return Response({"status": True, "homes" : serializer.data}, status= status.HTTP_200_OK)

        except Exception as e:
            message = f"somethings wents wrong _____ error : {e}"
            return Response({"status": False, "error": message}, status= status.HTTP_400_BAD_REQUEST)


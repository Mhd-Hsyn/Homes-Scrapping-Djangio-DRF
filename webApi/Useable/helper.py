import re
from decimal import Decimal
from dateutil import parser



def convert_to_decimal(value):
    if value:
        # Remove commas and dollar signs from the value
        cleaned_value = value.replace(',', '').replace('$', '')
        
        # Use regular expression to extract numeric part
        match = re.search(r'\b\d+(\.\d+)?\b', cleaned_value)
        
        if match:
            return Decimal(match.group())
        
    return None



def to_decimal(value):
    if value:
        # Use regular expression to extract numeric part
        match = re.search(r'\b\d+(\.\d+)?\b', str(value))
        if match:
            return Decimal(match.group())
    return None


def convert_positive_integer(value):
    if value:
        value = str(value)
        # Remove commas and dollar signs from the value
        cleaned_value = value.replace(',', '').replace('$', '')
        
        # Use regular expression to extract numeric part
        match = re.search(r'\b\d+\b', cleaned_value)
        
        if match:
            return int(match.group())
        
    return None



def convert_lot_size(lot_detail):
    if lot_detail:
        # Remove unwanted characters
        cleaned_detail = lot_detail.replace(',', '').strip().lower()
        
        # Check if the lot size is in square feet
        sqft_match = re.match(r'([\d,]+)\s*sq\s*ft', cleaned_detail)
        if sqft_match:
            return convert_to_decimal(sqft_match.group(1))
        
        # Check if the lot size is in acres
        acre_match = re.match(r'([\d.]+)\s*acre', cleaned_detail)
        if acre_match:
            # Convert acres to square feet (1 acre = 43,560 sq ft)
            acre_value = Decimal(acre_match.group(1))
            sqft_value = acre_value * Decimal('43560')
            return sqft_value
        else:
          return convert_to_decimal(lot_detail)
    
    return None



def convert_days_on_market(value):
    if value:
        if 'hours ago' in value or 'hours' in value:
          return 1
        else:
          return convert_positive_integer(value)
    return None


def convert_to_common_date_format(date_string):
    try:
        date_object = parser.parse(date_string).date()
        return date_object.strftime("%Y-%m-%d")
    except ValueError:
        # If parsing fails, return None
        return None
    
def extract_numeric_value(s):
    # Remove commas and non-numeric characters
    cleaned_value = re.sub(r'[^0-9.]', '', s)
    # Convert to Decimal
    print("___________",cleaned_value)
    return Decimal(cleaned_value) if cleaned_value else None
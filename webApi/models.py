from django.db import models
import uuid
from decimal import Decimal

# Create your models here.

class BaseModel(models.Model):
    id = models.UUIDField(default = uuid.uuid4, editable = False, primary_key = True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True, null = True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False, null = True, blank = True)

    class Meta:
        abstract = True


class Property_Type(BaseModel):
    name= models.CharField(max_length=225, default="", unique = True)
    
    def __str__(self):
        return f".{self.name}"



class Home(BaseModel):
    homeid = models.CharField(max_length=50, blank=True, null=True)
    homelink = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=30, decimal_places=2, blank=True, null=True)
    price_currency = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, default="",blank=True, null=True, db_index=True)
    state = models.CharField(max_length=10, default ="", blank=True, null=True, db_index=True)
    zip_code = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=225,blank=True, null=True)
    estimated_payment = models.DecimalField(max_digits=30,decimal_places=2,blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    beds = models.DecimalField(max_digits=30, decimal_places=2, blank=True, null=True)
    baths = models.DecimalField(max_digits=30, decimal_places=2, blank=True, null=True)
    sqft = models.DecimalField(max_digits=30, decimal_places=2, blank=True, null=True)
    lot_size_sqft = models.DecimalField(max_digits=30, decimal_places=2, blank=True, null=True)
    price_per_sqft = models.DecimalField(max_digits=30, decimal_places=2, blank=True, null=True)
    days_on_market= models.PositiveIntegerField(blank=True, null=True)
    year_built = models.PositiveIntegerField(blank=True, null=True)
    est_annual_tax = models.PositiveIntegerField(blank=True, null=True)
    hoa_fees = models.PositiveIntegerField(blank=True, null=True)
    property_type = models.ForeignKey(Property_Type, on_delete=models.CASCADE,blank=True, null=True)
    # agent details 
    agent_type = models.CharField(max_length=50, blank=True, null=True)
    agent_name = models.CharField(max_length=50, blank=True, null=True)
    agent_email = models.CharField(max_length=254,blank=True, null=True)
    agent_phone = models.CharField(max_length=50, blank=True, null=True)
    agent_agency_name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.address}, {self.city}, {self.state}"



class Home_Images(models.Model):
    id = models.UUIDField(default = uuid.uuid4, editable = False, primary_key= True)
    image = models.TextField()
    home = models.ForeignKey(Home, on_delete=models.CASCADE, blank=True, null=True, db_index = True)

    def __str__(self) -> str:
        return f"{self.home}"

class Price_History(BaseModel):
    date = models.DateField(auto_now=False, auto_now_add=False,blank=True, null=True)
    event = models.CharField(max_length=50, blank=True, null=True)
    price = models.DecimalField(max_digits=30, decimal_places=2, blank=True, null=True)
    change= models.CharField(max_length=50, blank=True, null=True)
    sqft_price = models.DecimalField(max_digits=30, decimal_places=2, blank=True, null=True)
    home = models.ForeignKey(Home, on_delete=models.CASCADE,blank=True, null=True, db_index = True)

    def __str__(self) -> str:
        return f"{self.home}"
    


class Deed_History(BaseModel):
    date = models.DateField(auto_now=False, auto_now_add=False,blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    sale_price = models.DecimalField(max_digits=30, decimal_places=2, blank=True, null=True)
    title_company= models.CharField(max_length=50, blank=True, null=True)
    home = models.ForeignKey(Home, on_delete=models.CASCADE,blank=True, null=True, db_index = True)

    def __str__(self) -> str:
        return f"{self.home}"


class Mortgage_History(BaseModel):
    date = models.DateField(auto_now=False, auto_now_add=False,blank=True, null=True)
    status = models.CharField(max_length=50,blank=True, null=True)
    loan_amount = models.DecimalField(max_digits=30, decimal_places=2, blank=True, null=True)
    loan_type= models.CharField(max_length=50, blank=True, null=True)
    home = models.ForeignKey(Home, on_delete=models.CASCADE,blank=True, null=True, db_index = True)

    def __str__(self) -> str:
        return f"{self.home}"
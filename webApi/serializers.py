from rest_framework import serializers
from decimal import Decimal, ROUND_DOWN


from .models import (
    Property_Type,
    Home,
    Home_Images,
    Price_History,
    Mortgage_History,
    Deed_History
)

class PriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Price_History
        fields = ['date', 'event', 'price', 'change', 'sqft_price']


class DeedHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Deed_History
        fields = ['date', 'type', 'sale_price', 'title_company']


class MortgageHistorySerializer (serializers.ModelSerializer):
    class Meta :
        model = Mortgage_History
        fields = ['date', 'status', 'loan_amount', 'loan_type']


class HomesSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    price_history = PriceHistorySerializer(many=True, read_only=True, source='price_history_set')
    deed_history = DeedHistorySerializer(many=True, read_only=True, source='deed_history_set')
    mortgage_history = MortgageHistorySerializer(many=True, read_only= True, source='mortgage_history_set')
    property_type = serializers.CharField(source="property_type.name")

    class Meta:
        model = Home
        exclude = ['created_at','updated_at', 'id']

    def get_images(self, obj):
        home_images = Home_Images.objects.filter(home= obj)
        images = [image_obj.image for image_obj in home_images]
        return images
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Modify the representation of lot_size_sqft
        lot_size_sqft = representation.get('lot_size_sqft', None)
        if lot_size_sqft is not None:
            lot_size_sqft = Decimal(lot_size_sqft)
            if lot_size_sqft >= 8712:
                lot_size_acres = (lot_size_sqft / Decimal(43560)).quantize(Decimal('0.00'), rounding=ROUND_DOWN)
                representation['lot_size_sqft'] = f"{lot_size_sqft} sqft | {lot_size_acres} acres"
            else:
                representation['lot_size_sqft'] = f"{lot_size_sqft} sqft"
        return representation
from django import forms
from .models import Coin

class CoinForm(forms.ModelForm):
	class Meta:
		model = Coin
		fields = [
			'have',
			'isCoin',
			'value',
			'unit',
			'country',
			'year',
			'description',
			'conservation',
			'marketPrice',
			'photoFront',
			'photoBack',]
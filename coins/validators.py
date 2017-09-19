from django.core.exceptions import ValidationError

def validade_positive(value):
	if value <= 0:
		raise ValidationError('%(value)s is not a positive number',params={'value': value},)

def validade_positive_zero(value):
	if value < 0:
		raise ValidationError('%(value)s is not a positive number',params={'value': value},)
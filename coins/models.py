import os
from django.core.files.storage import FileSystemStorage 
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.core.urlresolvers import reverse
from PIL import Image
# Create your models here.
from .utils import unique_slug_generator,toASCII
from .validators import *


class OverwriteFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=50):
		if os.path.exists(self.path(name)):
			os.remove(self.path(name))
		return name

class CoinQuerySet(models.query.QuerySet):
    def search(self, query):
        if query:
            query = query.strip()
            return self.filter(
                Q(value__iexact=query)|
                Q(unit__icontains=query)|
                Q(country__icontains=query)|
                Q(year__iexact=query)|
                Q(description__icontains=query)|
                Q(conservation__iexact=query)|
                Q(marketPrice__iexact=query)
                ).distinct()
        return self


class CoinManager(models.Manager):
    def get_queryset(self):
        return CoinQuerySet(self.model, using=self._db)
    def search(self, query):
    	return self.get_queryset().search(query)

class Coin(models.Model):
	CONSERVATION_STATES = [
        ('UNC', 'Uncirculated(100%)'),
        ('XF', 'Extremely Fine(90%)'),
        ('VF', 'Very Fine(70%)'),
        ('F', 'Fine(50%)'),
        ('G', 'Good(25%)'),
        ('P', 'Poor'),
    ]
	FS = OverwriteFileSystemStorage()

	id 			= models.AutoField(primary_key=True)
	slug		= models.SlugField(null=True,blank=True,editable=False)#unique=true
	owner		= models.ForeignKey(settings.AUTH_USER_MODEL)
	timestamp	= models.DateTimeField(auto_now_add=True)
	updated		= models.DateTimeField(auto_now=True)

	have 		= models.BooleanField(default=True)
	isCoin 		= models.BooleanField(default=True)
	value 		= models.DecimalField(max_digits=10,decimal_places=2,default=0,validators=[validade_positive_zero])
	unit 		= models.CharField(max_length=30,default='')
	country		= models.CharField(max_length=30,default='')
	year		= models.DecimalField(max_digits=5,decimal_places=0,null=True,blank=True,validators=[validade_positive_zero])
	description	= models.TextField(max_length=500,default='',blank=True)
	conservation= models.CharField(max_length=3,default='F',choices=CONSERVATION_STATES)
	marketPrice = models.DecimalField(max_digits=10,decimal_places=2,default=0,validators=[validade_positive_zero])
	photoFront	= models.ImageField(upload_to='photos/', storage=FS,blank=True)
	photoBack	= models.ImageField(upload_to='photos/', storage=FS,blank=True)
	
	objects = CoinManager()

	def get_absolute_url(self):
		return reverse('coins:view',kwargs={'slug':self.slug})

	def get_update_url(self):
		return reverse('coins:update',kwargs={'slug':self.slug})

	@property
	def name(self):
		return str(self.value)+' '+str(self.unit)+' '+self.country+'/'+str(self.year)

	def __str__(self):
		return self.name

def coin_pre_save_receiver(sender, instance, *args, **kwargs):
	frontPhotoOldName=""
	backPhotoOldName=""
	imgID=Coin.objects.latest('id').id+1
	try:
		old = Coin.objects.get(pk=instance.pk)
		frontPhotoOldName=old.photoFront.name
		backPhotoOldName=old.photoBack.name
		imgID=old.id
	except Exception:
		pass
	if(instance.year is None):
		instance.year=0
	instance.unit = toASCII(instance.unit).capitalize()
	instance.country = toASCII(instance.country).capitalize()
	if(instance.photoFront.name!='unknown.png' and instance.photoFront.name!=frontPhotoOldName):
		instance.photoFront.name=str(imgID)+"_front.jpg"#+instance.photoFront.name.split(".")[-1]
	if(instance.photoBack.name!='unknown.png' and instance.photoBack.name!=backPhotoOldName):
		instance.photoBack.name=str(imgID)+"_back.jpg"#+instance.photoFront.name.split(".")[-1]
	if not instance.slug:
		instance.slug=unique_slug_generator(instance)

pre_save.connect(coin_pre_save_receiver, sender=Coin)
###-	OLD STUFF	-###
import random
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse

def lrn_home_learning(request):
	random_number=random.randint(9000,66666);
	rand_bool=bool(random.getrandbits(1))
	coin_list=["Antigas","Internacionais","Raras","Especiais","Comemoraticas","Uma copia de cada"]
	context={	"var_method":"context variable",
				"django_power":random_number,
				"rand_bool":rand_bool,
				"coin_list":coin_list}
	return render(request, "learning-django/home_learning.html", context)
def lrn_inheritance(request):
	context={}
	return render(request, "learning-django/inheritance.html", context)
def lrn_links(request):
	context={}
	return render(request, "learning-django/links.html", context)
def lrn_home_old(request):
	version="simple version"
	to_replace="All about my coins and cedules, "+version+".\n<br><a href=\"/learn/\">main page</a>"#py2
	#to_replace=f"All about my coins and cedules, {version}.\n<br><a href=\"/learn/\">main page</a>"#py3
	return HttpResponse(to_replace)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView

from .forms import CoinForm
from .models import Coin
# Create your views here.

class CoinCreateView(LoginRequiredMixin,CreateView):
	form_class=CoinForm
	template_name='coins/form.html'
	login_url='/login/'
	def get_context_data(self,*args,**kwargs):
		context=super(CoinCreateView,self).get_context_data(*args,**kwargs)
		context['title']='Add'
		return context
	def form_valid(self,form):
		instance=form.save(commit=False)
		instance.owner=self.request.user
		return super(CoinCreateView,self).form_valid(form)

class CoinUpdateView(LoginRequiredMixin,UpdateView):
	form_class=CoinForm
	template_name='coins/form.html'
	login_url='/login/'
	def get_context_data(self,*args,**kwargs):
		context=super(CoinUpdateView,self).get_context_data(*args,**kwargs)
		context['title']='Update'
		return context
	def get_queryset(self):
		return Coin.objects.filter(owner=self.request.user);
	def form_valid(self,form):
		instance=form.save(commit=False)
		instance.owner=self.request.user
		return super(CoinUpdateView,self).form_valid(form)

class CoinDetailView(DetailView):
	queryset=Coin.objects.all()

class CoinListView(ListView):
	def get_queryset(self):
		sorterby = self.request.GET.get('sorter')
		query = self.request.GET.get('q')
		showCoins=int(self.request.GET.get('showcoins', None) is not None)
		notShowNotes=int(self.request.GET.get('shownotes', None) is None)
		if(showCoins==1 or notShowNotes == 0):
			qs = Coin.objects.filter(Q(have__iexact=self.kwargs['haveOnly'])&(Q(isCoin__iexact=showCoins)|Q(isCoin__iexact=notShowNotes))).search(query)
		else:
			qs=Coin.objects.none()
		if(sorterby=='newer'):
			qs=qs.order_by('timestamp').reverse()
		elif(sorterby=='older'):
			qs=qs.order_by('timestamp')
		elif(sorterby=='country'):
			qs=qs.order_by('country')
		elif(sorterby=='value'):
			qs=qs.order_by('value').reverse()
		elif(sorterby=='valueless'):
			qs=qs.order_by('value')
		elif(sorterby=='year'):
			qs=qs.order_by('year')
		elif(sorterby=='year-'):
			qs=qs.order_by('year').reverse()
		elif(sorterby=='conser'):
			qs=qs.order_by('conservation')
		elif(sorterby=='decript'):
			qs=qs.order_by('description')
		return qs
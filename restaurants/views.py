from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q # Q Look ups
from django.shortcuts import render, get_object_or_404
from django.http import	HttpResponse, HttpResponseRedirect
from django.views import View
from django.views.generic import (TemplateView, ListView, DetailView, CreateView, UpdateView)

from .forms import	RestaurantCreateForm, RestaurantLocationCreateForm
from .models import RestaurantLocation
from menus.models import Item


class RestaurantListView(LoginRequiredMixin, ListView):

	def get_queryset(self):
		return RestaurantLocation.objects.filter(owner=self.request.user)



class RestaurantDetailView(LoginRequiredMixin, DetailView):
	def get_queryset(self):
		return RestaurantLocation.objects.filter(owner=self.request.user)

	def get_item(self):
		return Item.objects.filter(restaurant=self.request.restaurant)



  
class RestaurantCreateView(LoginRequiredMixin, CreateView):
	form_class = RestaurantLocationCreateForm
	# login_url = '/login/' #Puedo sobreescribir la configuracion por defecto en base.py
	template_name = 'form.html'
	success_url = "/restaurants/"

	def form_valid(self, form):
		instance = form.save(commit=False)

		instance.owner = self.request.user 
		instance.save()
		return super(RestaurantCreateView, self).form_valid(form)

	def get_context_data(self, *args, **kwargs):
		context = super(RestaurantCreateView, self).get_context_data(*args, **kwargs)
		context['title'] = 'Add Restaurant'
		return context 


class RestaurantUpdateView(LoginRequiredMixin, UpdateView):
	form_class = RestaurantLocationCreateForm
	login_url = '/login/' #Puedo sobreescribir la configuracion por defecto en base.py
	template_name = 'restaurants/detail-update.html'
	success_url = "/restaurants/"


	def get_context_data(self, *args, **kwargs):
		context = super(RestaurantUpdateView, self).get_context_data(*args, **kwargs)
		name = self.get_object().name
		context['title'] = f'Update Restaurant: {name}'
		return context 

	def get_queryset(self):
		return RestaurantLocation.objects.filter(owner=self.request.user)




















# Create your views here.



# class AboutView(TemplateView):
# 	template_name = 'about.html'

# class ContactView(TemplateView):
# 	template_name = 'contact.html'



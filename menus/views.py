from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView
# Create your views here.
from .forms import ItemForm 
from .models import Item



class HomeView(View):
	'''Este codigo muestra las ultimas publicaciones de los usuarios 
	que seguidos por el usuario que se encuentra logeado, es la pagina de inicio
	de la aplicacion'''

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return render(request, "home.html", {})

		user = request.user
		is_following_user_ids = [x.user.id for x in user.is_following.all()]
		qs = Item.objects.filter(user__id__in = is_following_user_ids, public=True).order_by("-updated")[:3] #Ordena los resultados del queryset y lo limita a una cantidad determinada. 

		return render(request, "menus/home-feed.html", {'object_list': qs})



class ItemListView(LoginRequiredMixin, ListView):
	'''Muestra los items publicados por el usuario que se encuentra logeado'''

	def get_queryset(self):
		return Item.objects.filter(user=self.request.user)


class ItemDetailView(LoginRequiredMixin, DetailView):
	'''Muestra el detalle de cada uno de los items publicados, se encuentra sobreescrito 
	por la clase ItemUpdateView'''

	def get_queryset(self):
		return Item.objects.filter(user=self.request.user)


class ItemCreateView(LoginRequiredMixin, CreateView):
	template_name = 'form.html'
	form_class = ItemForm


	def form_valid(self, form):
		'''Mediante esta funcion se guarda en la base de datos 
		la informacion introducida en el formulario'''

		obj = form.save(commit=False)
		obj.user = self.request.user
		return super(ItemCreateView, self).form_valid(form)

	def get_form_kwargs(self):
		kwargs = super(ItemCreateView, self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs

	def get_queryset(self):
		return Item.objects.filter(user=self.request.user)

	def get_context_data(self, *args, **kwargs):
		context = super(ItemCreateView, self).get_context_data(*args, **kwargs)
		context['title'] = 'Create Item'
		return context

class ItemUpdateView(UpdateView):
	template_name = 'menus/detail-update.html'
	form_class = ItemForm



	def get_queryset(self):
		return Item.objects.filter(user=self.request.user)

	def get_context_data(self, *args, **kwargs):
		context = super(ItemUpdateView, self).get_context_data(*args, **kwargs)
		context['title'] = 'Update Item'

		return context

	'''Esta funcion trabaja directamente con el formulario de la clase'''	
	def get_form_kwargs(self):
		kwargs = super(ItemUpdateView, self).get_form_kwargs()
		kwargs['user'] = self.request.user

		return kwargs
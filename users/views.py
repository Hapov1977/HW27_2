from django.shortcuts import render

# Create your views here.
import json

from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from ads.models import LocationModel
from avito_django_proj.settings import TOTAL_ON_PAGE
from users.models import UserModel


@method_decorator(csrf_exempt, name="dispatch")
class UserListView(ListView):
    model = UserModel

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.annotate(
            total_ads=Count('admodel', filter=Q(admodel__is_published=True)))\
            .select_related('location').order_by('username')
        # self.object_list = self.object_list.prefetch_related("locations").annotate(
        #     total_ads=Count('ad__is_published', filter=Q(ad__is_published=True))
        # ).order_by('username')

        paginator = Paginator(self.object_list, TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        users = []

        for user in page_obj:
            users.append({
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role,
                'age': user.age,
                'location_id': user.location_id,
                'location': str(user.location),
                'total_ads': user.total_ads,
            })

        response = {
            "items": users,
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False, "indent": 4})


class UserDetailedView(DetailView):
    model = UserModel

    def get(self, request, *args, **kwargs):
        user = self.get_object()

        response = {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
            'age': user.age,
            'location_id': user.location_id,
            'location': str(user.location),
        }

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False, "indent": 4})


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = UserModel
    fields = ['username', 'first_name', 'last_name', 'role', 'password', 'age', 'location']

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)

        user = UserModel.objects.create(
            username=user_data.get('username'),
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            role=user_data.get('role'),
            password=user_data.get('password'),
            age=user_data.get('age')
        )
        location, created = LocationModel.objects.get_or_create(name=user_data.get['location'])
        user.location = location
        user.save()

        response = {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
            'age': user.age,
            'location_id': user.location_id,
            'location': str(user.location),
        }

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False, "indent": 4})


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = UserModel
    fields = ['username', 'first_name', 'last_name', 'role', 'password', 'age', 'location']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        user_data = json.loads(request.body)

        self.object.first_name = user_data.get('first_name')
        self.object.last_name = user_data.get('last_name')
        self.object.role = user_data.get('role')
        self.object.password = user_data.get('password')
        self.object.age = user_data.get('age')

        location, created = LocationModel.objects.get_or_create(name=user_data.get['location'])
        self.object.location = location

        self.object.save()

        response = {
            'id': self.object.id,
            'username': self.object.username,
            'first_name': self.object.first_name,
            'last_name': self.object.last_name,
            'role': self.object.role,
            'age': self.object.age,
            'location_id': self.object.location_id,
            'location': str(self.object.location),
        }

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False, "indent": 4})


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = UserModel
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)

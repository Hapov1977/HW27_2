import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.models import AdModel, CatModel
from HW27_2.settings import TOTAL_ON_PAGE
from users.models import UserModel


def index(request):
    response = {"status": "ok ok ok"}
    return JsonResponse(response, safe=True, json_dumps_params={"ensure_ascii": False, "indent": 4})


@method_decorator(csrf_exempt, name="dispatch")
class AdListView(ListView):
    model = AdModel

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.select_related('author').select_related('category').order_by('-price')

        paginator = Paginator(self.object_list, TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        ads = []

        for ad in page_obj:
            ads.append({
                'id': ad.id,
                'author_id': ad.author_id,
                'author': str(ad.author),
                'name': ad.name,
                'price': ad.price,
                'description': ad.description,
                'is_published': ad.is_published,
                'image': ad.image.url if ad.image else None,
                'category_id': ad.category_id,
            })

        response = {
            "items": ads,
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False, "indent": 4})


class AdDetailedView(DetailView):
    model = AdModel

    def get(self, request, *args, **kwargs):
        ad = self.get_object()

        response = {
            'id': ad.id,
            'author_id': ad.author_id,
            'author': str(ad.author),
            'name': ad.name,
            'price': ad.price,
            'description': ad.description,
            'is_published': ad.is_published,
            'image': ad.image.url if ad.image else None,
            'category_id': ad.category_id,
        }

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False, "indent": 4})


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = AdModel
    fields = ['name', 'author', 'price', 'description', 'is_published', 'image', 'category']

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)

        ad = AdModel.objects.create(
            name=ad_data["name"],
            price=ad_data["price"],
            description=ad_data["description"],
            is_published=ad_data["is_published"],
        )
        ad.author = get_object_or_404(UserModel, pk=ad_data.get('author_id'))
        ad.category = get_object_or_404(CatModel, pk=ad_data.get('category_id'))
        ad.save()

        response = {
            'id': ad.id,
            'author_id': ad.author_id,
            'author': str(ad.author),
            'name': ad.name,
            'price': ad.price,
            'description': ad.description,
            'is_published': ad.is_published,
            'image': ad.image.url if ad.image else None,
            'category_id': ad.category_id,
        }

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False, "indent": 4})


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = AdModel
    fields = ['name', 'price', 'description', 'is_published', 'image', 'category']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        ad_data = json.loads(request.body)

        self.object.name = ad_data.get('name')
        self.object.price = ad_data.get('price')
        self.object.description = ad_data.get('description')
        self.object.is_published = ad_data.get('is_published')
        self.object.category_id = ad_data.get('category_id')

        self.object.save()

        response = {
            'id': self.object.id,
            'author_id': self.object.author_id,
            'author': str(self.object.author),
            'name': self.object.name,
            'price': self.object.price,
            'description': self.object.description,
            'is_published': self.object.is_published,
            'image': self.object.image.url if self.object.image else None,
            'category_id': self.object.category_id,
        }

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False, "indent": 4})


@method_decorator(csrf_exempt, name='dispatch')
class AdImageView(UpdateView):
    model = AdModel
    fields = ['name', 'image']

    def patch(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES["image"]
        self.object.save()

        response = {
            'id': self.object.id,
            'author_id': self.object.author_id,
            'author': str(self.object.author),
            'name': self.object.name,
            'price': self.object.price,
            'description': self.object.description,
            'is_published': self.object.is_published,
            'image': self.object.image.url if self.object.image else None,
            'category_id': self.object.category_id,
        }

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False, "indent": 4})


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = AdModel
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class CatListView(ListView):
    model = CatModel

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.order_by('name')

        categories = []

        for category in self.object_list:
            categories.append({
                'id': category.id,
                'name': category.name,
            })

        response = categories

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False, "indent": 4})


class CatDetailedView(DetailView):
    model = CatModel

    def get(self, request, *args, **kwargs):
        category = self.get_object()

        response = {
            'id': category.id,
            'name': category.name,
        }

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False, "indent": 4})


@method_decorator(csrf_exempt, name='dispatch')
class CatCreateView(CreateView):
    model = CatModel
    fields = ['name']

    def post(self, request, *args, **kwargs):
        category_data = json.loads(request.body)

        category = CatModel.objects.create(
            name=category_data["name"],
        )

        category.save()

        response = {
            'id': category.id,
            'name': category.name,
        }

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False, "indent": 4})


@method_decorator(csrf_exempt, name='dispatch')
class CatUpdateView(UpdateView):
    model = CatModel
    fields = ['name']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        category_data = json.loads(request.body)

        self.object.name = category_data.get('name')

        self.object.save()

        response = {
            'id': self.object.id,
            'name': self.object.name,
        }

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False, "indent": 4})


@method_decorator(csrf_exempt, name='dispatch')
class CatDeleteView(DeleteView):
    model = CatModel
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)

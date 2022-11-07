from django.db import models


class CatModel(models.Model):
    # id = models.BigAutoField(auto_created=True, primary_key=True, unique=True)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class LocationModel(models.Model):
    name = models.CharField(max_length=150)
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Месторасположение"
        verbose_name_plural = "Месторасположения"


class AdModel(models.Model):
    IS_PUBLISHED = [
        (True, "Published"),
        (False, "Not Published"),
    ]

    # id = models.BigAutoField(auto_created=True, primary_key=True, unique=True)
    name = models.CharField(max_length=150)
    author = models.ForeignKey('users.UserModel', on_delete=models.CASCADE, null=True)
    price = models.PositiveIntegerField(default=0)
    description = models.CharField(max_length=2000)
    image = models.ImageField(upload_to='images/')
    is_published = models.BooleanField(choices=IS_PUBLISHED, default=True)
    category = models.ForeignKey(CatModel, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
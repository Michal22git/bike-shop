from .models import Category


def products(request):
    categories = Category.objects.all()
    bikes_category = Category.objects.get(name="Bikes")

    return {'categories': categories, 'bikes_category': bikes_category}

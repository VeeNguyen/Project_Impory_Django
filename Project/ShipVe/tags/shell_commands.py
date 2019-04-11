# from tags.models import Tag

Tag.objects.all()
# <QuerySet [<Tag: electronics>, <Tag: supplements>, <Tag: food>, <Tag: clothes>]>
Tag.objects.last()
Tag.objects.first()
electronics = Tag.objects.first()
electronics.title
'electronics'

electronics.slug
'electronics'

electronics.active
True

electronics.products
# <django.db.models.fields.related_descriptors.create_forward_many_to_many_manager.<locals>.ManyRelatedManager object at 0x7f40f8de4390>

electronics.products.all()
# <ProductQuerySet [<Product: Laptop>, <Product: Super Laptop>]>

electronics.products.all().first()
'Laptop'


# from products.models import Product
# qs = Product.objects.all()
qs
# <ProductQuerySet [<Product: Fishoil>, <Product: Cookies>, <Product: Laptop>, <Product: Super Laptop>, <Product: Shoes>]>


fishoil = qs.first()
fishoil
# <Product: Fishoil>
fishoil.title
'Fishoil'
fishoil.description
'Great fishoild from Alaska...'

fishoil.tag_set
# <django.db.models.fields.related_descriptors.create_forward_many_to_many_manager.<locals>.ManyRelatedManager object at 0x7f446d69c4a8>

fishoil.tag_set.all()
# <QuerySet [<Tag: supplements>]>

fishoil.tag_set.filter(title__icontains='supplements')
# <QuerySet [<Tag: supplements>]>

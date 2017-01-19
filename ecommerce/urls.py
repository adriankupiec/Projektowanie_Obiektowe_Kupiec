from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^cart/$', views.cart, name='cart'),
    url('^cart/remove/(?P<cart_item_pk>[0-9]+)$', views.cart_remove_item, name='cart_remove_item'),
    url('^cart/add/(?P<product_pk>[0-9]+)$', views.cart_add_product, name='cart_add_product'),
    url(r'^products/$', views.ProductsList.as_view(), name='product_list'),
    url(r'^product_categories/$', views.ProductCategoriesList.as_view(), name='product_categories_list'),
    url('^product_categories/(?P<product_category_pk>[0-9]+)$', views.product_category, name='product_category'),

]

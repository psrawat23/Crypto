from django.urls import path
from blockchain1 import views

urlpatterns = [
    path('',views.index,name="index"),
    path('mine_block/',views.mine_block,name="mine_block"),
    path('get_chain/',views.get_chain,name='get_chain'),
    path('is_valid/',views.is_valid,name='is_valid')
]

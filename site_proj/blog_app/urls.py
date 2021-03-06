from django.urls import path
from . import views

app_name = 'blog_app_name'
urlpatterns = [
    path('', views.post_list, name='post_list'),
    #! ViewsList method
    # path('view/', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('tag/<slug:tag__slug>/', views.post_list, name='post_tag'),
]
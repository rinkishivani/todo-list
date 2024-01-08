from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('<str:username>/<int:pk>/home/', views.superuser_home, name="superuser_home"),
    path('home/', views.home, name="home"),
    path('<int:pk>/task', views.task, name="task"),
    path('<int:pk>/delete', views.delete, name="delete"),
    path('new-task', views.create, name="create-task"),
    path('<int:pk>/update-task', views.update, name="update-task"),
    path('<int:pk>/soft-delete', views.soft_delete, name="soft-delete"),
    path('trash', views.trash, name="trash"),
    path('<int:pk>/restore', views.restore, name="restore"),

    path("login/", views.login_page, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_page, name="logout-page"),
    # path("orm/", views.orm, name="query"),
    # path('display-meta/', views.display_request_meta, name='display_request_meta'),
    # path('home/<int:pk>', views.delete, name="delete"),
]

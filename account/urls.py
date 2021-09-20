from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
	path('', views.UserListView.as_view(), name="user_list"),
	path('filter/', views.FilterUserView.as_view(), name="ufilter"),
	path('usercard/<int:pk>-<str:slug>/', views.UserDetailView.as_view(), name="user_detail"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

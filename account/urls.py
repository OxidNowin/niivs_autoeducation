from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
	path('', auth_views.LoginView.as_view(), name='login_view'),
	path('logout/', auth_views.LogoutView.as_view(), name='logout_view'),
	path('userlist/', views.UserListView.as_view(), name="user_list"),
	path('filter/', views.FilterUserView.as_view(), name="ufilter"),
	path('usercard/<int:pk>-<str:slug>/', views.UserDetailView.as_view(), name="user_detail"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

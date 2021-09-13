from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
	path('', views.PollListView.as_view(), name="poll_list"),
	path('<int:pk>/', views.PollDetailView.as_view(), name="poll_detail"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

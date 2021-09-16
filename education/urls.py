from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
	path('', views.UserListView.as_view(), name="usercard_list"),
	path('filter/', views.FilterUserCardView.as_view(), name="ufilter"),
	path('feducation/filter/', views.FilterFEducationView.as_view(), name="ffilter"),
	path('peducation/filter/', views.FilterPEducationView.as_view(), name="pfilter"),
	path('usercard/<int:pk>-<str:slug>/', views.UserDetailView.as_view(), name="usercard_detail"),
	path('feducation/', views.FEducationView.as_view(), name="feducation_view"),
	path('feducation/<int:pk>', views.FEducationDetailView.as_view(), name="feducation_detail_view"),
	path('get_fedu_xl/', views.FEducationView.get_fedu_xl, name="get_fedu_xl"),
	path('peducation/', views.PEducationView.as_view(), name="peducation_view"),
	path('peducation/<int:pk>', views.PEducationDetailView.as_view(), name="peducation_detail_view"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

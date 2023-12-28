from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
      path('', ViewProcessRequests.as_view(), name='index'),
      path('register/', RegistrateUser.as_view(), name='registration'),
      path('login/', BBLoginView.as_view(), name='login'),
      path('logout/', BBLogoutView.as_view(), name='logout'),
      path('request/create/', CreateRequest.as_view(), name='request_create'),
      path('accounts/profile/delete/<int:pk>', DeleteRequest.as_view(), name='request_delete'),
      path('accounts/profile/', ViewRequests.as_view(), name='profile'),
      path('requests/filter/', RequestListView.as_view(), name='request_list'),
      path('requests/filter/delete/<int:pk>', DeleteRequestFilter.as_view(), name='request_delete')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

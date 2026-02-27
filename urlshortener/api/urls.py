from django.urls import path
from .views import *
urlpatterns = [
    path('shorten/', CreateShortURLView.as_view(),name='create_short_url'),
    path('r/<str:shortened_url>/', RedirectShortURLView.as_view(), name='redirect_short_url'),
    path('urls/', ListShortURLsView.as_view(), name='list_short_urls'),
    path('clicks/<str:shortened_url>/', ClicksView.as_view(), name='click_detail'),
]
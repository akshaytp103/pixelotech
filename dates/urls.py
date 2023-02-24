from django.urls import path
from .views import ImageRatingView,ImageHistoryList

urlpatterns = [
    path('rateimage/', ImageRatingView.as_view(), name='rate_image'),
    path('history/', ImageHistoryList.as_view(), name='image_history_list'),
]

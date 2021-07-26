from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (get_auth_token, CategoryViewSet, CommentViewSet,
                    GenreViewSet, RegistrationAPIView, ReviewViewSet,
                    TitleViewSet, UserViewSet)

router_v1 = DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='users')
router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('titles', TitleViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/auth/token/', get_auth_token),
    path('v1/auth/email/', RegistrationAPIView.as_view()),
    path('v1/', include(router_v1.urls)),
]

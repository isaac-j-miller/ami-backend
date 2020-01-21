from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'notes', views.GeoNoteViewSet)
router.register(r'stacks', views.StackedImageViewSet)
router.register(r'overlays', views.OverlayImageViewSet)
router.register(r'users', views.UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'),
    path('overlays/req/',views.OverlayImageViewSet.request_overlay,name='request overlay')),
    path('overlays/req/',views.OverlayImageViewSet.possible_overlays, name='possible overlays'),
    path('users/req/',views.UserViewSet.authenticate, name='authenticate'),
    path('stacks/req/',views.StackedImageViewSet.request_dates, name='request dates'),
    path('notes/req/',views.GeoNoteViewSet.get_next_id,name='get next id'),
    path('notes/req/',views.GeoNoteViewSet.update_add_note,name='update or add note'),
    path('notes/req/',views.GeoNoteViewSet.del_id,name='delete note by id')
]
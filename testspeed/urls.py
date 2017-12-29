from rest_framework.routers import SimpleRouter

from .views import ClientViewSet, ServerViewSet, ResultViewSet

router = SimpleRouter(trailing_slash=False)

router.register("clients", ClientViewSet)
router.register("servers", ServerViewSet)
router.register("results", ResultViewSet)

urlpatterns = router.urls

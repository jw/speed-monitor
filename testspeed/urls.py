from django.urls import path
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import SimpleRouter

from .views import ClientViewSet, ServerViewSet, ResultViewSet

router = SimpleRouter(trailing_slash=False)

router.register("clients", ClientViewSet)
router.register("servers", ServerViewSet)
router.register("results", ResultViewSet)

DESCRIPTION = "The API of the speed-monitor."

urlpatterns = [
    path('docs/', include_docs_urls(title='speed-monitor',
                                    description=DESCRIPTION)),
]

urlpatterns += router.urls

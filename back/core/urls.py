from rest_framework.routers import DefaultRouter
from .views import PostViewset

router = DefaultRouter()
router.register("posts", PostViewset, "posts")

urlpatterns = router.urls
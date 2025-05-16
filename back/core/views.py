from rest_framework.viewsets import ModelViewSet
from .models import Post
from .serializers import PostSerializer

# Create your views here.
class PostViewset(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
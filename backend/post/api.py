from django.http import JsonResponse
from .serializers import PostSerializer
from .models import Post
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .forms import PostForm
# Create your views here.

@api_view(['GET'])
def post_list(request):
    posts = Post.objects.all() # change later to feed 
    serializer = PostSerializer(posts, many=True)
    return JsonResponse(serializer.data, safe=False)

# Gets the posts associated with specific user id
@api_view(['GET'])
def post_list_profile(request, id): #id will be own user id or id of user youre visiting
    posts = Post.objects.filter(created_by_id=id)

    serializer = PostSerializer(posts, many=True)
    return JsonResponse(serializer.data, safe=False)


# POST == create
@api_view(['POST'])
def post_create(request):

    form = PostForm(request.data)
    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()

        serializer = PostSerializer(post)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error':'add something here later'})

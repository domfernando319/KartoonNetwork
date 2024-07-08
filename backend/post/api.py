from django.http import JsonResponse
from .serializers import CommentSerializer, PostSerializer, PostDetailSerializer
from .models import Post, Like, Comment
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .forms import PostForm
from account.models import User
from account.serializers import UserSerializer

# Create your views here.

@api_view(['GET'])
def post_list(request):

    user_ids = [request.user.id]

    for user in request.user.friends.all():
        #print(user.name)
        user_ids.append(user.id)

    posts = Post.objects.filter(created_by_id__in = list(user_ids)) # change later to feed 


    serializer = PostSerializer(posts, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def post_detail(request, pk):
    post = Post.objects.get(pk=pk)

    return JsonResponse({
        'post': PostDetailSerializer(post).data
    })

# Gets the posts associated with specific user id
@api_view(['GET'])
def post_list_profile(request, id): #id will be own user id or id of user youre visiting
    posts = Post.objects.filter(created_by_id=id)
    user = User.objects.get(pk=id)

    posts_serializer = PostSerializer(posts, many=True)
    user_serializer = UserSerializer(user)
    return JsonResponse({
        'posts': posts_serializer.data,
        'user': user_serializer.data
    }, safe=False)


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

@api_view(['POST'])
def post_like(request, pk):
    post = Post.objects.get(pk=pk)
    if not post.likes.filter(liked_by=request.user):
        
        like = Like.objects.create(liked_by=request.user)
        post = Post.objects.get(pk=pk)
        post.likes_count += 1
        post.likes.add(like)
        post.save()

        return JsonResponse({'message': 'Post liked'})
    else:
        return JsonResponse({'message': 'Post already liked'})
    
@api_view(['POST'])
def post_create_comment(request, pk):
    comment = Comment.objects.create(body=request.data.get('body'), created_by=request.user)
    post = Post.objects.get(pk=pk)
    post.comments.add(comment)
    post.comments_count += 1
    post.save()

    serializer = CommentSerializer(comment)

    return JsonResponse(serializer.data, safe=False)
    
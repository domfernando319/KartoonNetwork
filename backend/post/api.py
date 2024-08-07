from django.http import JsonResponse
from .serializers import CommentSerializer, PostSerializer, PostDetailSerializer, TrendSerializer
from .models import Post, Like, Comment, Trend
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .forms import PostForm, AttachmentForm
from account.models import User, FriendRequest
from account.serializers import UserSerializer

# Create your views here.

@api_view(['GET'])
def post_list(request):

    user_ids = [request.user.id]

    for user in request.user.friends.all():
        #print(user.name)
        user_ids.append(user.id)

    posts = Post.objects.filter(created_by_id__in = list(user_ids)) # change later to feed 

    trend = request.GET.get('trend', '')

    if trend:
        posts = posts.filter(body__icontains='#' + trend)


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

    can_send_friend_request = True
    if request.user in user.friends.all():
        can_send_friend_request = False

    user_to_you = FriendRequest.objects.filter(created_for=request.user).filter(created_by=user)
    you_to_user = FriendRequest.objects.filter(created_for=user).filter(created_by=request.user)

    if user_to_you or you_to_user:
        can_send_friend_request = False

    return JsonResponse({
        'posts': posts_serializer.data,
        'user': user_serializer.data,
        'can_send_friend_request': can_send_friend_request,
    }, safe=False)


# POST == create
@api_view(['POST'])
def post_create(request):

    form = PostForm(request.POST)
    attachment = None
    attachment_form = AttachmentForm(request.POST, request.FILES)

    if attachment_form.is_valid():
        attachment = attachment_form.save(commit=False)
        attachment.created_by = request.user
        attachment.save()

    
    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user


        post.save()

        if attachment:
            post.attachments.add(attachment)
        user = request.user
        user.post_count += 1
        user.save()
        
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

@api_view(['DELETE'])
def post_delete(request, pk):
    post = Post.objects.filter(created_by=request.user).get(pk=pk)
    post.delete()

    return JsonResponse({'message': 'post deleted'})

@api_view(['GET'])
def get_trends(request):
    trends = Trend.objects.all()
    serializer = TrendSerializer(trends, many=True)

    return JsonResponse(serializer.data, safe=False)



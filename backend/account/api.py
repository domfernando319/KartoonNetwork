from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .forms import SignupForm
from .models import User, FriendRequest

@api_view(['GET'])
def me(request):
        return JsonResponse({
             'id': request.user.id, 
             'name': request.user.name,
             'email': request.user.email,
        })

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data
    message = 'success'
    
    form = SignupForm({
        'email': data.get('email'),
        'name': data.get('name'),
        'password1': data.get('password1'),
        'password2': data.get('password2'),
    })

    if form.is_valid():
        form.save()
        status = 200
        # send email verification later
    else:
        message = 'errorrrs'
        print(form.errors)
        status = 400
        # return JsonResponse({'message': form.errors}, status=400)
    return JsonResponse({'message': message, 'errors': form.errors}, status=status)



@api_view(['POST'])
def send_friend_request(request, pk):
        # get user from database
        user = User.objects.get(pk=pk)

        friend_request = FriendRequest(created_for=user, created_by=request.user)

        return JsonResponse({
             'message': 'friend request created'
        })
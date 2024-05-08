from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
import jwt, datetime

# Create your views here.
class RegisterView(APIView):  # extends the APIView class from rest_framework
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # improvements send email function before sending json response
        return Response(serializer.data)  # can customize the content of the response
    
# create login view
class LoginView(APIView):
    def post(self, request):
        # we are logging in using email and password
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found') 
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')  
        
        payload = {
            'id': user.id,
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=60),  # token lasts for only 60mins
            'iat': datetime.datetime.now(datetime.timezone.utc)
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')
        response = Response()

        # set token to cookies
        response.set_cookie(key='jwt', value=token, httponly=True, secure=True)  # we on ly want backend to access token
        response.data = {'jwt': token}
        
        return response
    
# user view to allow us get the cookie to retrieve the user
class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unathenticated!')  # if token is not set
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        # return Response(token)
        return Response(serializer.data)
    

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }

        return response
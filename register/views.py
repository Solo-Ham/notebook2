from django.shortcuts import render
from .serializers import RegisterSerializer, NoteSerializer, NoteDisplaySerializer, CustomTokenObtainSerializer, UserUpdateSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import views
from .models import CustomUser, Note
from rest_framework.permissions import IsAuthenticated, AllowAny
from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.mixins import DestroyModelMixin
from .mail import registration_email
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from .serializers import PasswordResetSerializer
# from .ser
# Create your views here.


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user.save()
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token


            registration_email(user)

            

            return Response (
                {
                    'refresh': str(refresh),
                    'access': str(access),
                    'email': user.email,
                    'name': user.name
                }, status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VerifyAccountView(views.APIView):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser.objects.get(pk=uid)


        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"Message": "Successful verification"})
        else:
            return Response({"Message": "Invalid verification link"})
    

class ActiveUser(views.APIView):
    permission_classes = [AllowAny]
    def get(self, request, pk):
        user = CustomUser.objects.get(pk=pk)
        print(request.user)

        serializer = RegisterSerializer(user, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CreateNoteView(generics.CreateAPIView):
    serializer_class = NoteSerializer
    permission_classes=[IsAuthenticated]
    def create(self, request,):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            note = serializer.save()
            note.author = request.user
            note.save()
            return Response(
            {  
                "title": note.title,
                    "body": note.body,
                    "time": note.date
            }, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )
    
class NoteUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    lookup_field = 'id'


class ShowNoteView(views.APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):
        notes = Note.objects.filter(author=request.user).order_by('-date')
        serializer = NoteDisplaySerializer(notes, many=True)
        for note in serializer.data:
            datetime_string = note.get('date')  # Get the 'date' field
            if datetime_string:  # Ensure the date exists
                parsed_datetime = datetime.fromisoformat(datetime_string)
                note['date'] = parsed_datetime.strftime("%B %d, %Y, %I:%M %p")  # Format the date


        # print(formatted_datetime)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer
    permission_classes = [AllowAny]


class UserDetail(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'email': user.email,
            'name': user.name
        })
    

# class DeleteNote(views.APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, pk):
#         try:
#             note = Note.objects.get(pk=pk)
#             note.delete()
#             return Response({'message': 'Note succesffully deleted'})
#         except Note.DoesNotExist:
#             return Response({'message': 'Error occured'})

class DeleteNote(generics.GenericAPIView, DestroyModelMixin):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    queryset = Note.objects.all()

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)







from django.http import HttpResponse, Http404
import os

def serve_static_file(request, filename):
    file_path = os.path.join('/home/solomon/Desktop/diary_front', filename)
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return HttpResponse(file.read(), content_type='text/html')
    else:
        raise Http404("File not found")



class NoteDetail(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        note = Note.objects.get(pk=pk)
        serializer = NoteSerializer(note, many=False)
        return Response(serializer.data)
    


class UserUpdate(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    lookup_field = 'id'
    serializer_class = UserUpdateSerializer


class PasswordResetCustomView(generics.CreateAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # user = CustomUser.objects.get(email=serializer.validated_data['email'])
        serializer.save()
        return Response({"Message": "Success: Please check your mail to complete the password reset steps."})
    

class PasswordResetConfirmView(generics.CreateAPIView):
    def post(self, request, uidb64, token):
        uid = urlsafe_base64_decode(uidb64).decode()
        try:
            user = CustomUser.objects.get(pk=uid)
            print(user.email)
            if not default_token_generator.check_token(user, token):
                return Response({"message": "Invalid token"})
        
            new_password = request.data.get('new_password')
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password reset succcessful"}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"message": "User is non-existent"})
        
             

  

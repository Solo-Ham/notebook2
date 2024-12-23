from .views import RegisterView, ActiveUser, CreateNoteView, NoteUpdateView, ShowNoteView, CustomTokenObtainPairView, UserDetail, serve_static_file, DeleteNote
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from .views import NoteDetail 
from .views import UserUpdate, VerifyAccountView, PasswordResetConfirmView, PasswordResetCustomView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('reset-password/', PasswordResetCustomView.as_view(), name='reset-password'),
    path('active-user/<int:pk>/', ActiveUser.as_view(), name='active-user'),
    path('create-note/', CreateNoteView.as_view(), name="create-note"),
    path('update-note/<int:id>/', NoteUpdateView.as_view(), name="note-update"),
    path('show-notes/', ShowNoteView.as_view(), name='show-notes'),
    path('api/token/', TokenObtainPairView.as_view(), name='login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('current-user/', UserDetail.as_view(), name='current-user'),
    path('<str:filename>/', serve_static_file, name='serve_static_file'),
    path('note-detail/<int:pk>/', NoteDetail.as_view(), name='note-detail'),
    path('note-delete/<int:pk>/', DeleteNote.as_view(), name='delete-note'),
    path('user-update/<int:id>/', UserUpdate.as_view(), name='user-update'),
    path('verify/<uidb64>/<token>/', VerifyAccountView.as_view(), name='verify-user'),
    path('confirm-password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='confirm-password-reset')]
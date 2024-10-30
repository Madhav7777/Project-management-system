"""userprojectdetails URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from userprojectapp.views import UserCreationView, AuthenticateUserView, GetUserDetailsView,\
UpdateUserDetailsView, DeleteUserDetailsView, CreateProjectView, RetrieveAllProjectsView,\
RetrieveSpecificProjectsView, UpdateProjectDetailsView, DeteleProjectDetailsView,TaskCreationView, \
    UpdateTaskView, RetriveAllTasks, RetrieveSpecificTaskDetails, DeteleTaskDetailsView,CommentsCreationView, \
        UpdateCommentView, RetriveAllComments, RetrieveSpecificCommentDetails, DeteleCommentDetailsView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/register', UserCreationView.as_view(), name="register-user"),    
    path('api/users/login', AuthenticateUserView.as_view(), name="login-user"),
    path('api/get-user/<int:id>', GetUserDetailsView.as_view(), name="get-user-details"),
    path('api/update-user/<int:id>',UpdateUserDetailsView.as_view(), name="update-user-details"),
    path('api/delete-user/<int:id>',DeleteUserDetailsView.as_view(), name="delete-user-details"),
    path('api/create-project', CreateProjectView.as_view(), name="create-project"),
    path('api/retrieve-all-project-details',RetrieveAllProjectsView.as_view(), name="retrieve-all-project-details"),
    path('api/project-details/<int:id>',RetrieveSpecificProjectsView.as_view(), name="retrieve-specific-project-details"),
    path('api/update-project-details/<int:id>',UpdateProjectDetailsView.as_view(), name="update-project-details"),
    path('api/detele-project-details/<int:id>',DeteleProjectDetailsView.as_view(), name="detele-project-details"),
    path('api/create-task',TaskCreationView.as_view(), name="task-creation"),
    path('api/update-task/<int:id>',UpdateTaskView.as_view(), name="update-task"),
    path('api/retrieve-all-tasks',RetriveAllTasks.as_view(), name="retrieve-all-tasks"),
    path('api/retrieve-specifc-task-details/<int:id>',RetrieveSpecificTaskDetails.as_view(), name="retrieve-specifc-task-details"),
   path('api/delete-specifc-task-details/<int:id>',DeteleTaskDetailsView.as_view(), name="delete-specifc-task-details"),
   path('api/create-comment-details',CommentsCreationView.as_view(), name="create-comment-details"),
   path('api/update-comment/<int:id>',UpdateCommentView.as_view(), name="update-comment"),
   path("api/retrieve-all-comments",RetriveAllComments.as_view(), name="retrieve-all-comments"),
   path('api/retrieve-specific-comment/<int:id>',RetrieveSpecificCommentDetails.as_view(), name="retrieve-specific-comment"),
   path('api/delete-comment/<int:id>',DeteleCommentDetailsView.as_view(), name="delete-comment")
]
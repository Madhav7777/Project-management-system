from rest_framework.response import Response
from rest_framework.views import APIView
from userprojectapp.exceptions import UserException, ProjectException,TaskException, CommentException
from userprojectapp.serializer import UserSerializer, ProjectSerializer, TasksSerializer, CommentsSerializer
from userprojectapp.models import User,Projects,Tasks
from userprojectapp.manager import UserManager, ProjectManager, TaskManager, CommentManager
from rest_framework import status
class UserCreationView(APIView):
    
    @staticmethod
    def post(request):
        try:
            data = request.data
            manager = UserManager()
            manager.register_user(data)
            return Response({"result": "Success", "message": "User Successfully Created"},
                            status=status.HTTP_200_OK)
        except UserException as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ValueError as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class AuthenticateUserView(APIView):
    
    @staticmethod
    def post(request):
        try:
            data = request.data
            manager = UserManager()
            result = manager.authenticate_user(data)
            return Response({"message": "User Login Successfully","result": result,},
                            status=status.HTTP_200_OK)
        except UserException as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ValueError as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
class GetUserDetailsView(APIView):
    
    @staticmethod
    def get(request, **kwargs):
        try:
            user_id = kwargs.get('id')  
            manager = UserManager()
            result = manager.get_user_details(user_id)
            json_data = UserSerializer(result).data
            return Response({"result": json_data,},
                            status=status.HTTP_200_OK)
        except UserException as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            

class UpdateUserDetailsView(APIView):
    
    @staticmethod
    def put(request,**kwargs):
        try:
            user_id = kwargs.get('id')
            manager = UserManager()
            result = manager.get_user_details(user_id)
            manager.update_user(request.data, result)
            return Response({"result": "Success", "message":"User updated successfully"}, status=status.HTTP_200_OK)
        
        except UserException as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeleteUserDetailsView(APIView):
    
   @staticmethod 
   def delete(request , **kwargs):
        try:
            user_id = kwargs.get('id')
            manager = UserManager()
            user = manager.get_user_details(user_id)
            user.delete()  # Delete the user
            return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class CreateProjectView(APIView):
    
    @staticmethod
    def post(request):
        try:
            data = request.data
            manager = ProjectManager()
            manager.create_project(data)
            return Response({"result": "Success", "message": "Project Successfully Created"},
                            status=status.HTTP_200_OK)
        except UserException as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ProjectException as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ValueError as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
class RetrieveAllProjectsView(APIView):
    
    @staticmethod
    def get(request):
        try:
            manager = ProjectManager()
            project_details = manager.get_all_project_details()
            json_data = ProjectSerializer(project_details,many=True).data
            return Response({"result": json_data, "message": "Project Details Fetched Successfully"},
                            status=status.HTTP_200_OK)
        except ProjectException as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class RetrieveSpecificProjectsView(APIView):
    
    @staticmethod
    def get(request, **kwargs):
        try:
            project_id = kwargs.get('id')  
            manager = ProjectManager()
            result = manager.get_project_details(project_id)
            json_data = ProjectSerializer(result).data
            return Response({"result": json_data, "message": "Project Details Fetched Successfully"},
                            status=status.HTTP_200_OK)
        except ProjectException as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class UpdateProjectDetailsView(APIView):
    
    @staticmethod
    def put(request,**kwargs):
        try:
            project_id = kwargs.get('id')
            manager = ProjectManager()
            project_details = manager.get_project_details(project_id)
            manager.updating_project_data(request.data, project_details)
            return Response({"result":"Data updated successfully"}, status=status.HTTP_200_OK)
        except ProjectException as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class DeteleProjectDetailsView(APIView):
    
    @staticmethod 
    def delete(request , **kwargs):
        try:
            project_id = kwargs.get('id')
            manager = ProjectManager()
            user = manager.get_project_details(project_id)
            user.delete()  # Delete the Project
            return Response({"message": "Project deleted successfully"}, status=status.HTTP_200_OK)
        except Projects.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)   
        
class TaskCreationView(APIView):
    
    @staticmethod
    @staticmethod
    def post(request):
        try:
            data = request.data
            manager = TaskManager()
            manager.cretaing_task(data)
            return Response({"result": "Success", "message": "Task Successfully Created"},
                            status=status.HTTP_200_OK)
        except UserException as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ProjectException as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except TaskException as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ValueError as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UpdateTaskView(APIView):
    
    @staticmethod
    def put(request, **kwargs):
        try:
            task_id = kwargs.pop('id', None) 
            manager = TaskManager()
            task_details = manager.get_task_details(task_id)
            manager.updating_task_data(request.data, task_details)
            return Response({"result":"Data updated successfully"}, status=status.HTTP_200_OK)
        except UserException as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ProjectException as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except TaskException as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ValueError as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
               
class RetriveAllTasks(APIView):
    
    @staticmethod
    def get(request):
        try:
            manager = TaskManager()
            task_details = manager.get_all_task_details()
            json_data = TasksSerializer(task_details,many=True).data
            return Response({"result": json_data, "message": "Task Details Fetched Successfully"},
                            status=status.HTTP_200_OK)
        except TaskException as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class RetrieveSpecificTaskDetails(APIView):
    
    @staticmethod
    def get(request, **kwargs):
        try:
            task_id = kwargs.get('id')  
            manager = TaskManager()
            result = manager.get_task_details(task_id)
            json_data = TasksSerializer(result).data
            return Response({"result": json_data, "message": "Task Details Fetched Successfully"},
                            status=status.HTTP_200_OK)
        except TaskException as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class DeteleTaskDetailsView(APIView):
    
    @staticmethod 
    def delete(request , **kwargs):
        try:
            task_id = kwargs.get('id')
            manager = TaskManager()
            task = manager.get_task_details(task_id)
            task.delete()  # Delete the Task
            return Response({"message": "Task deleted successfully"}, status=status.HTTP_200_OK)
        except Tasks.DoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND) 
            

    
    
class CommentsCreationView(APIView):
    
    
    @staticmethod
    def post(request):
        try:
            data = request.data
            manager = CommentManager()
            manager.creating_comments(data)
            return Response({"result": "Success", "message": "Comment Successfully Created"},
                            status=status.HTTP_200_OK)
        except UserException as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except CommentException as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except TaskException as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ValueError as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class UpdateCommentView(APIView):
    
    @staticmethod
    def put(request, **kwargs):
        try:
            comment_id = kwargs.pop('id', None) 
            manager = CommentManager()
            comment_details = manager.get_comment_details(comment_id)
            manager.update_comment(request.data, comment_details)
            return Response({"result":"Data updated successfully"}, status=status.HTTP_200_OK)
        except UserException as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except CommentException as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except TaskException as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ValueError as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            

class RetriveAllComments(APIView):
    
    @staticmethod
    def get(request):
        try:
            manager = CommentManager()
            comments_details = manager.get_all_comments()
            json_data = CommentsSerializer(comments_details,many=True).data
            return Response({"result": json_data, "message": "Comments Details Fetched Successfully"},
                            status=status.HTTP_200_OK)
        except CommentException as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class RetrieveSpecificCommentDetails(APIView):
    
    @staticmethod
    def get(request, **kwargs):
        try:
            comment_id = kwargs.get('id')  
            manager = CommentManager()
            result = manager.get_comment_details(comment_id)
            json_data = CommentsSerializer(result).data
            return Response({"result": json_data, "message": "Comments Details Fetched Successfully"},
                            status=status.HTTP_200_OK)
        except CommentException as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"result": "Failure", "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class DeteleCommentDetailsView(APIView):
    
    @staticmethod 
    def delete(request , **kwargs):
        try:
            comment_id = kwargs.get('id')
            manager = CommentManager()
            comment = manager.get_comment_details(comment_id)
            comment.delete()  # Delete the Task
            return Response({"message": "Comment deleted successfully"}, status=status.HTTP_200_OK)
        except Tasks.DoesNotExist:
            return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND) 
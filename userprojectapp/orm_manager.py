from userprojectapp.models import User,Projects,Tasks,Comments
from userprojectapp.exceptions import UserException, TaskException, ProjectException, CommentException
class UserOrmManager:
    
    @staticmethod
    def check_user_exists_with_same_name(user_name):
        user_name = user_name.strip().lower()
        return User.objects.filter(user_name = user_name).exists() 
    
    @staticmethod
    def check_user_exists_with_same_email(user_email):
        return User.objects.filter(email_id = user_email).exists() 
    
    @staticmethod
    def get_latest_user_id():
        return User.objects.order_by('-user_id').first()
    
    @staticmethod
    def check_email_and_password_matches(user_email,password):
        try:
            return User.objects.get(email_id = user_email,password = password)
        except User.DoesNotExist:
            raise UserException("Email and password do not match")
        
       
    @staticmethod
    def get_user_by_user_id(user_id):
        try:
            return User.objects.get(user_id = user_id)
        except User.DoesNotExist:
            raise UserException("user does not exist with this user id")
        
    @staticmethod
    def get_latest_project_id():
        return Projects.objects.order_by('-project_id').first()
    
    @staticmethod
    def get_user_by_user_name(user_name):
        try:
            return User.objects.get(user_name = user_name.strip().lower())
        except User.DoesNotExist:
            raise UserException("user does not exist with this user name")
        
    @staticmethod
    def get_user_all_projects_names(user_id):
        return Projects.objects.filter(project_owner_id = user_id).values_list('project_name',flat=True)
    
    @staticmethod
    def get_all_project_details():
        return Projects.objects.all()
    
    @staticmethod
    def get_project_by_project_id(project_id):
        try:
            return Projects.objects.get(project_id = project_id)
        except Projects.DoesNotExist:
            raise ProjectException("project does not exist with this project id")
    
    @staticmethod
    def check_task_exist_with_same_name_same_project(title,project):
         if Tasks.objects.filter(title=title, project=project).exists():
            raise TaskException("A task with this title already exists in the specified project.")
        
    @staticmethod
    def get_latest_task_id():
        return Tasks.objects.order_by('-task_id').first()
    
    @staticmethod
    def get_task_by_task_id(task_id):
        try:
            return Tasks.objects.get(task_id = task_id)
        except Tasks.DoesNotExist:
            raise TaskException("task does not exist with this task id")
        
    @staticmethod
    def check_task_exist_with_same_name_same_project_excluding_id(title,project,task_id):
         if Tasks.objects.filter(title=title, project=project).exclude(task_id=task_id).exists():
            raise TaskException("A task with this title already exists in the specified project.")
        
    @staticmethod
    def get_all_task_details():
        return  Tasks.objects.all()
    
    @staticmethod
    def get_latest_comment_id():
        return Comments.objects.order_by('-comment_id').first()
    
    
    @staticmethod
    def get_comment_by_comment_id(comment_id):
        try:
            return Comments.objects.get(comment_id = comment_id)
        except Comments.DoesNotExist:
            raise CommentException("comment does not exist with this comment id")
    
    @staticmethod
    def get_all_comments_details():
        return  Comments.objects.all()
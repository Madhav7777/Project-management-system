
from userprojectapp.exceptions import UserException,ProjectException,TaskException, CommentException
from userprojectapp.orm_manager import UserOrmManager
from userprojectapp.constant import ErrorMessages
from userprojectapp.models import User,Projects, Tasks, Comments
from datetime import datetime
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from userprojectapp.constant import TaskConstans,UserConstants
import re
class UserManager:
    @staticmethod
    def register_user(user_data):
        user_name = user_data.get('user_name')
        user_email = user_data.get('user_email')
        password = user_data.get('password')
        first_name = user_data.get('first_name')
        last_name = user_data.get('last_name')
        date_of_joining = user_data.get('date_of_joining')
        required_fields = {
        'user_name' : user_data.get('user_name'),
        'user_email' : user_data.get('user_email'),
        'password': user_data.get('password'),
        'first_name': user_data.get('first_name'),
        'last_name': user_data.get('last_name'),
        'date_of_joining': user_data.get('date_of_joining')
        }
        missing_fields = [field for field, value in required_fields.items() if value is None or (isinstance(value, str) and value.strip() == '')]

        if len(missing_fields) > 0:
            raise ValueError(f"The following fields are required: {', '.join(missing_fields)}")
        if  isinstance(date_of_joining,str):
            date_format = "%Y-%m-%d"  # Format that matches the date string
            parsed_date = datetime.strptime(date_of_joining, date_format)
            current_time = timezone.now().time()
            date_of_joining = datetime.combine(parsed_date, current_time)
        if not re.match(UserConstants.email_regex,user_email):
            raise UserException("Invalid Email Id")
        if not re.match(UserConstants.password_regex,password):
            raise UserException("Invalid Password. Password must conatins atleast one lower case,one upper case,one special character and minimum of length of 8")
        orm_manager = UserOrmManager()
        check_for_user_exits_with_same_name = orm_manager.check_user_exists_with_same_name(user_name)
        check_for_user_exits_with_same_email = orm_manager.check_user_exists_with_same_email(user_email)
        latest_user = orm_manager.get_latest_user_id()
        user_id = (latest_user.user_id + 1) if latest_user else 1
        if check_for_user_exits_with_same_name:
            raise UserException(ErrorMessages.USER_NAME_EXISTS_EXCEPTION)
        if check_for_user_exits_with_same_email:
            raise UserException(ErrorMessages.USER_EMAIL_EXISTS_EXCEPTION)
        try:
            User.objects.create(user_id = user_id , user_name = user_name,email_id = user_email,
                                password =password,
                                first_name =first_name,
                                last_name = last_name,
                                date_of_joining = date_of_joining
                                )
            
        except Exception as err:
            raise UserException(err)
        
        
    @staticmethod
    def authenticate_user(user_data):
        user_email = user_data.get('user_email')
        password = user_data.get('password')
        if not user_email:
             raise ValueError("Email is required")
        if not password:
              raise ValueError("Password is required") 
        orm_manager = UserOrmManager()
        check_email_exists = orm_manager.check_user_exists_with_same_email(user_email)
        if not check_email_exists:
            raise ValueError("Email does not exists")
        check_pasword_and_email_matches = orm_manager.check_email_and_password_matches(user_email, password)
        if check_pasword_and_email_matches:
            refresh = RefreshToken.for_user(check_pasword_and_email_matches)
            return {
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }
        else:
            return {"error": "Invalid email or password"}
        
    @staticmethod
    def get_user_details(user_id):
        orm_manager = UserOrmManager()
        return orm_manager.get_user_by_user_id(user_id)
    
    @staticmethod
    def update_user(data,user_data):
        updated =False
        if not all(data.values()):
            raise ValueError("All fields in requested project details must contain data.")
        if 'user_id' in data.keys():
            raise ValueError("Primary key can't be changed.")
        email_id= data.get('email_id')
        password = data.get('password')
        user_name = data.get('user_name')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        date_of_joined = data.get('date_of_joining')
        orm_manager = UserOrmManager()
        if email_id and not re.match(UserConstants.email_regex,email_id):
            raise UserException("invalid Email id")
        if email_id and email_id!=user_data.email_id:
            if orm_manager.check_user_exists_with_same_email(email_id):
                raise UserException(ErrorMessages.USER_EMAIL_EXISTS_EXCEPTION)
            updated = True
        if password and not re.match(UserConstants.password_regex,password):
            raise UserException("Invalid Password. Password must conatins atleast one lower case,one upper case,one special character and minimum of length of 8")
        if password and password!=user_data.password:
            updated = True
        if user_name and user_name!=user_data.user_name:
            if orm_manager.check_user_exists_with_same_name(user_name):
                raise UserException(ErrorMessages.USER_NAME_EXISTS_EXCEPTION)
            updated = True
        if first_name and first_name!=user_data.first_name:
            updated = True
        if last_name and last_name!=user_data.last_name:
            updated = True
        if date_of_joined and  isinstance(date_of_joined,str):
            date_format = "%Y-%m-%d"  # Format that matches the date string
            parsed_date = datetime.strptime(date_of_joined, date_format)
            current_time = timezone.now().time()
            date_of_joined = datetime.combine(parsed_date, current_time)
        if updated:
            user_data.user_name = user_name if user_name else user_data.user_name
            user_data.email = email_id if email_id else user_data.email_id
            user_data.password = password if password else user_data.password
            user_data.first_name = first_name if first_name else user_data.first_name
            user_data.last_name = last_name if last_name else user_data.last_name
            user_data.date_of_joining = date_of_joined if date_of_joined else user_data.date_of_joining
            user_data.save()
        else:
            raise UserException("Given Data is same as existing data.Please change data and submit")
            
class ProjectManager:    
    @staticmethod
    def create_project(data):
        project_name = data.get('project_name')
        description = data.get('description')
        project_owner_id = data.get('project_owner_id')

        required_fields = {
        'project_name' : project_name,
        'description' : description,
        'project_owner_id': project_owner_id
        
        }
        missing_fields = [field for field, value in required_fields.items() if value is None or (isinstance(value, str) and value.strip() == '')]
        if len(missing_fields) > 0:
            raise ValueError(f"The following fields are required: {', '.join(missing_fields)}")
        orm_manager = UserOrmManager()
        latest_project = orm_manager.get_latest_project_id()
        project_id = (latest_project.project_id + 1) if latest_project else 1
        user_details = orm_manager.get_user_by_user_id(project_owner_id)
        user_related_all_projects = orm_manager.get_user_all_projects_names(user_details.user_id)
        if project_name in user_related_all_projects:
            raise ProjectException("User already linked to same project")
        try:
            Projects.objects.create(project_id = project_id ,description = description, project_name = project_name,project_owner = user_details
                                )
            
        except Exception as err:
            raise ProjectException(err)
     
    @staticmethod   
    def get_all_project_details():
        try:
            orm_manager = UserOrmManager()
            return orm_manager.get_all_project_details()
        except Exception as err:
            raise ProjectException(err)
        
    @staticmethod
    def get_project_details(project_id):
        orm_manager = UserOrmManager()
        return orm_manager.get_project_by_project_id(project_id)
    
    @staticmethod
    def updating_project_data(requested_project_details, project_details):
        updated =False
        if not all(requested_project_details.values()):
            raise ValueError("All fields in requested project details must contain data.")
        if 'project_id' in requested_project_details.keys():
            raise ValueError("Primary key can't be changed.")
        project_owner = requested_project_details.get('project_owner')
        orm_manager = UserOrmManager() 
        user_data = orm_manager.get_user_by_user_id(project_owner) if project_owner else None

        # Only update if user_data is retrieved and differs from the current project owner
        if user_data and user_data.user_id != project_details.project_owner.id:
            project_details.project_owner = user_data
            updated = True
        # Update description and project name only if they're provided and differ from current values
        requested_description = requested_project_details.get('description')
        requested_project_name = requested_project_details.get('project_name')

        if requested_description and requested_description != project_details.description:
            project_details.description = requested_description
            updated = True
        if requested_project_name and requested_project_name != project_details.project_name:
            project_details.project_name = requested_project_name
            updated = True
        
        if updated:
            project_details.save()
        else:
            raise ValueError("Given Data is same as existing data.Please change data and submit")

        
class TaskManager:
    
    @staticmethod
    def  cretaing_task(data):
        title = data.get('title')
        project = data.get('project')
        orm_manager = UserOrmManager()
        project_id = data.get('project')
        project = orm_manager.get_project_by_project_id(project_id)
        data['project'] = project
        orm_manager.check_task_exist_with_same_name_same_project(title, project.project_id)
        required_fields = {
            'title': data.get('title'),
            'description': data.get('description'),
            'status': data.get('status'),
            'priority': data.get('priority'),
            'project': data.get('project'),
            'due_date': data.get('due_date')
        }

        # Check for any missing fields
        missing_fields = [field for field, value in required_fields.items() if value is None or (isinstance(value, str) and value.strip() == '')]
        
        # Raise a ValidationError if any required fields are missing
        if missing_fields:
            raise TaskException(
                f"The following fields are required: {', '.join(missing_fields)}"
            )
         # Validate status
        if data.get('status') not in TaskConstans.STATUS_CHOICES:
            raise TaskException(
                {"status": f"Invalid status. Must be one of: {', '.join(TaskConstans.STATUS_CHOICES)}"}
            )

        # Validate priority
        if data.get('priority') not in TaskConstans.PRIORITY_CHOICES:
            raise TaskException(
                {"priority": f"Invalid priority. Must be one of: {', '.join(TaskConstans.PRIORITY_CHOICES)}"}
            )
        assigned_to = data.get('assigned_to')
        user_data = orm_manager.get_user_by_user_id(assigned_to) if assigned_to else None
        data['assigned_to']= user_data
        latest_task = orm_manager.get_latest_task_id()
        task_id = (latest_task.task_id + 1) if latest_task else 1
        due_date = data.get('due_date')
        if isinstance(due_date,str):
            date_format = "%Y-%m-%d"  # Format that matches the date string
            parsed_date = datetime.strptime(due_date, date_format)
            current_time = timezone.now().time()
            due_date = datetime.combine(parsed_date, current_time)
        try:
            Tasks.objects.create(task_id = task_id ,
                                title = title,
                                description = data.get('description'),
                                status = data.get('status'),
                                priority = data.get('priority'),
                                assigned_to = data.get('assigned_to'),
                                project = data.get('project'),
                                due_date= due_date
                                )
            
        except Exception as err:
            raise ProjectException(err)
        
    @staticmethod
    def get_task_details(task_id):
        orm_manager = UserOrmManager()
        return orm_manager.get_task_by_task_id(task_id)
    
    @staticmethod
    def updating_task_data(requested_task_details, task_details):
        updated =False
        if not all(requested_task_details.values()):
            raise ValueError("All fields in requested Task details must contain data.")
        if 'task_id' in requested_task_details.keys():
            raise ValueError("Primary key can't be changed.")
        project_id = requested_task_details.get('project')
        user_id = requested_task_details.get('user')
        orm_manager = UserOrmManager() 
        project_data = orm_manager.get_project_by_project_id(project_id) if project_id else None
        title = requested_task_details.get('title') if requested_task_details.get('title') else task_details.title
        project_id = project_id if project_id else task_details.project_id
        orm_manager.check_task_exist_with_same_name_same_project_excluding_id(title,project_id,task_details.task_id)
            
        # Only update if project_data is retrieved and differs from the current project
        if project_data and project_data.project_id != task_details.project_id:
            task_details.project = project_data
            updated = True
        user_data = orm_manager.get_user_by_user_id(user_id) if user_id else None

        # Only update if user_data is retrieved and differs from the current project owner
        if user_data and user_data.user_id != task_details.assigned_to_id:
            task_details.assigned_to = user_data
            updated = True
        
        if 'status' in requested_task_details and requested_task_details['status'] not in TaskConstans.STATUS_CHOICES:
            raise ValueError(
                {"status": f"Invalid status. Must be one of: {', '.join(TaskConstans.STATUS_CHOICES)}"}
            )

        # Validate priority if provided
        if 'priority' in requested_task_details and requested_task_details['priority'] not in TaskConstans.PRIORITY_CHOICES:
            raise ValueError(
                {"priority": f"Invalid priority. Must be one of: {', '.join(TaskConstans.PRIORITY_CHOICES)}"}
            )

        fields_to_check = ['title', 'description', 'status', 'priority']

        if requested_task_details.get('due_date') and isinstance(requested_task_details['due_date'],str):
            date_obj = datetime.strptime(requested_task_details.get('due_date'), "%Y-%m-%d").date()
            date_only = task_details.due_date.date()
            if date_only != date_obj:
                updated = True
                
        # Track any changed fields
        for field in fields_to_check:
            if field in requested_task_details and requested_task_details[field] != getattr(task_details, field):
                updated = True

        
        if updated:
            task_details.title = requested_task_details.get('title', task_details.title)
            task_details.description = requested_task_details.get('description', task_details.description)
            task_details.status = requested_task_details.get('status', task_details.status)
            task_details.priority = requested_task_details.get('priority', task_details.priority)
            task_details.due_date = requested_task_details.get('due_date', task_details.due_date)
            task_details.save()
        else:
            raise ValueError("Given Data is same as existing data.Please change data and submit")
        
    @staticmethod
    def get_all_task_details():
        try:
            orm_manager = UserOrmManager()
            return orm_manager.get_all_task_details()
        except Exception as err:
            raise TaskException(err)
        
class CommentManager:
    
    @staticmethod
    def creating_comments(data):
        orm_manager = UserOrmManager()
        task_id = data.get('task')
        task = orm_manager.get_task_by_task_id(task_id)
        data['task'] = task
        user_id = data.get('user')
        user_data = orm_manager.get_user_by_user_id(user_id) 
        data['user']= user_data
        required_fields = {
            'content': data.get('content'),
            'user': data.get('user'),
            'task': data.get('task'),
        }

        # Check for any missing fields
        missing_fields = [field for field, value in required_fields.items() if value is None or (isinstance(value, str) and value.strip() == '')]
        
        # Raise a ValidationError if any required fields are missing
        if missing_fields:
            raise TaskException(
                f"The following fields are required: {', '.join(missing_fields)}"
            )
        latest_comment = orm_manager.get_latest_comment_id()
        comment_id = (latest_comment.comment_id + 1) if latest_comment else 1
        try:
            Comments.objects.create(comment_id = comment_id ,
                                content = data.get('content'),
                                user = data.get('user'),
                                task = data.get('task'),
                                )
            
        except Exception as err:
            raise CommentException(err)

    @staticmethod   
    def update_comment(requested_task_details,comment_details):
        updated =False
        if not all(requested_task_details.values()):
            raise ValueError("All fields in requested Task details must contain data.")
        if 'comment_id' in requested_task_details.keys():
            raise ValueError("Primary key can't be changed.")
        task_id = requested_task_details.get('task')
        user_id = requested_task_details.get('user')
        orm_manager = UserOrmManager() 
        task_data = orm_manager.get_task_by_task_id(task_id) if task_id else None
        user_data = orm_manager.get_user_by_user_id(user_id) if user_id else None
            
        if task_data and task_data.task_id != comment_details.task_id:
            comment_details.task = task_data
            updated = True

        if user_data and user_data.user_id != comment_details.user_id:
            comment_details.user = user_data
            updated = True
        
        if  requested_task_details.get('content') and  requested_task_details.get('content')!=comment_details.content:
            updated = True

        
        if updated:
            
            comment_details.content = requested_task_details.get('content', comment_details.content)
            comment_details.save()
            
        else:
            raise ValueError("Given Data is same as existing data.Please change data and submit")
        
    @staticmethod
    def get_comment_details(comment_id):
        orm_manager = UserOrmManager()
        return orm_manager.get_comment_by_comment_id(comment_id)
        
    @staticmethod
    def get_all_comments():
        try:
            orm_manager = UserOrmManager()
            return orm_manager.get_all_comments_details()
        except Exception as err:
            raise CommentException(err)
    

         
            
            
         
            
        
        
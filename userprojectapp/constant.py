
class ErrorMessages:
    USER_NAME_EXISTS_EXCEPTION = "User Already Exists With Same Name"
    USER_EMAIL_EXISTS_EXCEPTION = "User Already Exists With Same Email"
    
class UserConstants:
    email_regex = r"^[a-zA-Z][a-zA-Z0-9._%+-]*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    password_regex =  r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"

    
class TaskConstans:
    STATUS_CHOICES = ['To Do', 'In Progress', 'Done']
    PRIORITY_CHOICES = ['Low', 'Medium', 'High']

class CoreException(Exception):

    def __init__(self, message, log_message=None):
        """

        @type log_message: object: Detailed error message to log in console or log file
        """
        super().__init__(message, log_message)
        self.message = message
        self.error_log = log_message

    def __str__(self):
        return str(self.message)

    def get_error_log(self):
        return self.error_log
    
class UserException(CoreException):

    def __init__(self, message):
        super().__init__(message)
    
  
class ProjectException(CoreException):

    def __init__(self, message):
        super().__init__(message)      
        
class TaskException(CoreException):
    
    def __init__(self,message):
        super().__init__(message)
        
class CommentException(CoreException):
    
    def __init__(self,message):
        super().__init__(message)
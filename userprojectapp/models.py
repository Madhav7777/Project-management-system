from django.db import models
from django.db.models import DO_NOTHING
from datetime import datetime
from django.db import models
from django.utils import timezone


class User(models.Model):
    user_id = models.IntegerField(db_column="user_id", primary_key=True)
    user_name = models.CharField(db_column="user_name", unique=True,max_length=256)
    email_id = models.CharField( db_column="email_id", unique=True,max_length=256)
    password = models.CharField( db_column="password",max_length=256)
    first_name = models.CharField( db_column="first_name",max_length=256)
    last_name = models.CharField( db_column="last_name",max_length=256)
    date_of_joining = models.DateTimeField( db_column="date_of_joining")
    
    

    class Meta:
        managed = True
        db_table = "user"
        
class Projects(models.Model):
    project_id =models.IntegerField( db_column="project_id",primary_key=True )
    project_name = models.CharField( db_column="project_name",max_length=256)
    description = models.TextField( db_column="description")
    project_owner = models.ForeignKey( "User", db_column="project_user",
        related_name="user_project",
        on_delete=models.CASCADE)
    created_at =models.DateTimeField(db_column="created_at", default=timezone.now)
    
    class Meta:
        managed = True
        db_table = "projects"
        
class ProjectMembers(models.Model):
    project_member_id =models.IntegerField( db_column="project_member_id",primary_key=True )
    project = models.ForeignKey("Projects",db_column="project",
        related_name="project_details", on_delete=models.CASCADE)
    user = models.ForeignKey("User",db_column="user",related_name="user_details", on_delete=models.CASCADE)
    role = models.CharField(max_length=64,db_column="role")
    
    class Meta:
        managed = True
        db_table = "project_members"
        

class Tasks(models.Model):
    STATUS_CHOICES = [
        ('To Do', 'To Do'),
        ('In Progress', 'In Progress'),
        ('Done', 'Done'),
    ]
    
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    task_id = models.IntegerField( db_column="task_id",primary_key=True)
    title = models.CharField(db_column='title',max_length=256)
    description = models.TextField( db_column="description")
    status = models.CharField(db_column="status",max_length=64, choices=STATUS_CHOICES)
    priority = models.CharField(db_column="priority",max_length=64,choices=PRIORITY_CHOICES )
    assigned_to = models.ForeignKey("User",db_column="assigned_to",related_name="user_task",null=True,blank=True,
                                    on_delete=models.CASCADE)
    project = models.ForeignKey("Projects",db_column="project",
        related_name="project_tasks", on_delete=models.CASCADE)
    created_at =models.DateTimeField(db_column="created_at",default=timezone.now)
    due_date =models.DateTimeField(db_column="due_date")
    
    class Meta:
        managed = True
        db_table = "tasks"
       

class Comments(models.Model):
    comment_id = models.IntegerField(db_column="comment_id", primary_key=True)
    content = models.TextField(db_column="content")
    user = models.ForeignKey("User",db_column="assigned_to",related_name="user_comment",null=True,blank=True,
                                    on_delete=models.CASCADE)
    task = models.ForeignKey("Tasks",db_column="task",
        related_name="task_comment", on_delete=models.CASCADE)
    created_at =models.DateTimeField(db_column="created_at",default=timezone.now)

    class Meta:
        managed = True
        db_table = "comments"


    
    
    
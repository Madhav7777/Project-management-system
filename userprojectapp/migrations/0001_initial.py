# Generated by Django 4.0.6 on 2024-10-27 09:26

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('project_id', models.IntegerField(db_column='project_id', primary_key=True, serialize=False)),
                ('project_name', models.CharField(db_column='project_name', max_length=256)),
                ('description', models.TextField(db_column='description')),
                ('created_at', models.DateTimeField(db_column='created_at', default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'projects',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.IntegerField(db_column='user_id', primary_key=True, serialize=False)),
                ('user_name', models.CharField(db_column='user_name', max_length=256, unique=True)),
                ('email_id', models.CharField(db_column='email_id', max_length=256, unique=True)),
                ('password', models.CharField(db_column='password', max_length=256)),
                ('first_name', models.CharField(db_column='first_name', max_length=256)),
                ('last_name', models.CharField(db_column='last_name', max_length=256)),
                ('date_of_joining', models.DateTimeField(db_column='date_of_joining')),
            ],
            options={
                'db_table': 'user',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('task_id', models.IntegerField(db_column='task_id', primary_key=True, serialize=False)),
                ('title', models.CharField(db_column='title', max_length=256)),
                ('description', models.TextField(db_column='description')),
                ('status', models.CharField(db_column='status', max_length=64)),
                ('priority', models.CharField(db_column='priority', max_length=64)),
                ('created_at', models.DateTimeField(db_column='created_at', default=django.utils.timezone.now)),
                ('due_date', models.DateTimeField(db_column='due_date')),
                ('Assigned_to', models.ForeignKey(blank=True, db_column='assigned_to', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_task', to='userprojectapp.user')),
                ('project', models.ForeignKey(db_column='project', on_delete=django.db.models.deletion.DO_NOTHING, related_name='project_tasks', to='userprojectapp.projects')),
            ],
            options={
                'db_table': 'tasks',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='projects',
            name='project_owner',
            field=models.ForeignKey(db_column='project_user', on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_project', to='userprojectapp.user'),
        ),
        migrations.CreateModel(
            name='ProjectMembers',
            fields=[
                ('project_member_id', models.IntegerField(db_column='project_member_id', primary_key=True, serialize=False)),
                ('role', models.CharField(db_column='role', max_length=64)),
                ('project', models.ForeignKey(db_column='project', on_delete=django.db.models.deletion.DO_NOTHING, related_name='project_details', to='userprojectapp.projects')),
                ('user', models.ForeignKey(db_column='user', on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_details', to='userprojectapp.user')),
            ],
            options={
                'db_table': 'project_members',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('comment_id', models.IntegerField(db_column='comment_id', primary_key=True, serialize=False)),
                ('content', models.TextField(db_column='content')),
                ('created_at', models.DateTimeField(db_column='created_at', default=django.utils.timezone.now)),
                ('task', models.ForeignKey(db_column='task', on_delete=django.db.models.deletion.DO_NOTHING, related_name='task_comment', to='userprojectapp.tasks')),
                ('user', models.ForeignKey(blank=True, db_column='assigned_to', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_comment', to='userprojectapp.user')),
            ],
            options={
                'db_table': 'comments',
                'managed': True,
            },
        ),
    ]

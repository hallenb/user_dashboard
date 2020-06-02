from django.db import models
import re

class UserManager(models.Manager):
    def user_validator(self, data):
        errors = {}

        if len(data['fname']) < 2:
            errors['fname'] = "First name must be at least two characters"
        if len(data['lname']) < 2:
            errors['lname'] = "Last name must be at least two characters"
        if len(data['pw']) < 8:
            errors['pw'] = "Password must be at least eight characters"
        if data['pw'] != data['confpw']:
            errors['confpw'] = "Password did not match Confirm Password"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(data['email']):
            errors['email'] = "Invalid email address!"
        return errors

    def info_validator(self, data):
        errors = {}

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(data['email']):
            errors['email'] = "Invalid email address!"
        if len(data['fname']) < 2:
            errors['fname'] = "First name must be at least two characters"
        if len(data['lname']) < 2:
            errors['lname'] = "Last name must be at least two characters"
        return errors

    def pass_validator(self, data):
        errors = {}

        if len(data['pw']) < 8:
            errors['pw'] = "Password must be at least eight characters"
        if data['pw'] != data['confpw']:
            errors['confpw'] = "Password did not match Confirm Password"
        return errors



class UserLevels(models.Model):
    level = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class Users(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length = 50)
    email = models.CharField(max_length = 250)
    password = models.CharField(max_length = 255)
    description = models.TextField(blank=True)
    user_level = models.ForeignKey(UserLevels, related_name="userlevel", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Messages(models.Model):
    message = models.TextField()
    message_to = models.ForeignKey(Users, related_name="owner", on_delete=models.CASCADE)
    creator = models.ForeignKey(Users, related_name="author", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comments(models.Model):
    comment = models.TextField()
    creator = models.ForeignKey(Users, related_name="user", on_delete=models.CASCADE)
    message = models.ForeignKey(Messages, related_name="comment", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


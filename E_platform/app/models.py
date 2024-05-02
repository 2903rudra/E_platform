from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.

class CustomeUser(AbstractUser):
    email = models.EmailField(unique=True)
    user_type_choices = ((1,'ADMIN'),
                 (2,'STUDENT'),
                 (3,'COURSE PROVIDER'))
    user_type = models.IntegerField(choices=user_type_choices,default=1)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
class Admin(models.Model):
    user = models.OneToOneField(CustomeUser,on_delete=models.CASCADE)
    Full_Name = models.CharField(max_length=20)
    Mobile_no = models.CharField(max_length=10)
    EmailID = models.EmailField(max_length=255)
    DOB = models.DateField(null =True,blank=True)
    Gender_choices = (
        ('M','Male'),
        ('F','Female'),
        ('O','Others')
    )
    Gender = models.CharField(max_length=10,choices=Gender_choices,default='M')

    def __str__(self) -> str:
        return self.Full_Name


class Course(models.Model):
    course_name = models.CharField(max_length= 255, verbose_name='Course Name')
    CATEGORY_CHOICES = [
        ('c1','Tech Courses'),
        ('c2','Grade 9'),
        ('c3','Grade 10'),
        ('c4','Grade 11'),
        ('c5','Grade 12'),
    ]
    category_type = models.CharField(max_length=20,choices=CATEGORY_CHOICES,default='c1')
    created_at = models.DateTimeField(auto_now_add=True , verbose_name= 'Created At')
    updated_at = models.DateTimeField(auto_now = True, verbose_name= 'Updated At')

    def __str__(self) -> str:
        return self.course_name
    
class Assignment(models.Model):
    title = models.CharField(max_length=100 ,verbose_name='Assignment Title')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Course')
    description = models.TextField(verbose_name='Description')
    due_date = models.DateTimeField(verbose_name='Due Date')
    

class StudentAssignment(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(CustomeUser, on_delete=models.CASCADE)
    submission = models.FileField(upload_to='assignment_submissions/')
    marked = models.BooleanField(default=False)

class AssignmentFeedback(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(CustomeUser, on_delete=models.CASCADE)
    feedback = models.TextField()
    marks = models.FloatField()

class Quiz(models.Model):
    title = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self) -> str:
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=255)
    # Add other fields for question details

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    # Add other fields for choice details

    def __str__(self):
        return self.choice_text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomeUser, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f"Answer for Question: {self.question.question_text} by {self.user.username}"


class Quiz_Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    student = models.ForeignKey(CustomeUser, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.quiz.title} - {self.student.username} Result"

class Voucher(models.Model):
    code = models.CharField(max_length=100, unique=True, help_text="Unique code for the voucher")
    discount = models.DecimalField(max_digits=5, decimal_places=2, help_text="Discount percentage or amount")
    expiration_date = models.DateField(help_text="Expiration date of the voucher")
    
    # Use settings.AUTH_USER_MODEL to reference the custom user model
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vouchers', help_text="User who created the voucher")
    
    created_at = models.DateTimeField(auto_now_add=True, help_text="Creation timestamp")
    updated_at = models.DateTimeField(auto_now=True, help_text="Last updated timestamp")

    def __str__(self):
        return f"{self.code} - {self.discount}% off"

    class Meta:
        ordering = ['-created_at']  
        verbose_name = "Voucher"
        verbose_name_plural = "Vouchers"
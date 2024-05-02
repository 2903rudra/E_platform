from django import forms
from .models import *
from django.utils import timezone


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=255, widget=forms.TextInput(
        attrs={'placeholder': 'Email'}))
    password = forms.CharField(max_length=255, widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}))

class UserForm(forms.ModelForm):
    class Meta:
        models = CustomeUser
        fields = ['username', 'email', 'password', 'user_type']  # Add or remove fields as needed

        labels = {
            'username': 'Username',
            'email': 'Email',
            'password': 'Password',
            'user_type': 'User Type',
        }
        widgets = {
            'password': forms.PasswordInput(),
        }

class AdminForm(forms.ModelForm):
    password1 = forms.CharField(max_length=255, widget=forms.PasswordInput(
        attrs={'placeholder': 'Create Password'}))
    password2 = forms.CharField(max_length=255, widget=forms.PasswordInput(
        attrs={'placeholder': 'Re-enter Password'}))
    DOB = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date'}))  # Ensure proper widget for DOB FIELD

    class Meta:
        model = Admin
        fields = ['Full_Name', 'Mobile_no', 'EmailID',
                  'DOB', 'Gender', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2


class CourseForm(forms.ModelForm):
    # Define custom fields or override existing fields here
    # category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Category')

    class Meta:
        model = Course
        fields = '__all__'


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'course']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'


OptionFormSet = forms.inlineformset_factory(
    Question,  # Parent model
    Choice,   # Child model
    fields=['choice_text', 'is_correct'],  # Add other fields as needed
    extra=0,  # Number of extra forms to display
    can_delete=True,  # Allow deletion of existing options
    min_num=4,  # Minimum number of forms required
    validate_min=True,  # Validate minimum forms
)

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['choice']
        widgets = {
            'choice': forms.RadioSelect,  # Assuming single choice for each question
        }
class OptionForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = "__all__"


class AssignmentForm(forms.ModelForm):
    due_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date']

    def clean_due_date(self):
        due_date = self.cleaned_data['due_date']
        if due_date < timezone.now():
            raise forms.ValidationError("Due date must be in the future.")
        return due_date


class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = StudentAssignment
        fields = ['student', 'assignment', 'submission']

    def clean_submission(self):
        submission = self.cleaned_data['submission']
        if submission.size > 1024 * 1024 * 10:
            raise forms.ValidationError("File size must be less than 10MB.")
        return submission


class AssignmentFeedbackForm(forms.ModelForm):
    class Meta:
        model = AssignmentFeedback
        fields = ['feedback']

class QuizResultForm(forms.ModelForm):
    class Meta:
        model = Quiz_Result
        fields = ['student', 'quiz', 'score']

    def clean_score(self):
        score = self.cleaned_data['score']
        if score < 0 or score > 100:
            raise forms.ValidationError("Score must be between 0 and 100.")
        return score


class FeedbackForm(forms.Form):
    feedback = forms.CharField(widget=forms.Textarea)
    marks = forms.FloatField()


class VoucherForm(forms.ModelForm):
    class Meta:
        model = Voucher

        fields = ['code', 'discount', 'expiration_date']
        
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter voucher code'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter discount'}),
            'expiration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

        labels = {
            'code': 'Voucher Code',
            'discount': 'Discount',
            'expiration_date': 'Expiration Date',
        }
        
        help_texts = {
            'code': 'Unique code for the voucher.',
            'discount': 'Discount percentage or amount.',
            'expiration_date': 'Expiration date of the voucher.',
        }
    
    def clean(self):
        cleaned_data = super().clean()

        code = cleaned_data.get('code')
        if Voucher.objects.filter(code=code).exists():
            self.add_error('code', 'A voucher with this code already exists.')

        return cleaned_data
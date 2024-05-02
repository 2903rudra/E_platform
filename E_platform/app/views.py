from django.shortcuts import render, redirect, HttpResponse,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import *
import random
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

# ---------------------------------------------------------------------------
# Login view
# ---------------------------------------------------------------------------
def do_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():

            email = request.POST.get('email')
            password = request.POST.get('password')

            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                user_type = user.user_type
                if user_type == 1:  # Assuming user_type is an integer field
                    return redirect('super-panel')
                elif user_type == 2:
                    return HttpResponse('student')
                elif user_type == 3:
                    return HttpResponse('course provider')
                else:
                    messages.error(request, "Invalid Login!")
            else:
                messages.error(request, "Invalid Login!")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def generate_otp():
    return random.randint(100000, 999999)
    
def send_otp(email, otp):
    send_mail(
        'Email Verification OTP',
        f'Your OTP is: {otp}',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )

def admin_signup(request):
    if request.method == 'POST':
        form = AdminForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['EmailID']

            # Check if the email already exists
            if get_user_model().objects.filter(email=user_email).exists():
                messages.error(request, 'This email is already in use.')
                return redirect('admin-signup')  # Redirect back to the signup page
            
            # Create a new user instance
            user = get_user_model().objects.create_user(
                email=user_email,
                password=form.cleaned_data['password1'],
                username=user_email,  # You can set username as email if you want
                user_type=1  # Assuming 1 represents the admin user type
            )
            # Generate a random OTP and send it to the user's email
            otp = generate_otp()

            # Send the OTP to the user's email
            send_otp(user_email, otp)

            # Save the OTP in the session
            request.session['otp'] = otp
            request.session['email'] = user_email
            
            
            return redirect('verify_otp')
    else:
        form = AdminForm()

    return render(request, 'admin_signup.html', {'form': form})

def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')
        if entered_otp == str(stored_otp):
            # OTP verification successful
            email = request.session.get('email')
            Full_Name = request.POST.get('Full_Name')
            
            # Create an admin profile
            user = get_user_model().objects.get(email=email)
            admin_profile = Admin.objects.create(user=user, Full_Name=user.email)  # Customize this as per your Admin model

            # Redirect to a success page
            return redirect('super-panel')

    # OTP verification failed or GET request
    return render(request, 'verify_otp.html')

def feedback_page(request):
    return render(request, 'feedback.html')


# ------------------------------------------------------------------------------
# Course Views
# ------------------------------------------------------------------------------


def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course_list')  # Redirect to the list of courses
    else:
        form = CourseForm()
    return render(request, 'create_course.html', {'form': form})

def edit_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_list')  # Redirect to the list of courses
    else:
        form = CourseForm(instance=course)
    return render(request, 'edit_course.html', {'form': form, 'course': course})

def view_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'course_detail.html', {'course': course})

def course_list(request):
    courses = Course.objects.all()
    category_filter = request.GET.get('category')
    if category_filter:
        courses = courses.filter(category_type=category_filter)
    return render(request, 'course_list.html', {'courses': courses})

def Delete_course(request, course_id):
    course = get_object_or_404(Course,pk= course_id)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted successfully.')
        return redirect('course_list')
    return render(request, 'delete_course.html', {'cours': course})


def Super_panel(request):
    return render(request,'Super_panel.html')

def content_management(request):
    return render(request,'content_management.html')

def User_Management(request):
    return render(request,'user_management.html')

def create_assignment(request, course_id):
    # Get the course object based on the provided course_id
    course = get_object_or_404(Course, pk=course_id)
    
    if request.method == 'POST':
        # If the request method is POST, process the form data
        form = AssignmentForm(request.POST)
        if form.is_valid():
            # If the form data is valid, save the assignment associated with the course
            assignment = form.save(commit=False)
            assignment.course = course
            assignment.save()
            # Redirect to the course detail page after successfully creating the assignment
            return redirect('view_course', course_id=course_id)
    else:
        # If the request method is GET, render the assignment creation form
        form = AssignmentForm()
    
    # Render the create_assignment template with the form and course objects
    return render(request, 'create_assignment.html', {'form': form, 'course': course})

def edit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Assignment updated successfully.')
            return redirect('assignment_list')
    else:
        form = AssignmentForm(instance=assignment)
    return render(request, 'edit_assignment.html', {'form': form, 'assignment': assignment})

def assignment_list(request):
    assignments = Assignment.objects.all()
    return render(request, 'assignment_list.html', {'assignments': assignments})

def delete_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    if request.method == 'POST':
        assignment.delete()
        messages.success(request, 'Assignment deleted successfully.')
        return redirect('assignment_list')
    return render(request, 'delete_assignment.html', {'assignment': assignment})

def mark_assignment(request, assignment_id):
    assignment = get_object_or_404(StudentAssignment, pk=assignment_id)
    if request.method == 'POST':
        form = AssignmentSubmissionForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            # Redirect or display success message
    else:
        form = AssignmentSubmissionForm(instance=assignment)
    return render(request, 'mark_assignment.html', {'form': form, 'assignment': assignment})

def view_submissions(request):
    submissions = StudentAssignment.objects.all()
    return render(request, 'view_submissions.html', {'submissions': submissions})


# --------------------------------------------------------------------------------
# Quiz view
# --------------------------------------------------------------------------------
from django.urls import reverse

def create_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save()
            # Redirect to add_question view with the newly created quiz_id
            return redirect(reverse('add-question', kwargs={'quiz_id': quiz.id}))
    else:
        form = QuizForm()
    return render(request, 'create_quiz.html', {'form': form})

def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = quiz.question_set.all()
    return render(request, 'quiz_detail.html', {'quiz': quiz, 'questions': questions})

def add_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        option_formset = OptionFormSet(request.POST)
        if question_form.is_valid() and option_formset.is_valid():
            question = question_form.save(commit=False)
            question.quiz = quiz
            question.save()
            option_formset.instance = question
            option_formset.save()
            return redirect('take-quiz', quiz_id=quiz_id)
    else:
        question_form = QuestionForm()
        option_formset = OptionFormSet()
    return render(request, 'add_question.html', {'quiz': quiz, 'question_form': question_form, 'option_formset': option_formset})


from django.contrib.auth.decorators import login_required
@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = quiz.question_set.all()
    
    if request.method == 'POST':
        # Process form submissions
        for question in questions:
            form = AnswerForm(request.POST, prefix=str(question.id), instance=Answer(question=question))
            if form.is_valid():
                # Set the user_id field before saving
                answer = form.save(commit=False)
                answer.user_id = request.user.id
                answer.save()

        # Redirect to the quiz results page or any other appropriate page
        # Redirect to the create_quiz_result view with the quiz_id parameter
        return redirect('create-quiz-result',quiz_id=quiz_id)
 
    else:
        # Render the quiz form with only the first four choices for each question
        formset = []
        for question in questions:
            choices = Choice.objects.filter(question=question)[:4]  # Limit choices to first four
            answer_form = AnswerForm(prefix=str(question.id), instance=Answer(question=question))
            answer_form.fields['choice'].queryset = choices  # Set queryset for choice field
            formset.append(answer_form)
        return render(request, 'take_quiz.html', {'quiz': quiz, 'formset': formset})
    
def create_quiz_result(request,quiz_id):
    if request.method == 'POST':
        form = QuizResultForm(request.POST)
        if form.is_valid():
            # Save the form with the quiz_id
            form.instance.quiz_id = quiz_id
            form.save()
            return redirect('quiz-results',quiz_id=quiz_id)  # Redirect to the quiz results page
    else:
        form = QuizResultForm()
    return render(request, 'create_quiz_result.html', {'form': form})
def quiz_list(request):
    quizzes = Quiz.objects.all()
    quiz_results = Quiz_Result.objects.filter(quiz__in=quizzes)
    return render(request, 'quiz_list.html', {'quizzes': quizzes, 'quiz_results': quiz_results})

def quiz_results(request, quiz_id):
    quiz_results = Quiz_Result.objects.filter(quiz=quiz_id)
    return render(request, 'quiz_results.html', {'quiz_results': quiz_results})
# View for submitting an assignment
def submit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    if request.method == 'POST':
        form = AssignmentSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = request.user
            submission.save()
            messages.success(request, 'Assignment submitted successfully.')
            return redirect('assignment_list')
    else:
        form = AssignmentSubmissionForm()
    return render(request, 'submit_assignment.html', {'form': form, 'assignment': assignment})

def view_assignment_feedback(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    feedback = assignment.feedback.all()
    return render(request, 'assignment_feedback.html', {'assignment': assignment, 'feedback': feedback})

def list_students(request):
    students = CustomeUser.objects.filter(user_type=2)  # Filter students
    return render(request, 'list_students.html', {'students': students})

def add_student(request):
    if request.method == 'POST':
        # If the form is submitted, process the form data
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_students')
    else:
        # If it's a GET request, render the form
        form = UserForm()
    
    return render(request, 'add_student.html', {'form': form})

def edit_student(request, student_id):
    # Retrieve the student object or return a 404 error if not found
    student = get_object_or_404(CustomeUser, pk=student_id)
    
    if request.method == 'POST':
        # If the form is submitted, process the form data
        form = UserForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('list_students')
    else:
        # If it's a GET request, render the form with the student's current data
        form = UserForm(instance=student)
    
    return render(request, 'edit_student.html', {'form': form, 'student': student})

def suspend_student(request, student_id):
    # Fetch the student object and suspend the account
    student = CustomeUser.objects.get(pk=student_id)
    student.is_active = False
    student.save()
    return redirect('list_students')

def change_course(request, student_id):
    # Fetch the student object
    student = CustomeUser.objects.get(pk=student_id)
    if request.method == 'POST':
        # Process form data to change the course association
        # Update student.course or relevant field in CustomUser model
        return redirect('list_students')  # Redirect to list of students after course change
    else:
        # Render form for selecting desired course
        return render(request, 'change_course.html', {'student': student, 'courses': courses})
    


    # ---------------------------------------------------------------------------------------
# Marketing and Promotions View
# ---------------------------------------------------------------------------------------

def marketing_promotions(request):
    # Your logic for the Marketing and Promotions page goes here
    return render(request, 'marketing_promotions.html')

def track_clicks(request):
    # Your logic for the Marketing and Promotions page goes here
    return render(request, 'track_clicks.html')

def course_data(request):
    # Your logic for the Marketing and Promotions page goes here
    return render(request, 'course_data.html')

def referral_program(request):
    # Your logic for the Marketing and Promotions page goes here
    return render(request, 'referral_program.html')


# ---------------------------------------------------------------------------------------
# Offers View
# ---------------------------------------------------------------------------------------

def offers_view(request):
    return render(request, 'offers.html')

def create_voucher_view(request):
    if request.method == 'POST':
        form = VoucherForm(request.POST)
        
        if form.is_valid():
            form.save()
            
            return redirect('vouchers_list')
        else:
            return render(request, 'create_voucher.html', {'form': form})
    
    else:
        form = VoucherForm()
        
        return render(request, 'create_voucher.html', {'form': form})

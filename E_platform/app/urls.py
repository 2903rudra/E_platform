from django.urls import path
from.views import *
urlpatterns = [
    path('',do_login,name='login'),
    path('admin-signup/',admin_signup,name='admin-signup'),
    path('verify-otp',verify_otp,name='verify_otp'),
    path('feedback/', feedback_page, name='feedback_page'),
    path('offers/', offers_view, name='offers_page'),
    path('create-vouchers/', create_voucher_view, name='create_voucher'),

    # Course URLs
    path('course/', course_list, name='course_list'),
    path('course/<int:course_id>/',view_course, name='view_course'),
    path('course/create/', create_course, name='create_course'),
    path('course/<int:course_id>/edit/',edit_course, name='edit_course'),
    path('course/<int:course_id>/delete/', Delete_course, name='delete_course'),

    # Assignment URLs
    path('assignment/<int:course_id>/create/', create_assignment, name='create_assignment'),
    path('assignment/<int:assignment_id>/edit/', edit_assignment, name='edit_assignment'),
    path('assignment/<int:assignment_id>/delete/', delete_assignment, name='delete_assignment'),
    path('assignment/<int:assignment_id>/mark/', mark_assignment, name='mark_assignment'),
    path('assignment/submissions/', view_submissions, name='view_submissions'),
    path('assignment/<int:assignment_id>/submit/', submit_assignment, name='submit_assignment'),
    path('assignment-list/',assignment_list,name='assignment_list'),
    path('assignment/<int:assignment_id>/feedback/', view_assignment_feedback, name='view_assignment_feedback'),

    # Quiz URLs
    path('quiz/create/', create_quiz, name='create_quiz'),
    path('quiz/<int:quiz_id>/add/', add_question, name='add-question'),  # URL for adding questions
    path('quiz/<int:quiz_id>/take/', take_quiz, name='take-quiz'),
    path('create-quiz-result/<int:quiz_id>/',create_quiz_result,name='create-quiz-result'),
    path('quiz/<int:quiz_id>/results/', quiz_results, name='quiz-results'),

    path('quiz-list',quiz_list,name='quiz_list'),
    # path('quiz/<int:quiz_id>/edit/', edit_quiz, name='edit-quiz'),

    # # Delete Quiz
    # path('quiz/<int:quiz_id>/delete/', delete_quiz, name='delete-quiz'),

    # Quiz Detail
    path('quiz/<int:quiz_id>/', quiz_detail, name='quiz-detail'),

    # Quiz Results
    # path('quiz/<int:quiz_id>/results/', quiz_results, name='quiz-results'),
    # path('quiz/<int:quiz_id>/edit/', edit_quiz, name='edit_quiz'),
    # path('quiz/<int:quiz_id>/delete/', delete_quiz, name='delete_quiz'),



    ## Marketing and Promotions URL
    path('marketing-promotions/', marketing_promotions, name='marketing_promotions'),
    path('track-clicks/', track_clicks, name='track_clicks'),
    path('course-data/', course_data, name='course_data'),
    path('referral-program/', referral_program, name='referral_program'),

    

    

    # Miscellaneaous URLs
    # path('course/<int:course_id>/assignments/', view_assignments, name='view_assignments'),


    path('Super-panel',Super_panel,name='super-panel'),
    path('content-management',content_management,name='content-management'),
    path('user-management',User_Management,name='user-management'),
]
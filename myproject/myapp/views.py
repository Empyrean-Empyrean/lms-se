from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from .models import CustomUser, Course, Resource, Quiz, Assignment, ProgressReport, Message, Book

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def create_course(request):
    if request.user.is_instructor:
        if request.method == 'POST':
            title = request.POST.get('title')
            description = request.POST.get('description')
            course = Course(title=title, description=description, instructor=request.user)
            course.save()
            return redirect('course_list')
        return render(request, 'create_course.html')
    return redirect('home')

@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})

@login_required
def upload_resource(request, course_id):
    if request.user.is_instructor:
        if request.method == 'POST':
            title = request.POST.get('title')
            content = request.FILES.get('content')
            course = Course.objects.get(id=course_id)
            resource = Resource(title=title, content=content, course=course)
            resource.save()
            return redirect('resource_list', course_id=course_id)
        return render(request, 'upload_resource.html', {'course_id': course_id})
    return redirect('home')

@login_required
def resource_list(request, course_id):
    resources = Resource.objects.filter(course_id=course_id)
    return render(request, 'resource_list.html', {'resources': resources, 'course_id': course_id})

@login_required
def create_quiz(request):
    if request.user.is_instructor:
        if request.method == 'POST':
            title = request.POST.get('title')
            course_id = request.POST.get('course_id')
            questions = request.POST.get('questions')
            course = Course.objects.get(id=course_id)
            quiz = Quiz(title=title, questions=questions, course=course)
            quiz.save()
            return redirect('quiz_list')
        return render(request, 'create_quiz.html', {'courses': Course.objects.all()})
    return redirect('home')

@login_required
def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz_list.html', {'quizzes': quizzes})

@login_required
def create_assignment(request):
    if request.user.is_instructor:
        if request.method == 'POST':
            title = request.POST.get('title')
            course_id = request.POST.get('course_id')
            description = request.POST.get('description')
            due_date = request.POST.get('due_date')
            course = Course.objects.get(id=course_id)
            assignment = Assignment(title=title, description=description, due_date=due_date, course=course)
            assignment.save()
            return redirect('assignment_list')
        return render(request, 'create_assignment.html', {'courses': Course.objects.all()})
    return redirect('home')

@login_required
def assignment_list(request):
    assignments = Assignment.objects.all()
    return render(request, 'assignment_list.html', {'assignments': assignments})

@login_required
def student_progress(request, student_id):
    reports = ProgressReport.objects.filter(student_id=student_id)
    return render(request, 'student_progress.html', {'reports': reports})

@login_required
def send_message(request):
    if request.method == 'POST':
        recipient_id = request.POST.get('recipient_id')
        content = request.POST.get('content')
        recipient = CustomUser.objects.get(id=recipient_id)
        message = Message(sender=request.user, recipient=recipient, content=content)
        message.save()
        return redirect('inbox')
    users = CustomUser.objects.exclude(id=request.user.id)
    return render(request, 'send_message.html', {'users': users})

@login_required
def inbox(request):
    messages = Message.objects.filter(recipient=request.user)
    return render(request, 'inbox.html', {'messages': messages})

@login_required
def add_book(request):
    if request.user.is_librarian:
        if request.method == 'POST':
            title = request.POST.get('title')
            author = request.POST.get('author')
            isbn = request.POST.get('isbn')
            book = Book(title=title, author=author, isbn=isbn, uploaded_by=request.user)
            book.save()
            return redirect('book_list')
        return render(request, 'add_book.html')
    return redirect('home')

@login_required
def book_list(request):
    if request.user.is_librarian:
        books = Book.objects.all()
        return render(request, 'book_list.html', {'books': books})
    return redirect('home')

@login_required
def view_books(request):
    books = Book.objects.filter(available=True)
    return render(request, 'view_books.html', {'books': books})

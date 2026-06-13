from .models import ConnectionRequest
from django.contrib import messages
from .models import Resume, UserProfile
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.db.models import Q

def login_view(request):#1
    error_message = None
    
    if request.method == "POST":
        username_input = request.POST.get('username')
        password_input = request.POST.get('password')
        
        try:
            user = UserProfile.objects.get(
                username=username_input,
                password=password_input
            )
        except UserProfile.DoesNotExist:
            user = None
        
        if user is not None:
            # Login successful!
            request.session['user_id'] = user.id
            request.session['username'] =  user.username
            request.session['role'] = user. role
            
            # Now we check roles safely inside this block
            if user.role == "teacher":
                return redirect("home")
            elif user.role == "student":
                return redirect("home")
            else:
                return redirect("home")
       
        else:
            error_message = "Invalid username or password."
            
    return render(request, 'login.html', {'error': error_message})



def resume_page(request):
    
    if request.method == "POST":
        current_username = request.session.get('username')
        student_profile = UserProfile.objects.get(username=current_username)
        Resume.objects.update_or_create(
            profile=student_profile,
            defaults={
                'name': request.POST['name'],
                'email': request.POST['email'],
                'phone': request.POST['phone'],
                'education': request.POST['education'],
                'experience': request.POST['experience'],
                'college': request.POST['college'],
                'branch': request.POST['branch'],
                'skills': request.POST['skills'],
                'linkedin': request.POST.get('linkedin'),
                'github': request.POST.get('github'),
                'summary': request.POST.get('summary'),
                'projects': request.POST.get('projects'),
                'certifications': request.POST.get('certifications'),
                'theme': request.POST.get('theme', '1')
                }
             )
        return redirect('home')
    my_old_resume = Resume.objects.filter(profile=UserProfile.objects.get(username=request.session['username'])).first()
    return render(request, 'resume.html', {'resume': my_old_resume})

def list_resumes(request):
    all_resumes = Resume.objects.all()
    # Send the data to list.html, NOT resume.html
    return render(request, 'list.html', {'resumes': all_resumes})

def resume_detail(request, id):
    resume = Resume.objects.get(id=id)
    theme_choice=request.GET.get('theme')
    if not theme_choice:
        theme_choice = str(resume.theme)
    current_user = request.session.get('username')
    current_role = ''
    
    if current_user:
        profile = UserProfile.objects.filter(username=current_user).first()
        if profile:
            current_role = profile.role.lower().strip() 
    context = {
        'resume': resume,
        'current_user': current_user,
        'current_role': current_role
     }
    if theme_choice == '2':
        return render(request, 'detail_theme_2.html', context)
    elif theme_choice == '3':
        return render(request, 'detail_theme_3.html', context)
    else:
        return render(request, 'detail.html', context)
    
def send_request(request):
    if request.method == "POST":
        sender = request.POST.get("sender")
        receiver = request.POST.get("receiver")
        resume_exists = ConnectionRequest.objects.filter(sender=sender, receiver=receiver).exists()
        if not resume_exists:
            ConnectionRequest.objects.create(
                sender=sender,
                receiver=receiver,
                status="Pending"
        )
        messages.success(request, "Your request was sent successfully!")
    else:
        messages.warning(request, "You have already sent a request to this person!")
    return redirect('home')

def home(request):#2
    username = request.session.get('username')
    if not username:
        return render(request, "home.html")
    user_profile = UserProfile.objects.filter(username=username).first()
    if user_profile:
        role = user_profile.role.lower().strip() 
    else:
        role = "student" 
    notifications = ConnectionRequest.objects.filter(
        receiver=username,
        status='Pending'
    )
    if role == "student":
        student_resume = Resume.objects.filter(profile__username=username).first()
        all_teachers = UserProfile.objects.filter(role__icontains='teacher')
        student_accepted = ConnectionRequest.objects.filter(
                Q(sender=username) | Q(receiver=username),
                status__icontains='accept'
            )
        unique_accepted = {f"{req.sender}-{req.receiver}": req for req in student_accepted}.values()
        return render(request, "home.html", {
                "my_info": student_resume,
                "notifications": notifications,
                "teachers_list": all_teachers,
                "accepted_requests": unique_accepted,
                "logged_in_user": username
            })
    elif role == "teacher":
        teacher_accepted = ConnectionRequest.objects.filter(
            Q(sender=username) | Q(receiver=username),
            status__icontains='accept'
        )
        unique_accepted = {f"{req.sender}-{req.receiver}": req for req in teacher_accepted}.values()
        pending_requests = ConnectionRequest.objects.filter(
            receiver=username, 
            status__icontains='pending'
        )
        return render(request, "teacher.html", {
            "logged_in_user": username,
            "accepted_requests": unique_accepted,
            "notifications": pending_requests,
        })
    return render(request, "home.html")
    
def accept_request(request,request_id):
       req = ConnectionRequest.objects.filter(id=request_id).first()
       if req:
        ConnectionRequest.objects.filter(
            sender=req.sender, 
            receiver=req.receiver
        ).update(status="Accepted")
        
       return redirect('home')


def research_request(request):
    if request.method == "POST":
        sender_username = request.session.get('username')
        receiver_username = request.POST.get('receiver')
        req_type = request.POST.get('request_type', 'research')
        request_exists = ConnectionRequest.objects.filter(sender=sender_username, receiver=receiver_username).exists()
        if not request_exists:
            ConnectionRequest.objects.create(
                sender=sender_username,
                receiver=receiver_username,
                request_type=req_type,
                status="Pending"
            )
            messages.success(request, "Your request was sent successfully!")
        else:
            messages.warning(request, "You have already sent a request to this person!")
            
        return redirect('home')
        
def teacher_profile(request, username):
    teacher = UserProfile.objects.filter(username=username).first()
    teacher_resume = Resume.objects.filter(profile__username=username).first()
    return render(request, "teacher_profile.html", {
        "teacher": teacher,
        "resume": teacher_resume,
        "logged_in_user": request.session.get('username')
    })
def update_teacher_info(request):
    username = request.session.get('username')
    existing_resume = Resume.objects.filter(profile__username=username).first()
    
    if request.method == "POST":
        typed_email = request.POST.get('email')
        typed_college = request.POST.get('college')
        typed_branch = request.POST.get('branch')
        typed_experience = request.POST.get('experience')
        typed_skills = request.POST.get('skills')
        
        if existing_resume:
            existing_resume.email = typed_email
            existing_resume.college = typed_college
            existing_resume.branch = typed_branch
            existing_resume.experience = typed_experience
            existing_resume.skills = typed_skills
            existing_resume.save()
        else:
            user_profile = UserProfile.objects.filter(username=username).first()
            Resume.objects.create(
                profile=user_profile,
                email=typed_email,
                college=typed_college,
                branch=typed_branch,
                experience=typed_experience,
                skills=typed_skills
            )
        return redirect('home')
    return render(request, "teacher_info.html", {"resume": existing_resume})


def logout_user(request):
    request.session.flush() #explicitly
    return redirect('login')

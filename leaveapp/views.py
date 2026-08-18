from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Staff, Leave
from .forms import StaffForm, LeaveForm

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User


def index(request):
    return render(request, "index.html")


@login_required
def home(request):
    total_staff = Staff.objects.count()
    total_leave = Leave.objects.count()
    approved_leave = Leave.objects.filter(status="Approved").count()
    pending_leave = Leave.objects.filter(status="Pending").count()

    context = {
        "total_staff": total_staff,
        "total_leave": total_leave,
        "approved_leave": approved_leave,
        "pending_leave": pending_leave,
    }

    return render(request, "admin/home.html", context)


@login_required
def add_staff(request):
    if request.method == "POST":
        form = StaffForm(request.POST, request.FILES)

        print("FORM VALID:", form.is_valid())
        print("FORM ERRORS:", form.errors)

        if form.is_valid():
            print(form.cleaned_data)

            password = "12345"

            user = User.objects.create_user(
                username=form.cleaned_data["email"],
                email=form.cleaned_data["email"],
                password=password
            )

            staff = form.save(commit=False)
            staff.user = user
            staff.save()

            send_mail(
                subject="Welcome to SLMS",
                message=f"""
Hello {staff.name},

Your Staff Account has been created successfully.

Username: {user.username}
Password: {password}

Please change your password after first login.

Thank You
SLMS Team
""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[staff.email],
                fail_silently=False,
            )

            messages.success(request, "Staff Added Successfully")
            return redirect("view_staff")

    else:
        form = StaffForm()

    return render(request, "admin/add_staff.html", {"form": form})

@login_required
def view_staff(request):
    query = request.GET.get('q')

    if query:
        staff = Staff.objects.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(department__icontains=query) |
            Q(designation__icontains=query)
        )
    else:
        staff = Staff.objects.all()

    return render(request, 'admin/view_staff.html', {'staff': staff})





@login_required
def edit_staff(request, id):
    staff = get_object_or_404(Staff, id=id)

    if request.method == "POST":
        form = StaffForm(request.POST, request.FILES, instance=staff)
        if form.is_valid():
            form.save()
            return redirect("view_staff")
    else:
        form = StaffForm(instance=staff)

    return render(request, "admin/add_staff.html", {"form": form})



@login_required
def profile(request):
    return render(request, "admin/profile.html")


@login_required
def delete_staff(request, id):
    staff = get_object_or_404(Staff, id=id)
    staff.delete()
    return redirect("view_staff")



@login_required
def leave_request(request):
    leaves = Leave.objects.all()
    return render(request, 'admin/leave_request.html', {'leaves': leaves})

@login_required
def approve_leave(request, id):

    leave = get_object_or_404(Leave, id=id)

    leave.status = "Approved"
    leave.save()

    send_mail(
        subject="Leave Approved",
        message=f"""
Hello {leave.staff.name},

Your leave request has been APPROVED.

Leave Type : {leave.leave_type}
From Date : {leave.from_date}
To Date : {leave.to_date}

Thank You.
""",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[leave.staff.email],
        fail_silently=False,
    )

    messages.success(request, "Leave Approved Successfully")
    return redirect("leave_request")

@login_required
def reject_leave(request, id):

    leave = get_object_or_404(Leave, id=id)

    leave.status = "Rejected"
    leave.save()

    send_mail(
        subject="Leave Rejected",
        message=f"""
Hello {leave.staff.name},

Your leave request has been REJECTED.

Leave Type : {leave.leave_type}
From Date : {leave.from_date}
To Date : {leave.to_date}

Reason:
{leave.reason}

Thank You.
""",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[leave.staff.email],
        fail_silently=False,
    )

    messages.success(request, "Leave Rejected Successfully")
    return redirect("leave_request")


def admin_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("home")

        else:
            messages.error(request, "Invalid Username or Password")

    return render(request, "admin/admin_login.html")

@login_required
def user_logout(request):
    logout(request)
    return redirect("index")




#Staff

@login_required
def staff_dashboard(request):

    staff = request.user.staff

    total_leave = Leave.objects.filter(staff=staff).count()
    approved = Leave.objects.filter(staff=staff, status="Approved").count()
    pending = Leave.objects.filter(staff=staff, status="Pending").count()
    rejected = Leave.objects.filter(staff=staff, status="Rejected").count()

    context = {
        "staff": staff,
        "total_leave": total_leave,
        "approved": approved,
        "pending": pending,
        "rejected": rejected,
    }

    return render(request, "staff/staff_dashboard.html", context)


@login_required
def staff_home(request):
    return render(request, "staff/staff_home.html")


@login_required
def staff_apply_leave(request):

    if request.method == "POST":

        form = LeaveForm(request.POST)

        if form.is_valid():

            leave = form.save(commit=False)

            leave.staff = request.user.staff
            leave.status = "Pending"

            # Calculate leave days
            leave.leave_days = (
                leave.to_date - leave.from_date
            ).days + 1

            leave.save()

            send_mail(
                subject="New Leave Request",

                message=f"""
A new leave request has been submitted.

Staff Name : {leave.staff.name}
Department : {leave.staff.department}
Leave Type : {leave.leave_type}

From Date : {leave.from_date}
To Date : {leave.to_date}
Total Days : {leave.leave_days}

Reason : {leave.reason}

Status : Pending
""",

                from_email=settings.DEFAULT_FROM_EMAIL,

                recipient_list=[
                    "harshitab574@gmail.com"
                ],

                fail_silently=False,
            )

            messages.success(
                request,
                f"Leave Applied Successfully for {leave.leave_days} days."
            )

            return redirect("staff_leave_history")

    else:
        form = LeaveForm()

    return render(
        request,
        "staff/staff_apply_leave.html",
        {"form": form}
    )


def staff_login(request):
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        print("Username:", username)
        print("Password:", password)

        user = authenticate(
            request,
            username=username,
            password=password
        )

        print("Authenticated User:", user)

        if user is not None:
            login(request, user)
            return redirect("staff_dashboard")
        else:
            messages.error(request, "Invalid Username or Password")

    return render(request, "staff/staff_login.html")

@login_required
def staff_profile(request, id):
    staff = get_object_or_404(Staff, id=id)

    return render(
        request,
        "staff/staff_profile.html",
        {"staff": staff}
    )



@login_required
def staff_leave_history(request):
    staff = Staff.objects.get(user=request.user)
    leaves = Leave.objects.filter(staff=staff)
    return render(request, "staff/staff_leave_history.html", {"leaves": leaves})
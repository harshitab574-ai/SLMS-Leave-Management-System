from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Staff, Leave
from .forms import StaffForm, LeaveForm

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q


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
        if form.is_valid():
            form.save()
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
def apply_leave(request):
    if request.method == "POST":
        form = LeaveForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("leave_request")
    else:
        form = LeaveForm()

    return render(request, "admin/apply_leave.html", {"form": form})

@login_required
def leave_request(request):
    leaves = Leave.objects.all()
    return render(request, 'admin/leave_request.html', {'leaves': leaves})

@login_required
def approve_leave(request, id):
    leave = get_object_or_404(Leave, id=id)
    leave.status = "Approved"
    leave.save()
    return redirect('leave_request')

@login_required
def reject_leave(request, id):
    leave = get_object_or_404(Leave, id=id)
    leave.status = "Rejected"
    leave.save()
    return redirect('leave_request')


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

    staff = Staff.objects.first()

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
def staff_profile(request, id):
    staff = get_object_or_404(Staff, id=id)
    return render(request, "staff/staff_profile.html", {"staff": staff})


@login_required
def staff_apply_leave(request):

    if request.method == "POST":
        print(request.POST)   # Debug

        form = LeaveForm(request.POST)

        if form.is_valid():
            leave = form.save()
            print("Saved:", leave.id)
            messages.success(request, "Leave Applied Successfully")
            return redirect("staff_leave_history")
        else:
            print(form.errors)   # Debug

    else:
        form = LeaveForm()

    return render(request, "staff/staff_apply_leave.html", {"form": form})
@login_required
def staff_leave_history(request):
    leaves = Leave.objects.filter(staff=request.user.staff)
    return render(request, "staff/staff_leave_history.html", {"leaves": leaves})




def staff_login(request):

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
            return redirect("staff_dashboard")

        else:
            messages.error(request, "Invalid Username or Password")

    return render(request, "staff/staff_login.html")
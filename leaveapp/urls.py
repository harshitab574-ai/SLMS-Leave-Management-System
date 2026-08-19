from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # ==========================
    # Index
    # ==========================
    path("", views.index, name="index"),

    # ==========================
    # Admin Authentication
    # ==========================
    path("admin-login/", views.admin_login, name="admin_login"),
    path("logout/", views.user_logout, name="logout"),
   
    # ==========================
    # Admin Dashboard
    # ==========================
    path("home/", views.home, name="home"),

    # ==========================
    # Staff Management (Admin)
    # ==========================
    path("add-staff/", views.add_staff, name="add_staff"),
    path("view-staff/", views.view_staff, name="view_staff"),
    path("edit-staff/<int:id>/", views.edit_staff, name="edit_staff"),
    path("delete-staff/<int:id>/", views.delete_staff, name="delete_staff"),
    path("profile/", views.profile, name="profile"),

    # ==========================
    # Leave Management (Admin)
    # ==========================

    path("leave-request/", views.leave_request, name="leave_request"),
    path("approve-leave/<int:id>/", views.approve_leave, name="approve_leave"),
    path("reject-leave/<int:id>/",views.reject_leave,name="reject_leave"),

    # ==========================
    # Staff Module
    # ==========================
    path("staff-login/", views.staff_login, name="staff_login"),
    path("staff-dashboard/", views.staff_dashboard, name="staff_dashboard"),
    path("staff-home/", views.staff_home, name="staff_home"),
   path("staff-profile/<int:id>/", views.staff_profile, name="staff_profile"),
    path("staff-apply-leave/", views.staff_apply_leave, name="staff_apply_leave"),
   
    path(
    "staff-leave-history/",
    views.staff_leave_history,
    name="staff_leave_history"
),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
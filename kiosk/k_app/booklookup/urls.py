from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login_user, name="login"),   
    path('logout', views.logout_user, name="logout"),
    path('mode', views.set_mode, name="set_mode"),
    path('checkin', views.checkin, name="checkin"),
    path('Patrol_mode', views.patrol_home, name="patrol_home"),
    path('Assist_mode', views.assist_home, name="assist_home"),
    path('facilities_location', views.fac_loc, name="fac_loc"),
    path('request_librarians', views.req_lib, name="req_lib"),
    path('FAQ', views.faq, name="faq"),
    path('Booking_facilities', views.book_fac, name="book_fac"),
    path("Search_Results", views.search_results, name="search_results"),
]
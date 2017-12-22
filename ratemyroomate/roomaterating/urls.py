from django.conf.urls import url
from . import views

app_name = "roomaterating"
urlpatterns = (
    url(r'^$', views.IndexView.as_view(), name="index"),
    url(r'^all-colleges/$', views.CollegeView.as_view(), name="colleges"),
    url(r'^all-roommates/$', views.RoomateView.as_view(), name="roomates"),
    url(r'^all-roommates/(?P<pk>[0-9]+)/$', views.CollegeRoomatesView.as_view(), name="colleges-roomates"),
    url(r'^roommate/(?P<pk>[0-9]+)/$', views.RoommateDetail.as_view(), name="viewroommate"),
    url(r'roommate/add/$', views.RoomateCreateView.as_view(), name='add-roommate'),
    url(r'college/add/$', views.CollegeCreateView.as_view(), name='add-college'),
)


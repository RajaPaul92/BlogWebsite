from django.contrib import admin
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^loginAPI/$', views.loginAPI.as_view(), name='loginAPI'),

    url(r'^empDetails/$', views.empDetails, name='empDetails'),
    url(r'^empDetailsAPI/$', views.empDetailsAPI.as_view(), name='empDetailsAPI'),

    url(r'^empAdd/$', views.empAdd, name='empAdd'),
    url(r'^empAddAPI/$', views.empAddAPI.as_view(), name='empAddAPI'),

    url(r'^editEmployee/(?P<id>[\w\s,-]+)/$', views.editEmployee, name='editEmployee'),
    url(r'^updateEmp/(?P<id>[\w\s,-]+)/$', views.updateEmp, name="updateEmp"),
    url(r'^updateEmpAPI/(?P<id>[\w\s,-]+)/$', views.updateEmpAPI.as_view(), name='updateEmpAPI'),

    url(r'^deleteEmployee/(?P<id>[\w\s,-]+)/$', views.deleteEmployee, name='deleteEmployee'),

    url(r'^blog/$', views.blog, name='blog'),
    url(r'^blogAPI/$', views.blogAPI.as_view(), name='blogAPI'),
    url(r'^blogDetails/$', views.blogDetails, name='blogDetails'),
    url(r'^blogDetailsAPI/$', views.blogDetailsAPI.as_view(), name='blogDetailsAPI'),

    url(r'^editblog/(?P<id>[\w\s,-]+)/$', views.editblog, name= 'editblog'),
    url(r'^updateblog/(?P<id>[\w\s,-]+)/$',views.updateblog, name= 'updateblog'),
    url(r'^updateblogAPI/(?P<id>[\w\s,-]+)/$', views.updateblogAPI.as_view(), name='updateblogAPI'),
    url(r'^deleteblog/(?P<id>[\w\s,-]+)/$', views.deleteblog, name='deleteblog'),

#     user data

    url(r'^userlogin/$', views.userlogin, name='userlogin'),
    url(r'^userloginAPI/$', views.userloginAPI.as_view(), name='userloginAPI'),

    url(r'^userdata/$', views.userdata, name='userdata'),
    url(r'^userdataAPI/$', views.userdataAPI.as_view(), name='userdataAPI'),
    url(r'^userblogDetails/$', views.userblogDetails, name='userblogDetails'),
    url(r'^userblogDetailsAPI/$', views.userblogDetailsAPI.as_view(), name='userblogDetailsAPI'),

    url(r'^usereditblog/(?P<id>[\w\s,-]+)/$', views.usereditblog, name='usereditblog'),
    url(r'^userupdateblog/(?P<id>[\w\s,-]+)/$', views.userupdateblog, name='userupdateblog'),
    url(r'^userupdateblogAPI/(?P<id>[\w\s,-]+)/$', views.userupdateblogAPI.as_view(), name='userupdateblogAPI'),
    url(r'^userdeleteblog/(?P<id>[\w\s,-]+)/$', views.userdeleteblog, name='userdeleteblog'),

    url(r'^comment/$', views.comment, name='comment'),
    url(r'^commentAPI/$', views.commentAPI.as_view(), name='commentAPI'),
    url(r'^commentDetails/$', views.commentDetails, name='commentDetails'),
    url(r'^commentDetailsAPI/$', views.commentDetailsAPI.as_view(), name='commentDetailsAPI')
]

"""
URL configuration for stu_score_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app01 import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.student_list),

    #学生信息管理模块
    path('student/list/', views.student_list),
    path('student/add', views.student_add),
    path('student/<int:nid>/edit/', views.student_edit),
    path('student/<int:nid>/delete/', views.student_delete),

    #课程信息管理模块
    path('course/list/', views.course_list),
    path('course/add', views.course_add),
    path('course/<int:nid>/edit/', views.course_edit),
    path('course/<int:nid>/delete/', views.course_delete),

    #成绩信息管理模块
    path('grade/list', views.grade_list),
    path('grade/add', views.grade_add),
    path('grade/info', views.grade_info),
    path('grade/<int:nid>/edit', views.grade_edit),
    path('grade/<int:nid>/delete', views.grade_delete),

    #统计分析模块
    path('statistic/person', views.statistic_person),
    path('statistic/course', views.statistic_course),
    path('statistic/pie/', views.chart_pie),
    path('statistic/bar/', views.chart_bar),
]

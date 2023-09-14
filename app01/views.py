from django.shortcuts import render, redirect
from app01 import models
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from datetime import datetime
import pymysql, csv

#----------------------------------------------------------------------------------------------------------------------
"""数据导出部分"""

def from_mysql_get_score_info():
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        db='db_sc',
        password='ZZxxCC123',
        charset='utf8mb4')
    cursor_score = conn.cursor()
    sql_score = 'select * from app01_gradeinfo'
    cursor_score.execute(sql_score)
    data_score = cursor_score.fetchall()
    conn.close()
    return data_score

def from_mysql_get_student_info():
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        db='db_sc',
        password='ZZxxCC123',
        charset='utf8mb4')
    cursor_score = conn.cursor()
    sql_score = 'select * from app01_studentinfo'
    cursor_score.execute(sql_score)
    data_score = cursor_score.fetchall()
    conn.close()
    return data_score

def from_mysql_get_course_info():
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        db='db_sc',
        password='ZZxxCC123',
        charset='utf8mb4')
    cursor_score = conn.cursor()
    sql_score = 'select * from app01_courseinfo'
    cursor_score.execute(sql_score)
    data_score = cursor_score.fetchall()
    conn.close()
    return data_score

def write_csv():
    data1 = from_mysql_get_student_info()
    data2 = from_mysql_get_course_info()
    data3 = from_mysql_get_score_info()
    
    filename1 = 'student.csv'
    filename2 = 'course.csv'
    filename3 = 'score.csv'
    with open(filename1,mode='w',encoding='utf-8') as f1:
        write = csv.writer(f1,dialect='excel')
        for item in data1:
            write.writerow(item)
    with open(filename2,mode='w',encoding='utf-8') as f2:
        write = csv.writer(f2,dialect='excel')
        for item in data2:
            write.writerow(item)    
    with open(filename3,mode='w',encoding='utf-8') as f3:
        write = csv.writer(f3,dialect='excel')
        for item in data3:
            write.writerow(item)   
    f1.close
    f2.close
    f3.close

#----------------------------------------------------------------------------------------------------------------------
"""学生模块视图函数"""

def student_list(request):
    # 学生列表

    data_dict = {}
    value = request.GET.get('name')
    value2 = request.GET.get('major')
    value3 = request.GET.get('college')

    if value:
        data_dict["name__contains"] = value
    elif value2:
        data_dict["major__contains"] = value2
    elif value3:
        data_dict["college__contains"] = value3

    # print(data_dict)

    queryset = models.StudentInfo.objects.filter(**data_dict)

    form = StudentModelForm()

    return render(request, 'student_list.html', {'queryset':queryset, 'form':form})

class StudentModelForm(forms.ModelForm):
    class Meta:
        model = models.StudentInfo
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}

#ajax
@csrf_exempt
def student_add(request):
    form = StudentModelForm(data=request.POST)

    if form.is_valid():
        form.save()
        write_csv()
        return JsonResponse({"status":True})
    
    return JsonResponse({"status":False, 'error': form.errors})

#静态路由
def student_add2(request):
    if request.method == "GET":
        form = StudentModelForm()
        return render(request, 'student_add.html', {"form":form})

    else:
        form = StudentModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/student/list')
        else:
            return render(request, 'student_add.html', {"form": form})

def student_edit(request, nid):

    class StudentModelForm(forms.ModelForm):
        class Meta:
            model = models.StudentInfo
            fields = ['name','gender','birth','major', 'college']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            for name, field in self.fields.items():
                field.widget.attrs = {"class": "form-control"}
    if request.method == "GET":
        obj = models.StudentInfo.objects.filter(id=nid).first()

        form = StudentModelForm(instance=obj)

        return render(request, 'student_edit.html', {"form": form, "obj": obj})

    row_object = models.StudentInfo.objects.filter(id=nid).first()
    form = StudentModelForm(data=request.POST, instance=row_object)

    if form.is_valid():
        name = request.POST.get("name")
        major = request.POST.get("major")
        college = request.POST.get("college")
        sid = row_object.sid
        # print(name, sid)
        obj = models.GradeInfo.objects.filter(gid=sid)
        if(obj):
            # print("更新姓名")
            obj.update(s_name=name, major=major, college=college)
        form.save()
        write_csv()
        return redirect('/student/list')

    return render(request, 'student_edit.html', {"form": form})

def student_delete(request, nid):
    models.StudentInfo.objects.filter(id=nid).delete()
    write_csv()
    return redirect('/student/list')



#-----------------------------------------------------------------------------------------------------------------------
"""课程模块视图函数"""

def course_list(request):

    data_dict = {}
    value = request.GET.get("name")

    if value:
        data_dict["name__contains"] = value

    queryset = models.CourseInfo.objects.filter(**data_dict)
    
    form = CourseModelForm()

    return render(request, 'course_list.html', {'queryset':queryset, 'form':form})


class CourseModelForm(forms.ModelForm):
    class Meta:
        model = models.CourseInfo
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}

#ajax
@csrf_exempt
def course_add(request):
    form = CourseModelForm(data=request.POST)

    if form.is_valid():
        form.save()
        write_csv()
        return JsonResponse({"status":True})
    
    return JsonResponse({"status":False, 'error': form.errors})

#静态路由
def course_add2(request):
    if request.method == "GET":
        form = CourseModelForm()
        return render(request, 'course_add.html', {"form":form})

    else:
        form = CourseModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/course/list')
        else:
            return render(request, 'course_add.html', {"form": form})


def course_delete(request, nid):
    models.CourseInfo.objects.filter(id=nid).delete()
    write_csv()
    return redirect('/course/list')


def course_edit(request, nid):

    class CourseModelForm(forms.ModelForm):
        class Meta:
            model = models.CourseInfo
            fields = ['name', 'credit']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            for name, field in self.fields.items():
                field.widget.attrs = {"class": "form-control"}

    if request.method == "GET":
        obj = models.CourseInfo.objects.filter(id=nid).first()

        form = CourseModelForm(instance=obj)

        return render(request, 'course_edit.html', {"form": form, "obj": obj})

    row_object = models.CourseInfo.objects.filter(id=nid).first()
    form = CourseModelForm(data=request.POST, instance=row_object)

    if form.is_valid():
        form.save()
        write_csv()
        return redirect('/course/list')

    return render(request, 'course_edit.html', {"form": form})


#-----------------------------------------------------------------------------------------------------------------------
"""成绩模块视图函数"""

class GradeModelForm(forms.ModelForm):
    class Meta:
        model = models.GradeInfo
        fields = ['gid','c_name','score']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}

def grade_list(request):
    data_dict = {}

    course = request.GET.get('course')
    student = request.GET.get('student')

    if course:
        c_name= models.CourseInfo.objects.filter(name__contains=course)
        c_num=  models.CourseInfo.objects.filter(number__contains=course)

        if(c_name):
            for item in c_name:
                data_dict["c_name"] = item.id

        if(c_num):
            data_dict["number__contains"] = course

    if student:
        gid = models.StudentInfo.objects.filter(sid__contains=student)
        s_name = models.StudentInfo.objects.filter(name__contains=student)

        if(gid):
            for item in gid:
                data_dict["gid"] = item.sid

        if(s_name):
            data_dict["s_name__contains"] = student

    queryset = models.GradeInfo.objects.filter(**data_dict)

    form = GradeModelForm()
    return render(request, 'grade_list.html', {'form':form, 'queryset':queryset})

def grade_info(request):

    c_name = request.GET.get("c_name")

    gid = request.GET.get("gid")

    number = name = "暂无"
    
    if(c_name):
        number = models.CourseInfo.objects.filter(id=c_name).first().number

    if(gid):
        name = models.StudentInfo.objects.filter(sid=gid).first().name

    
    return JsonResponse({"number":number, "name":name})


@csrf_exempt
def grade_add(request):
    form = GradeModelForm(data=request.POST)

    if form.is_valid():
        form.instance.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c_name = request.POST.get("c_name")
        gid = request.POST.get("gid")
        number = models.CourseInfo.objects.filter(id=c_name).first().number
        name = models.StudentInfo.objects.filter(sid=gid).first().name
        credit = models.CourseInfo.objects.filter(id=c_name).first().credit
        major = models.StudentInfo.objects.filter(sid=gid).first().major
        college = models.StudentInfo.objects.filter(sid=gid).first().college
        form.instance.number = number
        form.instance.s_name = name
        form.instance.credit = credit
        form.instance.major = major
        form.instance.college = college

        form.save()
        write_csv()
        return JsonResponse({"status":True})
    
    return JsonResponse({"status":False, 'error': form.errors})


def grade_delete(request, nid):
    models.GradeInfo.objects.filter(id=nid).delete()
    write_csv()
    return redirect('/grade/list')


def grade_edit(request, nid):

    class GradeModelForm(forms.ModelForm):
        class Meta:
            model = models.GradeInfo
            fields = ['score']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            for name, field in self.fields.items():
                field.widget.attrs = {"class": "form-control"}

    if request.method == "GET":
        obj = models.GradeInfo.objects.filter(id=nid).first()

        form = GradeModelForm(instance=obj)

        return render(request, 'grade_edit.html', {"form": form, "obj": obj})

    row_object = models.GradeInfo.objects.filter(id=nid).first()
    form = GradeModelForm(data=request.POST, instance=row_object)

    if form.is_valid():
        form.instance.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        form.save()
        write_csv()
        return redirect('/grade/list')

    return render(request, 'grade_edit.html', {"form": form})

#-----------------------------------------------------------------------------------------------------------------------
"""统计分析模块视图函数"""

def statistic_person(request):


    data_dict = {}
    queryset = {}
    student = request.GET.get('student')
    search_data = request.GET.get('student', "")
    name = ""

    if student:
        gid = models.StudentInfo.objects.filter(sid=student)
        s_name = models.StudentInfo.objects.filter(name=student)

        if(gid):
            for item in gid:
                data_dict["gid"] = item.sid

        if(s_name):
            data_dict["s_name"] = student
    
    if data_dict:
        queryset = models.GradeInfo.objects.filter(**data_dict)
        if queryset:
            name = queryset.first().s_name

    tot_score = 0
    cnt = 0
    h_set = {"c_name" : "暂无", "score":"暂无"}
    l_set = {"c_name" : "暂无", "score":"暂无"}
    avg = "暂无"
    high = 0
    low = 0x3f3f3f3f

    if(queryset):
        for item in queryset:
            tot_score += item.score

            if item.score > high:
                high = item.score
                h_set = item
            
            if item.score < low:
                low = item.score
                l_set = item
            
            cnt = cnt + 1
    
    if(cnt):
        avg = tot_score/cnt

    infoset = {"h_set" : h_set, "l_set" : l_set, "avg":avg}

    return render(request, "statistic_person.html", {'queryset':queryset, 'name':name, 'infoset':infoset, 'search_data':search_data})


def statistic_course(request):
    data_dict = {}
    queryset = {}
    course = request.GET.get('course')
    search_data = request.GET.get('course', "")
    name = ""

    perfect = great = good = qualified = not_qualified = 0

    if course:
        c_name = models.CourseInfo.objects.filter(name=course)
        number = models.CourseInfo.objects.filter(number=course)

        if(c_name):
            data_dict["number"] = c_name.first().number

        if(number):
            data_dict["number"] = course
    
    if data_dict:
        queryset = models.GradeInfo.objects.filter(**data_dict)
        if queryset:
            name = queryset.first().c_name
            for item in queryset:
                if item.score >= 90:
                    perfect += 1
                elif 80 <= item.score <90:
                    great += 1
                elif 70 <= item.score < 80:
                    good += 1
                elif 60 <= item.score < 69:
                    qualified += 1
                else:
                    not_qualified += 1
    
    grade_set = {"perfect":perfect, "great":great, "good":good, "qualified":qualified, "not_qualified":not_qualified}

    return render(request, "statistic_course.html", {'queryset':queryset, 'name':name, 'grade_set':grade_set, 'search_data':search_data})


def chart_pie(request):
    data=[{"value": 0, "name" : '良好'}, {"value": 0, "name" : '优秀'}, {"value": 0, "name" : '及格'}, {"value": 0, "name" : '不及格'}, {"value": 0, "name" : '中等'}]
    data_dict = {}
    queryset = {}
    course = request.GET.get('course')
    name = ""

    perfect = great = good = qualified = not_qualified = 0

    if course:
        c_name = models.CourseInfo.objects.filter(name=course)
        number = models.CourseInfo.objects.filter(number=course)

        if (c_name):
            data_dict["number"] = c_name.first().number

        if (number):
            data_dict["number"] = course

    if data_dict:
        queryset = models.GradeInfo.objects.filter(**data_dict)
        if queryset:
            name = queryset.first().c_name
            for item in queryset:
                if item.score >= 90:
                    perfect += 1
                elif 80 <= item.score < 90:
                    great += 1
                elif 70 <= item.score < 80:
                    good += 1
                elif 60 <= item.score < 69:
                    qualified += 1
                else:
                    not_qualified += 1
            data[0]["value"] = great
            data[1]["value"] = perfect
            data[2]["value"] = qualified
            data[3]["value"] = not_qualified
            data[4]["value"] = good

    result = {"status":True, "data":data, "cname":str(name)}
    return JsonResponse(result)

def chart_bar(request):

    student = request.GET.get('student')
    data_dict = {}
    queryset = {}
    name = ""
    course_list=[]
    score_list=[]

    if student:
        gid = models.StudentInfo.objects.filter(sid=student)
        s_name = models.StudentInfo.objects.filter(name=student)

        if (gid):
            for item in gid:
                data_dict["gid"] = item.sid

        if (s_name):
            data_dict["s_name"] = student

    if data_dict:
        queryset = models.GradeInfo.objects.filter(**data_dict)
        if queryset:
            name = queryset.first().s_name
            for item in queryset:
                course_list.append(str(item.c_name))
                score_list.append(item.score)

    result = {"status":True, "data":{"score":score_list, "course":course_list}}
    return JsonResponse(result)

#-----------------------------------------------------------------------------------------------------------------------

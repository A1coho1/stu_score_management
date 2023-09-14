from django.db import models

class StudentInfo(models.Model):

    gender_choices = (
        ("M", "男"),
        ("F", "女"),
    )

    sid = models.CharField(verbose_name='学号', max_length=8, unique=True)

    name = models.CharField(verbose_name='姓名', max_length=20, unique=True)

    gender = models.CharField(verbose_name='性别', max_length=4, choices=gender_choices)

    birth = models.DateField(verbose_name='出生日期')

    major = models.CharField(verbose_name='专业', max_length=20)

    college = models.CharField(verbose_name='学院', max_length=20)

    def __str__(self):
        return self.sid

class CourseInfo(models.Model):

    number = models.CharField(verbose_name='课程号', max_length=20, unique=True)

    name = models.CharField(verbose_name='课程名称', max_length=20, unique=True)

    credit = models.IntegerField(verbose_name='学分')

    def __str__(self):
        return self.name

class GradeInfo(models.Model):

    gid = models.ForeignKey(to='StudentInfo', to_field='sid', verbose_name='学号', max_length=8, on_delete=models.CASCADE, related_name="gid")

    s_name = models.CharField(verbose_name='姓名', max_length=20)

    number = models.CharField(verbose_name='课程号', max_length=20)

    c_name = models.ForeignKey(
        to='CourseInfo', to_field='id', verbose_name='课程名称', max_length=20, on_delete=models.CASCADE)

    date = models.CharField(verbose_name='日期', max_length=20)

    score = models.DecimalField(verbose_name='成绩', max_digits=5, decimal_places=2) #精确到两位小数

    credit = models.IntegerField(verbose_name='学分')

    major = models.CharField(verbose_name='专业', max_length=20)

    college = models.CharField(verbose_name='学院', max_length=20)
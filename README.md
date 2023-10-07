# 学生管理系统

## 1. 项目简介
基于mysql+django的学生成绩管理系统，主要涉及学生信息管理、课程信息管理、成绩信息管理以及统计分析四个模块。
其中学生、课程、成绩三大模块均实现了增删改查功能，统计分析部分使用 [echarts](https://echarts.apache.org/zh/index.html) 进行可视化。

![](https://pic.imgdb.cn/item/6520fa16c458853aef28c6a8.png)

![](https://pic.imgdb.cn/item/6520fa16c458853aef28c689.png)

## 2. 涉及的主要技术栈
- 前端: Bootstrap+Jquery+AJAX
- 后端: Django

## 3. 项目部署

- Clone项目或下载zip到本地
- 进入项目根目录并安装依赖库:
```
pip install -r requirements.txt
```
- 进入/stu_score_management/settings.py修改数据库相关设置:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_sc',           # 要使用的数据库名称，建议新建一个数据库
        'USER': 'root',            # 用户名，默认为root
        'PASSWORD': '******',      # 你的密码
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

- 创建你刚刚所填写的数据库，以'db_sc'为例:
  ```
  create database db_sc;
  ```
  
- 执行数据库迁移命令:
  ```
  python manage.py makemigrations
  python manage.py migrate
  ```

- 启动项目:
  ```
  python manage.py runserver
  ```

## 4. 写在最后
- 此项目是为时两周的课程作业，由于时间比较紧张(因为本人懒，所以第二周才开始)，代码写得比较乱并且基本没有注释。    
- ~~秉持着能跑就行的精神~~，部分冗杂的代码也懒得删了(以后一定改)，遇到什么问题或者BUG可以在issues提。    
- 最后，喜欢的话请给我点个star⭐吧~
  
  

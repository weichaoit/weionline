from datetime import datetime

from django.db import models
from organization.models import CourseOrg
from organization.models import Teacher
from DjangoUeditor.models import UEditorField
# Create your models here.


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg,verbose_name='课程机构',null=True,blank=True,on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=64,verbose_name='课程名')
    desc = models.CharField(max_length=500,verbose_name='课程描述')
    # detail = UEditorField(verbose_name='课程详情',width=600,height=300,imagePath='course/ueditor/',filePath='course/ueditor/',default='')
    detail = models.CharField(verbose_name='课程详情',max_length=600,default='')
    teacher = models.ForeignKey(Teacher,verbose_name='老师',on_delete=models.DO_NOTHING,null=True,blank=True)
    degree = models.CharField(verbose_name='难度',choices=(('cj','初级'),('zj','中级'),('gj','高级')),max_length=10)
    learn_times = models.IntegerField(default=0,verbose_name='学习时长(分钟数)')
    students = models.IntegerField(default=0,verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0,verbose_name='收藏人数')
    image = models.ImageField(upload_to='course/image/%Y/%m/%d',verbose_name='课程封面',max_length=200,default='',null=False)
    click_nums = models.IntegerField(default=0,verbose_name='点击数')
    category = models.CharField(verbose_name='课程类别',max_length=20,default='后端开发')
    tag = models.CharField(verbose_name='课程标签',default='',max_length=10)
    create_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')
    youneed = models.CharField(verbose_name='课程须知',max_length=300,default='')
    teacher_tell = models.CharField(verbose_name='老师告知',max_length=300,default='')

    class Meta:
        verbose_name='课程'
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        "获取课程章节数"
        return self.lesson_set.all().count()

    def get_learn_users(self):
        '''获取学习用户人数'''
        return self.usercourse_set.all()[:5]

    def get_course_lesson(self):
        '''获取课程章节信息'''
        return self.lesson_set.all()

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course,verbose_name='课程',on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100,verbose_name='章节名')
    create_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name='章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_lesson_video(self):
        return self.video_set.all()


class Video(models.Model):
    lesson = models.ForeignKey(Lesson,verbose_name='章节',on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100,verbose_name='视频名称')
    url = models.CharField(max_length=200,verbose_name='视频地址',default='')
    learn_times = models.IntegerField(default=0,verbose_name='学习时长(分钟数)')
    create_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course,verbose_name='课程',on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100,verbose_name='名称')
    download = models.FileField(upload_to='course/resource/%Y/%m/%d',verbose_name='资源')
    create_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name

# _*_ coding: utf-8 _*_
__author__ = 'chaoge'
__date__ = '2018/5/22 12:28'
import xadmin
from .models import Course,Lesson,Video,CourseResource


class LessonInline(object):
    model = Lesson
    extra = 0


class CourseResourceInline(object):
    model = CourseResource
    extra = 0


class CourseAdmin(object):
    list_display = ['name','desc','detail','degree','detail','learn_times','students','fav_nums','image','click_nums','create_time']
    search_fields = ['name','desc','detail','degree','detail']
    list_filter = ['name','degree','detail','students','fav_nums','click_nums','create_time']
    model_icon = 'fa fa-book'
    inlines = [LessonInline,CourseResourceInline]
    list_editable = ['name', 'desc']
    refresh_times = [3,5]
    style_fields = {'detail':'ueditor'}


class LessonAdmin(object):
    list_display = ['course','name','create_time']
    search_fields = ['course__name','name']
    list_filter =['course__name','name','create_time']

class VideoAdmin(object):
    list_display = ['lesson','name','create_time']
    search_fields = ['lesson__name','name']
    list_filter =['lesson__name','name','create_time']


class CourseResourceAdmin(object):
    list_display = ['course','name','download','create_time']
    search_fields = ['course__name','name']
    list_filter =['course__name','name','create_time']


xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(CourseResource,CourseResourceAdmin)
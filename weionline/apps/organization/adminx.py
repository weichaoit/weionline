# _*_ coding: utf-8 _*_
__author__ = 'chaoge'
__date__ = '2018/5/22 14:44'

import xadmin
from .models import CityDict,CourseOrg,Teacher

class CityDictAdmin(object):
    list_display = ['name', 'desc','add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc','add_time']


class CourseOrgAdmin(object):
    list_display = ['name', 'desc','click_nums','fav_nums','image','address','city','add_time']
    search_fields = ['name', 'desc','address','city__name']
    list_filter = ['name', 'desc','click_nums','fav_nums','address','city__name','add_time']


class TeacherAdmin(object):
    list_display = ['org','name','work_years','work_company','work_position','points','click_nums','fav_nums']
    search_fields = ['name', 'desc','work_company','work_position','points']
    list_filter = ['org__name','name','work_years','work_company','work_position','points','click_nums','fav_nums']


xadmin.site.register(CityDict,CityDictAdmin)
xadmin.site.register(CourseOrg,CourseOrgAdmin)
xadmin.site.register(Teacher,TeacherAdmin)

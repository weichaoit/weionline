from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import CourseOrg,CityDict
from .forms import UserAskForm
from operation.models import UserFavorite

# Create your views here.

def org_decorator(func):
    def view_func(request,*args,**kwargs):
        global cont
        cont = {'active':'org'}

        return func(request,*args,**kwargs)

    return view_func


class OrgView(View):

    @org_decorator
    def get(self,request):


        title = '课程机构列表'
        global cont
        cont['title'] = title

        # 总数据
        all_org = CourseOrg.objects.all()
        # 课程机构/地区 筛选
        city_id = request.GET.get('city', '')
        if city_id:
            all_org = all_org.filter(city_id=city_id)

        category = request.GET.get('category', '')
        if category:
            all_org = all_org.filter(category=category)


        # 筛选条件
        cont['city_id'] = city_id
        cont['category'] = category

        # 城市
        all_city = CityDict.objects.all()
        cont['all_city'] = all_city

        # 排序
        sort = request.GET.get('sort','')
        if sort:
            if sort == 'student':
                all_org = all_org.order_by('-student')
            elif sort == 'course':
                all_org = all_org.order_by('-course_nums')

        cont['sort'] = sort
        # 统计机构总数
        org_count = all_org.count()
        cont['org_count'] = org_count

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_org,3, request=request)

        all_org = p.page(page)
        cont['all_org'] = all_org

        # print(cont)
        return render(request,'org/org-list.html',cont)


class AddUserAskView(View):
    '''
    添加学习咨询信息
    这是一个ajax请求的方法
    '''
    def post(self,request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            # 直接就添加到数据库了
            user_ask = userask_form.save(commit=True)
            return JsonResponse({'status':'ok'})
        else:
            return JsonResponse({'status':'no','msg':'添加出错','errors':userask_form.errors})


class OrgHomeView(View):
    '''
    机构首页
    '''
    def get(self,request,org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:3]
        is_fav = False
        if UserFavorite.objects.filter(user=request.user,fav_id=course_org.id,fav_type=2):
            is_fav = True
        return render(request,'org/org-detail-homepage.html',{
            'course_org': course_org,
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'org_id': org_id,
            'org_path': 'org_home',
            'is_fav': is_fav,
        })

class OrgCourseView(View):
    '''课程机构'''
    def get(self,request,org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_course = course_org.course_set.all()
        is_fav = False
        if UserFavorite.objects.filter(user=request.user,fav_id=course_org.id,fav_type=2):
            is_fav = True
        return render(request,'org/org-detail-course.html',{
            'all_course':all_course,
            'course_org': course_org,
            'org_id': org_id,
            'org_path': 'org_course',
            'is_fav': is_fav,
        })


class OrgDescView(View):
    '''机构介绍'''
    def get(self,request,org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        is_fav = False
        if UserFavorite.objects.filter(user=request.user,fav_id=course_org.id,fav_type=2):
            is_fav = True
        return render(request, 'org/org-detail-desc.html', {
            'course_org': course_org,
            'org_id': org_id,
            'org_path': 'org_desc',
            'is_fav': is_fav,
        })


class OrgTeacherView(View):
    '''机构讲师'''
    def get(self,request,org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()
        is_fav = False
        if UserFavorite.objects.filter(user=request.user,fav_id=course_org.id,fav_type=2):
            is_fav = True
        return render(request,'org/org-detail-teachers.html',{
            'course_org': course_org,
            'all_teachers': all_teachers,
            'org_id': org_id,
            'org_path': 'org_teacher',
            'is_fav': is_fav,
        })


class AddFavView(View):
    '''用户收藏课程'''
    def post(self,request):
        fav_id = request.POST.get('fav_id',0)
        fav_type = request.POST.get('fav_type','')
        # 是否收藏
        is_fav = False

        if not request.user.is_authenticated:

            return JsonResponse({'status':'no','msg':'用户未登录'})

        # 查看用户是否收藏
        exist_records = UserFavorite.objects.filter(user=request.user,fav_id=int(fav_id),fav_type=fav_type)
        if exist_records:
            # 如果有收藏该请求代表删除收藏
            exist_records.delete()
            return JsonResponse({'status': 'yes','msg':'收藏'})
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = fav_type
                user_fav.save()
                return JsonResponse({'status':'yes','msg':'已收藏'})
            else:
                return JsonResponse({'status':'no','msg':'收藏出错'})





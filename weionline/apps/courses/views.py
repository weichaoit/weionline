from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator,PageNotAnInteger
from django.http import JsonResponse

from .models import Course,CourseResource,Video
from operation.models import UserFavorite,CourseComment,UserCourse
from untils.mixin_untils import LoginRequiredMixin


# Create your views here.


class CourseListView(View):
    '''
    课程列表
    '''
    def get(self,request):
        all_course = Course.objects.all()
        # 热门课程
        hot_course = all_course.order_by('-click_nums')[:3]
        # 排序
        sort = request.GET.get('sort','')
        if sort:
            if sort == 'hot':
                all_course = all_course.order_by('-click_nums')
            elif sort == 'students':
                all_course = all_course.order_by('-students')

        # 分页
        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_course,4,request=request)

        course = p.page(page)

        return render(request,'course/course-list.html',{
            'all_course': course,
            'sort': sort,
            'hot_course': hot_course,
            'active':'course',
        })


class CourseDetailView(View):
    '''
    课程详情页面
    '''
    def get(self,request,course_id):
        course = Course.objects.get(id=course_id)
        # 增加课程点击数
        course.click_nums += 1
        course.save()

        # 用户是否收藏课程/机构
        is_course_fav = False
        is_org_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user.id,fav_id=course_id,fav_type=1):
                is_course_fav =True

            if UserFavorite.objects.filter(user=request.user.id,fav_id=course.course_org.id,fav_type=2):
                is_org_fav = True

        # 推荐课程标签
        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:1]
        else:
            relate_courses = []
        return render(request,'course/course-detail.html',{
            'course': course,
            'active': 'course',
            'relate_course': relate_courses,
            'is_course_fav': is_course_fav,
            'is_org_fav': is_org_fav,
        })


class CourseInfoView(LoginRequiredMixin,View):
    '''
    课程章节信息
    '''
    def get(self,request,course_id):
        course = Course.objects.get(id=course_id)
        # 查询该用户是否有学习该课程
        user_course_learn = UserCourse.objects.filter(user=request.user,course=course)
        if not user_course_learn:
            # 如果没有改记录则添加记录
            user_course = UserCourse(user=request.user,course=course)
            user_course.save()
        user_courses = UserCourse.objects.filter(course=course)
        # 学习该课程的用户id
        user_ids = [user_course.user.id for user_course in user_courses]
        # 获取所有课程信息
        all_user_course = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.course.id for user_course in all_user_course]
        relate_course = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]
        all_resource = CourseResource.objects.filter(id=course_id)
        return render(request,'course/course-video.html',{
            'course': course,
            'active': 'course',
            'all_resource': all_resource,
            'relate_course': relate_course,

        })


class CourseCommentView(LoginRequiredMixin,View):
    '''
    课程评论
    '''
    def get(self,request,course_id):
        course = Course.objects.get(id=course_id)
        all_resource = CourseResource.objects.filter(id=course_id)
        all_comment = CourseComment.objects.filter(course=course)
        return render(request,'course/course-comment.html',{
            'course': course,
            'active': 'course',
            'all_resource': all_resource,
            'all_comment': all_comment,
        })


class AddCommentView(View):
    '''
    用户添加课程评论
    '''
    def post(self,request):
        if not request.user.is_authenticated:
            return JsonResponse({'status':'0','msg':'用户未登录'})

        course_id = int(request.POST.get('course_id',0))
        comments = request.POST.get('comments','')
        if course_id > 0 and comments:
            course_comment = CourseComment()
            course = Course.objects.get(id=course_id)
            course_comment.course = course
            course_comment.comment = comments
            course_comment.user = request.user
            course_comment.save()
            return JsonResponse({'status':'1','msg':'添加成功'})
        else:
            return JsonResponse({'status':'0','msg':'添加失败'})


class VideoPlayView(View):
    def get(self,request,video_id):
        video = Video.objects.get(id=video_id)
        course = video.lesson.course
        # 查询该用户是否有学习该课程
        user_course_learn = UserCourse.objects.filter(user=request.user,course=course)
        if not user_course_learn:
            # 如果没有改记录则添加记录
            user_course = UserCourse(user=request.user,course=course)
            user_course.save()
        user_courses = UserCourse.objects.filter(course=course)
        # 学习该课程的用户id
        user_ids = [user_course.user.id for user_course in user_courses]
        # 获取所有课程信息
        all_user_course = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.course.id for user_course in all_user_course]
        relate_course = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]
        all_resource = CourseResource.objects.filter(id=course.id)
        return render(request,'course/course-play.html',{
            'course': course,
            'active': 'course',
            'all_resource': all_resource,
            'relate_course': relate_course,
            'video': video,
        })
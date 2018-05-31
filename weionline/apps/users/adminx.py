import xadmin
from xadmin import views

from .models import EmailVerifyRecord,Banner

class BaseSetting(object):
    '''后台主题设置'''
    enable_themes = True    # 打开后台主题选项
    use_bootswatch = True


class GlobalSettings(object):
    '''后台全局样式设置'''
    site_title = '在线教育后台管理系统'   # 后台title
    site_footer = 'weichaoit@163.com'   # 后台底部信息
    menu_style = 'accordion'    # 配置可折叠菜单


class EmailVerifyRecordAdmin(object):
    list_display = ['code','email','send_type','send_time']
    search_fields = ['code','email']
    list_filter = ['code','email','send_type','send_time']


class BannerAdmin(object):
    list_display = ['title','image','url','index','create_time']
    search_fields = ['title','image','url','index']
    list_filter = ['title','image','url','index','create_time']


xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSettings)
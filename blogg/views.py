from django.shortcuts import render,HttpResponse,redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from functools import wraps
from geetest import GeetestLib
from django.db.models import Count
import calendar,time,datetime
import json
from bs4 import BeautifulSoup
# Create your views here.

# 请在官网申请ID使用，示例ID不可使用
pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"

# 登录 包括验证码弹框
def login(request):
    if request.method == "POST":
        ret = {'status':0,'msg':''}
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 获取极验 滑动验证码相关的参数
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]
        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        if result:
            # 验证码正确
            # 利用auth模块做用户名和密码的校验
            user = auth.authenticate(username=username, password=password)
            if user:
                # 用户名密码正确
                # 给用户做登录
                auth.login(request, user)
                ret["msg"] = "/blogg/index/"
            else:
                # 用户名密码错误
                ret["status"] = 1
                ret["msg"] = "用户名或密码错误！"
        else:
            ret["status"] = 1
            ret["msg"] = "验证码错误"

        return JsonResponse(ret)
    return render(request,'login.html')


# 注销用户
def logout(request):
    auth.logout(request)
    return redirect('/blogg/index/')
#  主页面
def index(request):
    articles = models.Article.objects.all().order_by('create_date').reverse()

    return render(request,'index.html',{'articles':articles})




# 获取验证码图片的视图
def get_valid_img(request):
    # with open("valid_code.png", "rb") as f:
    #     data = f.read()
    # 自己生成一个图片
    from PIL import Image, ImageDraw, ImageFont
    import random

    # 获取随机颜色的函数
    def get_random_color():
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

    # 生成一个图片对象
    img_obj = Image.new(
        'RGB',
        (220, 35),
        get_random_color()
    )
    # 在生成的图片上写字符
    # 生成一个图片画笔对象
    draw_obj = ImageDraw.Draw(img_obj)
    # 加载字体文件， 得到一个字体对象
    font_obj = ImageFont.truetype("static/font/kumo.ttf", 28)
    # 开始生成随机字符串并且写到图片上
    tmp_list = []
    for i in range(5):
        u = chr(random.randint(65, 90))  # 生成大写字母
        l = chr(random.randint(97, 122))  # 生成小写字母
        n = str(random.randint(0, 9))  # 生成数字，注意要转换成字符串类型

        tmp = random.choice([u, l, n])
        tmp_list.append(tmp)
        draw_obj.text((20+40*i, 0), tmp, fill=get_random_color(), font=font_obj)

    print("".join(tmp_list))
    print("生成的验证码".center(120, "="))
    # 不能保存到全局变量
    # global VALID_CODE
    # VALID_CODE = "".join(tmp_list)

    # 保存到session
    request.session["valid_code"] = "".join(tmp_list)
    # 加干扰线
    # width = 220  # 图片宽度（防止越界）
    # height = 35
    # for i in range(5):
    #     x1 = random.randint(0, width)
    #     x2 = random.randint(0, width)
    #     y1 = random.randint(0, height)
    #     y2 = random.randint(0, height)
    #     draw_obj.line((x1, y1, x2, y2), fill=get_random_color())
    #
    # # 加干扰点
    # for i in range(40):
    #     draw_obj.point((random.randint(0, width), random.randint(0, height)), fill=get_random_color())
    #     x = random.randint(0, width)
    #     y = random.randint(0, height)
    #     draw_obj.arc((x, y, x+4, y+4), 0, 90, fill=get_random_color())

    # 将生成的图片保存在磁盘上
    # with open("s10.png", "wb") as f:
    #     img_obj.save(f, "png")
    # # 把刚才生成的图片返回给页面
    # with open("s10.png", "rb") as f:
    #     data = f.read()

    # 不需要在硬盘上保存文件，直接在内存中加载就可以
    from io import BytesIO
    io_obj = BytesIO()
    # 将生成的图片数据保存在io对象中
    img_obj.save(io_obj, "png")
    # 从io对象里面取上一步保存的数据
    data = io_obj.getvalue()
    return HttpResponse(data)

# 处理极验 获取验证码的视图
def get_geetest(request):
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)

# 注册
from blogg import forms
from blogg import models
def register(request):
    # post 请求
    if request.method == 'POST':
        print('i am coming')
        ret = {'status':0,'msg':'/blogg/register/'}
        regform = forms.RegForms(request.POST)
        print(request.POST)
        if regform.is_valid():
            user = regform.cleaned_data.get('username')
            pwd = regform.cleaned_data.get('password')
            email = regform.cleaned_data.get('email')
            avatar = request.FILES.get('avatar')
            print('avatar=',avatar)
            userdb = models.UserInfo.objects.filter(username=user)
            if userdb :
                pass
            else:
                regform.cleaned_data.pop('repwd')
                models.UserInfo.objects.create_user(username=user,password=pwd,email=email,avatar=avatar)
                ret['msg'] = '/blogg/login/'
            return JsonResponse(ret)
            # return redirect('/blogg/login/')
        else:
            ret['status'] =1
            ret['msg'] = regform.errors
            return JsonResponse(ret)
            # return render(request,'register.html',{'regform':regform})
    # get请求
    regform = forms.RegForms()
    return render(request,'register.html',{'regform':regform})


#  个人主页
def selfhome(request,username):
    # 获取用户
    print(username)
    user = models.UserInfo.objects.filter(username = username).first()
    print(user)
    if not user:
        return HttpResponse('404')
    user_blog = user.blog
    # 根据用户获取文章
    article = models.Article.objects.filter(user = user)
    # 根据用户获取文章分类
    cate_list = models.Article.objects.values('category').annotate(cate_count = Count('nid')).filter(user=user).values('category__title','cate_count')
    # 获取标签和标签数
    tag_list = models.Tag.objects.filter(blog=user_blog).annotate(c = Count('article'))
    print(tag_list)
    # 按时间分组
    time_group = models.Article.objects.filter(user=user).extra(select={"t":"date_format(create_date,'%%Y-%%m')"}).values('t').annotate(c = Count('nid')).values('t','c')
    # 日历
    tm = time.localtime(time.time())
    ret = time.strftime('%Y-%m',tm).split('-')

    calendarshow = calendar.month(int(ret[0]),int(ret[1]))
    return render(request,'selfhome.html',
                  {
                      'username':username,
                      'user_blog':user_blog,
                      'articles':article,
                      'cate_list':cate_list,
                      'tag_list':tag_list,
                      'time_group':time_group,
                      'calendarshow':calendarshow,
                  })

# 获取左侧菜单栏
def get_left_bar(username):
    user = models.UserInfo.objects.filter(username=username).first()
    blog = user.blog
    cate_list = models.Article.objects.values('category').annotate(cate_count=Count('nid')).filter(user=user).values(
        'category__title', 'cate_count')
    # 获取标签和标签数
    tag_list = models.Tag.objects.filter(blog=blog).annotate(c=Count('article'))
    print(tag_list)
    # 按时间分组
    time_group = models.Article.objects.filter(user=user).extra(select={"t": "date_format(create_date,'%%Y-%%m')"}).values(
        't').annotate(c=Count('nid')).values('t', 'c')
    # 日历
    tm = time.localtime(time.time())
    ret = time.strftime('%Y-%m', tm).split('-')
    calendarshow = calendar.month(int(ret[0]), int(ret[1]))
    return cate_list,tag_list,time_group,calendarshow
# 文章详细内容
def articleDtl(request,username,pk):
    user = models.UserInfo.objects.filter(username=username).first()
    blog = user.blog
    article = models.ArticleDetail.objects.filter(article=pk).first()
    print(article.pk)
    cate_list,tag_list,time_group,calendarshow=get_left_bar(username)

    # 评论列表
    comment_List = models.Comment.objects.filter(article=pk,parent_comment=None).reverse()
    cm2 = models.Comment.objects.filter(article=pk)

    return render(request,'articleDetail.html',{'article':article,'user_blog':blog,
                                                'cate_list': cate_list,
                                                'tag_list': tag_list,
                                                'time_group': time_group,
                                                'calendarshow': calendarshow,
                                                'comment_List':comment_List
                                                })

# 点赞处理
from django.db.models import F
def up_down(request):
    print(request.POST)
    is_up = json.loads(request.POST.get('is_up'))
    article_id  = request.POST.get('article_id')
    user = request.user
    response = {'status':True}
    if user.username:
        try:
            models.ArticleUpDown.objects.create(user = user,article_id = article_id,is_up = is_up)
            if is_up:
                models.Article.objects.filter(pk= article_id).update(up_count= F('up_count')+1 )
            else:
                models.Article.objects.filter(pk=article_id).update(down_count=F('down_count') + 1)
        except Exception as e:
            response['status'] = False
            response['first_action'] = models.ArticleUpDown.objects.filter(user = user,article_id = article_id).first().is_up
    else:
        response['islogin'] = False
    return JsonResponse(response)

#  评论
def comment(request):
    print(request.POST)
    sign = request.POST.get('sign') #　根评论标志位
    user = request.user
    content = request.POST.get('content')
    article_id = request.POST.get('article_id')
    response = {'tat':''}
    print(sign)
    # 用户登录并且根评论，添加到数据库
    if user.username and content:
        if not sign:
            commmet_obj =  models.Comment.objects.create(user=user,content=content,article_id=article_id)
            print(commmet_obj.user.avatar)
        else:
            commmet_obj = models.Comment.objects.create(user=user, content=content, article_id=article_id,parent_comment_id=sign)
            response['pa_name'] = commmet_obj.parent_comment.user.username
            response['pa_content'] = commmet_obj.parent_comment.content
            response['pa_createdate'] = commmet_obj.parent_comment.create_date
            response['pa_avatar'] = str(commmet_obj.parent_comment.user.avatar)
        response['content'] = commmet_obj.content
        response['create_date'] = commmet_obj.create_date
        response['avatar'] = str(commmet_obj.user.avatar)
        response['id'] = commmet_obj.pk
        print(commmet_obj.pk)

    return JsonResponse(response)


# 添加文章
def add_article(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        # 将html标签过滤掉 取出前100个
        bs = BeautifulSoup(content,'html.parser')
        # 过滤非法标签
        for tag in bs.find_all():
            if tag.name in ['script']:
                tag.decompose()
        desc = str(bs)[0:100]
        user = request.user
        #  保存到数据库
        article = models.Article.objects.create(
            user=user,
            title=title,
            desc=desc
        )
        models.ArticleDetail.objects.create(
            content = str(bs),
            article = article
        )
        return redirect('/blogg/index/')
    return render(request,'add_article.html')

# 上传添加文章时的文件
def upload(request):
    from blog import settings
    import json
    import os
    obj = request.FILES.get('imgFile')
    path = os.path.join(settings.MEDIA_ROOT,'add_article_img',obj.name)
    with open(path,'wb') as f:
        for line in obj:
            f.write(line)
    res = {
        'error':0,
        'url':'/media/add_article_img/'+obj.name
    }
    return HttpResponse(json.dumps(res))


# 显示评论树
def comment_tree(request,article_id):

    ret = models.Comment.objects.filter(article = article_id).order_by('create_date').reverse()
    ret = list(ret.values('pk','content','parent_comment','user'))
    print(ret)

    return JsonResponse(ret,safe=False)

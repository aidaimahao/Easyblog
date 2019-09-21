import os
if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')
    import django
    django.setup()

    from blogg import models
    # 添加用户
    # obj = [models.UserInfo(username='tom{}'.format(i),
    #                        password='12345{}'.format(i),
    #                        )for i in range(100)]
    # models.UserInfo.objects.bulk_create(obj,10)
    from bs4 import BeautifulSoup

    s = """
    <a class="videoNewsLeft" href="http://video.sina.com.cn/p/ent/2019-06-26/detail-ihytcerk9362455.d.html?opsubject_id=enttopnews" target="_blank">街舞：易烊千玺表白AC</a>
    """
    text = BeautifulSoup(s,'html.parser')
    print(text.text)

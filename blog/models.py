from django.db import models

# 分类列表
BIG_CLASS_LIST = [
    ('科普', '科普'), ('财经', '财经'), ('健康', '健康'), ('游戏', '游戏'), ('美食', '美食'), ('读书', '读书'), ('设计', '设计'),
    ('股市', '股市'), ('电影', '电影'), ('汽车', '汽车'), ('军事', '军事'), ('情感', '情感'), ('旅游', '旅游'), ('艺术', '艺术'),
]


# 用户表
class User(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=20)
    password = models.CharField(verbose_name='密码', max_length=256)
    email = models.EmailField(verbose_name='邮箱', max_length=254)
    status = models.BooleanField(verbose_name='状态', default=False)
    active = models.BooleanField(verbose_name='激活', default=False)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = '用户'


# 个人资料表
class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
    nickname = models.CharField(verbose_name='昵称', max_length=50)
    name = models.CharField(verbose_name='姓名', max_length=64, null=True, blank=True)
    sex = models.CharField(verbose_name='性别', choices=[('M', '男'), ('W', '女')], max_length=1, default='M')
    birthday = models.DateField(verbose_name='生日', null=True, blank=True)
    job = models.CharField(verbose_name='职业', max_length=128, null=True, blank=True)
    education = models.CharField(verbose_name='学历', max_length=16, choices=[
        ('小学', '小学'),
        ('初中', '初中'),
        ('高中', '高中'),
        ('大专', '大专'),
        ('本科', '本科'),
        ('研究生', '研究生'),
    ], null=True, blank=True)
    intro = models.CharField(verbose_name='简介', max_length=128, null=True, blank=True)
    icon = models.ImageField(verbose_name='头像', upload_to='icons/%Y/%m/%d', null=True, blank=True)

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name_plural = '个人资料'


# 个人指数表
class Exponent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
    fans = models.TextField(verbose_name='粉丝ID', null=True, blank=True)
    fans_num = models.IntegerField(verbose_name='粉丝数量', default=0)
    concern = models.TextField(verbose_name='关注ID', null=True, blank=True)
    concern_num = models.IntegerField(verbose_name='关注数量', default=0)
    collect = models.TextField(verbose_name='收藏ID', null=True, blank=True)
    collect_num = models.IntegerField(verbose_name='收藏数量', default=0)
    publish = models.TextField(verbose_name='发布ID', null=True, blank=True)
    publish_num = models.IntegerField(verbose_name='发布数量', default=0)
    reply_num = models.IntegerField(verbose_name='回复数量', default=0)
    zan_num = models.IntegerField(verbose_name='点赞数量', default=0)
    view_num = models.IntegerField(verbose_name='访问数量', default=0)

    class Meta:
        verbose_name_plural = '个人指数'


# 话题表
class Topic(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
    title = models.CharField(max_length=200)
    reply = models.TextField(verbose_name='回复ID', null=True, blank=True)
    reply_num = models.IntegerField(verbose_name='回复数量', default=0)
    view_num = models.IntegerField(verbose_name='访问数量', default=0)
    pub_time = models.DateTimeField(verbose_name='发布时间', auto_now_add=True)
    big_class = models.CharField(verbose_name='分类', max_length=32, choices=BIG_CLASS_LIST)
    type = models.CharField(verbose_name='类型', choices=[('text', '文本'), ('image', '图片'), ('audio', '音频')], max_length=5)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '话题'
        ordering = ['-pub_time']


# 文本选项表
class ChoiceText(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name='话题')
    text = models.CharField(verbose_name='文本', max_length=200)
    vote = models.IntegerField(verbose_name='票数', default=0)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = '文本选项'


# 图片选项表
class ChoiceImage(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name='话题')
    image = models.ImageField(verbose_name='图片', upload_to='topic/image/%Y/%m/%d')
    vote = models.IntegerField(verbose_name='票数', default=0)

    def __str__(self):
        return self.image

    class Meta:
        verbose_name_plural = '图片选项'


# 音频选项表
class ChoiceFile(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name='话题')
    audio = models.FileField(verbose_name='音频', upload_to='topic/audio/%Y/%m/%d')
    vote = models.IntegerField(verbose_name='票数', default=0)

    def __str__(self):
        return self.audio

    class Meta:
        verbose_name_plural = '音频选项'


# 评论表
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name='话题')
    content = models.TextField(verbose_name='内容')
    rep_time = models.DateTimeField(verbose_name='回复时间', auto_now_add=True)
    zan_num = models.IntegerField(verbose_name='点赞', default=0)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name_plural = '评论'
        ordering = ['-rep_time']
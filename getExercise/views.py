from django.shortcuts import render, redirect
from getExercise.models import Article, Comment, Ticket
from getExercise.form import CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login
from getExercise.form import LoginForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from  django.core.exceptions import ObjectDoesNotExist

# {} 集合
# [] 列表
'''
有类别的主页
def index(request):
    queryset = request.GET.get('tag')
    # 如果queryset有值就按值去查结果, 如果为空,则获取全部数据
    if queryset:
        article_list = Article.objects.filter(tag=queryset)
    else:
        article_list = Article.objects.all()
    context = {}
    index_page = render(request, 'index.html', context)
    context['article_list'] = article_list
    return index_page
'''

# 有默认分页且在筛选文章类别时也分页的主页
def index(request):
    context = {}
    queryset = request.GET.get('tag')
    if queryset:
        article_list = Article.objects.filter(tag=queryset)
    else:
        article_list = Article.objects.all()
    # if tag is None:
    #     article_list = Article.objects.all()
    #
    # if tag == 'life':
    #     article_list = Article.objects.filter(tag='life')
    # elif tag == 'tech':
    #     article_list = Article.objects.filter(tag='tech')
    # else:
    #     article_list = Article.objects.all()

    page_robot = Paginator(article_list, 2)
    page_num = request.GET.get('page')
    try:
        article_list = page_robot.page(page_num)
    except EmptyPage:
        article_list = page_robot.page(page_robot.num_pages)
        # 也可以设置页面404,找不到
        # raise Http404('EmptyPage!')
    except PageNotAnInteger:
        article_list = page_robot.page(1)

    context['article_list'] = article_list
    return render(request, 'index.html', context)

# 获取评论最新所有的数据并展示评论详情,
def detail(request, id, error_form=None):
    context = {}
    # 显示文章的投票人,投票信息
    vid_info = Article.objects.get(id=id)
    voter_id = request.user.profile.id
    try:
        user_ticket_for_this_article = Ticket.objects.get(voter_id=voter_id, article_id=id)
        context['user_ticket'] = user_ticket_for_this_article
    except:
        pass

    context['vid_info'] = vid_info

    # 显示最优评论
    form = CommentForm
    a = Article.objects.get(id=id)
    best_comment = Comment.objects.filter(best_comment=True, belong_to=a)
    if best_comment:
        context['best_comment'] = best_comment[0]
    article = Article.objects.get(id=id)
    context['article'] = article
    if error_form is not None:
        context['form'] = error_form
    else:
        context['form'] = form
    return render(request, 'detail.html', context)


# 提交评论
def detail_comment(request, id):
    form = CommentForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']
        comment = form.cleaned_data['comment']
        a = Article.objects.get(id=id)
        c = Comment(name=name, comment=comment, belong_to=a)
        c.save()
    else:
        return detail(request, id, error_form=form)

    return redirect(to='detail', id=id)

def detail_vote(request, id):
    voter_id = request.user.profile.id

    try:
        user_ticket_for_this_article = Ticket.objects.get(voter_id=voter_id, article_id=id)
        user_ticket_for_this_article.choice = request.POST['vote']
        user_ticket_for_this_article.save()
    except ObjectDoesNotExist:
        new_ticket = Ticket(voter_id=voter_id, article_id=id, choice=request.POST['vote'])
        new_ticket.save()

    return redirect(to='detail', id=id)

def index_login(request):
    context = {}
    if request.method == 'GET':
        form = AuthenticationForm

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
           login(request, form.get_user())
           return redirect(to='index')
    context['form'] = form
    return render(request, 'login.html', context)

def index_register(request):
    context = {}
    if request.method == 'GET':
        form = UserCreationForm
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='login')
    context['form'] = form
    return render(request, 'register.html', context)
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm
from .models import Post
from django.views.generic import ListView
from django.core.mail import send_mail

#! ViewsList method
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'blog_app/post/list.html'

def post_list(request):
    # posts = Post.published.all() 
    #! pagination
    object_list = Post.published.all()
    paginator = Paginator(object_list, 2)
    page = request.GET.get('num_page') #? num_page in html
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1) #? jaka strona bedzie wyswietliac pierwsza
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog_app/post/list.html',{'page': page, 'posts': posts})

def post_detail(request, year, month, day, post):  #* args, kwargs ???
    post = get_object_or_404(Post, slug=post, 
                                status='published', 
                                publish__year=year, 
                                publish__month=month, 
                                publish__day=day)
    return render(request, 'blog_app/post/detail.html', {'post': post})

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
        
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) zacheca do preczytania "{}"'.format(cd['name'], cd['email'], post.title)
            massage = 'Przecytaj post "{}" na stronie {}\n\n\tKomentarz dodany przez {}: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, massage, 'aramegabara@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog_app/post/share.html', {'post': post, 'form': form, 'sent': sent})
    
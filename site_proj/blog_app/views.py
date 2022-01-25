from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm, CommentForm
from .models import Post, Comment
from django.views.generic import ListView
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count

#! ViewsList method
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'blog_app/post/list.html'

def post_list(request, tag_slug=None):
    # posts = Post.published.all() 
    #! pagination
    object_list = Post.published.all()
    tag = None
    #! tags
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list, 4)
    page = request.GET.get('num_page') #? num_page in html
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1) #? jaka strona bedzie wyswietliac pierwsza
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog_app/post/list.html',{'page': page, 'posts': posts, 'tag': tag})

def post_detail(request, year, month, day, post):  #* args, kwargs ???
    post = get_object_or_404(Post, slug=post, 
                                status='published', 
                                publish__year=year, 
                                publish__month=month, 
                                publish__day=day)
    #! comments
    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post_id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    return render(request, 'blog_app/post/detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})


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
    
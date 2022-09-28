from django.shortcuts import render, redirect
from .models import TweetModel
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, TemplateView

# Create your views here.
def home(request):
    user = request.user.is_authenticated #사용자가 인증을 받았는지(로그인 완료)
    if user:
        return redirect('/tweet')
    else:
        return redirect('/sign-in')

# 글쓰기부분
def tweet(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            # all_tweet 이라는 변수안에다가 게시물 데이터 저장시키기
            all_tweet = TweetModel.objects.all().order_by('-created_at')
            return render(request, 'tweet/home.html',{'tweet':all_tweet})
        else:
            return redirect('/sign-in') #직접 온사람들은 다시 퉁겨 나갈것이다
    elif request.method == 'POST':
        # 지금 로그인 되어있는 사용자의 정보 전체를 들고온다
        user = request.user
        content = request.POST.get('my-content','')
        tags = request.POST.get('tag', '').split(',')

        if content == '':
            # 원래있던 데이터도 같이 보여주기 위해
            all_tweet = TweetModel.objects.all().order_by('-created_at')
            return render(request, 'tweet/home.html',{'error':'글은 공백일 수 없습니다.','tweet':all_tweet})
        else:
            # 밑에 4줄 줄이기
            my_tweet = TweetModel.objects.create(author=user, content=content)
            # 여러개의 테그가 리스트 형식으로 올테니 for 구문 돌림
            for tag in tags:
                if tag != '':
                    my_tweet.tags.add(tag)
            my_tweet.save()
            # my_tweet = TweetModel()
            # my_tweet.author = user
            # my_tweet.content = request.POST.get('my-content','')
            # my_tweet.save()
            return redirect('/tweet')

@login_required
def delete_tweet(request,id):
    my_tweet = TweetModel.objects.get(id=id)
    my_tweet.delete()
    return redirect('/tweet')

def tweet_detail(request,id):
    my_tweet = TweetModel.objects.get(id=id)
    tweet_comment = TweetModel.objects.filter(tweet_id=id).order_by('-created_at')
    return render(request, 'tweet/tweet_detail.html',{'tweet':my_tweet, 'comment':tweet_comment})

class TagCloudTV(TemplateView):
    template_name = 'taggit/tag_cloud_view.html'

# 테그가 있으면 보여주겠다.
class TaggedObjectLV(ListView):
    template_name = 'taggit/tag_with_post.html'
    model = TweetModel

    def get_queryset(self):
        return TweetModel.objects.filter(tags__name=self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context
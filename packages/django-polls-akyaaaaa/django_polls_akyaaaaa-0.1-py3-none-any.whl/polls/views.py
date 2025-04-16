import sys

from django.db.models import F
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView

from djangotutorial.dbconn.sqlite_conn import select_db
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.db import connection

from .models import Question, Choice


# Create your views here.
def index(request):
    # return render(request, 'polls/index.html')
    # return HttpResponse(f"<pre>{sys.path}</pre>")
    # latest_question_list = Question.objects.order_by("-pub_date")[:5]
    # output = ", ".join([q.question for q in latest_question_list])
    # return HttpResponse(output)
    return render(request, 'polls/index.html')


def detail(request, question_id):
    # question = get_object_or_404(Question, id=question_id)
    cho = Choice.objects.filter(question_id=question_id)
    # templates路径是省略到当前app下的templates目录（如果有这个目录）
    return render(request, 'polls/detail.html', {'choice': cho})


def all(request):
    # q = Question.objects.all()
    q = select_db(sql="select * from polls_question")
    # templates路径是省略到当前app下的templates目录（如果有这个目录）
    return render(request, 'polls/all.html', {'question': q})


def choice(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    return render(request, 'polls/choice.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # 找到具体的choice对象
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        # 核心逻辑
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})


@csrf_exempt  # 允许跨站请求（仅用于示例，生产环境需更安全的方式）
def vote_ajax(request):
    if request.method == 'POST':
        choice_id = request.POST.get('choice_id')
        try:
            # 获取选项对象并更新投票数
            choice = get_object_or_404(Choice, pk=choice_id)
            choice.votes += 1
            choice.save()

            # 返回更新后的投票数
            return JsonResponse({'votes': choice.votes})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)


class questionListView(ListView):
    # 重写模版名字
    template_name = "polls/all1.html"
    context_object_name = "questionList"
    model = Question

    # 重写get方法
    def get_queryset(self):
        """Return the last five published questions."""
        return self.model.objects.order_by("-pub_date")[:2]


class choiceForVotes(DetailView):
    # 重写模版名字
    template_name = "polls/a.html"
    context_object_name = "cho"
    model = Choice

    def get_object(self, queryset=None):
        # 从 URL 参数中获取 votes
        votes = self.kwargs.get("votes")
        # 根据 votes 字段查找对象
        return get_object_or_404(Choice, votes=votes)

"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from . import views

app_name = 'polls'  # 定义应用的命名空间
urlpatterns = [
    path("", views.index, name="index"),
    path("all/", views.all, name="all"),
    path("all1/", views.questionListView.as_view(), name="all1"),
    path("<int:question_id>/", views.detail, name="detail"),
    path("cho/<int:votes>/", views.choiceForVotes.as_view(), name="choiceForVotes"),

    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("<int:question_id>/choice/", views.choice, name="choice"),
    # 显示投票结果
    path('<int:question_id>/results/', views.results, name='results'),
    path('vote-ajax/', views.vote_ajax, name='vote_ajax'),  # 处理 投票增加的AJAX 请求

]

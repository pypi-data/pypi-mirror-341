# Create your tests here.
import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question, Choice


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question=question_text, pub_date=time)


def create_choice(question, choice_text, votes=0):
    return Choice.objects.create(question=question, choice_text=choice_text, votes=votes)


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        # 创建一个月之后的日期
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)


class PollsViewTest(TestCase):
    def testView(self):
        q1 = create_question('isak', 1)
        c = create_choice(q1, 'Choice 1')
        url = reverse("polls:detail", args=(q1.id,))
        response = self.client.get(url)
        self.assertContains(response, c.choice_text)

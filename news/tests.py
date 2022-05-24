from django.test import TestCase
from .models import Editor,Article,tags
import datetime as dt

# Create your tests here.
class EditorTestClass(TestCase):

    # Set up method
    def setUp(self):
        self.neal= Editor(first_name = 'Neal', last_name ='Waga', email ='neal.waga@student.moringaschool.com')

# Testing  instance
    def test_instance(self):
        self.assertTrue(isinstance(self.neal,Editor))

 # Testing Save Method
    def test_save_method(self):
        self.neal.save_editor()
        editors = Editor.objects.all()
        self.assertTrue(len(editors) > 0)


class ArticleTestClass(TestCase):

    def setUp(self):
        # Creating a new editor and saving it
        self.neal= Editor(first_name = 'Neal', last_name ='Waga', email ='neal.waga@student.moringaschool.com')
        self.neal.save_editor()

        # Creating a new tag and saving it
        self.new_tag = tags(name = 'testing')
        self.new_tag.save()

        self.new_article= Article(title = 'Test Article',post = 'This is a random test Post',editor = self.neal)
        self.new_article.save()

        self.new_article.tags.add(self.new_tag)

    def tearDown(self):
        Editor.objects.all().delete()
        tags.objects.all().delete()
        Article.objects.all().delete()

    # Method that will allow us to get today's news
    def test_get_news_today(self):
        today_news = Article.todays_news()
        self.assertTrue(len(today_news)>0)

    def test_get_news_by_date(self):
        test_date = '2017-03-17'
        date = dt.datetime.strptime(test_date, '%Y-%m-%d').date()
        news_by_date = Article.days_news(date)
        self.assertTrue(len(news_by_date) == 0)
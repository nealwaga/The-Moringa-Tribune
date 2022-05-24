from django.test import TestCase
from .models import Editor,Article,tags

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

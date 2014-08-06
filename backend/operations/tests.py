from django.test import TestCase

from operations.utils import create_workflow, load_workflow

# Create your tests here.
class AnimalTestCase(TestCase):
    def setUp(self):
        pass

    def test_create_workflow(self):
        w_id = create_workflow("sum_and_mul")
        print w_id


    def test_load_workflow(self):
        w_id = create_workflow("sum_and_mul")

        w = load_workflow(w_id)
        self.assertEqual(w.name, "sum_and_mul")
        
        
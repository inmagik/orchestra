from operations.utils import get_registered_op, create_workflow, create_registered_workflow
from orchestra_core import wf_register

from django.test import TestCase


def example_wf_descriptor():
    op1 = get_registered_op('sum')
    op2 = get_registered_op('mul')

    op2.connect_op(op2, "b")
    op1.connect_value(2, "a")
    op1.connect_value(3, "b")
    op2.connect_value(10, "a")

    ops = [op1, op2]

    return ops


# Create your tests here.
class AnimalTestCase(TestCase):
    def setUp(self):
        pass

    def test_create_workflow(self):
        ops = example_wf_descriptor()
        links = []
        wf = create_workflow('testwf', ops, links)

    def test_create_registered_workflow(self):
        wf_register.register_workflow('example_wf_descriptor', example_wf_descriptor)
        wf = create_registered_workflow('example_wf_descriptor')

    def test_run_registered_workflow(self):
        wf_register.register_workflow('example_wf_descriptor2', example_wf_descriptor)
        wf = create_registered_workflow('example_wf_descriptor2')
        wf.run()

    def test_load_workflow(self):
        pass

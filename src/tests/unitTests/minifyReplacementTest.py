import json
import unittest

from controllers.ProcessCodeController import ProcessCodeController
from service.renameStrategies.minifyReplacement import MinifyReplacement


class ProcessCodeControllerTests(unittest.TestCase):
    """
    Test the minify replacement strategy.
    """

    def test_single_call_function_name_length(self):
        r = MinifyReplacement()
        assert len(r.getFunctionName()) == 1

    def test_single_call_variable_name_length(self):
        r = MinifyReplacement()
        assert len(r.getVariableName()) == 1

    def test_single_call_variable_function_name_continuity(self):
        r = MinifyReplacement()
        assert ord(r.getVariableName()) < ord(r.getFunctionName())

    def test_single_call_variable_name_length_upper_limit(self):
        r = MinifyReplacement()
        for n in range(0, 25):
            r.getVariableName()
        assert ord(r.getVariableName()) == 122 and len(r.getFunctionName()) == 2

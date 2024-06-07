from django.test import TestCase
from django.http import QueryDict
from unittest.mock import MagicMock
from ..utils import validate_pagination_params


class TestUtils(TestCase):
    def test_valid_pagination_params(self):
        request = MagicMock()
        request.GET.get.return_value = '10'
        offset, limit = validate_pagination_params(request)
        self.assertEqual(offset, 10)
        self.assertEqual(limit, 10)

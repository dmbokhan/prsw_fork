import pytest
from unittest import mock

from . import UnitTest

from rsaw import RIPEstat
from rsaw.stat.rpki_validation_status import RPKIValidationStatus
from rsaw.stat.looking_glass import LookingGlass
from rsaw.stat.announced_prefixes import AnnouncedPrefixes


class TestRIPEstat(UnitTest):
    def mocked_get(*args):
        """Mock rsaw.api.get()"""

        class MockOutputResponse:
            def __init__(self, path, params):
                self.path = path
                self.params = params

        return MockOutputResponse(*args)

    def test__init__no_params(self):
        ripestat = RIPEstat()
        assert isinstance(ripestat, RIPEstat)

    def test__init__sourceapp(self):
        name = "testapp"
        ripestat = RIPEstat(sourceapp=name)
        assert ripestat.sourceapp is name

    def test__init__data_overload_limit(self):
        limit = "ignore"
        ripestat = RIPEstat(data_overload_limit=limit)
        assert ripestat.data_overload_limit is limit

    def test__init__invalid_data_overload_limit(self):
        with pytest.raises(ValueError):
            RIPEstat(data_overload_limit="invalid-parameter")

    @mock.patch("rsaw.ripe_stat.get", side_effect=mocked_get)
    def test__get_with_sourceapp(self, mock_get):
        app = "under-test"
        ripestat = RIPEstat(sourceapp=app)

        ripestat._get("/test")

        mock_get.assert_called()
        mock_get.assert_called_with("/test", {"sourceapp": app})

    @mock.patch("rsaw.ripe_stat.get", side_effect=mocked_get)
    def test__get_with_data_overload_limit(self, mock_get):
        ripestat = RIPEstat(data_overload_limit="ignore")
        print("debug: " + ripestat.sourceapp)

        ripestat._get("/test")

        mock_get.assert_called()
        mock_get.assert_called_with("/test", {"data_overload_limit": "ignore"})

    def test_announced_prefixes(self):
        assert self.ripestat.announced_prefixes.func == AnnouncedPrefixes

    def test_looking_glass(self):
        assert self.ripestat.looking_glass.func == LookingGlass

    def test_rpki_validation_status(self):
        assert self.ripestat.rpki_validation_status.func == RPKIValidationStatus

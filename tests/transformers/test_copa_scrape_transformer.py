import os
from datetime import datetime

from unittest.mock import call, patch
import pytest

from invisible_flow.globals_factory import GlobalsFactory
from invisible_flow.storage import LocalStorage
from invisible_flow.transformers.copa_scrape_transformer import CopaScrapeTransformer

from tests.helpers.if_test_base import IFTestBase


class TestCopaScrapeTransformer(IFTestBase):

    @pytest.fixture(autouse=True)
    def default_fixture(self):
        with patch('invisible_flow.app.StorageFactory.get_storage') as get_storage_mock:
            get_storage_mock.return_value = LocalStorage()
            self.transformer = CopaScrapeTransformer()

    def test_split_passes(self):
        self.copa = False
        self.no_copa = False
        raw_data = self.transformer.split()
        assert not raw_data['copa'].find(b'BIA') > -1
        assert not raw_data['no_copa'].find(b'COPA') > -1

    def test_upload_to_gcs(self):
        copa_split_csv = os.path.join(IFTestBase.resource_directory, 'copa_scraped_split.csv')
        no_copa_split_csv = os.path.join(IFTestBase.resource_directory, 'no_copa_scraped_split.csv')
        mock_converted_output = {"copa": open(copa_split_csv).read(), "no_copa": open(no_copa_split_csv).read()}
        with patch('invisible_flow.app.StorageFactory.get_storage') as get_storage_mock:
            with patch.object(LocalStorage, 'store_string') as mock:
                get_storage_mock.return_value = LocalStorage()
                self.transformer.upload_to_gcs(mock_converted_output)
        mock.assert_called()

    @patch('invisible_flow.app.GlobalsFactory.get_current_datetime_utc', lambda: datetime(2019, 3, 25, 5, 30, 50, 0))
    def test_transform(self):
        with patch('invisible_flow.app.StorageFactory.get_storage') as get_storage_mock:
            with patch.object(LocalStorage, 'store_string') as store_string_mock:
                with patch('invisible_flow.api.CopaScrape.scrape_copa_ready_for_entity') as mock_scrape_entity:
                    with patch('invisible_flow.api.CopaScrape.scrape_copa_not_in_entity') as mock_scrape_misc:
                        with patch.object(CopaScrapeTransformer, 'save_scraped_data'):
                            with patch.object(CopaScrapeTransformer, 'upload_to_gcs'):
                                get_storage_mock.return_value = LocalStorage()
                                mock_scrape_entity.return_value = b'some content'
                                mock_scrape_misc.return_value = b'some content'
                                CopaScrapeTransformer().transform(None, None)
        self.current_date = GlobalsFactory.get_current_datetime_utc().isoformat(sep='_').replace(':', '-')
        calls = [
            call("copa.csv", b"some content", f'Scrape-{self.current_date}/transformed'),
            call("misc-data.csv", b"some content", f'Scrape-{self.current_date}/transformed')
        ]
        store_string_mock.assert_has_calls(calls)

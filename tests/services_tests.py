
import test_suite

from service import ParserService


class ServicesTests(test_suite.AppEngineTestBase):

    def test_at_hour(self):
        chat_id = 0
        text = "/set at 20:30 Dinner time."
        ok = ParserService.parse_command(chat_id, text)
        self.assertTrue(ok)

    def test_at_hour_one_figure(self):
        chat_id = 0
        text = "/set at 1:30 Sleep time."
        ok = ParserService.parse_command(chat_id, text)
        self.assertTrue(ok)

    def test_at_minute(self):
        chat_id = 0
        text = "/set at 20:30 Dinner time."
        ok = ParserService.parse_command(chat_id, text)
        self.assertTrue(ok)

    def test_at_time_error(self):
        chat_id = 0
        text = "/set at 340:12230 Future time."
        ok = ParserService.parse_command(chat_id, text)
        self.assertFalse(ok)

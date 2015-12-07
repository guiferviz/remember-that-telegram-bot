
import test_suite

from service import SchedulerService


class ServicesTests(test_suite.AppEngineTestBase):

    def test_at_hour(self):
        text = "/set at 20:30 Dinner time."
        ok = SchedulerService.process_task(text)
        self.assertTrue(ok)

    def test_at_hour_one_figure(self):
        text = "/set at 1:30 Sleep time."
        ok = SchedulerService.process_task(text)
        self.assertTrue(ok)

    def test_at_minute(self):
        text = "/set at 20:30 Dinner time."
        ok = SchedulerService.process_task(text)
        self.assertTrue(ok)

    def test_at_time_error(self):
        text = "/set at 340:12230 Future time."
        ok = SchedulerService.process_task(text)
        self.assertFalse(ok)

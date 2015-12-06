

from mock import patch

import main

import test_suite


class HandlersTests(test_suite.AppEngineTestBase):

    @patch('main.BOT')
    def test_set_webhook(self, mock_main_bot):
        """
        Checks telegram bot set webhook is correct.
        """
        self.testapp.get(main.BOT_URL)
        assert mock_main_bot.setWebhook.called

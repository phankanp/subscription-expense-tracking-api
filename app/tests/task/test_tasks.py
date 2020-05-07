from app import tasks

import pytest


@pytest.mark.django_db
def test_task():
    assert tasks.send_email_reminder.run()

import datetime
import pytest
import six

from omniscript.invariant import EmailScheme, Severity, NOTIFICATION_SOURCES
from omniscript.notifications import Notifications, SendEmailRequest, SendNotificationRequest


def actions_check(actions):
    for action in actions:
        if action is None:
            return False
    return True


@pytest.fixture(scope="module")
def notifications(engine):
    """Notifications interface"""
    return Notifications(engine)


@pytest.fixture(scope="module")
def notifications_notifications(notifications):
    """Notifications on the capture engine."""
    return notifications.get_notifications()


@pytest.fixture(scope="module")
def new_notifications():
    """New notifications."""
    disabledSources = []
    for source in NOTIFICATION_SOURCES:
        disabledSources.append(source)

    severities = []
    for severity in Severity:
        severities.append({'enabled': True, 'severity': severity})

    newNotifications = []

    # Email
    newNotifications.append({
        'authentiation': False,
        'clearPassword': '',
        'clsid': 'FF13FDFE-31BA-40DD-AB8A-77A85C3A439A',
        'disabledSources': disabledSources,
        'id': 'FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFF0',
        'name': 'OS_Test_Email',
        'password': '',
        'port': 25,
        'recipient': 'someone@yahoo.com',
        'scheme': EmailScheme.SMTP,
        'sender': 'someone@yahoo.com',
        'server': 'smtp.somewhere.com',
        'severities': severities,
        'username': ''
    })
    # Execute
    newNotifications.append({
        'arguments': '',
        'clsid': '0D8DFB6C-237C-4ADE-8C37-E215D4F8CF00',
        'command': 'version',
        'directory': '/tmp',
        'disabledSources': disabledSources,
        'id': 'FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFF1',
        'name': 'OS_Test_Execute',
        'severities': severities
    })
    # Log
    newNotifications.append({
        'clsid': 'B2DA6C79-C270-4988-8A20-995A0BB7A1CE',
        'disabledSources': disabledSources,
        'id': 'FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFF2',
        'name': 'OS_Test_Log',
        'severities': severities
    })
    # SNMP Trap
    newNotifications.append({
        'clsid': 'ED19F042-0A45-44A6-9C47-E2A9D696881C',
        'community': 'public',
        'disabledSources': disabledSources,
        'id': 'FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFF3',
        'name': 'OS_Test_SNMPTrap',
        'recipient': 'someone@yahoo.com',
        'severities': severities
    })
    # syslog
    newNotifications.append({
        'clsid': '5D3B11A5-993F-4B18-B603-F1799AD3736E',
        'destination': 'someone@yahoo.com',
        'disabledSources': disabledSources,
        'id': 'FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFF4',
        'name': 'OS_Test_SysLog',
        'severities': severities
    })
    # Text Log
    newNotifications.append({
        'clsid': 'EF21EA89-80C3-4801-98F6-544677CF12D0',
        'currentFileCount': 1,
        'deleteFileCount': 0,
        'disabledSources': disabledSources,
        'fileCount': 1,
        'fileCountsEnabled': False,
        'fileName': 'notify',
        'fileNameAppend': '',
        'fileNameExtension': 'log',
        'filePath': '/tmp',
        'fileSize': 1,
        'fileSizesEnabled': False,
        'finished': False,
        'id': 'FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFF5',
        'name': 'OS_Test_TextLog',
        'severities': severities,
        'totalFileSizes': 1
    })
    return newNotifications


@pytest.mark.api
@pytest.mark.order(1)
def test_get_notifications(notifications_notifications):
    """Verifies the notifications can be retrieved."""
    assert (notifications_notifications is not None
            and isinstance(notifications_notifications.actions, list)
            and actions_check(notifications_notifications.actions)
            and isinstance(notifications_notifications.modificationTime, six.string_types)), (
        'Error in getting notifications')


@pytest.mark.api
@pytest.mark.order(2)
def test_get_notification(notifications, notifications_notifications):
    """Verifies a notification can be retrieved."""
    for action in notifications_notifications.actions:
        response = notifications.get_notification(action.id)
        assert (response is not None
                and isinstance(response.actions, list)
                and actions_check(response.actions)
                and isinstance(response.modificationTime, six.string_types)), (
            f'Error in getting notification "{action.id}"')


@pytest.mark.api
@pytest.mark.order(3)
def test_set_notifications(notifications, notifications_notifications):
    """Verifies the notifications can be set."""
    assert notifications.set_notifications(notifications_notifications) is not None, (
        'Error in setting notifications')


@pytest.mark.api
@pytest.mark.order(4)
def test_add_notifications(notifications, new_notifications):
    """Verifies a notification can be added."""
    for notification in new_notifications:
        assert notifications.set_notification(notification['id'], notification) is not None, (
            'Error in adding notifications')


@pytest.mark.api
@pytest.mark.order(5)
def test_modify_notifications(notifications, new_notifications):
    """Verifies a notification can be modified."""
    for notification in new_notifications:
        modifiedNotification = notification
        modifiedNotification['name'] += ' (Modified)'
        assert notifications.set_notification(modifiedNotification['id'],
                                              modifiedNotification) is not None, (
            'Error in modifying notifications')


@pytest.mark.api
@pytest.mark.order(6)
def test_delete_notifications(notifications, new_notifications):
    """Verifies a notification can be deleted."""
    for notification in new_notifications:
        assert notifications.delete_notification(notification['id']) is not None, (
            'Error in deleting notifications')


@pytest.mark.api
@pytest.mark.skip('Skipping email')
def test_send_email(notifications):
    """Verifies emails can be set."""
    email = {
        'body': 'This is a test email body.',
        'password': '',
        'port': 587,
        'recipients': '',
        'scheme': EmailScheme.SMTP_TLS,
        'sender': '',
        'server': '',
        'subject': 'This is a test email subject',
        'useAuthentication': False,
        'username': ''
    }
    assert notifications.send_email(SendEmailRequest(email)) is not None, (
        'Error in sending emails')


@pytest.mark.api
def test_send_notifications(notifications):
    """Verifies notifications can be set."""
    testNotifications = {
        'notifications': [
            {
                'context': '00000000-0000-0000-0000-000000000000',
                'longMessage': 'Test: long description 1',
                'severity': Severity.INFORMATIONAL,
                'shortMessage': 'Test: short description 1',
                'source': '00000000-0000-0000-0000-000000000000',
                'sourceKey': 0,
                'timestamp': f'{datetime.datetime.now().isoformat()}Z',
            },
            {
                'context': '00000000-0000-0000-0000-000000000000',
                'longMessage': 'Test: long description 2',
                'severity': Severity.INFORMATIONAL,
                'shortMessage': 'Test: short description 2',
                'source': '00000000-0000-0000-0000-000000000000',
                'sourceKey': 0,
                'timestamp': f'{datetime.datetime.now().isoformat()}Z',
            }
        ]
    }
    assert notifications.send_notifications(SendNotificationRequest(testNotifications)) is None, (
        'Error in sending notifications')

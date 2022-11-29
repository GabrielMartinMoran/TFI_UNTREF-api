from src.app.controllers.instant_actions_controller import InstantActionsController
from src.app.utils.http.request import Request
from src.domain.models.scheduling.tasks.task_action import TaskAction


def test_push_instant_action_returns_ok_when_instant_actions_is_pushed_successfully():
    controller = InstantActionsController(Request.from_body({'action': TaskAction.TURN_DEVICE_ON.value}))
    controller.device_repository.exists_for_user = lambda ble_id, user_id: True
    controller.instant_action_repository.clean_for = lambda device_id: None
    controller.instant_action_repository.push = lambda device_id, action: None

    actual = controller.push_instant_action('5c7b5ffc-90e7-1b85-f041-0595c912c905')

    assert actual.status_code == 200


def test_push_instant_action_returns_error_response_when_user_does_not_have_provided_device():
    controller = InstantActionsController(Request.from_body({'action': TaskAction.TURN_DEVICE_ON.value}))
    controller.device_repository.exists_for_user = lambda ble_id, user_id: False

    actual = controller.push_instant_action('5c7b5ffc-90e7-1b85-f041-0595c912c905')

    assert actual.status_code == 400
    assert actual.body['message'] == 'Provided device_id does not match any of the user devices'


def test_pull_instant_action_returns_obtained_instant_action_when_available():
    controller = InstantActionsController(Request.from_body({}))
    controller.device_repository.exists_for_user = lambda ble_id, user_id: True
    controller.instant_action_repository.clean_for = lambda device_id: None
    controller.instant_action_repository.pull = lambda device_id, pull_until: TaskAction.TURN_DEVICE_ON

    expected = {'action': TaskAction.TURN_DEVICE_ON.value}

    actual = controller.pull_instant_action('5c7b5ffc-90e7-1b85-f041-0595c912c905')

    assert actual.status_code == 200
    assert actual.body == expected


def test_pull_instant_action_returns_null_when_there_is_no_pending_instant_action():
    controller = InstantActionsController(Request.from_body({}))
    controller.device_repository.exists_for_user = lambda ble_id, user_id: True
    controller.instant_action_repository.clean_for = lambda device_id: None
    controller.instant_action_repository.pull = lambda device_id, pull_until: None

    expected = {'action': None}

    actual = controller.pull_instant_action('5c7b5ffc-90e7-1b85-f041-0595c912c905')

    assert actual.status_code == 200
    assert actual.body == expected


def test_pull_instant_action_returns_error_response_when_user_does_not_have_provided_device():
    controller = InstantActionsController(Request.from_body([]))
    controller.device_repository.exists_for_user = lambda ble_id, user_id: False

    actual = controller.pull_instant_action('5c7b5ffc-90e7-1b85-f041-0595c912c905')

    assert actual.status_code == 400
    assert actual.body['message'] == 'Provided device_id does not match any of the user devices'

import pytest

from state_machine import *

class NeverDone:
    def is_done(self):
        return False

@pytest.fixture
def basic():
    return StateMachine(NeverDone())

def test_no_state_on_start(basic):
    assert basic.state is None

def test_my_move_first(basic):
    basic.handle(SEND_MOVE_EVENT)
    assert basic.state is THEIR_MOVE_STATE

def test_their_move_first(basic):
    basic.handle(RECEIVE_MOVE_EVENT)
    assert basic.state is MY_MOVE_STATE

def test_illegal_move_by_me(basic):
    basic.handle(SEND_MOVE_EVENT)
    # This is a programmer error, so it should assert.
    with pytest.raises(AssertionError):
        basic.handle(SEND_MOVE_EVENT)

class ErrorHandler:
    def __init__(self):
        self.msg = None

    def __call__(self, msg):
        self.msg = msg

def test_illegal_move_by_them(basic):
    # This is an error by the other party, so it should
    # trigger on_error.
    basic.on_error = ErrorHandler()
    basic.handle(RECEIVE_MOVE_EVENT)
    assert basic.on_error.msg is None
    assert basic.state == MY_MOVE_STATE
    basic.handle(RECEIVE_MOVE_EVENT)
    assert basic.on_error.msg is not None
    assert basic.state == MY_MOVE_STATE

def test_early_exit_by_me(basic):
    basic.handle(RECEIVE_MOVE_EVENT)
    basic.handle(SEND_OUTCOME_EVENT)
    assert basic.state == DONE_STATE

def test_early_exit_by_them(basic):
    basic.handle(SEND_MOVE_EVENT)
    basic.handle(SEND_OUTCOME_EVENT)
    assert basic.state == DONE_STATE



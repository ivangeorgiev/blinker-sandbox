from contextlib import contextmanager
from unittest.mock import Mock
from blinker import signal, ANY


def test_named_signal_triggers_subscribers_passing_sender_and_kwargs():
    def printer(*args, **kwargs):
        received.append((args, kwargs))

    received = []
    sender = object()
    while signal("on_copy").receivers:
        signal("on_copy").disconnect(signal("on_copy").receivers.pop(0))
    signal("on_copy").connect(printer)
    signal("on_copy").send(sender, message="Message")
    assert received == [((sender,), {"message": "Message"})]


def test_named_signal_calls_only_subscriber_to_sender():
    def printer(*args, **kwargs):
        received.append((args, kwargs))

    received = []
    interesting_sender = object()
    other_sender = object()
    copy_signal = signal("on_copy")
    while copy_signal.receivers:
        copy_signal.disconnect(copy_signal.receivers.pop(0))
    copy_signal.connect(printer, sender=interesting_sender)
    copy_signal.send(interesting_sender, message="Important Message")
    copy_signal.send(other_sender, message="Other Message")
    assert received == [((interesting_sender,), {"message": "Important Message"})]


def test_connect_contextmanager():
    def printer(*args, **kwargs):
        received.append((args, kwargs))

    received = []
    sender = object()
    copy_signal = signal("on_copy")
    with copy_signal.connected_to(printer, sender):
        assert copy_signal.connected_to(printer, sender)
        copy_signal.send(sender, message="Yohoho")
        assert received == [((sender,), {"message": "Yohoho"})]

    received = []
    copy_signal.send(sender, message="Yohoho")
    assert received == []

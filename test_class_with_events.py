from contextlib import contextmanager
from blinker import Signal


class Application:
    def __init__(self):
        self._on_start = Signal()
        self._on_finish = Signal()

    def run(self):
        self._start()
        self._end()

    def _start(self):
        self._on_start.send(self, msg="started")

    def _end(self):
        self._on_finish.send(self, msg="finished")

    def on_start_receiver(self, receiver):
        self._on_start.connect(receiver)
        return receiver

    def on_finish_receiver(self, receiver):
        self._on_finish.connect(receiver)
        return receiver

    @contextmanager
    def on_start_connect(self, receiver):
        with self._on_start.connected_to(receiver):
            yield

    @contextmanager
    def on_finish_connect(self, receiver):
        with self._on_finish.connected_to(receiver):
            yield


def test_application_signals_trigger_receivers_from_context_manager():
    def receiver(*args, **kwargs):
        received.append((args, kwargs))

    received = []
    app = Application()
    with app.on_start_connect(receiver):
        with app.on_finish_connect(receiver):
            app.run()
    assert received == [((app,), {"msg": "started"}), ((app,), {"msg": "finished"})]


def test_application_signals_trigger_connected_receivers():
    def receiver(*args, **kwargs):
        received.append((args, kwargs))

    received = []
    app = Application()
    app.on_finish_receiver(receiver)
    app.run()
    assert received == [((app,), {"msg": "finished"})]


def test_application_signals_trigger_connected_receivers_with_decorator():
    app = Application()
    received = []

    @app.on_finish_receiver
    def receiver(*args, **kwargs):
        received.append((args, kwargs))

    app.run()
    assert received == [((app,), {"msg": "finished"})]

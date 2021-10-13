import time

from apscheduler.schedulers.background import BackgroundScheduler

from app.serial_controller import SerialController


class LightstripController:
    last_update = 0
    visualization = None

    def __init__(self, app, visualization):
        self.visualization = visualization
        self.serial_controller = SerialController(app)
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.loop)
        self.scheduler.start()

    def loop(self):
        while True:
            now = time.time()
            time_delta = now - self.last_update
            self.last_update = now
            lightstrip = self.visualization.update(time_delta)
            self.serial_controller.write(lightstrip)

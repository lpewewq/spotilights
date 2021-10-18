import time

from apscheduler.schedulers.background import BackgroundScheduler

from app.serial_controller import SerialController


class LightstripController:
    def __init__(self, app):
        self.last_update = 0
        self.job_running = False
        self.serial_controller = SerialController(app)
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

    def start_visualization(self, visualization):
        self.job_running = False
        time.sleep(0.1)  # let the loop thread end
        self.job_running = True
        self.scheduler.add_job(func=self.loop, args=(visualization,))

    def loop(self, visualization):
        while self.job_running:
            now = time.time()
            time_delta = now - self.last_update
            self.last_update = now
            lightstrip = visualization.update(time_delta)
            self.serial_controller.write(lightstrip)
        visualization.cleanup()

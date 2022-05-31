import time

class Clock:
    def __init__(self, fps):
        self.delta = 1./fps
        self.lastTime = time.time()

    def tick(self):
        currentTime = time.time()
        sleepTime = self.lastTime - currentTime
        if sleepTime > 0:
            time.sleep(sleepTime)
        else:
            if sleepTime < -.2:
                print (f"took too long: {sleepTime}")
        self.lastTime = time.time() + self.delta


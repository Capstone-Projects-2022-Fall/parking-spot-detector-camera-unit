from threading import Thread, Lock, Condition

# an object that keeps track of the latest
# frame so when resources become available
# the latest street view data is processed

class LatestFrame:
    # singleton design pattern
    # function invoked on object creation
    # - checks if an instance has been created
    #   and if it has returns the created instance
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(LatestFrame, cls).__new__(cls)
        return cls.instance

    # temporary constructor
    def __init__(self):
        self.available_frame = False
        self.frame = None
        self.mutex = Lock();
        self.consumable = Condition(lock=Lock())
        return

    # update frame using mutex to replace
    # the old frame with the new one
    def update_frame(self, frame):
        with self.consumable:
            # acquire r/w lock
            self.mutex.acquire()

            # update state
            self.frame = frame
            self.available_frame = True

            # release the lock
            self.mutex.release()

            # notify a worker that there
            # is an available frame for processing
            self.consumable.notify()

    # recieve a frame if there is one
    # uses mutex to remove the frame from
    # LatestFrame
    def recieve_frame(self):
        with self.consumable:
            # enter the waitlist for frames
            self.consumable.wait()

            # acquire r/w lock
            self.mutex.acquire()

            # capture frame
            frame = self.frame

            # update state
            self.frame = None
            self.available_frame = False

            # release the lock
            self.mutex.release()

        return frame

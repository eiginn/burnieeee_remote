import time

class Bucket:
    def __init__(self, size, interval, upd_func=None):
        self.size = size
        self.interval = interval
        self.last_transition = 0
        self.bucket = 0
        self.upd_func = upd_func

    def leak(self, amount=1):
        if amount < 0:
            raise ValueError
        now = time.monotonic()
        if now > self.last_transition + self.interval and self.bucket > 0:
            self.bucket -= amount
            self.last_transition = now
            print(f"Bucket: {self.bucket}")
            if self.upd_func is not None:
                self.upd_func(self.bucket)
        return True

    def tryfill(self, amount=1):
        if amount < 0 or amount > self.size:
            raise ValueError
        if self.bucket + amount > self.size:
            return False
        self.bucket += amount
        if self.upd_func is not None:
            self.upd_func(self.bucket)
        return True


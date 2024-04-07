# coding: utf-8

import time


class EventLoop:
    device = None
    vars = None

    def __init__(self, device, context=None):
        self.device = device
        self.vars = context

    def handle(self):
        x = self.vars.screen_width
        y = self.vars.screen_height
        center_x = int(x / 2)
        # self.device.swipe_handler(center_x, int(y / 4 * 3), center_x, int(y / 4))
        self.device.swipe_handler(center_x, int(y / 2), center_x, 50)

    def start(self, pause=1, until=None):
        count = 0
        while True:
            if until is not None:
                now = time.time()
                if now > until:
                    print('到达截止时间，退出')
                    break
            self.handle()
            count = count + 1
            print('$', end='', flush=True)
            if count % 100 == 0:
                print('')
            elif count % 25 == 0:
                print('.', end='', flush=True)
            time.sleep(pause)

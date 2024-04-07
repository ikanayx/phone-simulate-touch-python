# coding: utf-8

import wda

from common.device.i_device import Device
from common.logutil import logger

screen_path = 'temp/screen.png'


class IOSDevice(Device):
    client = None
    session = None
    dpi = 1  # iphone SE 的屏幕DPI为2，使用wda发送触摸指令时坐标(x,y)需要除以相应的dpi

    def __init__(self, address='http://127.0.0.1:8100'):
        self.client = wda.Client(address, _session_id='')
        size = self.client.window_size()
        self.screen_x = size.width
        self.screen_y = size.height

        self.session = self.client.session()
        self.dpi = self.session.scale

    def tap_handler(self, pos_x, pos_y):
        x = pos_x / self.dpi
        y = pos_y / self.dpi
        logger.debug('actually tap position: {0}, {1}'.format(x, y))
        self.session.tap(x, y)

    def swipe_handler(self, from_x, from_y, to_x, to_y, millisecond=50):
        # from_x = int(from_x / self.dpi) if from_x > 0 else 0
        # from_y = int(from_y / self.dpi) if from_y > 0 else 0
        # to_x = int(to_x / self.dpi) if to_x > 0 else 0
        # to_y = int(to_y / self.dpi) if to_y > 0 else 0
        # duration = millisecond / 1000  # wda accept duration with 'second' timeunit
        # logger.debug('actually swipe from ({0}, {1}) to ({2}, {3})'.format(from_x, from_y, to_x, to_y))
        self.session.swipe_up()
        # data = dict(fromX=from_x, fromY=from_y, toX=to_x, toY=to_y, velocity=5000)
        # self.session._session_http.post('/wda/dragfromtoforduration', data=data)
        # self.session.swipe(from_x, from_y, to_x, to_y, 0.001)
        # print('ios -> swipe_up')

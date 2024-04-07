# coding: utf-8

import sys
from sys import exit

from common.device.c_ios import IOSDevice
from common.device.c_android import AndroidDevice
from common.eventloop import EventLoop
from common.logutil import logger
from common.runtime import args_to_context
from time import time


if sys.version_info.major != 3:
    logger.error('请使用python3.x版本')
    exit(1)


if __name__ == '__main__':
    device = None
    try:
        ctx = args_to_context()
        if ctx.system_type == 'ios':
            if ctx.device_address == '':
                ctx.device_address = 'http://localhost:8100'
            device = IOSDevice(address=ctx.device_address)
        else:
            device = AndroidDevice(address=ctx.device_address)

        ctx.screen_width = device.screen_x
        ctx.screen_height = device.screen_y
        print(ctx)

        worker = EventLoop(device, ctx)
        start_unixTime = time()
        worker.start(pause=ctx.swipe_duration, until=start_unixTime + 60 * ctx.exec_time)

    except KeyboardInterrupt:
        print('\nCtrl+C 被按下, 程序即将退出.')
        exit()
    except Exception as unknown:
        print()
        logger.error("Unexpected/Unknown Exception occurred")
        logger.exception(unknown)
        exit()

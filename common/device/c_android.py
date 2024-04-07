# coding: utf-8

import numpy
import sys
import os
import subprocess

from io import StringIO
from PIL import ImageFile, Image
from common.logutil import logger

sys.path.insert(1, '../common')

try:
    from common.device.i_device import Device
    from common.device.adb import Adb
except Exception as ex:
    logger.error(ex)
    logger.error('请检查项目根目录中的 common 文件夹是否存在')
    exit(1)

screen_dir = './temp/'
screen_name = 'screen.png'
screen_path = screen_dir + screen_name
ImageFile.LOAD_TRUNCATED_IMAGES = True


class AndroidDevice(Device):
    SCREENSHOT_WAY = 0
    adb = None

    def __init__(self, address=''):
        self.adb = Adb(device=address)
        self.adb.test_device()
        # self.__check_screenshot()
        self.screen_x, self.screen_y = self.adb.get_size()

    def tap_handler(self, pos_x, pos_y):
        logger.debug('actually tap position: {0}, {1}'.format(pos_x, pos_y))
        self.adb.run('shell input tap {} {}'.format(pos_x, pos_y))

    def swipe_handler(self, from_x, from_y, to_x, to_y, millisecond=100):
        command = 'shell input swipe {} {} {} {} {}'.format(from_x, from_y, to_x, to_y, millisecond)
        # print(command)
        self.adb.run(command)

    def screen_capture_as_image(self):
        return self.__pull_screenshot()

    def __check_screenshot(self):
        while True:
            if self.SCREENSHOT_WAY < 0:
                logger.error('暂不支持当前设备')
                sys.exit()
            if not os.path.exists(screen_dir):  # 判断是否存在文件夹如果不存在则创建为文件夹
                os.makedirs(screen_dir)
            if os.path.isfile(screen_path):
                os.remove(screen_path)
            try:
                im = self.__pull_screenshot()
                im.load()
                im.close()
                logger.info('采用方式 {} 获取截图'.format(self.SCREENSHOT_WAY))
                break
            except Exception as pssEx:
                logger.error(pssEx)
                self.SCREENSHOT_WAY -= 1

    def __pull_screenshot(self, file_name=''):
        if 1 <= self.SCREENSHOT_WAY <= 3:
            process = subprocess.Popen(
                self.adb.adb_path + ' shell screencap -p',
                shell=True, stdout=subprocess.PIPE)
            binary_screenshot = process.stdout.read()
            if self.SCREENSHOT_WAY == 2:
                binary_screenshot = binary_screenshot.replace(b'\r\n', b'\n')
            elif self.SCREENSHOT_WAY == 1:
                binary_screenshot = binary_screenshot.replace(b'\r\r\n', b'\n')
            return Image.open(StringIO(binary_screenshot))
        elif self.SCREENSHOT_WAY == 0:
            if file_name == '':
                file_name = screen_path
            self.adb.run('shell screencap -p /sdcard/' + screen_name)
            self.adb.run('pull /sdcard/' + screen_name + ' ' + file_name)
            return Image.open('' + file_name)

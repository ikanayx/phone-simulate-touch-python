from sys import argv


class Context:
    screen_width = 1136
    screen_height = 640
    system_type = None
    device_address = ''
    exec_time = 0
    swipe_duration = 10

    def __str__(self):
        return f'''
  system_type:    {self.system_type}
  device_address: {self.device_address}
  screen_width:   {self.screen_width}px
  screen_height:  {self.screen_height}px
  exec_time:      {self.exec_time}min
  swipe_duration: {self.swipe_duration}s
        '''


def args_to_context():
    ctx = Context()
    args = argv[1:]
    if '--help' in args or '-h' in args:
        print('''
  -s, --system    设备类型。支持ios和android
  -a, --address   设备地址。如果是ios设备，默认http://127.0.0.1:8100；如果是android设备，默认为空，通过adb
                  devices获取第一台设备
  -t, --exec_time 执行时长。单位：分钟，默认150
  -d, --duration  滑动间隔。单位：秒，默认10
        ''')
        exit(0)

    argv_len = len(args)
    index = 0
    opts = ['--system', '-s', '--address', '-a', '--duration', '-d', '--exec-time', '-t', '--help', '-h']
    while index < argv_len:
        arg = args[index]
        if arg.index('=') > -1:
            pair = arg.split('=')
            identity_arg(pair[0], pair[1], ctx)
        elif arg in opts:
            next_idx = index + 1
            if next_idx >= argv_len:
                break
            if not args[next_idx].startswith('-'):
                value = args[next_idx]
                identity_arg(arg, value, ctx)
                index = index + 1
        index = index + 1
    return ctx


def identity_arg(key, value, ctx):
    if key in ['--system', '-s']:
        ctx.system_type = value
    elif key in ['--address', '-a']:
        ctx.device_address = value
    elif key in ['--duration', '-d']:
        ctx.swipe_duration = int(value)
    elif key in ['--exec-time', '-t']:
        ctx.exec_time = int(value)

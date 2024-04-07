# Overview

这个项目的用途是自动切换手机端的短视频，薅点羊毛

### 运行环境要求

- Python 3.x

### 程序参数

```sh
# 安装依赖
$ pip3 install -r requirements.txt

# 查看支持的参数
$ python3 start.py --help

  -s, --system    设备类型。支持ios和android
  -a, --address   设备地址。如果是ios设备，默认http://127.0.0.1:8100；如果是android设备，默认为空，通过adb
                  devices获取第一台设备
  -t, --exec_time 执行时长。单位：分钟，默认150
  -d, --duration  滑动间隔。单位：秒，默认10
```




### iPhone运行步骤

   1. 将 [WebDriverAgent](https://github.com/appium/WebDriverAgent) 克隆到本地

   2. 使用 Xcode 打开 WebDriverAgent 项目，配置个人证书（自行搜索相关教程，此处不展开）

   3. 连接 iPhone ，在 Xcode 菜单 Production → Destination 选中iPhone真机

         1. 在 Xcode 菜单 Production → Destination → Manage Run Destinations 打开设备管理界面

         2. 找到iPhone真机，记录对应的 Identifier，后面需要用到

   4. ⌘+B 启动编译

   5. ⌘+U 启动测试，注意手机要输入解锁密码

      > 提示Could not launch时，根据提示判断是否需要到 设置 → 通用 → 关于本机 → 滑到最底部，信任开发者证书

      首次编译成功后，下次可不启动Xcode，使用命令行进行测试

      ```shell
      $ PASSWORD="此处替换为macOS的开机密码"
      $ PROJECT_ROOT="此处替换为WebDriverAgent项目目录"
      $ UDID="此处替换为第3步获得的设备 Identifier"
      
      $ security unlock-keychain -p $PASSWORD ~/Library/Keychains/login.keychain
      
      $ xcodebuild -project $PROJECT_ROOT/WebDriverAgent.xcodeproj -scheme WebDriverAgentRunner -destination "id=$UDID" test
      ```

      

   6. Xcode 菜单 View → Debug Area → Show Consoles 打开调试控制台输出，查找下面的输出

      ```
      ServerURLHere->http://${ip地址}:8100<-ServerURLHere
      ```

      访问`http://${ip地址}:8100/status`，其中ip地址为上一步获得的ip地址。如果无法访问，则安装 libimobiledevice ，配置电脑到iPhone的端口转发

      ```shell
      $ brew install libimobiledevice
      
      # 使用第3步获取到的设备的 Identifier 替换下面命令的 ${udid}
      # 命令中的${local_port}，可使用8100，也可使用其它未被占用端口
      $ iproxy -u ${udid} ${local_port} 8100
      
      # 新开一个终端，测试 WebDriver 服务是否能正常访问
      $ curl 'http://127.0.0.1:${local_port}/status'
      ```

   7. 在当前项目根目录打开新的终端

      ```shell
      # 启动程序
      # 需要手动替换${local_port}为实际值（参考第6步）
      $ python3 start.py --system=ios --exec-time=130 --duration=10 --address=http://127.0.0.1:${local_port}
      ```

   8. WebDriverAgent在执行屏幕滑动操作时，duration参数设置为0.1s，实际滑动还是在1s以上

      如果需要加快滑动动画，使用Xcode打开 WebDriverAgent 项目，查找并打开`FBElementCommands.m`文件，在文件内查找`handleDrag`处理器，修改滑动逻辑

      ```objective-c
      + (id<FBResponsePayload>)handleDrag:(FBRouteRequest *)request
      {
        NSString *elementUdid = (NSString *)request.parameters[@"uuid"];
        XCUIElement *target = nil == elementUdid
          ? request.session.activeApplication
          : [request.session.elementCache elementForUUID:elementUdid];
        CGVector startOffset = CGVectorMake([request.arguments[@"fromX"] doubleValue],
                                            [request.arguments[@"fromY"] doubleValue]);
        XCUICoordinate *startCoordinate = [self.class gestureCoordinateWithOffset:startOffset element:target];
        CGVector endOffset = CGVectorMake([request.arguments[@"toX"] doubleValue],
                                          [request.arguments[@"toY"] doubleValue]);
        XCUICoordinate *endCoordinate = [self.class gestureCoordinateWithOffset:endOffset element:target];
        NSTimeInterval duration = [request.arguments[@"duration"] doubleValue];
      
        // 修改前
        // [startCoordinate pressForDuration:duration thenDragToCoordinate:endCoordinate];
      
        // 修改后 增加了withVelocity参数，参数值越大，滑动动画越快
        [startCoordinate pressForDuration:duration thenDragToCoordinate:endCoordinate withVelocity:5000 thenHoldForDuration:duration];
      
        return FBResponseWithOK();
      }
      ```

      

### Android运行步骤

1. 安装adb

2. Android 手机打开USB调试模式（自行搜索相关教程，此处不展开），并连接Mac

3. 如果有多台安卓设备同时连接，在终端输入`adb devices`获取设备标识，以下示例中，CIIRI7JF8XCU6H99为设备标识

   ```sh
   $ adb devices
   List of devices attached
   CIIRI7JF8XCU6H99	device
   ```

   

4. 在当前项目根目录打开新的终端

   ```sh
   # 启动程序
   # 需要手动替换${local_port}为实际值（参考第6步）
   $ python3 start.py --system=android --exec-time=130 --duration=10 --address=${替换为设备标识}
   ```

   


### 参考资料

- [macOS 平台上通过 Xcode 使用 wda 以及 libimobiledevice 安装说明](https://github.com/wangshub/wechat_jump_game/wiki/Android-和-iOS-操作步骤#二ios-手机操作步骤)
- openatx/facebook-wda [Github地址](https://github.com/openatx/facebook-wda)
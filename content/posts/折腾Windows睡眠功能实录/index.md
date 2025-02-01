+++
date = '2025-01-29T23:52:32+08:00'
languageCode = 'zh-cn'
draft = true
title = '折腾Windows睡眠功能实录'
+++

## 前言
看了好多好多网上的调教Windows睡眠功能的视频和帖子，没有一个能解决问题，提出的解决方案也都没有给出一个所以然。[Linus](https://www.bilibili.com/video/BV1Pv4y1d7Ms/?share_source=copy_web&vd_source=fb265942059a9ab2a1e9aaac585a4d43)和[差评君](https://www.bilibili.com/video/BV1k46GY5Eg1/?share_source=copy_web&vd_source=fb265942059a9ab2a1e9aaac585a4d43)通过反复测试的方法尝试寻找睡眠睡死、突然唤醒和“失眠”的规律，这也是我之前的寻找路径，但是反复测试需要的测试量过大，考虑的变量过多。全部测试出来实在不是很现实，不同的人的笔记本又有不同的情况，不讨论原理的话很难在其他人的电脑上复现，所以本文意在授人以渔。

如网上的好多方案一样，我也只是提供我笔记本的情况，以及对应的**看似成功了**的解决方案。希望能提供一些帮助。
## 问题
### 系统信息
这是一台新安装系统的Thinkbook 14+ ARA笔记本，无独显，处理器是[AMD Ryzen 6800H](https://www.amd.com/en/support/downloads/drivers.html/processors/ryzen/ryzen-6000-series/amd-ryzen-7-6800h.html)。系统信息如下

``` text
设备名称	HIDE-SEEK
处理器	AMD Ryzen 7 6800H with Radeon Graphics            3.20 GHz
机带 RAM	32.0 GB (27.7 GB 可用)
...
系统类型	64 位操作系统, 基于 x64 的处理器
笔和触控	没有可用于此显示器的笔或触控输入

版本	Windows 11 家庭中文版
版本号	24H2
安装日期	‎2024/‎12/‎22
操作系统版本	26100.2605
体验	Windows 功能体验包 1000.26100.36.0
```
### 问题描述
1. 进入睡眠以后掉电很快，没多久就因为耗电过多（4%）触发休眠门槛，导致系统休眠（hibernate）到硬盘。键盘灯亮，电源灯不呼吸，但是大小写锁定灯和FN锁定灯熄灭
1. 在连接电源睡眠，可能会卡死，出现无规律。卡死时键盘灯亮、电源灯不呼吸、电脑严重发热、但是风扇不转。无论按什么按钮（包括电源键）电脑均无反应，只能长按电源键断电。

## 现代待机

[现代待机](https://learn.microsoft.com/en-us/windows-hardware/design/device-experiences/modern-standby)是微软在Windows上退出的*新*的待机机制，实际上Windows已经使用了该机制10年以上，也算是经过了一些检验。这里从微软的文档中摘录一些内容，用以科普几个概念。

## 测试方案

### 问题一、睡眠键盘灯不熄灭，耗电高

按`win + x`和`a`打开管理员终端，输入 `powercfg /systempowerreport` 生成系统的电池报告，电池报告会生成在`%HOME%`目录下

![SW0%的电池报告](img/pic1.png)

发现在键盘灯点亮期间，系统电源状态是sleep，系统已经进入睡眠状态。进一步分析报告，发现软件的*Low Power State Time*是0%，同时DRIPS的统计时间中没有数据。说明由于软件的某些影响，系统整体没能进入低功耗的状态。

![有问题的DRIPS](img/pic2.png)

根据微软现代待机的[文档](https://learn.microsoft.com/en-us/windows-hardware/design/device-experiences/modern-standby-sleepstudy-common-problem-examples#no-software-drips-or-hardware-drips-due-to-a-missing-driver)，这可能是由于该硬件、或软件缺乏合适的驱动程序导致的。电池报告在下方列出了5个在本次睡眠中最活跃的5个设备。可以在被标记为红色*session blocker*中进一步查看被标记为高耗能的设备。

![最活跃的硬件](img/pic3.png)

可以看到，这些设备的活跃时间在90%以上，这是显然是不正常的，符合微软文档中设备异常活跃的描述。因此，需要找到该设备ID对应的设备是什么，去设备管理器中更新或重新安装驱动程序，并检查该设备是否存在其他问题。

向下继续翻电池报告，可以在*Detailed FX Devices Information*节中，找到每个设备ID对应的位置。

![Detailed FX Devices Information](img/pic4.png)

使用下面的代码定位设备的名称

``` pwsh
Get-PnpDevice | Select-Object -Property FriendlyName, InstanceId | Out-GridView
```

在弹出的窗口中搜索对应的设备位置，搜索即可找到对应的设备在设备管理器中的名字，在设备管理器中找到设备，尝试选择自动更新驱动程序。

在我的案例中，我发现是AMD的USB控制器和其下的USB集线器过于活跃，这些设备的驱动可能本身不含现代待机使用的*Low Power State* API，我额外检查了对应设备的电源管理设置，发现*允许计算机关闭此设备以节约电源*选项未勾选。我推测可能是因为系统无法以直接关闭设备的方式停止该设备活动，所以该设备活跃时间畸高。因此，勾选该项再次测试，发现系统可以正常进入睡眠，键盘灯正常熄灭。

除此之外，我还更新了我的外设的驱动（雷蛇鼠标），现在的外设功能不断丰富，我推测个别外设可能需要专门的驱动实现现代待机使用的*Low Power State* API，因此检查一下这些驱动也可能有帮助。

之后，睡眠期间键盘灯不关闭、耗电高的问题成功解决。

### 问题二、睡眠期间卡死

这个问题是该电脑长期存在的问题，重装系统也是出于该原因。检查电池报告，发现在睡眠卡死强制关机留下*Abnormal Shutdown*日志项，该日志项是在长按电源关机之后的下一次启动时生成的，内容应该来自系统从硬盘中页面文件中恢复的日志，一定程度上能反映卡死之前发生了什么。从所有的*Abnormal Shudown*日志发现，电脑在这是从未进入睡眠状态，而是在*Screen Off*后转入睡眠之前的某个时刻卡死。而在*Abnormal Shutdown*日志项中，均发现了*SystemSleepTransitionsToOn*项值畸高的情况。微软的文档并未有该项含义的详细解释，但是从项目词义可以推测系统反复尝试电源状态转换，推测可能是固件、硬件驱动或者硬件本身导致的问题。

2024年2月，有[帖子](https://www.saraba1st.com/2b/thread-2170734-1-1.html)讲AMD发布了6800H更新的驱动，解决了卡死的问题，但是帖子的回复中答复给出消极信息。此后AMD驱动可能还有后续更新。此外，联想在2024年12月还发布了笔记本的[BIOS更新](https://support.lenovo.com/bd/en/downloads/ds557402-bios-update-for-windows-11-64-bit-thinkbook-14-g4-ara-thinkbook-16-g4-ara)，更新文档中有一条值得注意。

> 4.Update Rembrandt PI to 1.0.0.Ba

抱着尝试的心态，我更新了[AMD的芯片组驱动](https://www.amd.com/zh-cn/support/download/drivers.html)和联想的BIOS，但是卡死并未好转。

经过进一步分析系统电源报告，我发现系统会在**睡眠期间充电至100%后卡死**
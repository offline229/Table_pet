# 更新日志
## 0329
开工，灰狗出现在桌面

错误百出地实现落地与拖拽了
## 0330
宠物之间可以交互了

优化了文件结构
## 0331
写了惯性

修正了状态切换bug

增加了天上下灰狗雨的功能？

GPT大人帮忙修复了一个神秘的bug，写好了自由框架选择
```
1. 托盘图标生命周期导致应用退出
在原来的实现中：tray_icon在create_tray_icon返回后成为局部变量被回收，在 Windows 和部分 Linux 桌面环境中，QSystemTrayIcon 的生命周期由 QApplication 管理。如果 QSystemTrayIcon 没有引用，被回收时会触发整个应用退出，因为系统认为应用图标已经消失，自然认为程序该关闭了
```
问了一下为啥只有dialog会触发这个bug
```
window_interaction 函数里调用了 dialog.exec_()，这是阻塞调用。

exec_() 会让事件循环暂停当前上下文，直到对话框关闭才继续执行。
所以阻塞应该导致了跳出并返回create_tray_icon，没阻塞的时候不会被回收
```
## 0401
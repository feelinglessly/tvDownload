# 用于下载视频

现仅支持华人和云影

华人：
- https://www.ece8.com/
- https://huarw.com/
    

云影：
- https://www.yuny.tv/


### config.yarn
```commandline
  max_reset: 5 // 最大重试次数
  max_ts_num: -1 // 最多下载多少个ts。当为正整数时就不会下载完全的视频。只在调试时避免下载太多
  max_thread_num: 5 // 最多下载线程数，针对的时一个视频同时下载ts数量。多个视频时会按照 视频数量 * max_thread_num 数计算
  auto_remove_ts: 1 // 是否自动删除下载的ts文件，ts文件是中间文件，如果为1，在合并完成后会删除ts文件

```


### 调试运行
python main.py


### 打包成桌面程序
- windows

使用 main.spec 中的配置打包
```commandline
cd bin\builds
.\build.bat
```


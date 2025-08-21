# 🎵 music_auto_copy

一个基于 **Python** 的小工具，可以将音乐文件按照 **标签信息（歌手 / 专辑）** 分类整理到目标目录。  
支持的音频格式：`.mp3`, `.flac`, `.wav`, `.m4a`, `.aac`, `.ogg`

---

## ✨ 功能特性
- 自动读取音频文件的 **歌手** 和 **专辑** 标签  
- 按照 `歌手/专辑` 结构整理文件夹  
- 多线程处理，加快文件移动速度  
- 自动清理源目录中的空文件夹  
- 生成日志文件 `music_organize.log`，方便排错  

---

## 📦 安装依赖
在运行脚本之前，需要安装 [mutagen](https://pypi.org/project/mutagen/)：

```bash
pip install mutagen

⚙️ 使用方法

使用你喜欢的编辑器打开 music_auto_copy.py

修改脚本开头的 配置区域：

source_dir = Path(r'C:\Users\admin\Desktop\source')   # 源文件目录
target_dir = Path(r'D:\music')                        # 输出目录


保存后运行脚本：

python music_auto_copy.py


脚本会：

扫描源目录下所有音频文件

根据标签整理并移动到目标目录

删除空文件夹

在当前目录生成 music_organize.log 日志

📖 示例输出
🎵 开始整理音乐……
🎧 发现 128 个音频候选文件，正在处理中……
✅ song1.mp3 → Artist1/AlbumA
✅ song2.flac → Artist2/AlbumB
🧹 删除空目录：C:\Users\admin\Desktop\source\old
✅ 整理完成！日志保存在 music_organize.log

📝 注意事项

源目录不存在时脚本会直接退出

如果音频缺少标签（歌手或专辑），文件会被跳过并记录在日志中

目标目录中已存在同名文件时，会跳过该文件

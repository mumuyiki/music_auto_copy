import os
import shutil
import logging
import re
from pathlib import Path
from mutagen import File as MutagenFile
from concurrent.futures import ThreadPoolExecutor, as_completed

# === 配置区域 ===
source_dir = Path(r'C:\Users\xuan\Desktop\source')
target_dir = Path(r'D:\backup\music')
AUDIO_EXTENSIONS = ['.mp3', '.flac', '.wav', '.m4a', '.aac', '.ogg']
THREADS = 8
log_path = Path("music_organize.log")
# ================

# 设置日志
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def sanitize_path_component(name: str) -> str:
    """清除路径中的非法字符"""
    return re.sub(r'[<>:"/\\|?*]', '_', name).strip()

def extract_tag_value(tag):
    """统一处理标签内容，无论是列表、对象还是字符串"""
    if tag is None:
        return None
    if isinstance(tag, list):
        return tag[0]
    if hasattr(tag, 'text') and isinstance(tag.text, list):
        return tag.text[0]
    return str(tag)

def get_tag(file_path: Path):
    try:
        audio = MutagenFile(file_path)
        if not audio:
            raise ValueError("文件格式不受支持")

        artist, album = None, None

        for tag in ('TPE1', 'artist', '©ART'):
            raw = audio.tags.get(tag)
            artist = extract_tag_value(raw)
            if artist:
                break

        for tag in ('TALB', 'album', '©alb'):
            raw = audio.tags.get(tag)
            album = extract_tag_value(raw)
            if album:
                break

        if not artist or not album:
            raise ValueError("缺少标签信息")

        return sanitize_path_component(artist), sanitize_path_component(album)

    except Exception as e:
        logging.warning(f"标签解析失败：{file_path}，原因：{e}")
        return None, None

def process_file(file_path: Path):
    try:
        if not file_path.suffix.lower() in AUDIO_EXTENSIONS:
            return

        artist, album = get_tag(file_path)
        if not artist or not album:
            logging.warning(f"跳过无效标签的文件：{file_path}")
            return

        dest_dir = target_dir / artist / album
        dest_dir.mkdir(parents=True, exist_ok=True)

        dest_path = dest_dir / file_path.name

        if dest_path.exists():
            logging.info(f"⚠️ 已存在，跳过：{file_path.name}")
            return

        shutil.move(str(file_path), str(dest_path))
        logging.info(f"✅ 移动：{file_path.name} → {dest_dir}")
        print(f"✅ {file_path.name} → {artist}/{album}")

    except Exception as e:
        logging.error(f"❌ 处理失败：{file_path}，错误：{e}")

def delete_empty_dirs(path: Path):
    """递归删除空目录"""
    for dir_path in sorted(path.glob("**/*"), key=lambda p: len(str(p)), reverse=True):
        if dir_path.is_dir() and not any(dir_path.iterdir()):
            try:
                dir_path.rmdir()
                logging.info(f"🧹 删除空目录：{dir_path}")
            except Exception as e:
                logging.warning(f"⚠️ 无法删除目录：{dir_path}，原因：{e}")

def main():
    print("🎵 开始整理音乐……")
    if not source_dir.exists():
        print("❌ 错误：原始目录不存在！")
        return

    music_files = [f for f in source_dir.glob('**/*') if f.is_file()]
    print(f"🎧 发现 {len(music_files)} 个音频候选文件，正在处理中……")

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = [executor.submit(process_file, file) for file in music_files]
        for future in as_completed(futures):
            pass

    delete_empty_dirs(source_dir)
    print("✅ 整理完成！日志保存在 music_organize.log")

if __name__ == '__main__':
    main()

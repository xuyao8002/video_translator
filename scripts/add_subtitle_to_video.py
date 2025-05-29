import subprocess
import os
import argparse
def add_subtitle_to_video(input_video_path, subtitle_path, output_video_path=None):

    if not os.path.isfile(input_video_path):
        raise FileNotFoundError(f"找不到视频文件：{input_video_path}")

    if not os.path.isfile(subtitle_path):
        raise FileNotFoundError(f"找不到字幕文件：{subtitle_path}")

    # 设置输出文件路径
    if output_video_path is None:
        output_video_path = os.path.join(
            os.path.dirname(input_video_path),
            "output_with_subtitle.mp4"
        )

    # 构建 ffmpeg 命令
    command = [
        'ffmpeg',
        '-i', input_video_path,           # 输入视频
        '-vf', f"subtitles={subtitle_path}",  # 烧录字幕（需要确保字幕格式支持）
        '-c:a', 'copy',                    # 直接复制音频流
        '-y',                              # 覆盖已有文件
        output_video_path
    ]

    print(f"开始合并字幕到视频，输出到：{output_video_path}")
    
    try:
        subprocess.run(command, check=True)
        print("✅ 字幕已成功添加到视频中！")
    except subprocess.CalledProcessError as e:
        print("❌ 合并失败：", e)

if __name__ == "__main__":
    # 示例用法
    parser = argparse.ArgumentParser()
    parser.add_argument("video_path")
    parser.add_argument("subtitle_path")
    args = parser.parse_args()
    video_path = args.video_path
    subtitle_path = args.subtitle_path
    add_subtitle_to_video(video_path, subtitle_path)

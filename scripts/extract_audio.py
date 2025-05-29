import subprocess
import os
import argparse
def extract_mp3_from_mp4(input_mp4_path, output_dir=None):
    if not os.path.isfile(input_mp4_path):
        raise FileNotFoundError(f"找不到文件：{input_mp4_path}")

    # 如果未指定输出目录，默认和视频文件在同一目录下
    if output_dir is None:
        output_dir = os.path.dirname(input_mp4_path)

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    output_mp3_path = os.path.join(output_dir, "output.mp3")

    # 构建 ffmpeg 命令
    command = [
        'ffmpeg',
        '-i', input_mp4_path,     # 输入文件
        '-q:a', '2',              # 音质参数（2 是高质量）
        '-map', 'a',              # 只提取音频流
        '-y',                     # 覆盖已存在的 output.mp3
        output_mp3_path
    ]

    print(f"开始提取音频，输出到：{output_mp3_path}")
    
    try:
        subprocess.run(command, check=True)
        print("✅ 音频提取成功！")
    except subprocess.CalledProcessError as e:
        print("❌ 提取音频失败：", e)

if __name__ == "__main__":
    # 示例用法
    parser = argparse.ArgumentParser()
    parser.add_argument("input_video")
    parser.add_argument("output_folder")
    args = parser.parse_args()
    input_video = args.input_video
    output_folder = args.output_folder
    extract_mp3_from_mp4(input_video, output_folder)

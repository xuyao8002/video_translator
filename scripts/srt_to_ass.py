import pysrt
import subprocess
import re
import textwrap
import argparse

# 配置默认字体大小和样式
DEFAULT_FONT_NAME = "Microsoft YaHei"
DEFAULT_FONT_SIZE = 10
DEFAULT_ALIGNMENT = 2  # 居中底部

def get_video_resolution(video_path):
    """使用 ffprobe 获取视频分辨率"""
    cmd = [
        "ffprobe", "-v", "error",
        "-of", "flat=s=_",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height",
        video_path
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = result.stdout.decode()

    width = int(re.search(r"width=(\d+)", output).group(1))
    height = int(re.search(r"height=(\d+)", output).group(1))

    return width, height

def estimate_wrap_width(width, height):
    """根据视频分辨率估算每行最大字符数"""
    is_portrait = height > width
    if is_portrait:
        if width >= 2160:
            return 35
        elif width >= 1080:
            return 20
        else:
            return 15
    else:
        if width >= 3840:
            return 100
        elif width >= 1920:
            return 50
        else:
            return 30

def wrap_text(text, width=30):
    """智能换行：英文按空格分词，中文按字符数"""
    lines = []
    for paragraph in text.split('\n'):
        if re.search(r'[\u4e00-\u9fff]', paragraph):  # 包含中文
            wrapped = textwrap.wrap(paragraph, width=width)
        else:  # 英文或纯字母
            wrapped = textwrap.wrap(paragraph, width=width)
        lines.extend(wrapped if wrapped else [''])
    return '\\N'.join(lines)

def srt_to_ass(input_srt_path, output_ass_path, video_path=None, lang='auto', width_factor=0.8):
    # 如果传入了视频路径，则自动获取分辨率
    if video_path:
        width, height = get_video_resolution(video_path)
        wrap_width = estimate_wrap_width(width, height)
    else:
        print("⚠️ 未指定视频路径，默认使用中等宽度换行")
        wrap_width = 40

    # 加载 SRT 文件
    subs = pysrt.open(input_srt_path, encoding="utf-8")

    # 准备 ASS 文件内容
    ass_content = []

    # 写入头部信息
    ass_content.append("[Script Info]")
    ass_content.append("Title: Converted Subtitle")
    ass_content.append("ScriptType: v4.00+")
    #ass_content.append(f"PlayResX: {width if video_path else 1280}")
    #ass_content.append(f"PlayResY: {height if video_path else 720}")
    ass_content.append("Scaled: yes")
    ass_content.append("Collisions: Normal")
    ass_content.append("")

    # 样式定义
    ass_content.append("[V4+ Styles]")
    ass_content.append("Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding")
    ass_content.append(f"Style: Default,{DEFAULT_FONT_NAME},{DEFAULT_FONT_SIZE},&H00FFFFFF,&H000000FF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,2,2,{DEFAULT_ALIGNMENT},10,10,10,1")
    ass_content.append("")

    # 事件部分
    ass_content.append("[Events]")
    ass_content.append("Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text")

    # 处理每个字幕项
    for i, sub in enumerate(subs):
        start_time = sub.start.to_time()
        end_time = sub.end.to_time()

        # 格式化时间：hh:mm:ss.cc
        def format_time(t):
            return f"{t.hour:02d}:{t.minute:02d}:{t.second:02d}.{int(t.microsecond / 10000):02d}"

        text = wrap_text(sub.text, wrap_width)

        event_line = f"Dialogue: 0,{format_time(start_time)},{format_time(end_time)},Default,,0,0,0,,{text}"
        ass_content.append(event_line)

    # 写入文件
    with open(output_ass_path, 'w', encoding='utf-8-sig') as f:
        f.write("\n".join(ass_content))

    print(f"✅ 已生成 ASS 字幕文件：{output_ass_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_srt")
    parser.add_argument("video_file")
    parser.add_argument("output_ass")
    args = parser.parse_args()
    input_srt = args.input_srt
    video_file = args.video_file
    output_ass = args.output_ass
    srt_to_ass(input_srt, output_ass, video_file)

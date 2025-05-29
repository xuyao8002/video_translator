import json
import argparse
from scripts.translate import translate
def time_format(seconds):
    """将秒数转换为SRT格式的时间"""
    ms = int(seconds * 1000) % 1000
    s = int(seconds) % 60
    m = int(seconds / 60) % 60
    h = int(seconds / (60 * 60))
    return "{:02d}:{:02d}:{:02d},{:03d}".format(h, m, s, ms)

def json_to_srt(json_path, srt_path):
    # 读取json文件
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # 准备SRT内容
    srt_content = ""
    for i, segment in enumerate(data, start=1):
        start_time = time_format(segment['start'])
        end_time = time_format(segment['end'])
        text = translate(segment['text'])
        
        # 组装单个字幕块
        srt_segment = f"{i}\n{start_time} --> {end_time}\n{text}\n\n"
        srt_content += srt_segment
    
    # 写入SRT文件
    with open(srt_path, 'w', encoding='utf-8') as srt_file:
        srt_file.write(srt_content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("json_file_path")
    parser.add_argument("output_srt_file_path")
    args = parser.parse_args()
    json_file_path = args.json_file_path
    output_srt_file_path = args.output_srt_file_path
    json_to_srt(json_file_path, output_srt_file_path)


import argparse
from scripts.extract_audio import extract_mp3_from_mp4
from scripts.split_sentence import transcribe_and_segment_to_json
from scripts.json_to_srt import json_to_srt
from scripts.srt_to_ass import srt_to_ass
from scripts.add_subtitle_to_video import add_subtitle_to_video
def process(input_video_path, output_folder):
    print("开始翻译")
    extract_mp3_from_mp4(input_video_path, output_folder)
    transcribe_and_segment_to_json(output_folder + "output.mp3", output_folder + "output.json")
    json_to_srt(output_folder + "output.json", output_folder + "output.srt")
    srt_to_ass(output_folder + "output.srt", output_folder + "output.ass", input_video_path)
    add_subtitle_to_video(input_video_path, output_folder + "output.ass", output_folder + "output.mp4") 
    print("翻译完成")
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_video_path")
    parser.add_argument("output_folder")
    args = parser.parse_args()
    input_video_path = args.input_video_path
    output_folder = args.output_folder
    print(f"输入视频路径: {input_video_path}")
    print(f"输出文件夹: {output_folder}")
    process(input_video_path, output_folder)

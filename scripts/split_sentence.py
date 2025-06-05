import json
import nltk
from faster_whisper import WhisperModel
import argparse
# 下载nltk的数据文件，用于句子分割
print("nltk开始下载punkt")
nltk.download('punkt')
nltk.download('punkt_tab')
def transcribe_and_segment_to_json(audio_path, output_json_path):
    # 初始化模型
    model = WhisperModel("tiny", device="cpu", compute_type="int8")
    # 使用 word_timestamps=True 来启用 words 属性
    segments, _ = model.transcribe(
        audio_path,
        beam_size=5,
        word_timestamps=True  # 关键参数，启用单词级时间戳
    )

    # 准备要写入json的数据
    transcript_data = []
    full_text = ""
    all_words = []

    # 首先收集所有单词及其时间戳
    for segment in segments:
        for word_info in segment.words:
            all_words.append(word_info)
            full_text += " " + word_info.word.strip()

    # 使用nltk进行句子分割
    sentences = nltk.tokenize.sent_tokenize(full_text.strip())

    current_sentence = ""
    sentence_segments = []
    current_start_time = None

    for word_info in all_words:
        if not current_sentence:
            current_start_time = word_info.start  # 记录当前句子的开始时间

        current_sentence += " " + word_info.word.strip()
        
        # 检查是否已经到达一个完整的句子结尾
        if any(sentence == current_sentence.strip() for sentence in sentences):
            matched_sentence = next(sentence for sentence in sentences if sentence == current_sentence.strip())
            
            # 添加到结果中
            sentence_segments.append({
                'start': current_start_time,
                'end': word_info.end,
                'text': matched_sentence
            })
            
            # 从sentences列表中移除已处理的句子
            sentences.remove(matched_sentence)
            current_sentence = ""  # 重置当前句子
            
        elif any(sentence.startswith(current_sentence.strip()) for sentence in sentences):
            # 如果当前句子是某个完整句子的开头，则继续构建
            continue
        else:
            # 如果当前构造的句子不是任何句子的开头或结尾，则重置
            current_sentence = ""
            current_start_time = None

    # 将数据写入json文件
    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(sentence_segments, json_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("audio_file_path")
    parser.add_argument("output_json_file_path")
    args = parser.parse_args()
    audio_file_path = args.audio_file_path
    output_json_file_path = args.output_json_file_path

    transcribe_and_segment_to_json(audio_file_path, output_json_file_path)


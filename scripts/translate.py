from transformers import MarianTokenizer, MarianMTModel
import ctranslate2
from pathlib import Path
# 加载模型和分词器
ct2_model_dir = "./ct2_model_en_zh"
model_name = "Helsinki-NLP/opus-mt-en-zh"
tokenizer = MarianTokenizer.from_pretrained(model_name)
if not Path(ct2_model_dir).exists():
    print("正在下载并转换模型...")
    # 加载 HuggingFace 模型和分词器
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)

    # 创建 TransformersConverter 实例并转换模型
    converter = ctranslate2.converters.TransformersConverter(model, tokenizer)
    converter.convert(ct2_model_dir)
    print(f"模型已保存至 {ct2_model_dir}")
translator = ctranslate2.Translator(ct2_model_dir, device="cpu")
def translate(text):
    # 分词
    tokens = tokenizer.convert_ids_to_tokens(tokenizer(text).input_ids)
    # 翻译
    results = translator.translate_batch([tokens])
    # 解码
    translated_tokens = results[0].hypotheses[0]
    translated_text = tokenizer.decode(
        tokenizer.convert_tokens_to_ids(translated_tokens),
        skip_special_tokens=True
    )
    return translated_text


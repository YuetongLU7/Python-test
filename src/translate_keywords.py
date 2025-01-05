from googletrans import Translator
import pandas as pd


def batch_translate(file_path):
    # 加载数据
    data = pd.read_csv(file_path)
    translator = Translator()

    # 确保 'keywords' 列为字符串，移除 NaN
    data['keywords'] = data['keywords'].fillna('').astype(str)

    # 合并所有关键词为一个长文本，使用换行符分隔
    combined_text = '\n'.join(data['keywords'].tolist())

    # 分块处理，避免超长文本问题
    def chunk_text(text, max_length=4000):
        chunks = []
        while len(text) > max_length:
            split_index = text.rfind('\n', 0, max_length)  # 在最大长度内找最后的换行符
            if split_index == -1:
                split_index = max_length  # 如果找不到换行符，直接按最大长度截断
            chunks.append(text[:split_index])
            text = text[split_index:].lstrip('\n')
        chunks.append(text)
        return chunks

    chunks = chunk_text(combined_text)

    # 翻译每一块并捕获异常
    translated_chunks = []
    for chunk in chunks:
        try:
            translated = translator.translate(chunk, src='zh-cn', dest='en').text
            translated_chunks.append(translated)
        except Exception as e:
            print(f"Error translating chunk: {chunk[:50]}..., Exception: {e}")
            translated_chunks.append(chunk)  # 保留原始文本

    # 合并翻译结果并拆分回行
    translated_text = '\n'.join(translated_chunks)
    translated_keywords = translated_text.split('\n')

    # 确保翻译结果与原始行数一致
    if len(translated_keywords) != len(data):
        print("Mismatch between original and translated rows!")
        return

    # 将翻译结果映射回 DataFrame
    data['translated'] = translated_keywords

    # 保存结果
    output_path = 'temp_files/translated_keywords.csv'
    data.to_csv(output_path, index=False)
    print(f"Translation complete and saved to {output_path}")



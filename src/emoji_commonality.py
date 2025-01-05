from matplotlib import pyplot as plt
import pickle
from word_commonality import calc_commonality
from deep_translator import GoogleTranslator


def translate_to_french(text: str):
    translation = GoogleTranslator(source='zh-CN', target='fr').translate(text)
    if not translation:
        raise ValueError(f"Translation failed for: {text}")
    return translation


def emoji_commonality(name_both: str = 'both', top_k: int = 5, figsize=(12, 12)):
    print('Calculate emoji_commonality')
    with open('temp_files/emoji_count.pkl', 'rb') as pf:
        dct = pickle.load(pf)
        d1_count = dct['d1']
        d2_count = dct['d2']

    common_df = calc_commonality(d1_count, d2_count)
    if 'commonality' not in common_df.columns:
        raise KeyError("common_df 缺少 'commonality' 列，请检查数据来源。")

    common_df.sort_values(by='commonality', ascending=False, inplace=True)
    top_k = min(top_k, common_df.shape[0])
    print(f'top_k should not exceed{common_df.shape[0]}')

    # 获取绘图数据
    common_values = common_df['commonality'].iloc[:top_k]
    y = list(range(len(common_values) - 1, -1, -1))
    emoji_labels = common_df['name'].iloc[:top_k].tolist()  # 使用 'name' 列作为标签

    # 绘制中文版本
    plt.close('all')
    plt.rc('font', family='SimSun', size=15)
    plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号
    plt.figure(1, figsize=figsize)
    plt.barh(y, common_values, color='C2')
    plt.yticks(y, emoji_labels)
    plt.xlabel('emoji共有性', fontsize=20)
    plt.ylabel('emoji', fontsize=20)
    plt.title(f'{name_both} Top {top_k} emojis', fontsize=20)

    plt.savefig(f'figs/{name_both} emoji commonality(zh).png')
    print(f'The Chinese version has been saved as: figs/{name_both} emoji commonality (zh).png')

    xlabel = translate_to_french('emoji共有性')
    ylabel = translate_to_french('emoji')
    title = translate_to_french(f'{name_both} Top {top_k} emojis')

    print(f"French translation: xlabel={xlabel}, ylabel={ylabel}, title={title}")

    plt.close('all')
    plt.figure(1, figsize=figsize)
    plt.barh(y, common_values, color='C2')
    plt.yticks(y, [translate_to_french(label) for label in emoji_labels])  # 翻译每个标签
    plt.xlabel(xlabel, fontsize=20)
    plt.ylabel(ylabel, fontsize=20)
    plt.title(title, fontsize=20)

    plt.savefig(f'figs/{name_both} emoji commonality(fr).png')
    print(f'The French version has been saved as: figs/{name_both} emoji commonality (fr).png')
    print('=' * 20)

    print(common_df.columns)


if __name__ == '__main__':
    emoji_commonality()

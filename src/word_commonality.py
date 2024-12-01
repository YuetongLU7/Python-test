from matplotlib import pyplot as plt
import pickle
from utils import calc_commonality
from deep_translator import GoogleTranslator


def translate_to_french(text: str):
    translation = GoogleTranslator(source='zh-CN', target='fr').translate(text)
    if not translation:
        raise ValueError(f"Translation failed for: {text}")
    return translation


def word_commonality(name_both: str = 'both', top_k: int = 25, figsize=(10, 12)):
    print('计算word_commonality')
    with open('temp_files/keyword_count.pkl', 'rb') as pf:
        dct = pickle.load(pf)
        d1_kw = dct['d1']
        d2_kw = dct['d2']
    common_df = calc_commonality(d1_kw, d2_kw)
    common_df.sort_values(by='commonality', ascending=False, inplace=True)
    print(f'top_k should not exceed{common_df.shape[0]}')
    plt.close('all')
    plt.rc('font', family='SimSun', size=15)
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    y = list(range(top_k - 1, -1, -1))
    plt.figure(1, figsize=figsize)
    plt.barh(y, common_df.iloc[:top_k, 3], color='C2')
    plt.yticks(y, common_df.iloc[:top_k, 0].tolist())
    plt.xlabel('词语共有性', fontsize=20)
    plt.ylabel('词语', fontsize=20)
    plt.title(f'{name_both} Top 25 words', fontsize=20)
    plt.savefig(f'figs/{name_both} word commonality(zh).png')

    xlabel = translate_to_french('词语共有性')
    ylabel = translate_to_french('词语')
    title = translate_to_french(f'{name_both} Top 25 words')

    plt.close('all')
    plt.rc('font', family='SimSun', size=15)
    plt.rcParams['axes.unicode_minus'] = False
    y = list(range(top_k - 1, -1, -1))
    plt.figure(1, figsize=figsize)
    plt.barh(y, common_df.iloc[:top_k, 3], color='C2')
    plt.yticks(y, [translate_to_french(label) for label in common_df.iloc[:top_k, 0].tolist()])
    plt.xlabel(xlabel, fontsize=20)
    plt.ylabel(ylabel, fontsize=20)
    plt.title(title, fontsize=20)
    plt.savefig(f'figs/{name_both} word commonality(fr).png')

    print('=' * 20)


if __name__ == '__main__':
    word_commonality()

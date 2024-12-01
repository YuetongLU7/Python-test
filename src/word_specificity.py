from matplotlib import pyplot as plt
import pickle
from utils import calc_specificity
from deep_translator import GoogleTranslator


def translate_to_french(text: str):
    translation = GoogleTranslator(source='zh-CN', target='fr').translate(text)
    if not translation:
        raise ValueError(f"Translation failed for: {text}")
    return translation


def word_specificity(name1: str = 'person 1', name2: str = 'person 2',
                     top_k: int = 25, word_min_count: int = 20,
                     figsize=(10, 12)):
    print('calculate word_specificity')
    with open('temp_files/keyword_count.pkl', 'rb') as pf:
        dct = pickle.load(pf)
        d1_kw = dct['d1']
        d2_kw = dct['d2']
    all_df = calc_specificity(d1_kw, d2_kw)
    print(f"word_min_count should not exceed{int(all_df['count'].max())}")
    all_df = all_df[all_df['count'] >= word_min_count]  # 词频小于20的词语，直接不考虑
    all_df.sort_values(by='specificity', inplace=True)
    print(f'top_k should not exceed{all_df.shape[0]}')
    plt.close('all')
    plt.rc('font', family='SimSun', size=15)
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    y = list(range(top_k - 1, -1, -1))
    plt.figure(1, figsize=figsize)
    all_df.sort_values(by='specificity', ascending=False, inplace=True)
    plt.barh(y, all_df.iloc[:top_k, 3], color='C1')
    plt.yticks(y, all_df.iloc[:top_k, 0].tolist())
    plt.xlabel('词语专属性', fontsize=20)
    plt.ylabel('词语', fontsize=20)
    plt.title(f'{name1} Top 25 words', fontsize=20)
    plt.savefig(f'figs/{name1} word specificity(zh).png')
    plt.figure(2, figsize=figsize)
    all_df.sort_values(by='specificity', ascending=True, inplace=True)
    plt.barh(y, -all_df.iloc[:top_k, 3])
    plt.yticks(y, all_df.iloc[:top_k, 0].tolist())
    plt.xlabel('词语专属性', fontsize=20)
    plt.ylabel('词语', fontsize=20)
    plt.title(f'{name2} Top 25 words', fontsize=20)
    plt.savefig(f'figs/{name2} word specificity(zh).png')

    xlabel = translate_to_french('词语专属性')
    ylabel = translate_to_french('词语')
    title = translate_to_french(f'{name1} Top 25 words')

    plt.close('all')
    plt.rc('font', family='SimSun', size=15)
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    y = list(range(top_k - 1, -1, -1))
    plt.figure(1, figsize=figsize)
    all_df.sort_values(by='specificity', ascending=False, inplace=True)
    plt.barh(y, all_df.iloc[:top_k, 3], color='C1')
    plt.yticks(y, [translate_to_french(label) for label in all_df.iloc[:top_k, 0].tolist()])
    plt.xlabel(xlabel, fontsize=20)
    plt.ylabel(ylabel, fontsize=20)
    plt.title(title, fontsize=20)
    plt.savefig(f'figs/{name1} word specificity(fr).png')
    plt.figure(2, figsize=figsize)
    all_df.sort_values(by='specificity', ascending=True, inplace=True)
    plt.barh(y, -all_df.iloc[:top_k, 3])
    plt.yticks(y, [translate_to_french(label) for label in all_df.iloc[:top_k, 0].tolist()])
    plt.xlabel(xlabel, fontsize=20)
    plt.ylabel(ylabel, fontsize=20)
    plt.title(f'{name2} Top 25 words', fontsize=20)
    plt.savefig(f'figs/{name2} word specificity(fr).png')

    # plt.show()
    print('=' * 20)


if __name__ == '__main__':
    word_specificity(min_cout=1)

import pandas as pd
from matplotlib import pyplot as plt
from collections import Counter
import pickle
from utils import calc_specificity
from deep_translator import GoogleTranslator


def translate_to_french(text: str):
    translation = GoogleTranslator(source='zh-CN', target='fr').translate(text)
    if not translation:
        raise ValueError(f"Translation failed for: {text}")
    return translation


def emoji_specificity(name1: str = 'person 1', name2: str = 'person 2',
                      top_k: int = 5, emoji_min_count: int = 1,
                      figsize=(10, 12)):
    print('计算emoji_specificity')
    raw = pd.read_csv('temp_files/keywords.csv')[['IsSender', 'emoji']].dropna()
    # 自己
    d1_emoji = ', '.join(raw.loc[raw['IsSender'] == 1, 'emoji'].to_list()).split(', ')
    # 对方
    d2_emoji = ', '.join(raw.loc[raw['IsSender'] == 0, 'emoji'].to_list()).split(', ')
    d1_count = Counter(d1_emoji)
    d2_count = Counter(d2_emoji)
    with open('temp_files/emoji_count.pkl', 'wb') as pf:
        pickle.dump({'d1': d1_count, 'd2': d2_count}, pf)
    all_df = calc_specificity(d1_count, d2_count)
    print(f"emoji_min_count should not exceed {int(all_df['count'].max())}")
    all_df = all_df[all_df['count'] > emoji_min_count]
    all_df.sort_values(by='specificity', inplace=True)
    print(f'top_k should not exceed {all_df.shape[0]}')
    plt.close('all')
    plt.rc('font', family='SimSun', size=15)
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    y = list(range(top_k - 1, -1, -1))
    plt.figure(1, figsize=figsize)
    all_df.sort_values(by='specificity', ascending=False, inplace=True)
    plt.barh(y, all_df.iloc[:top_k, 3], color='C1')
    plt.yticks(y, all_df.iloc[:top_k, 0].tolist())
    plt.xlabel('emoji专属性', fontsize=20)
    plt.ylabel('emoji', fontsize=20)
    plt.title(f'{name1} Top 5 emojis', fontsize=20)
    plt.savefig(f'figs/{name1} emoji specificity(zh).png')
    plt.figure(2, figsize=figsize)
    all_df.sort_values(by='specificity', ascending=True, inplace=True)
    plt.barh(y, -all_df.iloc[:top_k, 3])
    plt.yticks(y, all_df.iloc[:top_k, 0].tolist())
    plt.xlabel('emoji专属性', fontsize=20)
    plt.ylabel('emoji', fontsize=20)
    plt.title(f'{name2} Top 5 emojis', fontsize=20)
    plt.savefig(f'figs/{name2} emoji specificity(zh).png')

    xlabel = translate_to_french('emoji专属性')
    ylabel = translate_to_french('emoji')
    title = translate_to_french(f'{name2} Top 5 emojis')

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
    plt.savefig(f'figs/{name1} emoji specificity(fr).png')
    plt.figure(2, figsize=figsize)
    all_df.sort_values(by='specificity', ascending=True, inplace=True)
    plt.barh(y, -all_df.iloc[:top_k, 3])
    plt.yticks(y, [translate_to_french(label) for label in all_df.iloc[:top_k, 0].tolist()])
    plt.xlabel(xlabel, fontsize=20)
    plt.ylabel(ylabel, fontsize=20)
    plt.title(title, fontsize=20)
    plt.savefig(f'figs/{name2} emoji specificity(fr).png')
    # plt.show()
    print('=' * 20)


if __name__ == '__main__':
    emoji_specificity()

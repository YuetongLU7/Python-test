import pandas as pd
from collections import Counter
from pyecharts import options as opts
from pyecharts.charts import WordCloud
import pickle


def makeWC(data: list, name: str,
           bg_img=None  # 可自定义背景图片
           ):
    data = ', '.join(data).split(', ')
    wordCounter = Counter(data)
    if '[' in wordCounter:
        wordCounter.pop('[')
    if ']' in wordCounter:
        wordCounter.pop(']')
    # for key, val in wordCounter.most_common():
    #     print(key, val)
    count_res = [(key, val) for key, val in wordCounter.most_common()]
    wordcloud = (
        WordCloud()
        .add("", data_pair=count_res[:150], word_size_range=[15, 80], mask_image=bg_img,
             textstyle_opts=opts.TextStyleOpts(font_family='Microsoft YaHei', font_weight='bold'))
        .set_global_opts(title_opts=opts.TitleOpts(
            title=f'{name}Word Cloud',
            title_textstyle_opts=opts.TextStyleOpts(font_size=25,
                                                    color="midnight")))
        .render(f'figs/{name}_WC.html')
    )
    return wordCounter


def wc_main(name_both: str = 'both', name1: str = 'person 1', name2: str = 'person 2'):
    print('Calculate word frequency and make word cloud')
    raw = pd.read_csv('temp_files/keywords.csv')[['IsSender', 'keywords']].dropna()
    both = raw['keywords']
    d1 = raw.loc[raw['IsSender'] == 1, 'keywords']
    d2 = raw.loc[raw['IsSender'] == 0, 'keywords']
    makeWC(both.to_list(), name_both)
    d1_res = makeWC(d1.to_list(), name1)
    d2_res = makeWC(d2.to_list(), name2)
    with open('temp_files/keyword_count.pkl', 'wb') as pf:
        pickle.dump({'d1': d1_res, 'd2': d2_res}, pf)
    print('=' * 20)


if __name__ == '__main__':
    wc_main()

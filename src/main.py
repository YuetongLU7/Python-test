from parse import parse
from src.radar import generate_emotion_radar_chart
from word_cloud import wc_main
from word_specificity import word_specificity
from emoji_specificity import emoji_specificity
from word_commonality import word_commonality
from emoji_commonality import emoji_commonality
from time_analysis import time_ana
from translate_keywords import batch_translate
from emotion_analysis import analyze_emotions
import yaml
import os

# Open the file named 'config.yml' in read-only mode
with open('config.yml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)


def main(config_data):
    msg_file = config_data['msg_file']
    emoji_file = config_data['emoji_file']
    stopword_file = config_data['stopword_file']
    transform_file = config_data['transform_file']
    user_dict_file = config_data['user_dict_file']
    name_both = config_data['name_both']
    name1 = config_data['name1']
    name2 = config_data['name2']

    if not os.path.exists('figs'):
        os.mkdir('figs')
    if not os.path.exists('temp_files'):
        os.mkdir('temp_files')

    parse(msg_file, emoji_file, stopword_file, transform_file, user_dict_file)
    wc_main(name_both, name1, name2)
    # batch_translate('temp_files/keywords.csv')
    # word_specificity(name1, name2, **config_data['word_specificity'])
    # emoji_specificity(name1, name2, **config_data['emoji_specificity'])
    # word_commonality(name_both, **config_data['word_commonality'])
    # emoji_commonality(name_both, **config_data['emoji_commonality'])
    time_ana(msg_file, **config_data['time_analysis'])
    analyze_emotions("temp_files/translated_keywords.csv")
    generate_emotion_radar_chart("temp_files/emotion_analysis.csv")

    print('analysis done !')


if __name__ == '__main__':
    main(config)

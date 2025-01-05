from pyecharts import options as opts
from pyecharts.charts import Radar
import pandas as pd
import os


def generate_emotion_radar_chart(file_path, output_path="/figs/emotion_radar_chart.html"):
    data = pd.read_csv(file_path)
    average_emotions = data[['joy', 'anger', 'fear', 'sadness', 'surprise', 'disgust']].mean()
    labels = ['La joie', 'La colère', 'La peur', 'La triste', 'La surprise', 'Le dégoût']
    values = list(average_emotions)

    radar = (
        Radar()
        .add_schema(
            schema=[opts.RadarIndicatorItem(name=label, max_=1) for label in labels]
        )
        .add(
            series_name="Score moyens des émotions",
            data=[values],
            linestyle_opts=opts.LineStyleOpts(width=2),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Radar des émotions"),
            legend_opts=opts.LegendOpts(is_show=True),
        )
    )

    output_dir = "figs"
    output_path = os.path.join(output_dir, "emotion_radar_chart.html")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # Create directory if it does not exist

    # Save the radar chart
    radar.render(output_path)



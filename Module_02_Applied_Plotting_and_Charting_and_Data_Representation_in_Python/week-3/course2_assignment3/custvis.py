import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib import cm

np.random.seed(12345)

df = pd.DataFrame([np.random.normal(32000, 200000, 3650),
                   np.random.normal(43000, 100000, 3650),
                   np.random.normal(43500, 140000, 3650),
                   np.random.normal(48000, 70000, 3650)],
                  index=[1992, 1993, 1994, 1995])

intervals = []
for idx in df.index:
    interval = stats.norm.interval(0.95, np.mean(df.loc[idx]), stats.sem(df.loc[idx]))
    intervals.append(interval)

err = np.array([stats.norm.interval(0.95, np.mean(df.loc[idx]), stats.sem(df.loc[idx])) - np.mean(df.loc[idx])
                for idx in df.index]).T

index = df.T.describe().loc['mean', :].index.values
values = df.T.describe().loc['mean', :].values
y = np.mean(values)

plt.figure()
cmap = cm.get_cmap('coolwarm')

def calculate_probability(y, interval):
    if y < interval[0]:
        return 1
    elif y > interval[1]:
        return -1
    return 2 * ((interval[1] + interval[0]) / 2 - y) / (interval[1] - interval[0])

probs = [calculate_probability(y, interval) for interval in intervals]

colors = cmap(probs)
sm = cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(-1, 1))
sm.set_array([])

bars = plt.bar(range(len(values)), values, color=sm.to_rgba(probs))
plt.gca().errorbar(range(len(values)), values, yerr=abs(err), c='k', fmt=' ', capsize=15)
plt.xticks(range(len(values)), index)
plt.ylabel('Value')
plt.xlabel('Year')
plt.ylim([0, 60000])
plt.gca().set_title('Even Harder option')
plt.colorbar(sm, orientation='horizontal')
[plt.gca().spines[loc].set_visible(False) for loc in ['top', 'right']]
[plt.gca().spines[loc].set_alpha(0.3) for loc in ['left', 'bottom']]

yticks = plt.gca().get_yticks()
new_yticks = np.append(yticks, y)
plt.gca().set_yticks(new_yticks)

h_line = plt.axhline(y, color='gray', linestyle='--', linewidth=1)
text = plt.text(1.5, 57200, 'y={:5.0f}'.format(y), bbox={'fc': 'w', 'ec': 'w'}, ha='center')
text_annotations = [
    plt.text(bars[i].get_x() + bars[i].get_width() / 2, bars[i].get_height() + 10000,
             'probs={:.2f}'.format(1 - abs(probs[i]))) for i in range(len(bars))
]

def onclick(event):
    probs = [calculate_probability(event.ydata, interval) for interval in intervals]
    colors = cmap(probs)
    for i, bar in enumerate(bars):
        bar.set_color(colors[i])
    plt.gca().errorbar(range(len(values)), values, yerr=abs(err), c='k', fmt=' ', capsize=15)
    h_line.set_ydata(event.ydata)
    new_yticks = np.append(yticks, event.ydata)
    plt.gca().set_yticks(new_yticks)
    text.set_text('y={:5.0f}'.format(event.ydata))
    for i, text_ann in enumerate(text_annotations):
        text_ann.set_text('probs={:.2f}'.format(1 - abs(probs[i])))
    plt.gcf().canvas.draw()

plt.gcf().canvas.mpl_connect('button_press_event', onclick)
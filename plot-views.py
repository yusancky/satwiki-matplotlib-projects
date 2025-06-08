import csv
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.dates import DateFormatter, MonthLocator, DayLocator, drange, num2date
from matplotlib.ticker import FixedLocator, FuncFormatter

typ = '阅读数'

def format_date(x, pos=None):
    d = num2date(x)
    if d.month == 1:
        return f"{str(d.year)[2:4]}年1月"
    else:
        if d.year != 2020 or d.month != 7:
            return f"{d.month}月"
        else:
            return "20年7月"

def format_num(x, pos=None):
    return f"{int(x)}{(2 * (5 - len(str(int(x)))))* ' '}"

date1 = datetime(2020, 6, 28)
date2 = datetime(2025, 6, 1)
dates = drange(date1, date2, timedelta(hours=24))

y = []
with open('data/view.csv') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        if len(row) > 1:
            y.append(int(row[1]))

y = y[0:len(dates)]

font_path = "font"
font_files = font_manager.findSystemFonts(fontpaths=font_path)
for file in font_files:
    font_manager.fontManager.addfont(file)
plt.rcParams["font.sans-serif"] = "Noto Sans SC"
plt.rcParams["font.size"] = 15

fig, ax = plt.subplots()
ax.plot(dates, y, '#306FB6', linewidth=1, label=typ)
ax.set_ylim(0, min(max(y), 31000))
yticks = range(5000, min(max(y), 31000), 5000)
yticks_minor = range(1000, min(max(y), 31000), 1000)

ax.set_xlabel('日期', color='#306FB6')
ax.tick_params(axis='x', labelcolor='#306FB6')
ax.tick_params(axis='y', labelcolor='#306FB6', pad=-50)

fig.set_size_inches(16, 9)
ax.set_xlim(dates[0], dates[-1])
ax.xaxis.set_major_locator(MonthLocator(interval=6))
ax.xaxis.set_major_formatter(FuncFormatter(format_date))
ax.xaxis.set_minor_locator(MonthLocator())
ax.yaxis.set_major_locator(FixedLocator(yticks))
ax.yaxis.set_major_formatter(FuncFormatter(format_num))
ax.yaxis.set_minor_locator(FixedLocator(yticks_minor))
fig.tight_layout()

plt.title(f'{typ}统计', color='#306FB6')

plt.savefig('output/edit-view-counts.pdf', dpi = 480, bbox_inches='tight')
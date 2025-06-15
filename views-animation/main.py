import csv
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.dates import DateFormatter, MonthLocator, drange, num2date
from matplotlib.ticker import FixedLocator, FuncFormatter
from tqdm import tqdm

# 定义辅助函数
def format_number(x, pos=None):
    return f"{int(x)}{(2 * (5 - len(str(int(x)))))* ' '}"


# 设置时间跨度
date_start, date_end = datetime(2020, 6, 28), datetime(2025, 5, 31)
plot_start = datetime(2020, 12, 28)
dates = drange(date_start, date_end + timedelta(days=1), timedelta(days=1))

# 读取 CSV 数据
views = []
with open("data/view.csv") as file:
    reader = csv.reader(file)
    next(reader)
    views.extend(int(row[1]) for row in reader if len(row) > 1)

# 设置字体
font_path = "font"
font_files = font_manager.findSystemFonts(fontpaths=font_path)
for file in font_files:
    font_manager.fontManager.addfont(file)
plt.rcParams["font.sans-serif"] = "Noto Sans SC"
plt.rcParams["font.size"] = 18


def plot(date, output, dpi=240):
    # 创建图表
    fig, ax = plt.subplots(figsize=(16, 9))
    plt.title("阅读数统计", color="#1A60A6", fontsize=24)
    ax.plot(dates, views, color="#1A60A6", linewidth=1)

    # 设置 X 轴
    ax.set_xlim(date_start, date)
    ax.tick_params(axis="x", labelcolor="#8691A5")
    ax.xaxis.set_major_locator(MonthLocator(interval=3))
    ax.xaxis.set_ticklabels([])

    # 设置 Y 轴
    plot_days = (date - plot_start).days + 1
    max_view = 2000
    if plot_days < 478:
        max_view = int(2000 - 1.5 * (478 - plot_days))
    elif plot_days < 728:
        max_view = 56 * (plot_days - 478) + 2000
    else:
        max_view = int(16000 + 0.4 * (plot_days - 728))
    ax.set_ylim(0, max_view)
    if max_view >= 5000:
        yticks_major = range(2000, max_view, 2000)
        yticks_minor = range(500, max_view, 500)
    elif max_view >= 3000:
        yticks_major = range(1000, max_view, 1000)
        yticks_minor = range(200, max_view, 200)
    else:
        yticks_major = range(500, max_view, 500)
        yticks_minor = range(100, max_view, 100)
    ax.tick_params(axis="y", labelcolor="#8691A5", pad=-57.5)
    ax.yaxis.set_major_locator(FixedLocator(yticks_major))
    ax.yaxis.set_minor_locator(FixedLocator(yticks_minor))
    ax.yaxis.set_major_formatter(FuncFormatter(format_number))

    # 注明阅读数与日期
    ax.text(
        0.995,
        0.985,
        str(views[(date - date_start).days]),
        color="#7C4997",
        fontsize=60,
        ha="right",
        va="top",
        transform=ax.transAxes,
        alpha=0.9,
    )
    ax.text(
        0.995,
        0.89,
        date.strftime("%Y-%m-%d"),
        color="#815252",
        fontsize=20,
        ha="right",
        va="top",
        transform=ax.transAxes,
        alpha=0.9,
    )

    # 保存图片
    plt.tight_layout()
    for i in output:
        plt.savefig(i, dpi=dpi, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    plot_frames = 1
    plot_dates = drange(plot_start, date_end + timedelta(days=1), timedelta(days=1))
    plot_days_all = len(plot_dates)
    for date_num in tqdm(plot_dates):
        plot_now = num2date(date_num).replace(tzinfo=None)
        plot_days = (plot_now - plot_start).days + 1
        step = 1
        if plot_days <= 20 or plot_days > plot_days_all - 20:
            step = 5 - min(plot_days - 1, plot_days_all - plot_days) // 5
        elif plot_days > 850 and plot_days <= 1500 and plot_days % 2 == 0:
            plot_days += 1
            continue
        plot(
            plot_now,
            [f"output/{i}.png" for i in range(plot_frames, plot_frames + step)],
        )
        plot_days += 1
        plot_frames += step

import csv
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.dates import DateFormatter, MonthLocator, drange, num2date
from matplotlib.ticker import FixedLocator, FuncFormatter

# 定义辅助函数
def format_date(x, pos=None):
    date_obj = num2date(x)
    if date_obj.month <= 6:
        return f"{str(date_obj.year)[2:4]}年{date_obj.month}月"
    return (
        f"{date_obj.month}月"
        if date_obj.year != 2020
        else f"{str(date_obj.year)[2:4]}年{date_obj.month}月"
    )


def format_number(x, pos=None):
    return f"{int(x)}{(2 * (5 - len(str(int(x)))))* ' '}"


# 读取 CSV 数据
views_all = []
with open("data/view.csv") as file:
    reader = csv.reader(file)
    next(reader)
    views_all.extend(int(row[1]) for row in reader if len(row) > 1)
# 设置字体
font_path = "font"
font_files = font_manager.findSystemFonts(fontpaths=font_path)
for file in font_files:
    font_manager.fontManager.addfont(file)
plt.rcParams["font.sans-serif"] = "Noto Sans SC"
plt.rcParams["font.size"] = 18


def plot(year, month, day, output, dpi):
    # 设置时间跨度
    start_date = datetime(2020, 6, 28)
    end_date = datetime(year, month, day)
    dates = drange(start_date, end_date, timedelta(hours=24))
    days = len(dates)
    views = views_all[:days]

    # 创建图表
    fig, ax = plt.subplots(figsize=(16, 9))
    plt.title("阅读数统计", color="#1A60A6", fontsize=24)
    ax.plot(dates, views, color="#1A60A6", linewidth=1)

    # 设置 X 轴
    ax.set_xlim(dates[0], dates[-1])
    ax.tick_params(axis="x", labelcolor="#8691A5")
    ax.xaxis.set_major_locator(MonthLocator(interval=6))
    ax.xaxis.set_major_formatter(FuncFormatter(format_date))
    ax.xaxis.set_minor_locator(MonthLocator())

    # 设置 Y 轴
    max_view = 2000
    if days < 657:
        max_view = int(2000 - 1.2 * (658 - days))
    elif days < 728:
        max_view = 200 * (days - 658) + 2000
    else:
        max_view = int(16000 + 0.5 * (days - 728))
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
    ax.yaxis.set_major_formatter(FuncFormatter(format_number))
    ax.yaxis.set_minor_locator(FixedLocator(yticks_minor))

    # 注明阅读数与日期
    ax.text(
        0.995,
        0.985,
        str(views[-1]),
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
        end_date.strftime("%Y-%m-%d"),
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


if __name__ == "__main__":
    plot_now, plot_end, plot_days, plot_frames = (
        datetime(2020, 12, 28),
        datetime(2025, 6, 1),
        1,
        1,
    )
    while plot_now <= plot_end:
        step = 1
        if plot_days <= 5 or plot_days > 1617 - 5:
            step = 5
        elif plot_days <= 65 or plot_days > 1617 - 65:
            step = 2
        print(f"Ploting day {plot_days} for {step} frames.")
        plot(
            plot_now.year,
            plot_now.month,
            plot_now.day,
            [f"output/{i}.png" for i in range(plot_frames, plot_frames + step)],
            240,
        )
        plot_now += timedelta(days=1)
        plot_days += 1
        plot_frames += step

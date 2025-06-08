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
    for row in reader:
        if len(row) > 1:
            views_all.append(int(row[1]))

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
    end_date = datetime(args.year, args.month, args.day)
    dates = drange(start_date, end_date, timedelta(hours=24))
    views = views[: len(dates)]

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
    if len(dates) > 728:
        max_view = 16000
    elif len(dates) > 658:
        max_view = 200 * (len(dates) - 658) + 2000
    ax.set_ylim(0, max_view)
    if max_view >= 5000:
        yticks_major = range(2500, max_view, 2500)
    elif max_view >= 3000:
        yticks_major = range(1000, max_view, 1000)
    else:
        yticks_major = range(500, max_view, 500)
    yticks_minor = range(500, max_view, 500)
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
    plt.savefig(output, dpi=dpi, bbox_inches="tight")

if __name__ == '__main__:
    plot(2021, 6, 28, 'output/1.png', 240)

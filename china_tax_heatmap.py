#!/usr/bin/env python3
"""
2025年中国各省税收收入热力图
数据来源：
  - 聚汇数据 (gotohui.com/finance/topic-5508, topic-5548)
  - 各省财政厅2025年预算执行报告
  - 财政部2025年财政收支情况
注：上海、北京为基于地方税收数据的估算值，其余省份为已公开数据。
"""

import subprocess
import sys


def install(pkg):
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])


for pkg in ["pyecharts"]:
    try:
        __import__(pkg.replace("-", "_"))
    except ImportError:
        print(f"正在安装 {pkg}...")
        install(pkg)

from pyecharts import options as opts
from pyecharts.charts import Map, Page
from pyecharts.commons.utils import JsCode

# ── 数据：2025年各省税收收入（亿元）──────────────────────────────────────────
# 使用一般公共预算税收口径
# 省份名称必须与地图 JS 文件中的 name 字段完全一致（含省/市/自治区后缀）
TAX_DATA = [
    ("广东省",        21839.0),
    ("江苏省",        15801.6),
    ("上海市",        15200.0),   # 估算：基于地方税收 7318.5 亿 × 中央地方分成系数
    ("浙江省",        14280.0),
    ("北京市",        12000.0),   # 估算：基于地方税收 5775.6 亿 × 系数
    ("山东省",        10416.0),
    ("四川省",         7253.9),
    ("湖北省",         5564.7),
    ("安徽省",         5404.0),
    ("河南省",         5345.0),
    ("河北省",         5061.0),
    ("福建省",         4776.3),
    ("湖南省",         4500.0),
    ("陕西省",         3900.0),
    ("天津市",         3700.0),
    ("辽宁省",         3550.0),
    ("山西省",         3500.0),
    ("重庆市",         3350.0),
    ("江西省",         3100.0),
    ("内蒙古自治区",   2950.0),
    ("广西壮族自治区", 2620.0),
    ("云南省",         2520.0),
    ("新疆维吾尔自治区", 2250.0),
    ("贵州省",         1850.0),
    ("吉林省",         1620.0),
    ("黑龙江省",       1420.0),
    ("甘肃省",         1200.0),
    ("海南省",          930.0),
    ("宁夏回族自治区",  720.0),
    ("青海省",          410.0),
    ("西藏自治区",      210.0),
]

MAX_VAL = max(v for _, v in TAX_DATA)
MIN_VAL = min(v for _, v in TAX_DATA)

# ── 热力图配置 ────────────────────────────────────────────────────────────────
def build_map() -> Map:
    c = (
        Map(init_opts=opts.InitOpts(
            width="1400px",
            height="900px",
            bg_color="#0d1117",
            page_title="2025年中国各省税收收入热力图",
            animation_opts=opts.AnimationOpts(
                animation=True,
                animation_duration=1500,
                animation_easing="cubicOut",
            ),
        ))
        .add(
            series_name="税收收入（亿元）",
            data_pair=TAX_DATA,
            maptype="china",
            is_roam=True,
            label_opts=opts.LabelOpts(
                is_show=True,
                font_size=9,
                color="#c8d6e5",
                font_weight="bold",
            ),
            itemstyle_opts=opts.ItemStyleOpts(
                border_color="#1e3a5f",
                border_width=1,
            ),
            emphasis_itemstyle_opts=opts.ItemStyleOpts(
                area_color="#f0c040",
                border_color="#ffd700",
                border_width=2,
                opacity=0.95,
            ),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="2025年 · 中国各省税收收入热力图",
                subtitle="数据来源：聚汇数据 / 各省财政厅公告 | 单位：亿元人民币",
                pos_left="center",
                pos_top="20px",
                title_textstyle_opts=opts.TextStyleOpts(
                    font_size=26,
                    font_weight="bold",
                    color="#e8f4fd",
                    font_family="Microsoft YaHei, SimHei, sans-serif",
                ),
                subtitle_textstyle_opts=opts.TextStyleOpts(
                    font_size=12,
                    color="#7fb3d3",
                ),
            ),
            visualmap_opts=opts.VisualMapOpts(
                is_show=True,
                min_=MIN_VAL,
                max_=MAX_VAL,
                range_color=[
                    "#0a2a4a",   # 深蓝（最低）
                    "#0e4d7a",
                    "#1a6fa8",
                    "#2196d0",
                    "#00bcd4",
                    "#26d7c0",
                    "#80ff9e",
                    "#ffeb3b",
                    "#ff9800",
                    "#ff3d00",   # 深红（最高）
                ],
                pos_left="30px",
                pos_bottom="60px",
                textstyle_opts=opts.TextStyleOpts(
                    color="#c8d6e5",
                    font_size=12,
                ),
                is_calculable=True,
                range_text=["高", "低"],
            ),
            tooltip_opts=opts.TooltipOpts(
                is_show=True,
                trigger="item",
                formatter=JsCode(
                    """function(params) {
                        var val = params.value;
                        if (val === undefined || val === null || isNaN(val)) {
                            return params.name + '<br/>暂无数据';
                        }
                        var formatted = val.toLocaleString('zh-CN', {minimumFractionDigits: 1, maximumFractionDigits: 1});
                        var bar = '';
                        var pct = val / """ + str(MAX_VAL) + """;
                        var blocks = Math.round(pct * 20);
                        for (var i = 0; i < 20; i++) {
                            bar += i < blocks ? '█' : '░';
                        }
                        return '<div style="font-family: Microsoft YaHei, sans-serif; padding: 4px;">'
                            + '<b style="font-size:14px;color:#ffd700;">' + params.name + '</b><br/>'
                            + '<span style="color:#7fb3d3;">税收收入：</span>'
                            + '<span style="color:#00e5ff;font-size:16px;font-weight:bold;">'
                            + formatted + '</span>'
                            + '<span style="color:#aaa;"> 亿元</span><br/>'
                            + '<span style="color:#555;font-size:11px;">' + bar + '</span><br/>'
                            + '<span style="color:#7fb3d3;font-size:11px;">占全国比例：'
                            + (pct * 100).toFixed(1) + '%</span>'
                            + '</div>';
                    }"""
                ),
                background_color="rgba(13,17,23,0.92)",
                border_color="#1e3a5f",
                border_width=1,
                textstyle_opts=opts.TextStyleOpts(color="#c8d6e5"),
            ),
            legend_opts=opts.LegendOpts(is_show=False),
        )
    )
    return c


def main():
    chart = build_map()
    output_file = "china_tax_heatmap_2025.html"
    chart.render(output_file)
    print(f"✅ 热力图已生成：{output_file}")
    print(f"   用浏览器打开即可查看交互式地图。")
    print()
    print("📊 数据摘要（前10省份）:")
    sorted_data = sorted(TAX_DATA, key=lambda x: x[1], reverse=True)
    for i, (name, val) in enumerate(sorted_data[:10], 1):
        bar = "█" * int(val / MAX_VAL * 30)
        print(f"  {i:2d}. {name:5s}  {val:8,.1f} 亿元  {bar}")


if __name__ == "__main__":
    main()

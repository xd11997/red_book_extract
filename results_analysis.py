import matplotlib
import pandas as pd
import emoji
import seaborn as sns
import matplotlib.pyplot as plt
import platform
import matplotlib_inline

file_name = input("请输入需要分析的csv文件名称：") # 小红书_西安后海_笔记内容.csv

def most_hot_tag(file_name):
    df = pd.read_csv(file_name)
    # 创建一个空字典以计算每个标签出现的次数
    tag_counts = {}
    for index, row in df.iterrows():
        tags_cell = row['笔记标签']
        if isinstance(tags_cell, str):
            tags = tags_cell.split(",")
            for tag in tags:
                tag = tag.strip()
                tag_counts[tag] = tag_counts.get(tag, 0) + 1

    sorted_tag_counts = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
    new_df = pd.DataFrame(columns=['笔记标签', '出现次数'])
    for tag, count in sorted_tag_counts:
        new_df = new_df._append({'笔记标签': tag, '出现次数':count}, ignore_index=True)

    new_df.to_csv(f'{file_name}_标签频次.csv', index=False)
    print(new_df.to_string())
    return

def content_emoji_importance(file_name):
    df = pd.read_csv(file_name)
    df['笔记内容'] = df['笔记内容'].astype(str)
    df['emoji_nums'] = df['笔记内容'].apply(lambda desc: len(emoji.emoji_list(desc)))
    print(df['emoji_nums'].to_string())
    print(df['emoji_nums'].describe())
    pass
    return

def data_distribution(file_name):
    df = pd.read_csv(file_name)
    df = df[~df['点赞数'].str.contains('\+')]
    df['点赞数'] = df['点赞数'].astype('int')
    print(df.点赞数.describe())
    matplotlib_inline.backend_inline.set_matplotlib_formats('png', 'svg')
    # 获取操作系统类型
    system = platform.system()
    if system == 'Windows':
        font = {'family': 'SimHei'}
    elif system == 'Darwin':
        font = {'family': 'Arial Unicode MS'}
    else:
        # 如果是其他系统，可以使用系统默认字体
        font = {'family': 'sans-serif'}
    # 设置全局字体
    matplotlib.rc('font', **font)

    sns.histplot(df.点赞数)
    plt.xlabel('likes')
    plt.ylabel('distribution')
    plt.title('likes_distribution')
    plt.show()
    return

if __name__ == "__main__":
    most_hot_tag(file_name)
    # content_emoji_importance(file_name)
    # data_distribution(file_name)

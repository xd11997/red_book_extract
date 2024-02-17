import pandas as pd

file_name = input("请输入需要分析的csv文件名称：") # 小红书_美国商科转码硕士_笔记内容.csv

def most_hot_tag(file_name):
    df = pd.read_csv(file_name)

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
if __name__ == "__main__":
    most_hot_tag(file_name)
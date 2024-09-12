import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import requests
import json

# 初始化主题变量
current_theme = "flatly"  # 浅色主题
dark_theme = "superhero"  # 深色主题

# 创建主窗口
app = tb.Window(themename=current_theme)
app.title("Music API")
app.geometry("600x600")

# 创建输入框和按钮的框架
input_frame = ttk.Frame(app)
input_frame.pack(pady=10)

# 输入标签
music_label = ttk.Label(input_frame, text="请输入音乐链接：")
music_label.grid(row=0, column=0, padx=5, pady=5)

# 输入框
music_entry = ttk.Entry(input_frame, width=40)
music_entry.grid(row=0, column=1, padx=5, pady=5)

# 提交按钮
submit_button = ttk.Button(input_frame, text="提交", command=lambda: app.after(0, submit_form))
submit_button.grid(row=1, column=0, columnspan=2, pady=10)

# 主题切换按钮
def toggle_theme():
    global current_theme
    if current_theme == "flatly":
        current_theme = dark_theme
    else:
        current_theme = "flatly"
    app.style.theme_use(current_theme)

toggle_button = ttk.Button(input_frame, text="切换白天/黑夜模式", command=toggle_theme)
toggle_button.grid(row=2, column=0, columnspan=2, pady=10)

# 输出框架
output_frame = ttk.Frame(app)
output_frame.pack(pady=10)

# 输出文本框显示关键字匹配结果
keyword_result = tk.Text(output_frame, height=6, width=70)
keyword_result.pack(pady=5)

# 输出文本框显示所有评论
comment_result = tk.Text(output_frame, height=10, width=70)
comment_result.pack(pady=5)

# 输出文本框显示推测的曲风
genre_result = tk.Text(output_frame, height=3, width=70)
genre_result.pack(pady=5)

# 加载关键词和曲风
def load_keywords():
    with open("keywords.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        return [keyword.lower() for keyword in data["keywords"]]

keywords = load_keywords()

# 处理表单提交
def submit_form():
    music_link = music_entry.get()
    if not music_link:
        return
    # 构造 API 请求链接
    try:
        link_params = music_link.split('?')[1]
    except IndexError:
        comment_result.delete("1.0", tk.END)
        comment_result.insert(tk.END, "请输入有效的音乐链接")
        return

    api_url = f"https://music-apin-etease.vercel.app/comment/music?{link_params}&limit=100"

    # 清空结果区域
    keyword_result.delete("1.0", tk.END)
    comment_result.delete("1.0", tk.END)
    genre_result.delete("1.0", tk.END)

    # 显示“请稍后...”
    keyword_result.insert(tk.END, "请稍后...\n")
    comment_result.insert(tk.END, "请稍后...\n")
    genre_result.insert(tk.END, "正在推测曲风...\n")

    # 发送请求
    try:
        response = requests.post(api_url)
        data = response.json()
        comments = data.get("comments", [])
        comment_count = len(comments)

        # 展示评论结果
        result_text = f"评论数：{comment_count}\n\n"
        keyword_result_text = ""
        genre_set = set()  # 存储推测出的曲风

        for comment in comments:
            result_text += f"Nickname: {comment['user']['nickname']}\nContent: {comment['content']}\n\n"
            comment_content_lowercase = comment['content'].lower()
            for keyword in keywords:
                if keyword in comment_content_lowercase:
                    keyword_result_text += f"Nickname: {comment['user']['nickname']}\nContent: {comment['content']}\n\n"
                    genre_set.add(keyword)

        # 更新输出
        comment_result.delete("1.0", tk.END)
        comment_result.insert(tk.END, result_text)

        keyword_result.delete("1.0", tk.END)
        if keyword_result_text:
            keyword_result.insert(tk.END, f"包含关键词的评论：\n\n{keyword_result_text}")
        else:
            keyword_result.insert(tk.END, "未找到包含关键词的评论")

        # 推测曲风
        if genre_set:
            genre_result.delete("1.0", tk.END)
            genre_result.insert(tk.END, f"推测曲风：{', '.join(genre_set)}")
        else:
            genre_result.delete("1.0", tk.END)
            genre_result.insert(tk.END, "未找到明确的曲风关键词")

    except Exception as e:
        comment_result.delete("1.0", tk.END)
        comment_result.insert(tk.END, f"请求出错：{e}")

# 运行主循环
app.mainloop()
 
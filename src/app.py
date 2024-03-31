# coding=utf-8
#
# Copyright 2024 Toshihiko Aoki
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to ion writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import tkinter as tk
from tkinter import Scrollbar, Text, StringVar, Label
import pyperclip
from translate import Translate


class ClipboardEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Clip Translate")
        self.translator = Translate()
        self.clipboard_content = StringVar()

        self.left_label = Label(root, text="clipboard")
        self.left_label.grid(row=0, column=0, padx=2, pady=2, sticky="w")
        self.right_label = Label(root, text="edit")
        self.right_label.grid(row=0, column=1, padx=2, pady=2, sticky="w")

        # 右グリッド編集
        self.textbox = Text(root, height=10, width=40, font=("Helvetica", 10), wrap=tk.WORD)
        self.textbox.grid(row=1, column=1, padx=2, pady=2, sticky="nsew")

        # 左グリッドラベル
        self.label = Text(root, height=10, width=40, font=("Helvetica", 10), wrap=tk.WORD)
        self.label.config(state="disabled")
        self.label.grid(row=1, column=0, padx=2, pady=2, sticky="nsew")

        # 右グリッド編集
        self.textbox = Text(root, height=10, width=40, font=("Helvetica", 10), wrap=tk.WORD)
        self.textbox.grid(row=1, column=1, padx=2, pady=2, sticky="nsew")

        scrollbar = Scrollbar(root, command=self.textbox.yview)
        scrollbar.grid(row=1, column=2, sticky='ns')
        self.textbox.config(yscrollcommand=scrollbar.set)

        root.columnconfigure(1, weight=1)
        root.rowconfigure(0, weight=1)

        # ボタン
        self.copy_button = tk.Button(root, text="sync（edit lost）", command=self.refresh_clipboard_content)
        self.copy_button.grid(row=2, column=0, padx=2, pady=2)
        self.copy_button = tk.Button(root, text="update", command=self.copy_to_clipboard)
        self.copy_button.grid(row=2, column=1, padx=2, pady=2)

        # 初期表示
        self.refresh_clipboard_content()

    def refresh_clipboard_content(self):
        current_content = pyperclip.paste()
        self.clipboard_content.set(current_content)
        self.label.config(state="normal")
        self.label.delete(1.0, tk.END)
        self.label.insert(tk.END, current_content)
        self.label.config(state="disable")
        self.textbox.delete(1.0, tk.END)
        self.textbox.insert(tk.END, self.translator.translate(current_content))

    def copy_to_clipboard(self):
        new_content = self.textbox.get(1.0, tk.END)
        pyperclip.copy(new_content.strip())
        self.refresh_clipboard_content()


if __name__ == "__main__":
    root = tk.Tk()
    app = ClipboardEditor(root)
    root.mainloop()

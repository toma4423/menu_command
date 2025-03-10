#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
sudoコマンド実行GUIランチャー

このスクリプトは、LinuxのsudoコマンドをGUIから実行するためのランチャーです。
ユーザーは、GUI上のボタンをクリックすることで、登録されたsudoコマンドをルート権限で別ターミナルで実行できます。
ボタンの追加、削除、編集は設定画面から行い、設定はJSONファイルに保存されます。

仕様:
- ボタンをクリックすると、対応するsudoコマンドを別ターミナルで実行します
- 設定画面からボタンの追加、削除、編集が可能です
- 設定はJSONファイル (config.json) に保存されます
- エラー発生時はダイアログでメッセージを表示します

制限事項:
- sudoパスワードの入力が必要な場合があります
- 設定ファイルに安全でないコマンドを登録しないよう注意が必要です
"""

import json
import os
import subprocess
import sys
import traceback
import time
import threading
import tkinter as tk
from tkinter import messagebox, simpledialog, Listbox, scrolledtext


class CommandLauncher:
    """
    コマンド実行ランチャーのメインクラス
    
    ボタン表示、コマンド実行、設定管理などの機能を提供します。
    """
    
    def __init__(self, root, config_file="config.json"):
        """
        CommandLauncherクラスの初期化
        
        Args:
            root (tk.Tk): Tkinterのルートウィンドウ
            config_file (str): 設定ファイルのパス（デフォルト: config.json）
        """
        self.root = root
        self.config_file = config_file
        self.buttons = []
        self.button_frames = []
        
        # ルートウィンドウの設定
        self.root.title("sudoコマンド実行ランチャー")
        self.root.geometry("400x500")
        self.root.minsize(400, 300)
        
        # メインフレーム（スクロール可能）
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # キャンバスとスクロールバーの作成
        self.canvas = tk.Canvas(self.main_frame)
        self.scrollbar = tk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # スクロールバーとキャンバスのパッキング
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # キャンバス内にボタンを配置するフレーム
        self.button_container = tk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.button_container, anchor=tk.NW, width=self.canvas.winfo_width())
        
        # キャンバスサイズ変更時の処理
        self.canvas.bind('<Configure>', self.on_canvas_configure)
        self.button_container.bind('<Configure>', self.on_frame_configure)
        
        # 下部フレーム（設定ボタンと閉じるボタン）
        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # 設定ボタン
        self.settings_button = tk.Button(
            self.bottom_frame,
            text="設定",
            command=self.open_settings,
            height=2,
            width=15
        )
        self.settings_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # 閉じるボタン
        self.close_button = tk.Button(
            self.bottom_frame,
            text="閉じる",
            command=self.root.destroy,
            height=2,
            width=15
        )
        self.close_button.pack(side=tk.RIGHT)
        
        # 設定を読み込み、ボタンを生成
        self.load_config_and_create_buttons()
    
    def on_canvas_configure(self, event):
        """
        キャンバスのサイズが変更されたときに呼び出されるイベントハンドラ
        
        Args:
            event: イベントオブジェクト
        """
        # キャンバス内のウィンドウの幅を調整
        self.canvas.itemconfig(self.canvas_window, width=event.width)
    
    def on_frame_configure(self, event):
        """
        ボタンコンテナのサイズが変更されたときに呼び出されるイベントハンドラ
        
        Args:
            event: イベントオブジェクト
        """
        # キャンバスのスクロール領域を調整
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def load_config_and_create_buttons(self):
        """
        設定ファイルからコマンド情報を読み込み、ボタンを生成します。
        
        エラー発生時は、エラーメッセージをダイアログで表示します。
        """
        try:
            # 既存のボタンフレームをクリア
            for frame in self.button_frames:
                frame.destroy()
            self.button_frames = []
            self.buttons = []
            
            # 設定ファイルの読み込み
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            # ボタンの生成
            if "buttons" in config_data:
                for item in config_data["buttons"]:
                    self.create_button_with_controls(item["label"], item["command"])
                
        except FileNotFoundError:
            result = messagebox.askquestion(
                "エラー", 
                f"設定ファイル '{self.config_file}' が見つかりません。\n"
                "新しい設定ファイルを作成しますか？"
            )
            
            if result == "yes":
                # 空の設定を保存
                self.save_config({"buttons": []})
            else:
                # アプリケーションを終了
                self.root.destroy()
            
        except json.JSONDecodeError:
            result = messagebox.askquestion(
                "エラー", 
                f"設定ファイル '{self.config_file}' の形式が正しくありません。\n"
                "設定をリセットしますか？"
            )
            
            if result == "yes":
                # 空の設定を保存
                self.save_config({"buttons": []})
            else:
                # アプリケーションを終了
                self.root.destroy()
            
        except Exception as e:
            messagebox.showerror(
                "エラー", 
                f"設定ファイルの読み込み中にエラーが発生しました。\n"
                f"エラー: {str(e)}\n"
                f"詳細: {traceback.format_exc()}"
            )
    
    def create_button_with_controls(self, label, command):
        """
        ボタンと操作コントロール（編集・削除ボタン）を含むフレームを作成します。
        
        Args:
            label (str): ボタンに表示するラベル
            command (str): 実行するコマンド
        """
        # ボタンを配置するフレーム
        button_frame = tk.Frame(self.button_container)
        button_frame.pack(fill=tk.X, pady=3)
        self.button_frames.append(button_frame)
        
        # メインボタン（コマンド実行用）
        main_button = tk.Button(
            button_frame,
            text=label,
            command=lambda cmd=command: self.execute_command(cmd),
            height=2,
            width=30
        )
        main_button.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self.buttons.append(main_button)
        
        # 編集ボタン
        edit_button = tk.Button(
            button_frame,
            text="編集",
            command=lambda lbl=label, cmd=command: self.edit_button(lbl, cmd),
            height=2
        )
        edit_button.pack(side=tk.LEFT, padx=2)
        
        # 削除ボタン
        delete_button = tk.Button(
            button_frame,
            text="削除",
            command=lambda lbl=label: self.delete_button(lbl),
            height=2
        )
        delete_button.pack(side=tk.LEFT)
    
    def execute_command(self, command):
        """
        指定されたコマンドをOSのターミナルで実行します。
        コマンドは常にスクリプトと同じディレクトリで実行されます。
        
        Args:
            command (str): 実行するコマンド
        
        エラー発生時は、エラーメッセージをダイアログで表示します。
        """
        try:
            # スクリプトのディレクトリを取得
            script_dir = os.path.dirname(os.path.abspath(__file__))
            
            # sudo を先頭に付ける（ただし、既にsudoで始まる場合は付けない）
            if not command.strip().startswith("sudo "):
                full_command = f"sudo {command}"
            else:
                full_command = command
            
            # 現在のディレクトリをスクリプトのディレクトリに変更する一時的なスクリプトを作成
            temp_script_path = os.path.join(script_dir, "temp_command.sh")
            with open(temp_script_path, 'w') as f:
                f.write('#!/bin/bash\n')
                f.write(f'cd "{script_dir}"\n')  # スクリプトのディレクトリに移動
                f.write(f'{full_command}\n')     # コマンドを実行
                f.write('echo ""\n')             # 空行を出力
                f.write('echo "コマンドが完了しました。Enterキーを押すと閉じます..."\n')
                f.write('read\n')                # キー入力を待つ
            
            # 一時スクリプトに実行権限を付与
            os.chmod(temp_script_path, 0o755)
            
            # ターミナルエミュレータを決定（環境に応じて適切なものを選択）
            terminal_emulators = ['x-terminal-emulator', 'lxterminal', 'gnome-terminal', 'xterm']
            terminal_cmd = None
            
            for emulator in terminal_emulators:
                if subprocess.call(['which', emulator], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
                    terminal_cmd = emulator
                    break
            
            if terminal_cmd is None:
                raise Exception("ターミナルエミュレータが見つかりませんでした")
            
            # ターミナルを起動してコマンドを実行
            if terminal_cmd == 'gnome-terminal':
                subprocess.Popen([terminal_cmd, '--', '/bin/bash', temp_script_path])
            elif terminal_cmd in ['lxterminal', 'x-terminal-emulator']:
                subprocess.Popen([terminal_cmd, '-e', f'/bin/bash {temp_script_path}'])
            else:  # xterm など
                subprocess.Popen([terminal_cmd, '-e', f'/bin/bash {temp_script_path}'])
            
            # 少し待ってから一時スクリプトを削除（非同期実行のため）
            def delete_temp_script():
                time.sleep(2)  # 2秒待つ
                try:
                    if os.path.exists(temp_script_path):
                        os.remove(temp_script_path)
                except:
                    pass
            
            # 別スレッドで一時ファイル削除を実行
            threading.Thread(target=delete_temp_script, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror(
                "実行エラー", 
                f"コマンド '{command}' の実行準備中にエラーが発生しました。\n"
                f"エラー: {str(e)}\n"
                f"詳細: {traceback.format_exc()}"
            )
    
    def open_settings(self):
        """
        設定画面を開きます。
        
        設定画面では、ボタンの追加が可能です。
        （編集と削除は各ボタンの横のコントロールから行います）
        """
        # 設定ウィンドウの作成
        settings_window = tk.Toplevel(self.root)
        settings_window.title("設定")
        settings_window.geometry("400x200")
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # 設定データを読み込む
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            if "buttons" not in config_data:
                config_data["buttons"] = []
        except (FileNotFoundError, json.JSONDecodeError):
            config_data = {"buttons": []}
        
        # 追加ボタンフレーム
        add_frame = tk.Frame(settings_window)
        add_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 追加ボタン
        add_button = tk.Button(
            add_frame, 
            text="新しいボタンを追加", 
            command=lambda: self.add_button(settings_window, config_data),
            height=2,
            width=20
        )
        add_button.pack(fill=tk.X)
        
        # 設定の説明ラベル
        tk.Label(
            settings_window, 
            text="※ ボタンの編集と削除は、メイン画面の各ボタンの横にあるコントロールから行えます。",
            wraplength=380,
            justify=tk.LEFT
        ).pack(padx=10, pady=10, fill=tk.X)
        
        # 閉じるボタン
        close_button = tk.Button(
            settings_window, 
            text="閉じる", 
            command=settings_window.destroy,
            height=2
        )
        close_button.pack(fill=tk.X, padx=10, pady=10)
    
    def add_button(self, parent_window, config_data):
        """
        新しいボタンを追加します。
        
        Args:
            parent_window (tk.Toplevel): 親ウィンドウ
            config_data (dict): 設定データ
        """
        # 新しいウィンドウを作成
        add_window = tk.Toplevel(parent_window)
        add_window.title("ボタン追加")
        add_window.geometry("400x200")
        add_window.transient(parent_window)
        add_window.grab_set()
        
        # ラベルとエントリーのフレーム
        input_frame = tk.Frame(add_window)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # ラベル（ボタン名）入力
        tk.Label(input_frame, text="ボタン名:").grid(row=0, column=0, sticky=tk.W, pady=5)
        label_entry = tk.Entry(input_frame, width=30)
        label_entry.grid(row=0, column=1, sticky=tk.W + tk.E, pady=5)
        
        # コマンド入力
        tk.Label(input_frame, text="コマンド:").grid(row=1, column=0, sticky=tk.W, pady=5)
        command_entry = tk.Entry(input_frame, width=30)
        command_entry.grid(row=1, column=1, sticky=tk.W + tk.E, pady=5)
        
        # 説明テキスト
        tk.Label(
            add_window, 
            text="※ コマンドには絶対パスを指定してください。\n例: /usr/bin/apt update",
            justify=tk.LEFT
        ).pack(padx=10, pady=5, anchor=tk.W)
        
        # ボタンフレーム
        button_frame = tk.Frame(add_window)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 追加ボタン
        def confirm_add():
            label = label_entry.get().strip()
            command = command_entry.get().strip()
            
            if not label:
                messagebox.showerror("エラー", "ボタン名を入力してください。")
                return
            
            if not command:
                messagebox.showerror("エラー", "コマンドを入力してください。")
                return
            
            # ボタンを追加
            config_data["buttons"].append({"label": label, "command": command})
            
            # 設定を保存
            self.save_config(config_data)
            
            # ボタンを再生成
            self.load_config_and_create_buttons()
            
            # 追加ウィンドウを閉じる
            add_window.destroy()
        
        add_button = tk.Button(
            button_frame,
            text="追加",
            command=confirm_add,
            width=10,
            height=2
        )
        add_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # キャンセルボタン
        cancel_button = tk.Button(
            button_frame,
            text="キャンセル",
            command=add_window.destroy,
            width=10,
            height=2
        )
        cancel_button.pack(side=tk.LEFT)
    
    def edit_button(self, current_label, current_command):
        """
        既存のボタンを編集します。
        
        Args:
            current_label (str): 現在のボタン名
            current_command (str): 現在のコマンド
        """
        # 設定データを読み込む
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            if "buttons" not in config_data:
                config_data["buttons"] = []
        except (FileNotFoundError, json.JSONDecodeError):
            config_data = {"buttons": []}
        
        # 編集対象のボタンのインデックスを検索
        target_index = None
        for i, button in enumerate(config_data["buttons"]):
            if button["label"] == current_label and button["command"] == current_command:
                target_index = i
                break
        
        if target_index is None:
            messagebox.showerror("エラー", "編集対象のボタンが見つかりませんでした。")
            return
        
        # 編集ウィンドウを作成
        edit_window = tk.Toplevel(self.root)
        edit_window.title("ボタン編集")
        edit_window.geometry("400x200")
        edit_window.transient(self.root)
        edit_window.grab_set()
        
        # ラベルとエントリーのフレーム
        input_frame = tk.Frame(edit_window)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # ラベル（ボタン名）入力
        tk.Label(input_frame, text="ボタン名:").grid(row=0, column=0, sticky=tk.W, pady=5)
        label_entry = tk.Entry(input_frame, width=30)
        label_entry.insert(0, current_label)
        label_entry.grid(row=0, column=1, sticky=tk.W + tk.E, pady=5)
        
        # コマンド入力
        tk.Label(input_frame, text="コマンド:").grid(row=1, column=0, sticky=tk.W, pady=5)
        command_entry = tk.Entry(input_frame, width=30)
        command_entry.insert(0, current_command)
        command_entry.grid(row=1, column=1, sticky=tk.W + tk.E, pady=5)
        
        # 説明テキスト
        tk.Label(
            edit_window, 
            text="※ コマンドには絶対パスを指定してください。\n例: /usr/bin/apt update",
            justify=tk.LEFT
        ).pack(padx=10, pady=5, anchor=tk.W)
        
        # ボタンフレーム
        button_frame = tk.Frame(edit_window)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 保存ボタン
        def confirm_edit():
            label = label_entry.get().strip()
            command = command_entry.get().strip()
            
            if not label:
                messagebox.showerror("エラー", "ボタン名を入力してください。")
                return
            
            if not command:
                messagebox.showerror("エラー", "コマンドを入力してください。")
                return
            
            # ボタンを更新
            config_data["buttons"][target_index] = {"label": label, "command": command}
            
            # 設定を保存
            self.save_config(config_data)
            
            # ボタンを再生成
            self.load_config_and_create_buttons()
            
            # 編集ウィンドウを閉じる
            edit_window.destroy()
        
        save_button = tk.Button(
            button_frame,
            text="保存",
            command=confirm_edit,
            width=10,
            height=2
        )
        save_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # キャンセルボタン
        cancel_button = tk.Button(
            button_frame,
            text="キャンセル",
            command=edit_window.destroy,
            width=10,
            height=2
        )
        cancel_button.pack(side=tk.LEFT)
    
    def delete_button(self, label):
        """
        ボタンを削除します。
        
        Args:
            label (str): 削除するボタンのラベル
        """
        # 確認ダイアログ
        if not messagebox.askyesno("確認", f"'{label}' を削除してもよろしいですか？"):
            return
        
        # 設定データを読み込む
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            if "buttons" not in config_data:
                config_data["buttons"] = []
        except (FileNotFoundError, json.JSONDecodeError):
            config_data = {"buttons": []}
        
        # 削除対象のボタンを検索
        for i, button in enumerate(config_data["buttons"]):
            if button["label"] == label:
                # ボタンを削除
                del config_data["buttons"][i]
                break
        
        # 設定を保存
        self.save_config(config_data)
        
        # ボタンを再生成
        self.load_config_and_create_buttons()
    
    def save_config(self, config_data):
        """
        設定データをファイルに保存します。
        
        Args:
            config_data (dict): 設定データ
        """
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror(
                "保存エラー", 
                f"設定の保存中にエラーが発生しました。\n"
                f"エラー: {str(e)}\n"
                f"詳細: {traceback.format_exc()}"
            )


def main():
    """
    メイン関数
    
    アプリケーションのエントリーポイントです。
    """
    # Tkルートウィンドウを作成
    root = tk.Tk()
    
    # CommandLauncherインスタンスを作成
    app = CommandLauncher(root)
    
    # アプリケーションを実行
    root.mainloop()


if __name__ == "__main__":
    main() 
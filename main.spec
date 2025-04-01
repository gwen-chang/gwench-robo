# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

block_cipher = None

# --- データファイルの指定 ---
# アプリケーションの実行に必要なデータファイルやフォルダを指定します。
# 各タプルは (ソースパス, 宛先パス) の形式です。
# ソースパス: プロジェクト内のファイルまたはフォルダのパス。
# 宛先パス: バンドルされたアプリケーション内の配置場所。
# バンドルのルートに配置する場合は、宛先パスに '.' を使用します。
datas = [
    ('config.ini.sample', '.'),  # config.ini.sample をルートに配置
    ('persona.ini', '.'),  # persona.ini をルートに配置 (存在する場合)
    # 他に必要なデータファイルがあればここに追加
]

# --- 隠れたインポートの指定 ---
# PyInstaller が自動検出できない、動的にインポートされるモジュールを指定します。
hiddenimports = [
    # 必要なモジュールをここに追加します。例:
    # 'your_hidden_module',
    'websockets',
    'google.generativeai',
    'requests',
    'configparser',
    'json',
    'time',
    'logging',
    'threading',
    'queue',
    'sys',
    'os',
    're',
    'subprocess',
    'socket', # config.ini.sampleから必要と判断
    'urllib.parse', # config.ini.sampleから必要と判断
]

# --- 解析 ---
# スクリプトを解析し、依存関係を特定します。
a = Analysis(
    ['main.py'],  # メインスクリプトの名前に置き換えてください (今回は main.py のままでOK)
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# --- PYZ ---
# Python コードの圧縮アーカイブを作成します。
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# --- EXE ---
# 実行ファイルを作成します。
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='gwench-robo',  # 実行ファイルの名前をここに指定 (日本語非対応のため gwench-robo)
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # コンソールウィンドウを表示する場合は True、非表示にする場合は False
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

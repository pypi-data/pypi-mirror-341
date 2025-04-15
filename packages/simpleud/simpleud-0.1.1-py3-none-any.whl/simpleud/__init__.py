"""
SimpleUD - シンプルなファイルアップロード・ダウンロードライブラリ

サーバーとの間でファイルをアップロード・ダウンロードするための
シンプルで使いやすいPythonライブラリです。
同期処理と非同期処理の両方をサポートしています。
"""

from .uploader import FileUploaderDownloader

__version__ = '0.1.0'
__all__ = ['FileUploaderDownloader']
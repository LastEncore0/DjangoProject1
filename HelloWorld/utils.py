import json

from django.shortcuts import redirect
from django.utils.translation import get_language, activate


def get_current_language():
    """ 現在の言語を取得し、存在しない場合はデフォルト (ja) に設定する """
    lang = get_language()
    if lang not in ["ja", "en", "zh-hans"]:  # 定義済みの言語リスト
        lang = "ja"  # デフォルトは日本語
    return lang

def set_language(request):
    lang = request.GET.get("lang", "ja")
    if lang not in ["ja", "en", "zh-hans"]:
        lang = "ja"

    activate(lang)  # 新しい言語に切り替わる
    print("Language:", lang)
    response = redirect(request.META.get("HTTP_REFERER", "/"))
    response.set_cookie("django_language", lang)  # cookieで言語を記録
    print("Cookie:", response.cookies)
    return response

# 翻訳Jsonを読み取る
with open("translations.json", encoding="utf-8") as f:
    translations = json.load(f)

def get_translated_text(lang, key):
    """  翻訳をゲットしてなければ日本語に """
    return translations.get(lang, {}).get(key, translations["ja"].get(key, key))

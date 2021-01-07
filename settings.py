import os
from os.path import join, dirname
from dotenv import load_dotenv
import slackweb

SLACK_COCO = os.environ.get("SLACK_COCO")
SLACK_LANCERS = os.environ.get("SLACK_LANCERS")
SLACK_CLOWDWORKS = os.environ.get("SLACK_CLOWDWORKS")

LINE_TOKEN = os.environ.get("LINE_TOKEN")

# Lancers カテゴリー名
CAT_NAME = [
    """カテゴリの種類

    1. Web
    2. IT・プログラミング
    3. デザイン
    """
    'web', 
    'system',
    'design'
]

# coconala カテゴリー名
coco_cat = [
    """カテゴリの種類

    1. Webサイト制作・Webデザイン
    2. IT・プログラミング
    3. 集客・Webマーケティング
    """
    '22?categoryId=22&recruiting=true&page=1', 
    '11?categoryId=11&recruiting=true&page=1',
    '16?categoryId=16&recruiting=true&page=1'
]


# クラウドワークス カテゴリー名
cloud_cat = [
    """カテゴリの種類

    ホームページ制作・Webデザイン
    デザイン
    サイト運営・ビジネス
    アプリ・スマートフォン開発
    """
    'web_products', 
    'design',
    'business',
    'software_development'
]
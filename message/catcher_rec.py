import requests
import io
from linebot.models import TemplateSendMessage, ConfirmTemplate, MessageAction, BubbleContainer, ImageComponent, \
    URIAction, BoxComponent, TextComponent, SeparatorComponent, ButtonComponent
from . import default
import const.tag

KEY = default.KEY_CATCHER_REC
START = 'ロールモデル マッチングを開始します！\n' \
        '「終了」と入力してセッション自体を終了します！'
CONFIRM = TemplateSendMessage(
    template=ConfirmTemplate(
        actions=[
            MessageAction(label='Yes', text='Yes'),
            MessageAction(label='No', text='No'),
        ]))
COMMON_TAG = 'キャッチャーとの共通の項目'
CONFIRM_TEXT = 'この方はどうでしょうか？'
SORRY = 'ごめんなさい！マッチする人が現状はいません。\n' \
        '運営に連絡くだされば、なんとか探します！'
END = 'よかったです！実際に取材したい場合は運営へお問い合わせください！'

BASE_URL = 'https://teenmakers.jp/wp-json/wp/v2/'


def get_catcher(uid):
    msg = PROFILE
    res = requests.get(BASE_URL + 'posts/' + str(uid), timeout=5)
    if res.status_code != requests.codes.ok:
        return None
    j = res.json()
    img_url = j['_links']['wp:featuredmedia'][0]['href']
    name = j['title']['rendered']
    url = "https://teenmakers.jp/archives/" + str(uid)
    work = j['acf']['work']
    job = j['acf']['job']
    res = requests.get(img_url, timeout=5)
    if res.status_code != requests.codes.ok:
        return None
    j = res.json()
    img = j['guid']['rendered']
    img = 'https' + img[4:]
    msg.hero.url = img
    msg.hero.action.uri = url

    msg.body.contents[0].text = name + ' さん'

    msg.body.contents[1].contents[0].contents[1].text = work
    msg.body.contents[1].contents[1].contents[1].text = job

    msg.footer.contents[1].action.uri = url

    return msg


def get_common_tags_msg(common_tags):
    msg = io.StringIO()
    msg.write(COMMON_TAG)
    for tag in common_tags:
        msg.write('\n・' + const.tag.tags[tag])
    return msg.getvalue()


PROFILE = BubbleContainer(
    direction='ltr',
    hero=ImageComponent(
        url='https://example.com/cafe.jpg',
        size='full',
        aspect_ratio='20:13',
        aspect_mode='cover',
        action=URIAction(uri='https://example.com', label='label')
    ),
    body=BoxComponent(
        layout='vertical',
        contents=[
            # title
            TextComponent(text='Brown Cafe', weight='bold', size='xl'),
            # info
            BoxComponent(
                layout='vertical',
                margin='lg',
                spacing='sm',
                contents=[
                    BoxComponent(
                        layout='baseline',
                        spacing='sm',
                        contents=[
                            TextComponent(
                                text='Work',
                                color='#aaaaaa',
                                size='sm',
                                flex=1
                            ),
                            TextComponent(
                                text='Shinjuku, Tokyo',
                                wrap=True,
                                color='#666666',
                                size='sm',
                                flex=5
                            )
                        ],
                    ),
                    BoxComponent(
                        layout='baseline',
                        spacing='sm',
                        contents=[
                            TextComponent(
                                text='Job',
                                color='#aaaaaa',
                                size='sm',
                                flex=1
                            ),
                            TextComponent(
                                text="10:00 - 23:00",
                                wrap=True,
                                color='#666666',
                                size='sm',
                                flex=5,
                            ),
                        ],
                    ),
                ],
            )
        ],
    ),
    footer=BoxComponent(
        layout='vertical',
        spacing='sm',
        contents=[
            # separator
            SeparatorComponent(),
            # websiteAction
            ButtonComponent(
                style='link',
                height='sm',
                action=URIAction(label='経歴をチェックする', uri="https://example.com")
            )
        ]
    ),
)

import requests
from linebot.models import MessageAction, ButtonsTemplate, TemplateSendMessage, ConfirmTemplate, BubbleContainer, \
    URIAction, ImageComponent, BoxComponent, TextComponent, ButtonComponent, SeparatorComponent

import models.status as st

# default commands
KEY_END = '終了'
MSG_END = 'ありがとうございました！またのご利用をお待ちしております！'
KEY_SKIP = 'スキップ'
MSG_SKIP = 'スキップします！'

KEY_CONTACT = 'お問い合わせ'
MSG_CONTACT_DEFAULT = 'お問い合わせありがとうございます。\n' \
                      '運営が対応致しますので、続けてお問い合わせ内容をご入力ください！\n' \
                      '「終了」と入力してお問い合わせが終わります！'

# Self Reflection
KEY_SELF_REFLECTION = '自己分析'
MSG_SELF_REFLECTION = '今後対応致します。少々お待ちください！'

# BN Creation
KEY_BN_CREATE = '記事作成'
MSG_BN_CREATE = '記事の作成を開始します！\n' \
                '「次」と入力して次の質問に行けます！\n' \
                '「終了」と入力してセッション自体を終了します！'
MSG_BN_CREATE_1 = '取材の中で印象に残っていることを書き出してみてください！ (5分)\n\n' \
                  '***\n驚いた、共感できた、発見があった、疑問に思ったなどの印象に残っている事を思いつくままに書き出してみましょう\n***\n\n' \
                  '終わり次第「次」と入力して次の質問に行けます！'
MSG_BN_CREATE_2 = 'いくつかを更に掘り下げてみましょう！その中から、特に自分にとって大事だと思うものを3つ選んでみてください！' \
                  '終わり次第「次」と入力して次の質問に行けます！'
MSG_BN_CREATE_3_1 = '意外だった'
MSG_BN_CREATE_3_2 = '初めて知ったことだった'
MSG_BN_CREATE_3_3 = '知っていたが、新たな発見があった'
MSG_BN_CREATE_3_4 = '疑問を感じた'
MSG_BN_CREATE_3_5 = '自分とは異なる考え方・価値観だった'
MSG_BN_CREATE_3 = TemplateSendMessage(
    alt_text='印象に残っている理由はなんですか？', template=ButtonsTemplate(
        title='印象に残っている理由はなんですか？', text='...', actions=[
            MessageAction(label=MSG_BN_CREATE_3_1, text=MSG_BN_CREATE_3_1),
            MessageAction(label=MSG_BN_CREATE_3_2, text=MSG_BN_CREATE_3_2),
            MessageAction(label=MSG_BN_CREATE_3_3, text=MSG_BN_CREATE_3_3),
            # MessageAction(label=MSG_BN_CREATE_3_4, text=MSG_BN_CREATE_3_4),
            MessageAction(label=MSG_BN_CREATE_3_5, text=MSG_BN_CREATE_3_5)
        ]))

MSG_BN_CREATE_T1_1 = '具体的に書いてみてください\n' \
                     '（どう意外だったのか、意外だと感じたのはなぜか、など）'
MSG_BN_CREATE_T1_2 = '印象に残っている部分を思い返し、深掘りしてみて、どんな気づき、学びがありましたか？'
MSG_BN_CREATE_T1_3 = 'そんな気づきや学びを踏まえて、どのように今後に活かそう（実際に行動にうつそう）と思いますか？（どんな小さいことでも構いません！）'

MSG_BN_CREATE_T2_1 = '初めて知って、どのように思いましたか？'
MSG_BN_CREATE_T2_2 = 'その話の中で、あなたにとって大切だと感じたこと、気づき、学びがありましたか？'
MSG_BN_CREATE_T2_3 = 'そんな大切だと感じたことや気づきや学びを踏まえて、どのように今後に活かそう（実際に行動にうつそう）と思いますか？（どんな小さいことでも構いません！）'

MSG_BN_CREATE_T3_1 = 'どのような発見、気づき、学びでしたか？具体的に書いてみてください'
MSG_BN_CREATE_T3_2 = 'そんな気づきや学びを踏まえて、どのように今後に活かそう（実際に行動にうつそう）と思いますか？（どんな小さいことでも構いません！）'

MSG_BN_CREATE_T5_1 = '自分の考え方とどのように違いましたか？'
MSG_BN_CREATE_T5_2 = '違う考え方・価値観と出会い、考え方に変化はありましたか？'

# Message-branch dictionary
bn_dict_1 = {1: MSG_BN_CREATE_T1_1, 2: MSG_BN_CREATE_T1_2, 3: MSG_BN_CREATE_T1_3, 4: MSG_END}
bn_dict_2 = {1: MSG_BN_CREATE_T2_1, 2: MSG_BN_CREATE_T2_2, 3: MSG_BN_CREATE_T2_3, 4: MSG_END}
bn_dict_3 = {1: MSG_BN_CREATE_T3_1, 2: MSG_BN_CREATE_T3_2, 3: MSG_END}
bn_dict_4 = {1: MSG_BN_CREATE_T5_1, 2: MSG_BN_CREATE_T5_2, 3: MSG_END}

type_dict = {st.Type.BN_CREATE_TRACK1: bn_dict_1,
             st.Type.BN_CREATE_TRACK2: bn_dict_2,
             st.Type.BN_CREATE_TRACK3: bn_dict_3,
             st.Type.BN_CREATE_TRACK5: bn_dict_4}

# Catcher
KEY_CATCHER = 'ロールモデル'
MSG_CATCHER = 'ロールモデル マッチングを開始します！\n' \
              '「終了」と入力してセッション自体を終了します！'
MSG_CATCHER_CONFIRM = TemplateSendMessage(
    template=ConfirmTemplate(
        actions=[
            MessageAction(label='Yes', text='Yes'),
            MessageAction(label='No', text='No'),
        ]))
MSG_CATCHER_CONFIRM_TEXT = 'このかたはどうでしょうか？'
MSG_CATCHER_SORRY = 'ごめんなさい！マッチする人が現状はいません。\n' \
                    '運営に連絡くだされば、なんとか探します！'
MSG_CATCHER_END = 'よかったです！実際に取材したい場合は運営へお問い合わせください！'

BASE_URL = 'https://teenmakers.jp/wp-json/wp/v2/'
user_id = 'U728af6e5de3a116a994649e896faa6d7'


def get_catcher(uid):
    msg = CATCHER_FORMAT
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


CATCHER_FORMAT = BubbleContainer(
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

MSG_DEFAULT = TemplateSendMessage(
    alt_text='Buttons alt text', template=ButtonsTemplate(
        title="メッセージありがとうございます！", text="以下の4つのボタンからしたいことを選択してください",
        actions=[
            MessageAction(label='自己分析', text=KEY_SELF_REFLECTION),
            MessageAction(label='記事作成', text=KEY_BN_CREATE),
            MessageAction(label='ロールモデルマッチング', text=KEY_CATCHER),
            MessageAction(label='運営にお問い合わせ', text=KEY_CONTACT),
        ]))



def main():
    get_catcher(515)


if __name__ == '__main__':
    main()

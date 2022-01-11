from linebot.models import TemplateSendMessage, MessageAction, ButtonsTemplate

KEY_END = '終了'
END = 'ありがとうございました！またのご利用をお待ちしております！'
KEY_NEXT = '次'

KEY_SELF_REF = '自己分析'
KEY_BN_CREATE = '記事作成'
KEY_CATCHER_REC = 'ロールモデル'
KEY_CONTACT = 'お問い合わせ'
MENU = TemplateSendMessage(
    alt_text='Buttons alt text', template=ButtonsTemplate(
        title="メッセージありがとうございます！", text="以下の4つのボタンからしたいことを選択してください",
        actions=[
            MessageAction(label='自己分析', text=KEY_SELF_REF),
            MessageAction(label='記事作成', text=KEY_BN_CREATE),
            MessageAction(label='ロールモデルマッチング', text=KEY_CATCHER_REC),
            MessageAction(label='運営にお問い合わせ', text=KEY_CONTACT),
        ]))

ASK_FOR_NEXT = '終わり次第「次」と入力して次の質問に行けます！'

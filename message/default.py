from linebot.models import TemplateSendMessage, MessageAction, ButtonsTemplate
import message as ms

KEY_END = '終了'
END = 'ありがとうございました！またのご利用をお待ちしております！'
KEY_NEXT = '次'
MENU = TemplateSendMessage(
    alt_text='Buttons alt text', template=ButtonsTemplate(
        title="メッセージありがとうございます！", text="以下の4つのボタンからしたいことを選択してください",
        actions=[
            MessageAction(label='自己分析', text=ms.self_ref.KEY),
            MessageAction(label='記事作成', text=ms.bn_create.KEY),
            MessageAction(label='ロールモデルマッチング', text=ms.catcher_rec.KEY),
            MessageAction(label='運営にお問い合わせ', text=ms.contact.KEY),
        ]))

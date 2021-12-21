# default commands
from linebot.models import TextSendMessage, QuickReply, QuickReplyButton, PostbackAction, MessageAction, \
    ButtonsTemplate, TemplateSendMessage

KEY_END = '中断'
MSG_END = 'お疲れさまでした。またのご利用をお待ちしております！'
KEY_SKIP = 'スキップ'
MSG_SKIP = 'スキップします！'

MSG_DEFAULT = TemplateSendMessage(
    alt_text='Buttons alt text', template=ButtonsTemplate(
        title="メッセージありがとうございます！", text="以下の3つのボタンからしたいことを選択してください",
        actions=[
            MessageAction(label='自己分析', text='自己分析'),
            MessageAction(label='記事作成', text='記事作成'),
            MessageAction(label='ロールモデル', text='ロールモデル'),
        ]))

# BN Creation
KEY_BN_CREATE = '作成'
MSG_BN_CREATE = '記事の作成を開始します！\n' \
                '「次」と入力して次の質問に行けます！\n' \
                '「中断」と入力してセッション自体を終了します！'
MSG_BN_CREATE_1 = '取材の中で印象に残っていることを書き出してみてください！ (5分)\n\n' \
                  '***\n驚いた、共感できた、発見があった、疑問に思ったなどの印象に残っている事を思いつくままに書き出してみましょう\n***\n\n' \
                  '終わり次第「次」と入力して次の質問に行けます！\n'
MSG_BN_CREATE_2 = 'いくつかを更に掘り下げてみましょう！その中から、特に自分にとって大事だと思うものを3つ選んでみてください！' \
                  '終わり次第「次」と入力して次の質問に行けます！\n'
MSG_BN_CREATE_3_1 = '意外だった'
MSG_BN_CREATE_3_2 = '初めて知ったことだった'
MSG_BN_CREATE_3_3 = '知っていたが、新たな発見があった'
MSG_BN_CREATE_3_4 = '疑問を感じた'
MSG_BN_CREATE_3_5 = '自分とは異なる考え方・価値観だった'
MSG_BN_CREATE_3 = TemplateSendMessage(
    alt_text='Buttons alt text', template=ButtonsTemplate(
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

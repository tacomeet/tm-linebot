from linebot.models import TemplateSendMessage, ButtonsTemplate, MessageAction
import message as ms
from models.status_type import StatusType

KEY = '記事作成'
START = '記事の作成を開始します！\n' \
        '「次」と入力して次の質問に行けます！\n' \
        '「終了」と入力してセッション自体を終了します！'
M_1 = '取材の中で印象に残っていることを書き出してみてください！ (5分)\n\n' \
     '***\n驚いた、共感できた、発見があった、疑問に思ったなどの印象に残っている事を思いつくままに書き出してみましょう\n***\n\n' \
     '終わり次第「次」と入力して次の質問に行けます！'
M_2 = 'いくつかを更に掘り下げてみましょう！その中から、特に自分にとって大事だと思うものを3つ選んでみてください！' \
     '終わり次第「次」と入力して次の質問に行けます！'
M_3_1 = '意外だった'
M_3_2 = '初めて知ったことだった'
M_3_3 = '知っていたが、新たな発見があった'
M_3_4 = '疑問を感じた'
M_3_5 = '自分とは異なる考え方・価値観だった'
M_3 = TemplateSendMessage(
    alt_text='印象に残っている理由はなんですか？', template=ButtonsTemplate(
        title='印象に残っている理由はなんですか？', text='.', actions=[
            MessageAction(label=M_3_1, text=M_3_1),
            MessageAction(label=M_3_2, text=M_3_2),
            MessageAction(label=M_3_3, text=M_3_3),
            # MessageAction(label=_3_4, text=_3_4),
            MessageAction(label=M_3_5, text=M_3_5)
        ]))

T1_1 = '具体的に書いてみてください\n' \
       '（どう意外だったのか、意外だと感じたのはなぜか、など）'
T1_2 = '印象に残っている部分を思い返し、深掘りしてみて、どんな気づき、学びがありましたか？'
T1_3 = 'そんな気づきや学びを踏まえて、どのように今後に活かそう（実際に行動にうつそう）と思いますか？（どんな小さいことでも構いません！）'

T2_1 = '初めて知って、どのように思いましたか？'
T2_2 = 'その話の中で、あなたにとって大切だと感じたこと、気づき、学びがありましたか？'
T2_3 = 'そんな大切だと感じたことや気づきや学びを踏まえて、どのように今後に活かそう（実際に行動にうつそう）と思いますか？（どんな小さいことでも構いません！）'

T3_1 = 'どのような発見、気づき、学びでしたか？具体的に書いてみてください'
T3_2 = 'そんな気づきや学びを踏まえて、どのように今後に活かそう（実際に行動にうつそう）と思いますか？（どんな小さいことでも構いません！）'

T5_1 = '自分の考え方とどのように違いましたか？'
T5_2 = '違う考え方・価値観と出会い、考え方に変化はありましたか？'

bn_dict_1 = {1: T1_1, 2: T1_2, 3: T1_3, 4: ms.default.END}
bn_dict_2 = {1: T2_1, 2: T2_2, 3: T2_3, 4: ms.default.END}
bn_dict_3 = {1: T3_1, 2: T3_2, 3: ms.default.END}
bn_dict_4 = {1: T5_1, 2: T5_2, 3: ms.default.END}

type_dict = {StatusType.BN_CREATE_TRACK1: bn_dict_1,
             StatusType.BN_CREATE_TRACK2: bn_dict_2,
             StatusType.BN_CREATE_TRACK3: bn_dict_3,
             StatusType.BN_CREATE_TRACK5: bn_dict_4}

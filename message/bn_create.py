from linebot.models import TemplateSendMessage, ButtonsTemplate, MessageAction
from models.status_type import StatusType
from . import default

KEY = default.KEY_BN_CREATE
START = '記事の作成を開始します！\n' \
        '「次」と入力して次の質問に行けます！\n' \
        '「終了」と入力してセッション自体を終了します！'
M_1 = [
    START,
    '取材の中で印象に残っていることを書き出してみてください！\n\n'
    '驚いた、共感できた、発見があった、疑問に思ったなどの印象に残っている事を思いつくままに書き出してみましょう',
    default.ASK_FOR_NEXT
]
M_2 = [
    '進捗：[ ■■□□□□□□□□ ] (20%)',
    'いくつかを更に掘り下げてみましょう！その中から、特に自分にとって大事だと思うものを3つ選んでみてください！',
    default.ASK_FOR_NEXT
]
M_3_1 = '意外だった'
M_3_2 = '初めて知ったことだった'
M_3_3 = '知っていたが、新たな発見があった'
M_3_4 = '疑問を感じた'
M_3_5 = '自分とは異なる考え方・価値観だった'
M_3_BODY = TemplateSendMessage(
    alt_text='印象に残っている理由はなんですか？', template=ButtonsTemplate(
        title='印象に残っている理由はなんですか？', text='.', actions=[
            MessageAction(label=M_3_1, text=M_3_1),
            MessageAction(label=M_3_2, text=M_3_2),
            MessageAction(label=M_3_3, text=M_3_3),
            # MessageAction(label=_3_4, text=_3_4),
            MessageAction(label=M_3_5, text=M_3_5)
        ]))
M_3 = [
    '進捗：[ ■■■■□□□□□□ ] (40%)',
    M_3_BODY
]

T1_1 = [
    '進捗：[ ■■■■■□□□□□ ] (50%)',
    '具体的に書いてみてください\n'
    '（どう意外だったのか、意外だと感じたのはなぜか、など）',
    default.ASK_FOR_NEXT
]
T1_2 = [
    '進捗：[ ■■■■■■■□□□ ] (70%)',
    '印象に残っている部分を思い返し、深掘りしてみて、どんな気づき、学びがありましたか？',
    default.ASK_FOR_NEXT
]
T1_3 = [
    '進捗：[ ■■■■■■■■■□ ] (90%)',
    'そんな気づきや学びを踏まえて、どのように今後に活かそう（実際に行動にうつそう）と思いますか？（どんな小さいことでも構いません！）',
    default.ASK_FOR_NEXT
]
T2_1 = [
    '進捗：[ ■■■■■□□□□□ ] (50%)',
    '初めて知って、どのように思いましたか？',
    default.ASK_FOR_NEXT
]
T2_2 = [
    '進捗：[ ■■■■■■■□□□ ] (70%)',
    'その話の中で、あなたにとって大切だと感じたこと、気づき、学びがありましたか？',
    default.ASK_FOR_NEXT
]
T2_3 = [
    '進捗：[ ■■■■■■■■■□ ] (90%)',
    'そんな大切だと感じたことや気づきや学びを踏まえて、どのように今後に活かそう（実際に行動にうつそう）と思いますか？（どんな小さいことでも構いません！）',
    default.ASK_FOR_NEXT
]

T3_1 = [
    '進捗：[ ■■■■■■□□□□ ] (60%)',
    'どのような発見、気づき、学びでしたか？具体的に書いてみてください',
    default.ASK_FOR_NEXT
]
T3_2 = [
    '進捗: ........🦉..🚩',
    '進捗：[ ■■■■■■■■□□ ] (80%)',
    'そんな気づきや学びを踏まえて、どのように今後に活かそう（実際に行動にうつそう）と思いますか？\n'
    '（どんな小さいことでも構いません！）',
    default.ASK_FOR_NEXT
]

T5_1 = [
    '進捗：[ ■■■■■■□□□□ ] (60%)',
    '自分の考え方とどのように違いましたか？', default.ASK_FOR_NEXT
]
T5_2 = [
    '進捗：[ ■■■■■■■■□□ ] (80%)',
    '違う考え方・価値観と出会い、考え方に変化はありましたか？',
    default.ASK_FOR_NEXT
]

bn_dict_1 = {1: T1_1, 2: T1_2, 3: T1_3, 4: default.END}
bn_dict_2 = {1: T2_1, 2: T2_2, 3: T2_3, 4: default.END}
bn_dict_3 = {1: T3_1, 2: T3_2, 3: default.END}
bn_dict_4 = {1: T5_1, 2: T5_2, 3: default.END}

type_dict = {StatusType.BN_CREATE_TRACK1: bn_dict_1,
             StatusType.BN_CREATE_TRACK2: bn_dict_2,
             StatusType.BN_CREATE_TRACK3: bn_dict_3,
             StatusType.BN_CREATE_TRACK5: bn_dict_4}

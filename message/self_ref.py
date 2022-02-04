from linebot.models import TemplateSendMessage, MessageAction, ButtonsTemplate, ConfirmTemplate
from . import default

KEY = default.KEY_SELF_REF
START = '自己分析を開始します！\n' \
        '「次」または必要項目を入力して次の質問に行けます！\n' \
        '「終了」と入力してセッション自体を終了します！'
TYPE_SELECT = 'どの項目について自己分析を行いますか？'
M_1_EXP = '経験'
M_1_PERS = '個性'
M_1_VIS = 'ビジョン'
M_1_TURN = 'ターニングポイント'
M_1 = [
    START,
    TemplateSendMessage(
        alt_text=TYPE_SELECT, template=ButtonsTemplate(
            title=TYPE_SELECT, text='上から順番に行うことをお勧め致します！', actions=[
                MessageAction(label=M_1_EXP, text=M_1_EXP),
                MessageAction(label=M_1_PERS, text=M_1_PERS),
                MessageAction(label=M_1_VIS, text=M_1_VIS),
                MessageAction(label=M_1_TURN, text=M_1_TURN),
            ]))
]
# Experience
EXP_1_EX = '例：小さい頃アメリカに住んでおり、英語が話せる'
EXP_1 = [
    '進捗：[ ■□□□□□□□□□ ] (10%)',
    '趣味や独学で身につけたことなどを書き出してください',
    EXP_1_EX,
    default.ASK_FOR_NEXT
]
EXP_2_BODY = TemplateSendMessage(
    template=ConfirmTemplate(
        actions=[
            MessageAction(label='Yes', text='Yes'),
            MessageAction(label='No', text='No'),
        ], text='自分の経験を十分に書けましたか？'),
    alt_text='自分の経験を十分に書けましたか？')
EXP_2 = [
    '進捗：[ ■■□□□□□□□□ ] (20%)',
    EXP_2_BODY,
]
EXP_3_YES = [
    '進捗：[ ■■■■□□□□□□ ] (40%)',
    '一番大事にしている経験はどれですか？ その経験に対して以降の質問に答えて頂きます',
    default.ASK_FOR_NEXT
]
EXP_3_NO = [
    '進捗：[ ■■■□□□□□□□ ] (30%)',
    '人より少し得意だと思うことを書き出してください',
    default.ASK_FOR_NEXT
]
EXP_4 = [
    '進捗：[ ■■■■□□□□□□ ] (40%)',
    '一番楽しんでいるものはどれですか？ その経験に対して以降の質問に答えて頂きます',
    default.ASK_FOR_NEXT
]
EXP_5 = [
    '進捗：[ ■■■■■□□□□□ ] (50%)',
    'それのどういうところを楽しんでいますか？',
    default.ASK_FOR_NEXT
]
EXP_6 = [
    '進捗：[ ■■■■■■□□□□ ] (60%)',
    'それを始めたきっかけは何ですか？',
    default.ASK_FOR_NEXT
]
EXP_7 = [
    '進捗：[ ■■■■■■■□□□ ] (70%)',
    'やっている時はどう感じていますか？',
    default.ASK_FOR_NEXT
]

EXP_8 = [
    '進捗：[ ■■■■■■■■□□ ] (80%)',
    'この経験から何か学んだことはありますか？',
    default.ASK_FOR_NEXT
]
EXP_9 = [
    '進捗：[ ■■■■■■■■■□ ] (90%)',
    'これからも続けていきたいですか？その理由は何ですか？',
    default.ASK_FOR_NEXT
]

# Personality
PERS_1_EX = '例：細かいところに気が付く'
PERS_1 = [
    '進捗：[ ■□□□□□□□□□ ] (10%)',
    'あなたの得意なこと（他の人より苦労なくできること）や苦手なことを書き出してください！',
    PERS_1_EX,
    default.ASK_FOR_NEXT
]
PERS_2 = [
    '進捗：[ ■■■□□□□□□□ ] (30%)',
    TemplateSendMessage(
        template=ConfirmTemplate(
            actions=[
                MessageAction(label='Yes', text='Yes'),
                MessageAction(label='No', text='No'),
            ], text='具体的に書けましたか？'),
        alt_text='具体的に書けましたか？')
]

PERS_3_YES = [
    '進捗：[ ■■■■■□□□□□ ] (50%)',
    '一番気にしている短所を選んでください',
    default.ASK_FOR_NEXT
]
PERS_3_NO_EX = '例：リーダシップがある。サークルの代表をやったり、友達を誘えってイベント・勉強会を開いたりした。'
PERS_3_NO = [
    '進捗：[ ■■■■□□□□□□ ] (40%)',
    'それらの個性を（良い意味でも悪い意味でも）発揮したエピソードを書き出してください！',
    PERS_3_NO_EX,
    default.ASK_FOR_NEXT
]
PERS_4 = PERS_3_YES
PERS_5 = [
    '進捗：[ ■■■■■■■□□□ ] (70%)',
    'その短所にも、メリットがあるとしたら、どんなところだと思いますか？',
    default.ASK_FOR_NEXT
]
PERS_6 = [
    '進捗：[ ■■■■■■■■□□ ] (80%)',
    TemplateSendMessage(
        template=ConfirmTemplate(
            actions=[
                MessageAction(label='Yes', text='Yes'),
                MessageAction(label='No', text='No'),
            ], text='その短所を直したいと思いますか？'),
        alt_text='その短所を直したいと思いますか？')
]

PERS_7_YES = [
    '進捗：[ ■■■■■■■■■□ ] (90%)',
    'その短所を直すために、何ができると思いますか？',
    default.ASK_FOR_NEXT
]
PERS_7_NO = [
    '進捗：[ ■■■■■■■■■□ ] (90%)',
    'その状態を乗り越える方法は何かありますか？',
    default.ASK_FOR_NEXT
]

# Vision
VIS_1_EX_1 = '例：自分の経験してきた音楽とプログラミングを組み合わせた分野で貢献したい'
VIS_1_EX_2 = '例：誠実な自分でありたい'
VIS_1 = [
    '進捗：[ ■□□□□□□□□□ ] (10%)',
    '今までの⾃分の⼈⽣で起こった事象から感じたことやこれからも⼤切にしたい考えなどを書き出してください',
    VIS_1_EX_1,
    VIS_1_EX_2,
    default.ASK_FOR_NEXT
]
VIS_2 = [
    '進捗：[ ■■□□□□□□□□ ] (20%)',
    TemplateSendMessage(
        template=ConfirmTemplate(
            actions=[
                MessageAction(label='Yes', text='Yes'),
                MessageAction(label='No', text='No'),
            ], text='ビジョンは書けそうですか？'),
        alt_text='ビジョンは書けそうですか？')
]

VIS_3_YES = [
    '進捗：[ ■■■■■■■□□□ ] (75%)',
    '⾃分の「経験」や「個性」からどのように過ごしたら・何をしていたら幸せに感じるか、自分のビジョンを書き出してください！',
    default.ASK_FOR_NEXT
]
VIS_3_NO = [
    '進捗：[ ■■■□□□□□□□ ] (30%)',
    '今まで経験してきたことはどんな側面を楽しんでいましたか？',
    default.ASK_FOR_NEXT
]
VIS_4 = [
    '進捗：[ ■■■■□□□□□□ ] (40%)',
    'あなたにとって幸せな状態とはどんな状態ですか？',
    default.ASK_FOR_NEXT
]
VIS_5 = [
    '進捗：[ ■■■■■□□□□□ ] (50%)',
    '逆にどうしてもやりたくないことや許容し難い価値観はありますか？',
    default.ASK_FOR_NEXT
]
VIS_6 = [
    '進捗：[ ■■■■■■□□□□ ] (60%)',
    '収入が安定して、時間があるとしたら何をして過ごしたいですか？',
    default.ASK_FOR_NEXT
]
VIS_7 = [
    '進捗：[ ■■■■■■■□□□ ] (70%)',
    '5年後にどんな自分でいられたら嬉しいですか？',
    default.ASK_FOR_NEXT
]
VIS_8 = VIS_3_YES
VIS_9 = [
    '進捗：[ ■■■■■■■■□□ ] (80%)',
    TemplateSendMessage(
        template=ConfirmTemplate(
            actions=[
                MessageAction(label='Yes', text='Yes'),
                MessageAction(label='No', text='No'),
            ], text='具体的に書けましたか？'),
        alt_text='具体的に書けましたか？')
]
VIS_10_YES = [
    '進捗：[ ■■■■■■■■■□ ] (90%)',
    'ビジョンと価値観を合わせて1〜3つのスローガンを作成しましょう！',
    default.ASK_FOR_NEXT
]
VIS_10_NO = [
    '進捗：[ ■■■■■■■■□□ ] (85%)',
    'そのビジョンや価値観が表されたエピソードを書き出してください',
    default.ASK_FOR_NEXT
]
VIS_11 = VIS_10_YES

TURN_1_1 = 'ターニングポイントとは、「⼈⽣における重⼤な転換期など」のことです。挫折体験とは、「過去に起こった出来事で思い通りに⾏かずに⼼砕かれた経験など」のことです。'
TURN_1_2 = 'それらだと思うものについてその時に何が起きたのかを書き出してください。'
TURN_1 = [
    '進捗：[ ■□□□□□□□□□ ] (10%)',
    TURN_1_1,
    TURN_1_2,
    default.ASK_FOR_NEXT
]
TURN_2 = [
    '進捗：[ ■■■□□□□□□□ ] (30%)',
    'その時どう感じましたか？',
    default.ASK_FOR_NEXT
]
TURN_3 = [
    '進捗：[ ■■■■□□□□□□ ] (45%)',
    'そこからどのように行動しましたか？',
    default.ASK_FOR_NEXT
]
TURN_4 = [
    '進捗：[ ■■■■■■□□□□ ] (60%)',
    'どのように考え方は変わりましたか？',
    default.ASK_FOR_NEXT
]
TURN_5 = [
    '進捗：[ ■■■■■■■□□□ ] (75%)',
    'その体験はどのように個性やビジョンに関わっていますか？',
    default.ASK_FOR_NEXT
]
TURN_6 = [
    '進捗：[ ■■■■■■■■■□ ] (90%)',
    'どのように考え方は変わりましたか？',
    default.ASK_FOR_NEXT
]

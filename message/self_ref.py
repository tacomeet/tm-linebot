from linebot.models import TemplateSendMessage, MessageAction, ButtonsTemplate, ConfirmTemplate
from . import default

KEY = default.KEY_SELF_REF
START = '自己分析を開始します！\n' \
        '「次」または必要項目を入力して次の質問に行けます！\n' \
        '「終了」と入力してセッション自体を終了します！'
M_1_EXP = '経験'
M_1_PERS = '個性'
M_1_VIS = 'ビジョン'
M_1_TURN = 'ターニングポイント'
M_1 = TemplateSendMessage(
    alt_text='どの項目について自己分析を行いますか？', template=ButtonsTemplate(
        title='どの項目について自己分析を行いますか？', text='上から順番に行うことをお勧め致します！', actions=[
            MessageAction(label=M_1_EXP, text=M_1_EXP),
            MessageAction(label=M_1_PERS, text=M_1_PERS),
            MessageAction(label=M_1_VIS, text=M_1_VIS),
            MessageAction(label=M_1_TURN, text=M_1_TURN),
        ]))

# Experience
EXP_1 = '趣味や独学で身につけたことなどを書き出してください（5分ほど）\n' \
        '終わり次第「次」と入力して次の質問に行けます！'
EXP_1_EX = '例：小さい頃アメリカに住んでおり、英語が話せる'
EXP_2 = TemplateSendMessage(
    template=ConfirmTemplate(
        actions=[
            MessageAction(label='Yes', text='Yes'),
            MessageAction(label='No', text='No'),
        ], text='自分の経験を十分に書けましたか？'),
    alt_text='自分の経験を十分に書けましたか？')
EXP_3_YES = '一番大事にしている経験はどれですか？ その経験に対して以降の質問に答えて頂きます\n' \
            '終わり次第「次」と入力して次の質問に行けます！'
EXP_3_NO = '人より少し得意だと思うことを書き出してください（5分ほど）\n' \
           '終わり次第「次」と入力して次の質問に行けます！'
EXP_4 = '一番楽しんでいるものはどれですか？ その経験に対して以降の質問に答えて頂きます\n' \
        '終わり次第「次」と入力して次の質問に行けます！'
EXP_5 = 'それのどういうところを楽しんでいますか？\n' \
        '終わり次第「次」と入力して次の質問に行けます！'
EXP_6 = 'それを始めたきっかけは何ですか？\n' \
        '終わり次第「次」と入力して次の質問に行けます！'
EXP_7 = 'やっている時はどう感じていますか？\n' \
        '終わり次第「次」と入力して次の質問に行けます！'
EXP_8 = 'この経験から何か学んだことはありますか？\n' \
        '終わり次第「次」と入力して次の質問に行けます！'
EXP_9 = 'これからも続けていきたいですか？その理由は何ですか？\n' \
        '終わり次第「次」と入力して次の質問に行けます！'

# Personality
PERS_1 = 'あなたの得意なこと（他の人より苦労なくできること）や苦手なことを書き出してください！\n' \
         '終わり次第「次」と入力して次の質問に行けます！'
PERS_1_EX = '例：細かいところに気が付く'
PERS_2 = TemplateSendMessage(
    template=ConfirmTemplate(
        actions=[
            MessageAction(label='Yes', text='Yes'),
            MessageAction(label='No', text='No'),
        ], text='具体的に書けましたか？'),
    alt_text='具体的に書けましたか？')
PERS_3_YES = '一番気にしている短所を選んでください\n' \
             '終わり次第「次」と入力して次の質問に行けます！'
PERS_3_NO = 'それらの個性を（良い意味でも悪い意味でも）発揮したエピソードを書き出してください！（3分）\n' \
            '終わり次第「次」と入力して次の質問に行けます！'
PERS_3_NO_EX = '例：リーダシップがある。サークルの代表をやったり、友達を誘えってイベント・勉強会を開いたりした。'
PERS_4 = PERS_3_YES
PERS_5 = 'その短所にも、メリットがあるとしたら、どんなところだと思いますか？\n' \
         '終わり次第「次」と入力して次の質問に行けます！'
PERS_6 = TemplateSendMessage(
    template=ConfirmTemplate(
        actions=[
            MessageAction(label='Yes', text='Yes'),
            MessageAction(label='No', text='No'),
        ], text='その短所を直したいと思いますか？'),
    alt_text='その短所を直したいと思いますか？')
PERS_7_YES = 'その短所を直すために、何ができると思いますか？\n' \
             '終わり次第「次」と入力して次の質問に行けます！'
PERS_7_NO = 'その状態を乗り越える方法は何かありますか？\n' \
            '終わり次第「次」と入力して次の質問に行けます！'

# Vision
VIS_1 = '今までの⾃分の⼈⽣で起こった事象から感じたことやこれからも⼤切にしたい考えなどを書き出してください'
VIS_1_EX_1 = '例：自分の経験してきた音楽とプログラミングを組み合わせた分野で貢献したい'
VIS_1_EX_2 = '例：誠実な自分でありたい'
VIS_2 = TemplateSendMessage(
    template=ConfirmTemplate(
        actions=[
            MessageAction(label='Yes', text='Yes'),
            MessageAction(label='No', text='No'),
        ], text='ビジョンは書けそうですか？'),
    alt_text='ビジョンは書けそうですか？')
VIS_3_YES = '⾃分の「経験」や「個性」からどのように過ごしたら・何をしていたら幸せに感じるか、自分のビジョンを書き出してください！'
VIS_3_NO = '今まで経験してきたことはどんな側面を楽しんでいましたか？'
VIS_4 = 'あなたにとって幸せな状態とはどんな状態ですか？'
VIS_5 = '逆にどうしてもやりたくないことや許容し難い価値観はありますか？'
VIS_6 = '収入が安定して、時間があるとしたら何をして過ごしたいですか？'
VIS_7 = '5年後にどんな自分でいられたら嬉しいですか？'
VIS_8 = VIS_3_YES
VIS_9 = TemplateSendMessage(
    template=ConfirmTemplate(
        actions=[
            MessageAction(label='Yes', text='Yes'),
            MessageAction(label='No', text='No'),
        ], text='具体的に書けましたか？'),
    alt_text='具体的に書けましたか？')
VIS_10_YES = 'ビジョンと価値観を合わせて1〜3つのスローガンを作成しましょう！'
VIS_10_NO = 'そのビジョンや価値観が表されたエピソードを書き出してください'
VIS_11 = VIS_10_YES

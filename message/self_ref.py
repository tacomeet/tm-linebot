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

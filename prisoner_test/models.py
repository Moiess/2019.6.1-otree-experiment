from typing import Union

from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range,
    Currency)
from otree.currency import Currency

doc = """
囚徒困境博弈
Prisoner Dilemma Game
"""


class Constants(BaseConstants):    # 常量设置
    name_in_url = 'prisoner_test'  # 网页名
    players_per_group = 2          # 每组人数
    num_rounds = 100               # 回合数

    instructions_template = 'prisoner_test/Instructions.html'

    # 收益矩阵
    betray_payoff = c(300)
    betrayed_payoff = c(0)
    both_cooperate_payoff = c(200)
    both_defect_payoff = c(100)


class Subsession(BaseSubsession):  # 会话设置
    def creating_session(self):
        self.group_randomly()


class Group(BaseGroup):            # 组设置
    pass

class Player(BasePlayer):                     # 玩家设置
    decision = models.StringField(            # 选择
        choices=['合作', '不合作'],
        doc="""This player's decision""",
        widget=widgets.RadioSelect
    )

    def other_player(self):

        return self.get_others_in_group()[0]  # 获得其余组员列表中的第一个

    def set_payoff(self):                     # 构建收益矩阵
        payoff_matrix = {
            '合作':
                {
                    '合作': Constants.both_cooperate_payoff,
                    '不合作': Constants.betrayed_payoff
                },
            '不合作':
                {
                    '合作': Constants.betray_payoff,
                    '不合作': Constants.both_defect_payoff
                }
        }
        # 计算个人收益及个人总收益
        self.payoff = payoff_matrix[self.decision][self.other_player().decision]
        self.cumulative_payoff = sum([p.payoff for p in self.in_all_rounds()])

    name = models.StringField(label='你的名字')      # 姓名，储存为字符型
    number = models.IntegerField(label='你的学号')   # 学号，储存为整数型
    cumulative_payoff = models.CurrencyField()      # 总收益，储存为货币型

#













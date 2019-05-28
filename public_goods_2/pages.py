from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
import random

class Introduction(Page):
    """Description of the game: How to play and returns expected"""
    def is_displayed(self):
        self.group.set_id_list()
        self.player.chat_nickname()
        return self.round_number == 1


class Contribute(Page):
    """Player: Choose how much to contribute"""
    form_model = 'player'
    form_fields = ['contribution']
    timeout_seconds = 30
    timer_text = '请在剩余时间内完成选择，若未选择视为贡献100点'

    def before_next_page(self):                # 倒计时结束策略
        if self.timeout_happened:
            me = self.player
            me.contribution = c(random.randint(0,100))
            me.is_random = True


class GroupWaitPage(WaitPage):

    wait_for_all_groups = True
    body_text = '正在等待所有人入场...'
    title_text = '请稍等(如果出现长时间等待情况请举手示意老师或巡场同学)'


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_id_list()
        self.group.set_payoffs()
        self.group.set_avg_payoff()
        for p in self.group.get_players():
            p.set_cum_payoff()
        self.group.set_cum_payoff_rank()
        for p in self.group.get_players():
            p.set_rank()

    body_text = "请等待其他成员完成以继续"


class Results(Page):
    """Players payoff: How much each has earned"""

    def vars_for_template(self):
        company_payoff = None
        company_rank = None
        company_multiplier = None

        if self.player.role() == 'A':
            company_payoff = self.group.total_contribution_A
            company_rank = self.group.rank_a
        elif self.player.role() == 'B':
            company_payoff = self.group.total_contribution_B
            company_rank = self.group.rank_b
        elif self.player.role() == 'C':
            company_payoff = self.group.total_contribution_C
            company_rank = self.group.rank_c
        elif self.player.role() == 'D':
            company_payoff = self.group.total_contribution_D
            company_rank = self.group.rank_d

        if company_rank == 1:
            company_multiplier = 6
        elif company_rank == 2:
            company_multiplier = 4
        elif company_rank == 3:
            company_multiplier = 2
        elif company_rank == 4:
            company_multiplier = 1

        return{
            'player_role': self.player.role(),
            'company_payoff': company_payoff,
            'company_rank': company_rank,
            'company_multiplier': company_multiplier
        }

    timeout_seconds = 30


class Information(Page):
    """player's information"""
    form_model = 'player'
    form_fields = ['name', 'number', '_class']

    def is_displayed(self):
        return self.round_number == 1


page_sequence = [
    Introduction,
    Information,
    GroupWaitPage,
    Contribute,
    ResultsWaitPage,
    Results
]

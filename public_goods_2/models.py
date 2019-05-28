from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

doc = """

"""


class Constants(BaseConstants):
    name_in_url = 'public_goods_2'
    players_per_group = None
    num_rounds = 100

    instructions_template = 'public_goods_2/Instructions.html'

    # """Amount allocated to each player"""
    endowment = c(100)
    multiplier = 2


class Subsession(BaseSubsession):

    def vars_for_admin_report(self):
        contributions = [p.contribution for p in self.get_players() if p.contribution is not None]
        if contributions:
            return {
                'avg_contribution': sum(contributions)/len(contributions),
                'min_contribution': min(contributions),
                'max_contribution': max(contributions),
            }
        else:
            return {
                'avg_contribution': '(no data)',
                'min_contribution': '(no data)',
                'max_contribution': '(no data)',
            }


class Group(BaseGroup):
    total_contribution_A = models.CurrencyField()
    total_contribution_B = models.CurrencyField()
    total_contribution_C = models.CurrencyField()
    total_contribution_D = models.CurrencyField()
    individual_share_A = models.CurrencyField()
    individual_share_B = models.CurrencyField()
    individual_share_C = models.CurrencyField()
    individual_share_D = models.CurrencyField()
    avg_payoff = models.CurrencyField()
    rank_a = models.IntegerField()
    rank_b = models.IntegerField()
    rank_c = models.IntegerField()
    rank_d = models.IntegerField()

    def set_avg_payoff(self):
        self.avg_payoff = sum([p.payoff for p in self.get_players()])/len([p.contribution for p in self.get_players()])

    def set_payoffs(self):
        self.total_contribution_A = sum(p.contribution for p in self.get_players() if p.role() == 'A')
        self.total_contribution_B = sum(p.contribution for p in self.get_players() if p.role() == 'B')
        self.total_contribution_C = sum(p.contribution for p in self.get_players() if p.role() == 'C')
        self.total_contribution_D = sum(p.contribution for p in self.get_players() if p.role() == 'D')
        # print('A:',self.total_contribution_A,'B:',self.total_contribution_B,'C:',self.total_contribution_C,'D:',self.total_contribution_D)
        contribution = {
            'A': sum(p.contribution for p in self.get_players() if p.role() == 'A') / len([p.contribution
                                                                                           for p in self.get_players()
                                                                                           if p.role() == 'A']),
            'B': sum(p.contribution for p in self.get_players() if p.role() == 'B') / len([p.contribution
                                                                                           for p in self.get_players()
                                                                                           if p.role() == 'B']),
            'C': sum(p.contribution for p in self.get_players() if p.role() == 'C') / len([p.contribution
                                                                                           for p in self.get_players()
                                                                                           if p.role() == 'C']),
            'D': sum(p.contribution for p in self.get_players() if p.role() == 'D') / len([p.contribution
                                                                                           for p in self.get_players()
                                                                                           if p.role() == 'D'])
        }
        # print(contribution)
        c = sorted(contribution.items(), key=lambda x: x[1], reverse=True)
        fir = float(3*c[0][1])
        sec = float(3*c[1][1])
        thr = float(3*c[2][1])
        fou = float(3*c[3][1])
        c1 = [(c[0][0], fir), (c[1][0], sec), (c[2][0], thr), (c[3][0], fou)]

        self.individual_share_A = dict(c1)['A']
        self.individual_share_B = dict(c1)['B']
        self.individual_share_C = dict(c1)['C']
        self.individual_share_D = dict(c1)['D']

        rank = dict(enumerate(dict(c).keys()))
        rank1 = {v: k for k, v in rank.items()}
        self.rank_a = rank1['A'] + 1
        self.rank_b = rank1['B'] + 1
        self.rank_c = rank1['C'] + 1
        self.rank_d = rank1['D'] + 1

        for p in self.get_players():
            if p.role() == 'A':
                p.payoff = (Constants.endowment - p.contribution) + self.individual_share_A
            elif p.role() == 'B':
                p.payoff = (Constants.endowment - p.contribution) + self.individual_share_B
            elif p.role() == 'C':
                p.payoff = (Constants.endowment - p.contribution) + self.individual_share_C
            elif p.role() == 'D':
                p.payoff = (Constants.endowment - p.contribution) + self.individual_share_D

    def set_cum_payoff_rank(self):
        player_list = dict(zip([p.id_in_group for p in self.get_players()], [p.cumulative_payoff
                                                                            for p in self.get_players()]))
        rank = dict(enumerate(dict(sorted(player_list.items(), key=lambda x: x[1], reverse=True)).keys()))
        self.session.vars['cumulative_payoff_rank'] = {v: k for k, v in rank.items()}
        # print(self.session.vars['cumulative_payoff_rank'])

    def set_id_list(self):
        a = 1
        b = 1
        for p in self.get_players():
            if p.in_round(1)._class == 0:
                p.id_in_class = a
                a += 1
            else:
                p.id_in_class = b
                b += 1
        pass

class Player(BasePlayer):
    contribution = models.CurrencyField(
        min=0, max=Constants.endowment,
        doc="""The amount contributed by the player""",
    )

    name = models.StringField()
    number = models.IntegerField()
    _class = models.IntegerField(choices=[
        [0, '网络1701'],
        [1, '信工1701'],
    ])
    id_in_class = models.IntegerField()
    cumulative_payoff = models.CurrencyField()
    rank = models.IntegerField()
    is_random = models.BooleanField(initial=False)

    def set_cum_payoff(self):
        self.cumulative_payoff = sum([p.payoff for p in self.in_all_rounds()])

    def role(self):
        if self.in_round(1)._class == 0:
            if int(self.id_in_class) % 2 == 0:
                return 'A'
            else:
                return 'B'
        else:
            if int(self.id_in_class) % 2 == 0:
                return 'C'
            else:
                return 'D'

    def set_rank(self):
        self.rank = self.session.vars['cumulative_payoff_rank'][self.id_in_group] + 1

    def chat_nickname(self):
        return '公司 {} ID {} '.format(self.role(), self.id_in_group)
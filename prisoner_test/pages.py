from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants

class GroupWaitPage(WaitPage):

    wait_for_all_groups = True
    body_text = '正在等待所有人入场...'
    title_text = '请稍等(如果出现长时间等待情况请举手示意老师或巡场同学)'

    def vars_for_template(self):                   # 个人选择（大神写的码）
        me = self.player
        return{}

class Introduction(Page):                      # 介绍页面
                   # 时间限制
    timer_text = '将在以下时间后自动继续下一页'   # 设置倒计时显示信息

    def is_displayed(self):                    # 页面显示条件
        return self.round_number == 1

class Decision(Page):                          # 选择界面

    form_model = 'player'                      # 表单形式
    form_fields = ['decision']                 # 表单域

    def vars_for_template(self):               # 获得对手姓名 存在bug
        me = self.player
        oppoent = me.other_player().in_round(1).name
        return {'others_name': oppoent}

    timeout_seconds = 30                       # 时间限制
    timer_text = '请在剩余时间内完成选择，若未选择视为选择合作'  # 倒计时显示信息

    def before_next_page(self):                # 倒计时结束策略
        if self.timeout_happened:
            me = self.player
            me.decision = '合作'

class ResultsWaitPage(WaitPage):                   # 等待界面

    template_name = 'prisoner_test/WaitPage.html'  # 模板页设置
    def after_all_players_arrive(self):            # 待每组所有成员到达后计算收益

        for p in self.group.get_players():
            p.set_payoff()

    body_text = '另一位参与者正在选择……'             # 显示信息
    title_text = '请稍等(如果出现长时间等待情况请举手示意老师或巡场同学)'

class Results(Page):                               # 结果页面

    def vars_for_template(self):                   # 个人选择（大神写的码）
        me = self.player
        opponent = me.other_player()
        return {
            'my_decision': me.decision,
            'opponent_decision': opponent.decision,
            'same_choice': me.decision == opponent.decision,
        }

    timeout_seconds = 30
    timer_text = '将在以下时间后自动继续下一回合'

class Information(Page):
    '''player's information'''
    form_model = 'player'
    form_fields = ['name', 'number']

    def is_displayed(self):
        return self.round_number == 1



page_sequence = [
    Information,
    Introduction,
    GroupWaitPage,
    Decision,
    ResultsWaitPage,
    Results
]

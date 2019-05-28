# 这个程序用来模拟在不改变其他人贡献的情况下改变个人行为对总体收益的影响的变化
# 被注释的print函数都是在编写程序是用来检查运行情况的，保留在程序中

import xlrd  # Excel读取包
import xlwt  # Excel写入包


def read_excel():  # 读取数据
    workbook = xlrd.open_workbook(r'C:\Users\Administrator\Desktop\2018-12-13班级试验数据整理——个人相关.xlsx')
    global data  # 将读进来的数据存入一个全局变量data
    data = workbook.sheet_by_index(0)
    # print(data.name, data.nrows, data.ncols, data.row_values(1, start_colx=0, end_colx=2))
    # print(data.cell(1, 0))


class Player:  # 玩家类
    def __init__(self, id):  # 输入一个ID，从数据中读出它的公司，贡献
        self.id = id
        self.Cur_payoff = 0
        self.contribution = data.cell_value((round_number-1)*31+self.id, 3)
        self.company = int(data.cell_value(self.id, 8))
        # print('ID: ', self.id, '  贡献', self.contribution.value, '公司', self.company.value)

    def payofff(self):  # 计算四个公司分别的总贡献
        contributions[int(self.company)-1] += int(self.contribution)
        # print(contributions)


def game_start():  # 主程序
    # 写入文件部分
    file = xlwt.Workbook()
    table = file.add_sheet('sheet1')
    # table.write(0, 0, 'test')
    table.cell_overwrite_ok = True
    table.write(0, 0, 'ID')
    table.write(0, 1, '公司')
    table.write(0, 2, '贡献')
    table.write(0, 3, '本回合收益')
    table.write(0, 4, '总收益')
    table.write(0, 5, '总收益排名')
    table.write(0, 6, '回合数')
    file.save(r'模拟实验——临时文件（如需保存请另存为）.xls')
    # 初始化一些后面用到的变量，将收益，总收益，排名放入列表或字典中方便处理
    Personal_payoff = {}
    personal_curpayoff = []
    player_list = []
    for i in range(31):
        personal_curpayoff.append(0)
        player_list.append(i+1)
    # 输入实验ID
    test = int(input('请输入希望改变数据的玩家ID(1到31):'))
    if test >= 32 or test <= 0:
        print('玩家ID为1到31！')
    else:
        # player = Player(test)
        print('玩家ID：', test, '\n',
              '玩家最终排名：第', int(data.cell_value(1023+test, 10)), '名', '\n',
              '玩家所在公司：', {1: 'A', 2: 'B', 3: 'C', 4: 'D'}[data.cell_value(1023+test, 8)], '公司')
    # 回合开始
    global round_number
    round_number = 1
    for i in range(1, 35):  # 第一个循环从第一回合到第34回合
        print('第', i, '回合:')
        # 创建一个全局变量用来储存每个回合四个公司分别的总贡献，并在回合开始时重置
        global contributions
        contributions = [0, 0, 0, 0]
        personal_payoff = []

        for j in range(1, 32):  # 第二个循环从ID1到ID31
            if j == test:  # 如果循环到实验ID则输出信息
                player = Player(test)
                print(test, '号玩家在实验中本回合贡献了', data.cell_value((round_number-1)*31+test, 3))
                player.contribution = int(input('请输入本回合贡献(0-100)：'))
                player.payofff()  # 调用函数，将个人贡献加到公司总贡献里去
            else:
                player = Player(j)
                player.payofff()
            table.write((i-1)*31+j, 1, player.company)  # 将个人所属公司写入Excel
            table.write((i-1)*31+j, 2, player.contribution)  # 将个人贡献写入Excel
        # 计算总贡献排名(round函数即取四舍五入）
        rank = dict(sorted([
            (1, round(contributions[0] / 8)),
            (2, round(contributions[1] / 8)),
            (3, round(contributions[2] / 7)),
            (4, round(contributions[3] / 8))
        ], key=lambda x: x[1]))
        # print(rank)
        # 先将每个公司的总贡献排名计算公司收益
        contributions = {1: contributions[0], 2: contributions[1], 3: contributions[2], 4: contributions[3]}
        payoff = {list(rank.keys())[0]: round(rank[list(rank.keys())[0]] * 1),
                  list(rank.keys())[1]: round(rank[list(rank.keys())[1]] * 2),
                  list(rank.keys())[2]: round(rank[list(rank.keys())[2]] * 3),
                  list(rank.keys())[3]: round(rank[list(rank.keys())[3]] * 6)}
        # print(payoff)
        # print(Payoff)
        # 分别计算每名玩家本回合收益，并储存在预先设定好的列表中
        for j in range(1, 32):
            player = Player(j)
            # print(player.company)
            personal_payoff.append(100-player.contribution+int(payoff[player.company]))
        Personal_payoff[i] = personal_payoff
        # 分别计算每名玩家的总收益，并储存在预先设定好的列表中
        for j in range(31):
            personal_curpayoff[j] += Personal_payoff[i][j]
        # 计算排名：共分为四步
        # 第一步：将总收益列表与玩家列表合并为一个字典，方便排序及调取
        personal_rank = zip(player_list, personal_curpayoff)
        # 第二步：使用sorted函数将其排序
        personal_rank = dict(sorted(personal_rank, key=lambda x: x[1], reverse=True))
        # 第三步：使用enumerate函数将排好序的玩家ID提取出来，并和排名一起组成一个新的字典
        personal_rank = dict(enumerate(personal_rank, 1))
        # 第四步：将新的字典调整成{玩家ID：排名}的格式
        personal_rank = {v: k for k, v in personal_rank.items()}
        # print(personal_rank, '\n', Personal_payoff, '\n', personal_curpayoff)
        # 显示实验玩家本回合信息
        print(test, '号玩家本回合收益为', personal_payoff[test-1], '\n',
              '总收益为：', personal_curpayoff[test-1], '\n'
              '总收益排名为：', personal_rank[test])
        # 将本回合数据写入Excel
        for j in range(1, 32):
            table.write((i-1)*31+j, 0, j)
            table.write((i-1)*31+j, 3, personal_payoff[j-1])
            table.write((i-1)*31+j, 4, personal_curpayoff[j-1])
            table.write((i-1)*31+j, 5, personal_rank[j])
            table.write((i-1)*31+j, 6, i)
        # 回合数+1，本回合结束开始下一回合
        round_number += 1
        # 保存Excel
        file.save(r'模拟实验——临时文件（如需保存请另存为）.xls')


if __name__ == '__main__':
    read_excel()
    game_start()

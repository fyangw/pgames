# -*- coding: utf-8 -*-

import random
import pgzero
import os

TITLE = "口算对战"
WIDTH = 800
HEIGHT = 600

"""
口算对战
出题口算，由两个玩家同时抢答
"""

class MentalArithQuestion(object):
    """四则运算类"""


    def __init__(self)->None:
        """初始化类实例对象。
        Args:无。
        Returns:无返回值，直接初始化实例对象的属性。
        """
        self.a = 0
        self.b = 0
        self.operator = '='
        self.answer = 0
        self.make_restricted_question()

    def make_restricted_question(self)->None:
        """生成一个答案限定范围的四则运算问题。"""
        while self.answer <= 0 or self.answer > 200: 
            self.make_question()

    def make_question(self)->None:
        """生成一个随机的四则运算问题。
        Args:无参数。
        Returns:无返回值，但会更新对象的属性：
            - a: 第一个随机数，范围在1到100之间。
            - b: 第二个随机数，范围在1到100之间。
            - operator: 随机选择的四则运算符，包括'+', '-', '*', '/'。
            - answer: a 和 b 进行 operator 运算后的结果。
        """
        self.a = random.randint(1, 100)
        self.b = random.randint(1, 100)
        self.operator = random.choice(['+', '-', '*', '/'])
        if self.operator == '+':
            self.answer = self.a + self.b
        elif self.operator == '-':
            self.answer = self.a - self.b
        elif self.operator == '*':
            self.answer = self.a * self.b
        else:
            self.answer = self.a // self.b


    def check_correct(self, player_answer)->bool:
        """判断玩家答案是否正确
        Args:player_answer (str): 玩家输入的答案
        Returns:
            bool: 如果玩家答案与正确答案相等，则返回True；否则返回False
        """
        return int(player_answer) == self.answer
    

    def get_question_str(self)->str:
        """将当前对象转化为字符串形式返回。
        Args:无参数。
        Returns:
            str: 当前对象转化为字符串形式的结果，格式为"{a} {operator} {b} ="。
        """
        return f'{self.a} {self.operator} {self.b} ='


class MentalArithBattle(object):
    """口算对战类"""


    def __init__(self)->None:
        """初始化游戏对象。
        Args:无。
        Returns:无返回值。
        """
        self.player_list = [
            MentalArithPlayer((0, HEIGHT//6), 'x123qweasd', 'z', 'c'), 
            MentalArithPlayer((WIDTH//2, HEIGHT//6), 'm678yuihjk', 'n', ',')
        ]
        self.main_pos = (WIDTH//10, HEIGHT//2)
        self.game_init = True
        self.game_over = False
        self.question = None
        self.question_left = 3
        self.set_question()


    def set_question(self)->None:
        """设置新问题，并清空所有玩家的答案，同时减少剩余问题数量。
        Args:无参数。
        Returns:无返回值。
        """
        self.question = MentalArithQuestion()
        for player in self.player_list:
            player.answer = 0
        self.question_left -= 1


    def process_input(self, key)->None:
        """处理玩家的输入
        Args:
            key (str): 玩家输入的按键
        Returns:None
        """
        # 同时接受玩家1和玩家2的输入
        processed_input = False
        for player in self.player_list:
            if key in player.key_num_str:
                # 添加一位数字
                player.answer = player.answer * 10 + player.key_num_str.index(key)
                processed_input = True
            elif key == player.key_backspace:
                # 删除一位数字
                player.answer = player.answer // 10
                processed_input = True
            if processed_input == True and self.question.check_correct(player.answer):
                # 玩家答对了，加分
                player.score += 1
                # 生成新问题
                self.set_question()
                # 如果问题都答完了，游戏结束
                if self.question_left < 0:
                    self.game_over = True
                break


class MentalArithPlayer(object):
    """口算对战玩家，仅作为状态保存"""

    def __init__(self, pos, key_num_str, key_ok, key_backspace):
        """初始化计算器对象
        Args:
            pos: 显示位置
            key_num_str: 数字键的字符串表示，索引序号是0-9，如'0123456789'
            key_ok: 确认键的字符串表示
            key_backspace: 退格键的字符串表示
        Returns:
            None
        Attributes:
            pos: 显示位置
            key_num_str: 数字键的字符串表示
            key_ok: 确认键的字符串表示
            key_backspace: 退格键的字符串表示
            answer: 当前输入的答案
            score: 当前得分
        """
        self.pos = pos
        self.key_num_str = key_num_str
        self.key_ok = key_ok
        self.key_backspace = key_backspace
        self.answer = 0
        self.score = 0
    
    def to_key_dict(self)->dict:
        """将按键字符串和按键名称转换为按键字典
        Args:无参数。
        Returns:
            dict: 包含按键字符串的字典，其中键为按键名称，值为按键字符串。
        """
        key_dict = {}
        for i in range(len(self.key_num_str)):
            key_dict[chr(ord('0') + i)] = self.key_num_str[i]
        key_dict['ok'] = self.key_ok
        key_dict['backspace'] = self.key_backspace
        return key_dict
    

    def to_key_dict_message(self)->str:
        """将按键字符串和按键名称转换为按键字典
        Args:无参数。
        Returns:
            str: 包含按键字符串的字典，其中键为按键名称，值为按键字符串。
        """
        key_dict = self.to_key_dict()
        message = ""
        for k, v in key_dict.items():
            message += f"{k}: {v}\n"
        return message


def update()->None:
    """pgzero框架的更新函数
    Args:无参数。
    Returns:无返回值。
    """
    pass

def on_key_down(key, mod, unicode)->None:
    """pgzero框架的处理按键按下事件
    Args:
        key: 按键编码
        mod: 按键修饰符
        unicode: 按键对应的Unicode字符
    Returns:None
    """
    global battle
    if battle.game_init:
        battle.game_init = False
    elif battle.game_over:
        battle.__init__()
    else:
        battle.process_input(unicode)


def draw():
    """pgzero框架的绘制游戏界面
    Args:无
    Returns:无
    """
    global battle
    screen.clear()
    screen.fill('black')
    screen.draw.text("Mental Arithmatic", (5, 5), color='white')
    if battle.game_init:
        # 游戏初始化阶段，显示玩家按键设置
        for i in range(len(battle.player_list)):
            player = battle.player_list[i]
            screen.draw.text(f"Player{i+1} Keys:\n{player.to_key_dict_message()}", player.pos, color='white')
        screen.draw.text("Press any key to start game", (5, HEIGHT // 3 * 2), color='green')
    elif battle.game_over:
        # 游戏结束阶段，显示获胜者
        if battle.player_list[0].score > battle.player_list[1].score:
            won_message = "Player 1 Won"
        else:
            won_message = "Player 2 Won"
        screen.draw.text(won_message, (WIDTH // 2, HEIGHT // 2), color='green')
        screen.draw.text("Press any key to start a new game.", (5, HEIGHT // 3 * 2), color='green')
    else:
        # 游戏进行阶段，显示玩家得分和当前输入的答案
        for i in range(len(battle.player_list)):
            player = battle.player_list[i]
            screen.draw.text(f"Player{i+1} Score: {player.score} Answer: {player.answer}", player.pos, color='white')
        screen.draw.text(battle.question.get_question_str(), battle.main_pos, color='white')

# 初始化游戏对象
global battle
battle = MentalArithBattle()

if __name__ == '__main__':
    # 启动游戏
    #os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pgzero.run(
        WIDTH,
        HEIGHT,
        fps=30,
    )

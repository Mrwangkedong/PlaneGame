import pygame
from game_items import *


class HUBPanel(object):
    """所有面板精灵的控制类"""

    margin = 10  # 精灵之间的间距
    white = (255, 255, 255)  # 白色
    gray = (64, 64, 64)  # 灰色

    reward_score = 100000  # 奖励分值
    level2_score = 100000  # 级别2分值
    level3_score = 500000  # 级别3分值

    recore_filename = "record.txt"

    def __init__(self, display_group):
        # 基本数据
        self.score = 0  # 初始得分
        self.lives_count = 3  # 初始生命数
        self.level = 1  # 游戏级别
        self.best_score = self.read_best_score()  # 最好成绩
        # 图像精灵
        # 状态精灵（暂停/继续）
        self.status_sprite = StatusButton(("game_pause_nor.png", "game_resume_nor.png"), display_group)
        self.status_sprite.rect.topleft = (self.margin, self.margin)  # 设置精灵左上角位置
        # 生命计数精灵
        self.lives_spire = GameSprite("lives.png", 0, display_group)
        self.lives_spire.rect.bottomright = (
            SCREEN_RECT.w - self.lives_spire.rect.w, SCREEN_RECT.h - self.margin)
        # 炸弹精灵
        self.bomb_sprite = GameSprite("bomb.png", 0, display_group)
        self.bomb_sprite.rect.bottomleft = (self.margin, SCREEN_RECT.h - self.margin)  # 设置炸弹精灵位置与左下角

        # 数字标签精灵
        self.score_label = Label("%d" % self.score, 32, self.gray, display_group)  # 得分标签
        self.score_label.rect.midleft = (self.status_sprite.rect.right + self.margin, self.status_sprite.rect.centery)

        self.bomb_label = Label("X 3", 32, self.gray, display_group)  # 炸弹标签
        self.bomb_label.rect.midleft = (self.bomb_sprite.rect.right + self.margin, self.bomb_sprite.rect.centery)

        self.lives_label = Label("X %d" % self.lives_count, 32, self.gray, display_group)  # 生命数标签
        self.lives_label.rect.midright = (SCREEN_RECT.right - self.margin, self.bomb_label.rect.centery)

        # 屏幕中央提示标签精灵，==先创建，然后为达到一下精灵的出现与消失，先暂不添加精灵组；在需要时候再添加以及移除==
        self.best_label = Label("Best:%d" % self.best_score, 48, self.white)  # 最好成绩标签

        self.status_label = Label("Game Paused!", 36, self.white)  # 状态标签

        self.tip_label = Label("Press space and again.", 22, self.white)  # 提示信息标签

    def showBomb(self, count):
        """修改炸弹数量"""
        self.bomb_label.set_text("X %d" % count)
        self.bomb_label.rect.midleft = (
            self.bomb_sprite.rect.right + self.margin, self.bomb_sprite.rect.centery)  # 重新设置位置

    def showLives(self):
        """显示生命数量"""
        # 设置生命数字
        self.lives_label.set_text("X %d" % self.lives_count)
        # 设置生命计数标签位置
        self.lives_label.rect.midright = (SCREEN_RECT.right - self.margin, self.bomb_label.rect.centery)
        # 调整生命计数精灵位置
        self.lives_spire.rect.bottomright = (
            SCREEN_RECT.w - self.lives_spire.rect.w, SCREEN_RECT.h - self.margin)

    def increase_score(self, enemy_score):
        """增加游戏得分

        :param enemy_score:摧毁敌机的分值
        :return:增加 enemy_score 后，游戏级别是否提升
        """
        # 计算游戏得分
        score = self.score + enemy_score

        # 判断是否需要增加一条命
        if score // self.reward_score != self.score // self.reward_score:
            self.lives_count += 1
            self.showLives()
        self.score = score

        # 更新最好成绩
        self.best_score = score if score > self.best_score else self.best_score

        # 更新游戏级别
        if score < self.level2_score:
            level = 1
        elif score < self.level3_score:
            level = 2
        else:
            level = 3

        is_upgrade = level != self.level
        self.level = level

        # 修改得分标签及其内容
        self.score_label.set_text("%d" % self.score)
        self.score_label.rect.midleft = (self.status_sprite.rect.right + self.margin, self.status_sprite.rect.centery)

        return is_upgrade

    def save_best_score(self):
        """将最好的成绩写入文件中"""
        print(self.best_score)
        with open(self.recore_filename, 'w') as f:
            f.write(str(self.best_score))

    def read_best_score(self):
        """将最好的成绩写入文件中"""
        with open(self.recore_filename, 'r') as f:
            return int(f.read())

    def panel_paused(self, is_game_over, display_group):
        """
        中间提示信息的出现
        :param diaplay_group: 精灵组
        :param is_game_over: 结束游戏-T/暂停游戏-F
        :return:
        """
        # 如果此时精灵组中已经包含，则return
        if display_group.has(self.best_label, self.status_label, self.tip_label):
            return

        # 根据是否游戏结束设置不同信息
        text = "Game Over!" if is_game_over else "Game Paused！"
        tip = "Press space and again!" if is_game_over else "Press space and continue！"

        # 设置标签文字
        self.best_label.set_text("Best: %d" % self.best_score)
        self.status_label.set_text(text)
        self.tip_label.set_text(tip)

        # 设置精灵位置
        self.best_label.rect.center = SCREEN_RECT.center
        self.status_label.rect.midbottom = (self.best_label.rect.centerx, self.best_label.rect.y - 2 * self.margin)
        self.tip_label.rect.midtop = (self.best_label.rect.centerx, self.best_label.rect.bottom + 6 * self.margin)

        # 添加到精灵组
        display_group.add(self.best_label, self.status_label, self.tip_label)

        # 切换精灵状态
        self.status_sprite.switch_status(True)

    def panel_continue(self, display_group):
        """
        继续游戏，中间提示信息的消失
        :param diaplay_group: 精灵组
        :return:
        """

        display_group.remove(self.best_label, self.status_label, self.tip_label)
        # 切换精灵状态
        self.status_sprite.switch_status(False)

    def reset_panel(self):
        """重置面板数据"""
        self.score = 0
        self.lives_count = 3

        # 重置精灵数据
        self.increase_score(0)  # 能够重置level，并且能够重置label的位置
        self.showLives()  # 重置lives_label的位置
        self.showBomb(3)


















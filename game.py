import pygame, random
from typing import List

from game_hud import *
from game_items import *


class Game(object):
    #     游戏核心类
    def __init__(self):
        # 游戏窗口
        self.main_window = pygame.display.set_mode(SCREEN_RECT.size)
        # 游戏状态
        self.is_game_over = False
        self.is_game_pause = False

        # 音乐播放器

        # 游戏精灵组
        self.all_group = pygame.sprite.Group()  # 所有精灵组
        self.enemies_group = pygame.sprite.Group()  # 敌机精灵组
        self.supplies_group = pygame.sprite.Group()  # 道具精灵组

        # ===============游戏精灵==============
        # 背景精灵
        # 1）创建两个精灵，然后在init中进行位置初始化
        # background_image1 = GameBackground(True, self.all_group)   # 游戏背景精灵
        # background_image2 = GameBackground(False, self.all_group)   # 游戏背景精灵
        # 2）创建两个精灵，未在init中进行位置初始化，手动初始化位置
        # background_image2.rect.y = -background_image2.rect.h  # 在类的初始化中进行改变

        # 3）创建两个精灵，不传入组信息，手动添加到精灵组里面
        self.all_group.add(GameBackground(True), GameBackground(False))

        # 创建控制面板
        self.hud_panel = HUBPanel(self.all_group)

        # 英雄飞机精灵
        self.hero_sprite = HreoPlane(self.all_group)
        self.hud_panel.showBomb(self.hero_sprite.bomb_count)  # 根据飞机属性设置炸弹数量

        # 创建敌机精灵(初始），等级变化时再次调用
        self.creat_enemies()

        # 创建空投
        self.creat_supplies()

        pass

    def reset_game(self):
        """重置游戏数据"""
        self.is_game_over = self.is_game_pause = False
        # 重置面板
        self.hud_panel.reset_panel()
        # 销毁当前页面敌机,子弹
        for enemy in self.enemies_group:
            enemy.kill()
        for bullet in self.hero_sprite.bullets_group:
            bullet.kill()
        # 重新创建飞机
        self.creat_enemies()
        # 重置英雄飞机位置
        self.hero_sprite.rect.midbottom = HERO_DEFAULT_MID_BOTTOM

    def start_game(self):
        """开启游戏主逻辑"""
        # 创建时钟
        clock = pygame.time.Clock()

        # 动画帧数计数器
        frame_count = 0

        while True:
            # 监听玩家生命数是否为0，死了没 ！！！！
            self.is_game_over = self.hud_panel.lives_count == 0

            # 处理事件监听
            if self.event_handle():
                # 若返回True则发生了退出事件，保存最好成绩
                self.hud_panel.save_best_score()
                return
            # 根据游戏状态切换界面显示内容
            if self.is_game_over:
                self.hud_panel.panel_paused(True, self.all_group)
                print("游戏结束~")
            elif self.is_game_pause:  # 游戏暂停中...
                print("游戏暂停...")
            else:  # 游戏进行中...
                # 增加得分
                if self.hud_panel.increase_score(1):
                    print("游戏难度进行升级，当前级别%d" % self.hud_panel.level)
                    self.creat_enemies()  # 增加敌机数量
                # 处理长按时间按键移动
                keys = pygame.key.get_pressed()  # get_pressed() 得到一个元组,一个及长的set()
                move_hor = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]  # 水平的移动基数
                move_ver = keys[pygame.K_DOWN] - keys[pygame.K_UP]  # 竖直移动基数

                # 监听飞机碰撞
                self.check_collide()

                # 游戏帧数控制
                frame_count = (frame_count + 1) % FRAME_INTERVAL
                # 精灵组更新
                self.all_group.update(frame_count == 0, move_hor, move_ver)

            self.all_group.draw(self.main_window)  # 精灵组进行绘制,Every time

            # 刷新页面
            pygame.display.update()

            # 设置刷新率，一秒钟刷新60帧
            clock.tick(60)

    def event_handle(self):
        """获取并处理事件"""
        for event in pygame.event.get():
            # 设置退出按钮
            if event.type == pygame.QUIT:
                # 退出按钮被点击
                return True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # 用户按下esc键
                return True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # 用户按下空格键
                if self.is_game_over:
                    # 面板中间信息消失
                    self.hud_panel.panel_continue(self.all_group)
                    # 游戏结束，重置游戏
                    self.reset_game()
                else:
                    # 游戏未结束，暂停/继续游戏，出现/消失面板
                    self.is_game_pause = not self.is_game_pause
                    self.hud_panel.panel_paused(False, self.all_group) if self.is_game_pause \
                        else self.hud_panel.panel_continue(self.all_group)

            # 修改炸弹数量（按键b）
            if not self.is_game_pause and not self.is_game_over:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                    # 释放炸弹
                    score = self.hero_sprite.blowup(self.enemies_group)  # 引爆所有飞机
                    self.hud_panel.showBomb(self.hero_sprite.bomb_count)  # 根据飞机属性设置炸弹数量
                    if self.hud_panel.increase_score(score):
                        print("游戏难度进行升级，当前级别%d" % self.hud_panel.level)
                        self.creat_enemies()  # 增加敌机数量
                elif event.type == HERO_DEAD_EVENT:
                    # 玩家飞机死掉
                    self.hud_panel.lives_count -= 1
                    self.hud_panel.showLives()
                    self.hud_panel.showBomb(self.hero_sprite.bomb_count)
                elif event.type == HERO_POWER_OFF_EVENT:
                    # 取消英雄飞机无敌
                    self.hero_sprite.is_power = False
                    pygame.time.set_timer(HERO_POWER_OFF_EVENT, 0)  # 设置定时器延时为0，可用取消定时器
                elif event.type == HERO_FIRE_EVENT:
                    # 发射子弹
                    self.hero_sprite.fire(self.all_group)
                elif event.type == THROW_SUPPLY_EVENT:
                    # 随机投放（一个）道具
                    supply = random.choice(self.supplies_group.sprites())
                    supply.throw_supply()
                elif event.type == BULLET_ENHANCED_OFF_EVENT:
                    self.hero_sprite.bullets_kind = 0  # 子弹恢复
                    pygame.time.set_timer(BULLET_ENHANCED_OFF_EVENT, 0)
                # 测试
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    supply = random.choice(self.supplies_group.sprites())
                    supply.throw_supply()

        return False

    def creat_enemies(self):
        """创建敌机"""
        # 获取当前敌机精灵组中的精灵数量
        count = len(self.enemies_group.sprites())
        groups = (self.all_group, self.enemies_group)

        # 根据不同的关卡创建不同数量的飞机
        if self.hud_panel.level == 1 and count == 0:
            # 关卡1
            for i in range(16):
                EnemyPlane(3, 0, *groups)

        elif self.hud_panel.level == 2 and count == 16:
            # 关卡2
            for enemy in self.enemies_group.sprites():
                enemy.max_speed = 5
            for i in range(8):
                EnemyPlane(5, 0, *groups)
            for i in range(2):
                EnemyPlane(1, 1, *groups)  # 创建中级飞机
        elif self.hud_panel.level == 3 and count == 26:
            for enemy in self.enemies_group.sprites():
                enemy.max_speed += 2
            for i in range(8):
                EnemyPlane(7, 0, *groups)
            for i in range(2):
                EnemyPlane(3, 1, *groups)  # 创建中级飞机
            for i in range(2):
                EnemyPlane(1, 2, *groups)  # 创建高级飞机

    def check_collide(self):
        """检查是否有碰撞"""
        # 1)检查子弹与敌机的碰撞
        # 子弹和敌机的碰撞分析  hit_enemies是一个字典，key为enemies_group中被碰撞精灵，value为与key精灵碰撞的子弹精灵
        hit_enemies = pygame.sprite.groupcollide(self.enemies_group, self.hero_sprite.bullets_group,
                                                 False, False, pygame.sprite.collide_mask)
        for enemy in hit_enemies:
            # 已经被摧毁的飞机不需要再处理
            if enemy.hp <= 0:
                continue
            for bullet in hit_enemies[enemy]:
                bullet.kill()  # 销毁子弹
                enemy.hp -= bullet.damage  # 修改敌机生命值
                if enemy.hp > 0:
                    continue
                if self.hud_panel.increase_score(enemy.value):
                    self.creat_enemies()
                # 这个飞机已经被摧毁，不需要遍历下一刻子弹
                break
        # 3)检查飞机与道具之间的碰撞
        collied_supplies = pygame.sprite.spritecollide(self.hero_sprite, self.supplies_group,
                                                     False, pygame.sprite.collide_mask)
        if collied_supplies:
            collied_supply = collied_supplies[0]
            collied_supply.rect.y = SCREEN_RECT.h
            # 重置位置
            # 如果是炸弹补给
            if collied_supply.kind == 0:
                self.hero_sprite.bomb_count += 1  # 炸弹数量增加
                self.hud_panel.showBomb(self.hero_sprite.bomb_count)  # 更新面板
            else:  # 子弹增强
                self.hero_sprite.bullets_kind = 1  # 设置子弹种类
                pygame.time.set_timer(BULLET_ENHANCED_OFF_EVENT, 20000)  # 设置子弹增强，20s后取消【在event_handle中进行捕获】



        # 2)检查飞机与敌机的碰撞
        # 英雄飞机有无敌
        if self.hero_sprite.is_power:
            return
        # 英雄飞机没有无敌
        collide_enemies = pygame.sprite.spritecollide(self.hero_sprite, self.enemies_group, False,
                                                      pygame.sprite.collide_mask)

        # 过滤掉处于爆炸状态的飞机
        enemies = list(filter(lambda x: x.hp > 0, collide_enemies))

        if enemies:
            self.hero_sprite.hp = 0  # 英雄飞机被撞毁
            self.hero_sprite.is_power = True

        for enemy in enemies:
            enemy.hp = 0  # 敌机生命值变为0

    def creat_supplies(self):
        """创建两个道具，一个炸弹补给，一个子弹补给"""
        Supply(0, self.supplies_group, self.all_group)  # 炸弹补给
        Supply(1, self.supplies_group, self.all_group)  # 子弹补给
        # 设置补给投放事件，30s一次
        pygame.time.set_timer(THROW_SUPPLY_EVENT, 25000)



if __name__ == '__main__':
    # 初始化游戏
    pygame.init()

    # 开始游戏
    Game().start_game()

    # 释放游戏资源
    pygame.quit()

import random
from typing import Any

import pygame

# 定义全局变量
SCREEN_RECT = pygame.Rect(0, 0, 450, 800)
FRAME_INTERVAL = 20  # 帧数控制间隔
HERO_BOMB_COUNT = 3  # 英雄默认炸弹数量
# 英雄默认初始位置
HERO_DEFAULT_MID_BOTTOM = (SCREEN_RECT.centerx, SCREEN_RECT.bottom - 90)
# 英雄死亡事件
HERO_DEAD_EVENT = pygame.USEREVENT
# 取消英雄无敌事件
HERO_POWER_OFF_EVENT = pygame.USEREVENT + 1
# 英雄发射子弹事件
HERO_FIRE_EVENT = pygame.USEREVENT + 2
# 子弹速度
BULLET_SPEED = -10
# 补给投放事件
THROW_SUPPLY_EVENT = pygame.USEREVENT + 3
# 取消子弹强化的定时事件
BULLET_ENHANCED_OFF_EVENT = pygame.USEREVENT + 4


class GameSprite(pygame.sprite.Sprite):
    res_path = "res/images/"

    def __init__(self, image_name, speed, *group):
        """初始化精灵对象"""
        # 调用父类方法，把当前精灵对象放到精灵组里
        super(GameSprite, self).__init__(*group)

        # 创建图片
        self.image = pygame.image.load(self.res_path + image_name)
        # 获取矩形
        self.rect = self.image.get_rect()
        # 设置移动速度
        self.speed = speed
        # 生成遮罩属性（mask）,提高碰撞检测的执行效率。
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *args: Any, **kwargs: Any) -> None:
        """更新元素内容"""
        self.rect.y += self.speed


class GameBackground(GameSprite):
    """游戏背景类"""

    def __init__(self, is_alt, *group):
        """如果是True，显示框中，若为False，隐藏在框上方"""
        super(GameBackground, self).__init__("background.png", 1, *group)
        if is_alt is False:
            self.rect.y = -self.rect.h

    def update(self, *args: Any, **kwargs: Any) -> None:
        super(GameBackground, self).update(*args)

        # 如果图片已经滚动到底部，则立即回到窗口的最上面，重新显示
        if self.rect.y == self.rect.h:
            self.rect.y = -self.rect.h  # 此时用了两张图片，当下面一张到达底部，重新回到上面


class StatusButton(GameSprite):
    """游戏面板状态按钮类"""

    def __init__(self, image_names, *group):
        """images_name 接收两张图片，第一张是暂停标；第二张是运行标"""
        super(StatusButton, self).__init__(image_names[0], 0, *group)

        # 准备用于切换的两张图片
        self.status_images = [pygame.image.load(self.res_path + image_name) for image_name in image_names]

    def switch_status(self, is_pause):
        """根据是否暂停，转化状态图片对象"""
        self.image = self.status_images[1 if is_pause else 0]


class Label(pygame.sprite.Sprite):
    """标签精灵"""
    res_path = "res/font/Marker Felt.ttf"

    def __init__(self, text, size, color, *groups):
        """初始化标签精灵的数据"""
        super(Label, self).__init__(*groups)

        # 创建字体对象
        self.font = pygame.font.Font(self.res_path, size)

        # 字体的颜色
        self.color = color

        # 精灵属性(必备)
        self.image = self.font.render(text, True, self.color)
        self.rect = self.image.get_rect()

    def set_text(self, text):
        """更新显示文本内容"""
        self.image = self.font.render(text, True, self.color)
        self.rect = self.image.get_rect()


class Plane(GameSprite):
    """飞机类"""

    def __init__(self, hp, speed, value, wav_name, normal_names, hurt_name, destroy_names, *group):
        """
        飞机精灵类的初始化
        :param hp: 生命值
        :param speed: 飞机速度
        :param value: 击毁价值
        :param wav_name: 音频文件名称
        :param normal_names: 正常飞行图像名称列表
        :param hurt_name: 受伤图像名称
        :param destroy_names: 被击毁图像名称列表
        :param group: 精灵组
        """
        super(Plane, self).__init__(normal_names[0], speed, *group)
        # 飞机基本属性
        self.hp = hp
        self.max_hp = hp
        self.value = value
        self.wav_name = wav_name

        # 图像属性
        # 1)正常图像列表及索引
        self.normal_images = [pygame.image.load(self.res_path + name) for name in normal_names]
        self.normal_index = 0
        # 2)受伤图像列表
        self.hurt_image = pygame.image.load(self.res_path + hurt_name)
        # 3)摧毁图像列表及索引
        self.destroy_images = [pygame.image.load(self.res_path + name) for name in destroy_names]
        self.destroy_index = 0

    def reset_plane(self):
        """重置飞机"""
        self.hp = self.max_hp

        self.normal_index = 0
        self.destroy_index = 0

        self.image = self.normal_images[0]

    def update(self, *args: Any, **kwargs: Any) -> None:
        """更新状态，准备下一次显示的内容"""
        # 是否动画要更新,如果为False，不更新
        if not args[0]:
            return

        if self.hp == self.max_hp:
            # 切换要显示的图片
            self.image = self.normal_images[self.normal_index]
            # 计算下次显示的缩影
            self.normal_index = (self.normal_index + 1) % len(self.normal_images)
        elif self.hp > 0:
            # 受伤
            self.image = self.hurt_image
        else:
            # 死亡
            if self.destroy_index < len(self.destroy_images):
                self.image = self.destroy_images[self.destroy_index]
                self.destroy_index += 1
            else:
                self.reset_plane()


class HreoPlane(Plane):
    """英雄飞机类"""

    def __init__(self, *group):
        """初始化"""
        self.is_power = False  # 是否无敌
        self.bomb_count = HERO_BOMB_COUNT  # 炸弹数量
        self.bullets_kind = 0  # 子弹类型 - 0表示单排，1表示双排
        self.bullets_group = pygame.sprite.Group()  # 子弹精灵组
        # 继承父类飞机属性
        super(HreoPlane, self).__init__(1, 5, 0, "me_dowm.wav", ['hero%d.png' % i for i in range(1, 3)], "lives.png",
                                        ['hero_blowup_n%d.png' % j for j in range(1, 5)], *group)
        # 初始英雄飞机位置，位于屏幕下底部
        self.rect.midbottom = HERO_DEFAULT_MID_BOTTOM

        # 创建玩家飞机之后，每0.2秒激活一次
        pygame.time.set_timer(HERO_FIRE_EVENT, 200)

    def update(self, *args: Any, **kwargs: Any) -> None:
        """

        args[0]: 是否要更新下一帧动画
        args[1]：水平方向移动基数
        args[2]：垂直方向移动基数
        """
        super(HreoPlane, self).update(args[0])
        if len(args) != 3 or self.hp <= 0:
            return

        self.rect.x += args[1] * self.speed
        self.rect.x = 0 if self.rect.x <= 0 else self.rect.x
        self.rect.right = SCREEN_RECT.right if self.rect.right >= SCREEN_RECT.right else self.rect.right

        self.rect.y += args[2] * self.speed
        self.rect.y = 0 if self.rect.y <= 0 else self.rect.y
        self.rect.bottom = SCREEN_RECT.bottom if self.rect.bottom >= SCREEN_RECT.bottom else self.rect.bottom

    def blowup(self, enemies_group):
        """炸毁所有敌机，返回得到的总分值"""
        # 判断是否能够发起引爆
        if self.bomb_count <= 0 or self.hp <= 0:
            return 0

        # 引爆所有敌机，累计得分
        self.bomb_count -= 1
        score = 0
        for enemy in enemies_group.sprites():
            if enemy.rect.bottom >= 0:
                score += enemy.value  # 增加得分
                enemy.hp = 0  # 爆炸

        return score

    def reset_plane(self):
        """重置英雄飞机"""
        super(HreoPlane, self).reset_plane()

        self.is_power = True  # 无敌
        self.bomb_count = HERO_BOMB_COUNT
        self.bullets_kind = 0  # 子弹

        # 发布时间，让游戏主逻辑更新页面 #pygame.event.Event(HERO_DEAD_EVENT) 封装为对象
        pygame.event.post(pygame.event.Event(HERO_DEAD_EVENT))

        # 发布定时事件，设置三秒无敌时间
        pygame.time.set_timer(HERO_POWER_OFF_EVENT, 3000)

    def fire(self, *display_group):
        """英雄飞机发射一轮新的子弹"""
        # 准备子弹要显示到的组
        groups = (display_group, self.bullets_group)

        # 创建新子弹并定位
        for i in range(3):
            bullet = Bullet(self.bullets_kind, *groups)
            y = self.rect.y - i * 35

            if self.bullets_kind == 0:
                bullet.rect.midbottom = (self.rect.centerx, y)
            else:
                bullet.rect.midbottom = (self.rect.centerx - 20, y)  # bullet
                Bullet(self.bullets_kind, *groups).rect.midbottom = (self.rect.centerx + 20, y)  # bullet2


class EnemyPlane(Plane):
    """敌机类"""

    def __init__(self, max_speed, kind, *group):
        self.kind = kind
        self.max_speed = max_speed
        # 小飞机
        if kind == 0:
            super(EnemyPlane, self).__init__(1, 1, 1000, 'enemy1_down.wav', ['enemy0.png'],
                                             'enemy0.png', ['enemy0_down%d.png' % i for i in range(1, 5)], *group)
        elif kind == 1:
            print("创建中级飞机")
            super(EnemyPlane, self).__init__(6, 1, 6000, 'enemy2_down.wav', ['enemy1.png'],
                                             'enemy1_hit.png', ['enemy1_down%d.png' % i for i in range(1, 5)], *group)
        else:
            print("创建高级飞机")
            super(EnemyPlane, self).__init__(15, 1, 15000, 'enemy3_down.wav',
                                             ['enemy2.png', 'enemy2_n2.png'],
                                             'enemy2_hit.png', ['enemy2_down%d.png' % i for i in range(1, 7)], *group)
        self.reset_plane()  # ==初始化==飞机位置（随机）

    def reset_plane(self):
        """重置敌机"""
        super(EnemyPlane, self).reset_plane()  # 重置飞机基本属性

        # 敌机飞机的数据重置
        x = random.randint(0, SCREEN_RECT.w - self.rect.w)
        y = random.randint(0, SCREEN_RECT.h - self.rect.h) - SCREEN_RECT.h

        self.rect.topleft = (x, y)

        # 设置飞机速度
        self.speed = random.randint(1, self.max_speed)

    def update(self, *args: Any, **kwargs: Any) -> None:
        """更新图像和位置"""

        # 调用父类方法更新飞机图像 - 注意args 需要拆包
        super(EnemyPlane, self).update(*args)

        # 判敌机是否被摧毁，否则需要根据速度更新位置
        if self.hp > 0:
            self.rect.y += self.speed

        # 判断是否飞出屏幕，飞出则需要reset_plane
        if self.rect.y >= SCREEN_RECT.h:
            self.reset_plane()


class Bullet(GameSprite):
    """子弹精灵类"""

    def __init__(self, kind, *group):
        """初始化子弹数据"""
        image_name = "bullet1.png" if kind == 0 else "bullet2.png"
        super(Bullet, self).__init__(image_name, BULLET_SPEED, *group)

        self.damage = 1  # 杀伤力

    def update(self, *args: Any, **kwargs: Any) -> None:
        """更新子弹的数据"""
        super(Bullet, self).update(*args)

        # 判断子弹状态，飞出屏幕之外
        if self.rect.bottom < 0:
            self.kill()  # 杀死


class Supply(GameSprite):
    """道具精灵"""

    def __init__(self, kind, *group):
        # kind = 0为炸弹  kind=1为弹药补给
        image_name = "prop_type_1.png" if kind == 0 else "prop_type_0.png"
        super(Supply, self).__init__(image_name, 5, *group)
        self.wav_name = "get_%s.wav" % ("bomb" if kind == 0 else "bullet")
        self.kind = kind
        self.rect.y = SCREEN_RECT.h  # 初始化在屏幕下面

    def update(self, *args: Any, **kwargs: Any) -> None:
        """修改道具位置"""
        if self.rect.y > SCREEN_RECT.h:  # 如果在屏幕之外，不继续移动
            return
        super(Supply, self).update(*args)

    def throw_supply(self):
        """投放道具"""
        self.rect.bottom = 0  # 移动到窗口顶部
        self.rect.x = random.randint(0, SCREEN_RECT.w - self.rect.w)

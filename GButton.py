"""_author_=王柯栋"""
import pygame


class GButton:
    initBtnColor = ()
    initTextColor = ()

    def __init__(self, button_site, button_text, window):
        GButton.initColor = button_site[4]  # 保存原始btn颜色
        GButton.initTextColor = button_text[2]  # 保存原始text颜色
        # 设置框属性
        self.left, self.top, self.button_width, self.button_height, self.button_rgb \
            = \
            button_site[0], button_site[1], button_site[2], button_site[3], button_site[4]
        # 设置文字属性
        self.text_content, self.text_size, self.text_rgb \
            = \
            button_text[0], button_text[1], button_text[2]
        # creatButton
        self.drawButton(window, self.button_rgb, self.text_rgb)

    def drawButton(self, window, btnColor, textColor):
        # 1、画矩形
        rect = pygame.draw.rect(window, btnColor,
                                (self.left, self.top, self.button_width, self.button_height))
        # 2、文字设置
        font = pygame.font.Font("font/douyuFont-2.otf", self.text_size)
        text = font.render(self.text_content, True, textColor)
        # 3、设置文字居中
        window.blit(text, (rect.left + (rect.width - text.get_width()) / 2,
                           rect.top + (rect.height - text.get_height()) / 2))
        pass

    # 点击按钮效果
    def clickDownButton(self, window):
        self.drawButton(window, (228, 238, 246), (73, 156, 84))

    # 释放按钮效果
    def clickUpButton(self, window):
        self.drawButton(window, self.button_rgb, self.text_rgb)

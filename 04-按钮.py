"""_author_=王柯栋"""

import pygame

from GButton import GButton

WIN_WIDTH = 800
WIN_HEIGHT = 600

pygame.init()
# 设置窗口大小
window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
# 设置标题
pygame.display.set_caption("24K黄金大神")
window.fill((72, 207, 127))  # 填充颜色，将之前背景图片进行覆盖
pygame.display.flip()  # 进行图片展示

# 创建两个矩形框，放置确定与取消
rect_yes_x, rect_yes_y, rect_width, rect_height= 30, 100, 100, 50
rect_yes = pygame.draw.rect(window, (255, 0, 0), (30, 100, 100, 50))
# print(rect_one.bottom)  # 画完的图是有属性的
rect_no = pygame.draw.rect(window, (0, 255, 0), (30, 210, 100, 50))
pygame.display.update()

# 在框中进行文字添加
font_yes = pygame.font.Font("font/douyuFont-2.otf", 30)
text_yes = font_yes.render("确定", True, (43, 43, 43))
print(rect_yes.top)
# 通过进行计算，设置文字居中。
window.blit(text_yes, (rect_yes.left + (rect_yes.width - text_yes.get_width())/2, rect_yes.top + (rect_yes.height - text_yes.get_height())/2))
font_no = pygame.font.Font("font/douyuFont-2.otf", 30)
text_no = font_yes.render("取消", True, (43, 43, 43))
window.blit(text_no, (rect_no.left + (rect_no.width - text_no.get_width())/2, rect_no.top + (rect_no.height - text_no.get_height())/2))
pygame.display.update()

# 测试工具类
new_button = GButton((30, 310, 100, 50, (255, 0, 0)), ("测试", 30, (43, 43, 43)),window)
print(new_button.top)
pygame.display.update()

while True:
    for event in pygame.event.get():
        # 设置退出
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            print(1,new_button.left,x,new_button.left+new_button.button_width)
            if new_button.left <= x <= new_button.left+new_button.button_width and \
                    new_button.top <= y <= new_button.top+new_button.button_height:
                new_button.clickDownButton(window)
                pygame.display.update()
        elif event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            print(1, new_button.left, x, new_button.left + new_button.button_width)
            if new_button.left <= x <= new_button.left + new_button.button_width and \
                    new_button.top <= y <= new_button.top + new_button.button_height:
                new_button.clickUpButton(window)
                pygame.display.update()


pass
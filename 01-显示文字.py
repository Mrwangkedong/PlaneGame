"""_author_=王柯栋"""
import pygame

WIDTH = 800
HEIGHT = 600

pygame.init()
#设置窗口大小
window = pygame.display.set_mode((WIDTH,HEIGHT))
#设置标题
pygame.display.set_caption("24K黄金大神")
#设置背景图片
bacImg = pygame.image.load("img/background/woman.png")
new_bacImg = pygame.transform.scale(bacImg,(WIDTH,HEIGHT))
window.blit(new_bacImg,(0,0))  #进行图片渲染
window.fill((72,207,127)) #填充颜色，将之前背景图片进行覆盖
pygame.display.flip() #进行图片展示
#==================================显示文字================================
# 1、创建字体对象
#Font(字体文件/ttf文件，字号)
font = pygame.font.Font("font/douyuFont-2.otf",30)
# 2、创建文字对象
# render(文字，True，字体颜色，背景颜色)
text = font.render("新澳门",True,(226,236,244),(43,43,43))
# 3、渲染到窗口上
window.blit(text,(0,0))
# 4、进行静态资源更新
pygame.display.update()

# 5、操作文字
# 1)获取大小
w,h = text.get_size()
# 2)进行缩放，选择
#rotozoom(缩放/旋转对象，旋转角度，缩放比例)
new_text = pygame.transform.rotozoom(text,0,1.2)
window.blit(new_text,(120,0))
pygame.display.update()

#设置loop
while True:
    for event in pygame.event.get():
        #设置退出
        if event.type == pygame.QUIT:
            quit()
"""_author_=王柯栋"""
import random

import pygame

GAME_NAME = "24K黄金大神"
WIDTH = 800
HEIGHT = 600

def gameInit():
    # 1.初始化操作
    pygame.init()
    # 2.创建游戏窗口
    # set_mode设置窗口大小
    window = pygame.display.set_mode((800,600))

    # 2.1 设置游戏标题
    pygame.display.set_caption(GAME_NAME)

    # 2.2 设置游戏背景
    bgPhoto = pygame.image.load("img/background/woman.png")
    window.blit(bgPhoto, (0, 0))

    #=============游戏开始页面静态效果=============
    # ①.加载图片
    img1 = pygame.image.load("img/puke/A.jpg")
    # ②.渲染图片
    # bilt(渲染图片，位置/坐标信息)
    window.blit(img1,(0,0))
    # ③.操作图片
    # 1) 获取图片大小
    w,h = img1.get_size()
    # 2) 旋转与缩放
    #scale(缩放对象，目标大小),生成新的图片对象
    new_img1 = pygame.transform.scale(img1,(100,100)) #若比例与之前不同，会发生形变
    window.blit(new_img1,(200,0))
    #rotozoom(缩放/旋转对象，旋转角度，缩放比例)
    new_img2 = pygame.transform.rotozoom(img1,0,1.2)
    window.blit(new_img2, (300, 0))

    #刷新页面，使得更改后的页面
    pygame.display.flip() #--第一次刷新
    pygame.display.update() #--第一次之后的刷新


    # 3.保持游戏运行
    # game loop
    while True:
        # 4.检测事件
        # pygame.event.get()获取当前事件的发生
        for event in pygame.event.get():
            # 设置退出按钮操作[点击关闭按钮]
            if event.type == pygame.QUIT:
                exit()
            pass





if __name__ == '__main__':
    # gameInit()
    for i in range(10):
        print(random.randint(1,2))
    pass
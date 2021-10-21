import pygame, time, math

WIN_WIDTH = 800
WIN_HEIGHT = 600

pygame.init()
# 设置窗口大小
window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
# 设置标题
pygame.display.set_caption("24K黄金大神")
window.fill((72, 207, 127))  # 填充颜色，将之前背景图片进行覆盖
pygame.display.flip()  # 进行图片展示

count = 0  # 同价事件发生的次数
while True:
    # for中的代码只有事件发生的时候才会执行
    for event in pygame.event.get():
        count += 1
        print(count,event.type)
        """
        QUIT   -    点击关闭按钮时间
        
        1、鼠标事件
        MOUSEBUTTONDOWN:鼠标按下（1025）
        MOUSEBUTTONUP：鼠标松开（1026）
        MOUSEMOTION：鼠标移动（1024）
        
        鼠标位置属性   --   pos   --   event.pos
        
        2、键盘事件
        KEYDOWN：键盘按下
        KEYUP：键盘弹起
        
        按键值属性 --  key  ---  event.key  --   AC编码
        chr(event.key) 进行转化，遇到特殊键位会报错 
        """
        # 设置退出
        if event.type == pygame.QUIT:
            quit()
        #  鼠标事件
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("鼠标按下",event.pos)
        elif event.type == pygame.MOUSEMOTION:
            print("鼠标移动")
        elif event.type == pygame.MOUSEBUTTONUP:
            print("鼠标松开")

        if event.type == pygame.KEYDOWN:
            print("键盘按下",event.key)
        if event.type == pygame.KEYUP:
            print("键盘弹起")
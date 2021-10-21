import pygame,time,math

WIN_WIDTH = 800
WIN_HEIGHT = 600

pygame.init()
# 设置窗口大小
window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
# 设置标题
pygame.display.set_caption("24K黄金大神")
window.fill((72, 207, 127))  # 填充颜色，将之前背景图片进行覆盖
pygame.display.flip()  # 进行图片展示
# 1、显示静态球
# draw.circle(window,线颜色，圆心位置，半径，线宽)
circle_y = 100
circle_x = 100
circle_r = 20
pygame.draw.circle(window, (255, 255, 255), (circle_x, circle_y), circle_r, 1)
pygame.display.update()

run_time = 1
run_direction = 1
while True:
    run_time += 1
    # if run_time % 15000 == 0 and circle_y <= WIN_HEIGHT:
    #     #  2、移动动画
    #     circle_y += 1
    #     pygame.draw.circle(window, (72, 207, 127), (circle_x, circle_y - 1), 20, 50)  # 将上一个置为白色，与背景色相同
    #     pygame.draw.circle(window, (255, 255, 255), (circle_x, circle_y), 20, 50)  # 画出新的图形
    #     pygame.display.update()

    # 3、缩放动画
    # if run_time % 15000 == 0 and circle_r <= math.sqrt((WIN_WIDTH/2 * WIN_WIDTH/2)+(WIN_HEIGHT/2 * WIN_HEIGHT/2)):
    #     pygame.draw.circle(window, (72, 207, 127), (circle_x, circle_y), circle_r, 50)  # 将上一个置为白色，与背景色相同
    #     circle_y += 1
    #     circle_x += 1
    #     circle_r += math.sqrt(2)
    #     pygame.draw.circle(window, (255, 255, 255), (circle_x, circle_y), circle_r, 50)  # 画出新的图形
    #     pygame.display.update()

    # 4、上下弹
    if circle_y+circle_r <= WIN_HEIGHT and run_time % 15000 == 0:
        pygame.draw.circle(window, (72, 207, 127), (circle_x, circle_y), 20, 50)  # 将上一个置为白色，与背景色相同
        circle_y += run_direction  # 改变y值
        pygame.draw.circle(window, (255, 255, 255), (circle_x, circle_y), 20, 50)  # 画出新的图形
        pygame.display.update()  # 更新
        if circle_y+circle_r == WIN_HEIGHT or circle_y - circle_r == 0:
            run_direction *= -1   # 改变移动方向


    for event in pygame.event.get():
        # 设置退出
        if event.type == pygame.QUIT:
            quit()

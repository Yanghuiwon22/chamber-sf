import matplotlib.pyplot as plt
import pygame
import os

# Matplotlib로 그래프 생성 및 이미지로 저장
plt.plot([1, 2, 3, 4], [10, 20, 25, 30])
plt.title("Matplotlib Graph")
plt.savefig("graph_matplotlib.png")  # 그래프를 이미지로 저장
plt.close()  # plt 창 닫기

# Pygame 초기화
pygame.init()

# 창 크기 설정
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Matplotlib Graph in Pygame")

# 이미지 불러오기
graph_image = pygame.image.load("graph_matplotlib.png")
graph_image = pygame.transform.scale(graph_image, (width, height))  # 창 크기에 맞춰 이미지 크기 조정

# 루프 변수
running = True

# 메인 루프
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 화면에 이미지 그리기
    screen.blit(graph_image, (0, 0))

    # 화면 업데이트
    pygame.display.flip()

# Pygame 종료
pygame.quit()

# 그래프 이미지 파일 삭제
os.remove("graph_matplotlib.png")

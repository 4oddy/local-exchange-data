import socket
import pygame

pygame.init()

HOST = socket.gethostbyname(socket.gethostname())
PORT = 1255

disp = pygame.display.set_mode((640, 480))
pygame.display.set_caption('game')

clock = pygame.time.Clock()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

usr, addr = server.accept()

running = True

player = pygame.Rect((200, 200), (10, 10))

up = False
down = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                down = True
                up = False
            if event.key == pygame.K_UP:
                up = True
                down = False

    if up:
        player.y -= 1
    if down:
        player.y += 1

    if player.y < 0:
        player.y = 480

    if player.y > 480:
        player.y = 0

    disp.fill((0, 0, 0))

    usr.sendall(f'{player.x},{player.y}'.encode('utf-8'))

    disp.fill((255, 255, 255), player)

    data = usr.recv(1024).decode('utf-8')

    pos_x = int(data.split(',')[0])
    pos_y = int(data.split(',')[1])

    disp.fill((255, 255, 255), ((pos_x, pos_y), (10, 10)))

    pygame.display.flip()
    clock.tick(60)

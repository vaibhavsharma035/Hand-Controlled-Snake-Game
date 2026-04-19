import pygame
import random
import cv2
import mediapipe as mp
import os

# ---------------- WINDOW POSITIONS ----------------
os.environ['SDL_VIDEO_WINDOW_POS'] = "50,100"   # Snake game position

pygame.init()

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hand Controlled Snake")

# Move webcam window later
cv2.namedWindow("Hand Tracking")
cv2.moveWindow("Hand Tracking", 700, 100)

# ---------------- GAME SETTINGS ----------------
clock = pygame.time.Clock()
snake_speed = 5   # CHANGE SPEED HERE

BLOCK = 20

snake = [(300, 200)]
direction = "RIGHT"

food = (
    random.randrange(0, WIDTH, BLOCK),
    random.randrange(0, HEIGHT, BLOCK)
)

# ---------------- CAMERA ----------------
cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

running = True

while running:
    screen.fill((0, 0, 0))

    success, frame = cap.read()
    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:

            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

            x_tip = int(hand.landmark[8].x * 640)
            y_tip = int(hand.landmark[8].y * 480)

            if y_tip < 150:
                direction = "UP"
            elif y_tip > 330:
                direction = "DOWN"
            elif x_tip < 200:
                direction = "LEFT"
            elif x_tip > 440:
                direction = "RIGHT"

    cv2.imshow("Hand Tracking", frame)

    # Snake movement
    x, y = snake[0]

    if direction == "UP":
        y -= BLOCK
    elif direction == "DOWN":
        y += BLOCK
    elif direction == "LEFT":
        x -= BLOCK
    elif direction == "RIGHT":
        x += BLOCK

    head = (x, y)

    if x < 0 or y < 0 or x >= WIDTH or y >= HEIGHT or head in snake:
        running = False

    snake.insert(0, head)

    if head == food:
        food = (
            random.randrange(0, WIDTH, BLOCK),
            random.randrange(0, HEIGHT, BLOCK)
        )
    else:
        snake.pop()

    for s in snake:
        pygame.draw.rect(screen, (0, 255, 0), (*s, BLOCK, BLOCK))

    pygame.draw.rect(screen, (255, 0, 0), (*food, BLOCK, BLOCK))

    pygame.display.update()

    if cv2.waitKey(1) & 0xFF == 27:
        break

    clock.tick(snake_speed)

cap.release()
cv2.destroyAllWindows()
pygame.quit()
import pygame
from pygame.locals import QUIT, KEYUP, KEYDOWN, K_q, K_w, K_s, K_SPACE, KMOD_CTRL
from pygame.key import get_mods
from random import randint, choice
from pong import PyGameObject

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
PADDLE_HORIZONTAL_MARGIN = 15
PADDLE_WIDTH, PADDLE_HEIGHT = 16, 80
PADDLE_VERTICAL_MARGIN = PADDLE_HEIGHT / 2
INITIAL_SPEED = 2.2
FPS = 60
MIN_FLIP_TIME = FPS * 10
FLIP_TIME_CHANGE = int(MIN_FLIP_TIME / 4)
LEFT_PADDLE_COLUMN = PADDLE_HORIZONTAL_MARGIN
RIGHT_PADDLE_COLUMN = SCREEN_WIDTH - PADDLE_HORIZONTAL_MARGIN
TOP_MARGIN = PADDLE_VERTICAL_MARGIN
BOTTOM_MARGIN = SCREEN_HEIGHT - PADDLE_VERTICAL_MARGIN
BALL_RADIUS = 6
ACCELERATION = 1.04

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
time_until_flip = flip_time = FPS * 100
paddle_speed = INITIAL_SPEED
ball_speed = INITIAL_SPEED * ACCELERATION**2

paddle_1 = PyGameObject.newPaddle(PADDLE_WIDTH, PADDLE_HEIGHT)
paddle_1.x = LEFT_PADDLE_COLUMN
paddle_1.y = screen.get_height() / 2
paddle_2 = PyGameObject.newPaddle(PADDLE_WIDTH, PADDLE_HEIGHT)
paddle_2.x = RIGHT_PADDLE_COLUMN
paddle_2.y = screen.get_height() / 2
paddle_2.invertMovement()

ball = PyGameObject.newBall(BALL_RADIUS)
ball.x = screen.get_width() / 2
ball.y = screen.get_height() / 2
ball.changeMovement(pygame.Vector2(0, -3))
ball.movement.scale_to_length(ball_speed)
ball.movement.rotate_ip(randint(0, 360))


def ball_movement_correction():
  if ball.movement.x < 1 and ball.movement.x > -1:
    ball.movement.x *= 1 / abs(ball.movement.x)
    ball.movement.y *= 1 / abs(ball.movement.x)
  elif ball.movement.y < 1 and ball.movement.y > -1:
    ball.movement.y *= 1 / abs(ball.movement.y)
    ball.movement.x *= 1 / abs(ball.movement.y)


ball_movement_correction()

words = ("PING", "PONG")
pygame.display.set_caption(" ".join([choice(words) for _ in range(4)]))

running = True

while running:
  for event in pygame.event.get():
    if event.type == QUIT:
      running = False
      continue
    elif event.type == KEYUP and event.key == K_q:
      if get_mods() & KMOD_CTRL:
        running = False
        continue
    elif event.type == KEYDOWN and event.key in (K_w, K_s, K_SPACE):
      if event.key == K_w:
        paddle_1.changeMovement(pygame.Vector2(0, -1 * paddle_speed))
        paddle_2.changeMovement(pygame.Vector2(0, -1 * paddle_speed))
      elif event.key == K_s:
        paddle_1.changeMovement(pygame.Vector2(0, paddle_speed))
        paddle_2.changeMovement(pygame.Vector2(0, paddle_speed))
      else:
        paddle_1.changeMovement(pygame.Vector2(0, 0))
        paddle_2.changeMovement(pygame.Vector2(0, 0))

  if ball.x <= LEFT_PADDLE_COLUMN or ball.x >= RIGHT_PADDLE_COLUMN:
    running = False
    continue

  for paddle in (paddle_1, paddle_2):
    if paddle.y < TOP_MARGIN:
      paddle.y = TOP_MARGIN
      paddle.changeMovement(pygame.Vector2(0, 0))
    elif paddle.y > BOTTOM_MARGIN:
      paddle.y = BOTTOM_MARGIN
      paddle.changeMovement(pygame.Vector2(0, 0))
    else:
      paddle.move()

  if ball.y <= BALL_RADIUS and ball.movement.y < 0:
    ball.movement.y *= -1
  elif ball.y >= SCREEN_HEIGHT - BALL_RADIUS and ball.movement.y > 0:
    ball.movement.y *= -1
  for paddle in (paddle_1, paddle_2):
    if ball.hitbox.colliderect(paddle.hitbox):
      ball_speed *= ACCELERATION
      paddle_speed *= ACCELERATION
      ball_x, ball_y = ball.hitbox.center
      paddle_x, paddle_y = paddle.hitbox.center
      reboundVector = pygame.Vector2(paddle_x - ball_x,
                                     paddle_y - ball_y).normalize()
      ball.movement.rotate_ip(ball.movement.angle_to(reboundVector) + 180)
      ball.movement.scale_to_length(ball_speed)
      ball_movement_correction()
      if paddle_1.movement.length() > 0:
        paddle_1.movement.scale_to_length(paddle_speed)
      if paddle_2.movement.length() > 0:
        paddle_2.movement.scale_to_length(paddle_speed)
      continue

  ball.move()

  time_until_flip -= 1
  if time_until_flip <= 0:
    paddle_1.invertMovement()
    paddle_2.invertMovement()
    if flip_time <= MIN_FLIP_TIME:
      time_until_flip = flip_time = MIN_FLIP_TIME
    else:
      time_until_flip = flip_time = flip_time - FLIP_TIME_CHANGE

  screen.fill("black")
  pygame.draw.rect(screen, *paddle_1.drawProperties())
  pygame.draw.rect(screen, *paddle_2.drawProperties())
  color, pos, radius = ball.drawProperties()
  pygame.draw.circle(screen, color, (pos.x, pos.y), radius)
  pygame.display.update()

  clock.tick(FPS)

pygame.quit()

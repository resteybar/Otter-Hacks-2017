import turtle
import os
import math
import random
import sys
import pygame
import time

# Set up the Screen
wn = turtle.Screen()

wn.bgcolor("black")
wn.title("Seedvolution")
wn.bgpic("startScreen.gif")

var = input()

wn.bgpic("space_invaders_background.gif")

# Register the Shapes
turtle.register_shape("player.gif")
turtle.register_shape("sprout.gif")
turtle.register_shape("flower.gif")
turtle.register_shape("earth.gif")
turtle.register_shape("pollution.gif")
turtle.register_shape("invader.gif")
turtle.register_shape("sun_enemy.gif")
turtle.register_shape("bomb_enemy.gif")
turtle.register_shape("bullet.gif")

# Draw border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300, -300)
border_pen.pendown()
border_pen.pensize(3)

for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()

score = 0

scorePen = turtle.Turtle()
scorePen.speed(0)
scorePen.color("white")
scorePen.penup()
scorePen.setposition(-290, 280)
scoreString = "Score: {}" .format(score)
scorePen.write(scoreString, False, align = "left", font=("Arial", 14, "normal"))
scorePen.hideturtle()

player = turtle.Turtle()
player.color("blue")
player.shape("player.gif")
player.penup()
player.speed(0)
player.setposition(0, -250)
player.setheading(90)

playerSpeed = 50

##########################
playerisdead = False
#########################
numberEnemies = 5

enemies = []

for i in range(numberEnemies):
    enemies.append(turtle.Turtle())

    for enemy in enemies:
        enemy.color("red")
        enemy.shape("invader.gif")
        enemy.penup()
        enemy.speed(0)
        x = random.randint(-200, 200)
        y = random.randint(100, 250)
        enemy.setposition(x, y)

enemySpeed = 5

##########################
reachedboundary = False
##########################

bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("bullet.gif")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(.5, .5)
bullet.hideturtle()

bulletSpeed = 100

bulletState = "ready"

def move_left():
    x = player.xcor()
    x -= playerSpeed
    if x < -280:
        x = -280
    player.setx(x)

def move_right():
    x = player.xcor()
    x += playerSpeed
    if x > 280:
        x = 280
    player.setx(x)

def fire_bullet():
    global bulletState

    print (bulletState == "ready")
    if (bulletState == "ready"):
        os.system("afplay laser.wav&")
        bulletState = "fire"

        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x, y)
        bullet.showturtle()

def isCollision(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2) + math.pow(t1.ycor()-t2.ycor(),2))

    if distance < 30:
        return True
    else:
        return False

turtle.listen()
turtle.onkey(move_left, "Left")
turtle.onkey(move_right, "Right")
turtle.onkey(fire_bullet, "space")

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()

mixer = pygame.mixer
mixer.music.load("seedvoltionTheme.wav")
mixer.music.play(-1)

while not playerisdead:
    for enemy in enemies:
        x = enemy.xcor()
        x += enemySpeed
        enemy.setx(x)

        ##########################
        if enemy.xcor() > 280:
            for e in enemies:
                y = e.ycor()
                if y > player.ycor():
                    y -= 40
                    e.sety(y)
                else:
                    reachedboundary = True
            enemySpeed *= -1

        if enemy.xcor() < -280:
            for e in enemies:
                y = e.ycor()
                if y > player.ycor():
                    y -= 40
                    e.sety(y)
                else:
                    reachedboundary = True
            enemySpeed *= -1
        ##########################

        if isCollision (bullet, enemy):
            os.system("afplay explosion.wav&")
            bullet.hideturtle()
            bulletState = "ready"
            bullet.setposition(0, -400)
            x = random.randint(-200, 200)
            y = random.randint(100, 250)
            enemy.setposition(x, y)

            score += 10
            scoreString = "Score: {}" .format(score)
            scorePen.clear()
            scorePen.write(scoreString, False, align = "left", font=("Arial", 14, "normal"))

            if(score > 20):
                #enemy.shape("player.gif")
                player.shape("sprout.gif")
                enemy.shape("pollution.gif")
                wn.bgpic("pokemon.gif")
            if(score > 30):
                player.shape("flower.gif")
                enemy.shape("bomb_enemy.gif")
                wn.bgpic("sky.gif")
            if(score > 40):
                player.shape("earth.gif")
                enemy.shape("sun_enemy.gif")
                wn.bgpic("space.gif")

        ##########################
        if isCollision(player, enemy) or reachedboundary:
            player.hideturtle()
            if not reachedboundary:
                enemy.hideturtle()
            print ("Game Over")
            playerisdead = True
            sys.exit()
            break
        ##########################

    if bulletState == "fire":
        y = bullet.ycor()
        y += bulletSpeed
        bullet.sety(y)

    if bullet.ycor() > 275:
        bullet.hideturtle()
        bulletState = "ready"


raw_input("")

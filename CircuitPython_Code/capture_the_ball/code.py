import pykit_explorer
import random
import math
from lcd_display import LCDDisplay
from digital_io import DigitalInput
from imu_sensor import IMUSensor

lcd = LCDDisplay()
btn = DigitalInput(board.D3)
imu = IMUSensor()

#variables
centerX = 100
centerY = 50
radius = 20
game_over = False
score = 0
gamePiece_radius = 4

group, palette = lcd.make_group(0x000000)
gamePiece = lcd.draw_circle(random.randint(200, 230), random.randint(10, 100), gamePiece_radius, fill=0xFFFF00, outline=0xFFFF00)
gameEnemy = lcd.draw_circle(random.randint(10, 40), random.randint(10, 40), gamePiece_radius, fill=0xFF0000, outline=0xFF0000)
circle = lcd.draw_circle(centerX, centerY, radius, fill=0x0000FF, outline=0xFFFFFF)
label = lcd.add_label(group, "", 120, 60, color=0xFF0000)
score_label = lcd.add_label(group, f"Score: {score}", 30, 10, color=0xFFFFFF, scale=1)
group.append(circle)
group.append(gamePiece)
group.append(gameEnemy)

lcd.backlight_on()

def update_circle():
    circle.x = centerX-radius
    circle.y = centerY-radius

def angle_to_position(angleX, angleY):
    cx = 120 + int(angleY * 4)
    cy = 67 - int(angleX * 2)
    return cx, cy
    circle.center = (cx, cy)

def distance(x1, y1, x2, y2):
    return math.sqrt(((x2+gamePiece_radius) - (x1)) ** 2 + ((y2+gamePiece_radius) - (y1)) ** 2)

def capture_game_piece():
    if(distance(centerX, centerY, gamePiece.x, gamePiece.y) <= radius + gamePiece_radius):
        gamePiece.x = random.randint(10, 200)
        gamePiece.y = random.randint(10, 100)
        
        return True
    return False

def capture_game_enemy():
    if(distance(centerX, centerY, gameEnemy.x, gameEnemy.y) <= radius + gamePiece_radius):
        gameEnemy.x = random.randint(50, 190)
        gameEnemy.y = random.randint(20, 100)
        
        return True
    return False


while True:
    if(game_over == False):
        angleX = imu.tilt_angle_x
        angleY = imu.tilt_angle_y
        centerX, centerY = angle_to_position(angleX, angleY)
        circle.fill = 0x0000FF
    update_circle()
    
    if(capture_game_enemy()):
        game_over = True
        label.text = "Game Over"
        label.color = 0xFF0000 
        circle.fill = 0xFF0000
        gameEnemy.x = 500
        gameEnemy.y = 500
        gamePiece.x = 400
        gamePiece.y = 400
    
    if(capture_game_piece()):
        gamePiece.x = random.randint(10, 200)
        gamePiece.y = random.randint(10, 100)
        gameEnemy.x = random.randint(50, 190)
        gameEnemy.y = random.randint(20, 100)
        while(distance(centerX, centerY, gamePiece.x, gamePiece.y) <= radius + gamePiece_radius):
            gamePiece.x = random.randint(10, 200)
            gamePiece.y = random.randint(10, 100)
        while(distance(centerX, centerY, gameEnemy.x, gameEnemy.y) <= radius + gamePiece_radius):
            gameEnemy.x = random.randint(50, 190)
            gameEnemy.y = random.randint(20, 100)   
        circle.fill = 0x00FF00
        score += 1
        score_label.text = f"Score: {score}"
    

    if(centerX + radius > 240 or centerX - radius < -15 or centerY + radius > 130 or centerY - radius < -15):
        circle.fill = 0xFF0000
        game_over = True
        gamePiece.x = 300
        gamePiece.y = 300
        circle.x = 400
        circle.y = 400
        if(label.text != "Place your game flat"):
            label.text = "Game Over"
            label.color = 0xFF0000
    if(btn.is_pressed()):
        if(-10 >imu.tilt_angle_x or imu.tilt_angle_x <10) or (-10 >imu.tilt_angle_y or imu.tilt_angle_y <10):
            game_over = True
            label.text = "Place your game flat"
            label.color = 0xFF0000
            gamePiece.x = 300
            gamePiece.y = 300
            gameEnemy.x = 400
            gameEnemy.y = 400
            centerX = 500
            centerY = 500
        
        gamePiece.x = random.randint(200, 230)
        gamePiece.y = random.randint(10, 100)
        gameEnemy.x = random.randint(10, 40)
        gameEnemy.y = random.randint(20, 100)
        while(distance(gamePiece.x, gamePiece.y, gameEnemy.x, gameEnemy.y) <= radius + gamePiece_radius) and (distance(gamePiece.x, gamePiece.y, gameEnemy.x, gameEnemy.y) <= radius + gamePiece_radius):
            gameEnemy.x = random.randint(50, 190)
            gameEnemy.y = random.randint(20, 100)
        score = 0
        score_label.text = f"Score: {score}"

        if(-10 <imu.tilt_angle_x <10) and (-10 <imu.tilt_angle_y <10):
            circle.fill = 0x0000FF
            game_over = False
            label.text = ""
            circle.center = (120, 67)
        elif(game_over == True):
            label.text = "Place your game flat"
            gamePiece.x = 300
            gamePiece.y = 300
            gameEnemy.x = 400
            gameEnemy.y = 400
            centerX = 500
            centerY = 500

    if score >= 20:
        label.text = "You Win!"
        label.color = 0x00FF00
        game_over = True
        gameEnemy.x = 500
        gameEnemy.y = 500
        gamePiece.x = 300
        gamePiece.y = 300
        circle.x = 400
        circle.y = 400
    time.sleep(0.1)

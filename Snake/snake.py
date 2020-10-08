import sys, pygame, random, os
import threading

# ----- Traer High Scores -----
from io import open

try: #revisa si existe el archivo
    contador = open('highScore.txt', 'r', encoding="utf8")
    contador.close()
except: #Si no existe el archivo lo crea
    contador = open('highScore.txt', 'w+', encoding="utf8")
    contador.write('0')
    contador.close()


# ----- Game instance -----
pygame.init()


# ----- Colores -----
WHITE = 255, 255, 255
BLACK = 0, 0, 0
RED = 255, 0, 0
DARKBLUE = 20, 2, 161


# ----- Clases -----

class Lines:
    def __init__(self, x, y, y2, id):
        self.x = x
        self.y = y
        self.y2 = y2
        self.id = id
        pygame.draw.line(screen, DARKBLUE, (x, y), (x, y2), 10)

class VLines:
    def __init__(self, x, x2, y, id):
        self.x = x
        self.x2 = x2
        self.y = y
        self.id = id
        pygame.draw.line(screen, DARKBLUE, (x, y), (x2, y), 10)

class Snake:
    def __init__(self, x, y, wh):
        self.x = x
        self.y = y
        self.wh = wh


class Coin:
    def __init__(self, x, y, wh):
        self.x = x
        self.y = y
        self.wh = wh

# ----- Variables Globales -----
contador = open('highScore.txt', 'r', encoding="utf8") #abre el archivo en modo lectura
count = int(contador.read())
contador.close() # cierra el archivo

W = 800
H = 1000


HIGHSCORE = count
count = 0

xCOINS = [160, 240, 320, 360, 400, 480, 560, 600, 640, 680, 720, 640, 560, 160, 280]
yCOINS = [160, 240, 320, 360, 400, 480, 560, 600, 640, 680, 720, 640, 560, 760, 800, 840, 920]
COIN_VALUE = 1000

snakeArray = []
coinArray = []

pygame.display.set_caption('Snake')
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()


SNAKE_SIZE = 40
snake_xImpulse = 0
snake_yImpulse = -SNAKE_SIZE

impact = False
gameOver = False
vidas = 3
dir = 'vertical'
index = 0


changed = False
# ----- Instancias -----
header = Snake(W/2, W/2, SNAKE_SIZE)
snakeArray.append(header)






# ----- Funciones -----

def SaveScore():
    global count

    contador = open('highScore.txt', 'w+', encoding="utf8")
    contenido = contador.readlines()
    contenido = []
    if count > HIGHSCORE:
        contador.write(str(count))
    else:
        contador.write((str(HIGHSCORE)))
    count = 0
    contador.close()

def GetHeaderPos():
    snake_head = snakeArray[len(snakeArray) - 1]
    return snake_head

def Limites(derecha, izquierda, arriba, abajo):
    global impact

    if GetHeaderPos().x >= derecha:
        impact = True
    if GetHeaderPos().x <= izquierda:
        impact = True
    if GetHeaderPos().y >= abajo:
        impact = True
    if GetHeaderPos().y <= arriba:
        impact = True


def RandomPoints():
    global coinArray

    xPoint = int(random.randrange(0, len(xCOINS)))
    yPoint = int(random.randrange(0, len(yCOINS)))
    if len(coinArray) < 2:
        coinArray.append(Coin(xCOINS[xPoint], yCOINS[yPoint], SNAKE_SIZE))
    for coin in coinArray:
        pygame.draw.rect(screen, RED, ((coin.x, coin.y, SNAKE_SIZE, SNAKE_SIZE)))

def Movimiento():
    global impact
    global count
    global coinArray
    global snakeArray

    for item in snakeArray:
        pygame.draw.rect(screen, WHITE, ((item.x, item.y, SNAKE_SIZE, SNAKE_SIZE)))
        for aItem in snakeArray:
            if item != aItem:
                if item.x == aItem.x and item.y == aItem.y:
                    impact = True

        for c in coinArray:
            if c.x == item.x and c.y == item.y:
                snakeArray.append(

                    Snake(snakeArray[len(snakeArray) - 1].x + snake_xImpulse, snakeArray[len(snakeArray) - 1].y + snake_yImpulse, SNAKE_SIZE)

                )
                coinArray.remove(c)
                count += COIN_VALUE

    snakeArray.append(

        Snake(snakeArray[len(snakeArray) - 1].x + snake_xImpulse, snakeArray[len(snakeArray) - 1].y + snake_yImpulse, SNAKE_SIZE)

    )
    snakeArray.pop(0)

def LifeControl():
    global gameOver
    global vidas
    global snakeArray
    global impact

    if impact == True:
        vidas -= 1
        snakeArray = []
        snakeArray.append(header)
        if vidas <= 0:
            gameOver = True
        impact = False


def DrawHighScore(x, y):
    font = pygame.font.SysFont('MSGOTHIC.TTF', 36)
    scoreText = 'HIGHSCORE: ' + str(HIGHSCORE)
    img = font.render(scoreText, True, DARKBLUE)
    screen.blit(img, (x, y))

def DrawScore(x, y):
    font = pygame.font.SysFont('MSGOTHIC.TTF', 36)
    scoreText = 'SCORE: ' + str(count)
    img = font.render(scoreText, True, DARKBLUE)
    screen.blit(img, (x, y))

def Line():
    derecha = Lines(778, 100, 978, 'derecha')
    izquierda = Lines(21, derecha.y, derecha.y2, 'izquierda')
    arriba = VLines(derecha.x, izquierda.x, derecha.y, 'arriba')
    abajo = VLines(derecha.x, izquierda.x, derecha.y2, 'abajo')
    Limites(730, 2, 110, 940)


# ----- Escena -----
def Juego():
    global dir
    global snake_xImpulse
    global snake_yImpulse
    global gameOver
    global vidas
    global HIGHSCORE

    vidas = 3
    limiter = 0
    gameOver = False
    while not gameOver:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dir != 'horizontal' and limiter == 0:
                    snake_xImpulse = -SNAKE_SIZE
                    snake_yImpulse = 0
                    dir = 'horizontal'
                    limiter += 1
                elif event.key == pygame.K_RIGHT and dir != 'horizontal' and limiter == 0:
                    snake_xImpulse = SNAKE_SIZE
                    snake_yImpulse = 0
                    dir = 'horizontal'
                    limiter += 1
                if event.key == pygame.K_UP and dir != 'vertical' and limiter == 0:
                    snake_xImpulse = 0
                    snake_yImpulse = -SNAKE_SIZE
                    dir = 'vertical'
                    limiter += 1
                elif event.key == pygame.K_DOWN and dir != 'vertical' and limiter == 0:
                    snake_xImpulse = 0
                    snake_yImpulse = SNAKE_SIZE
                    dir = 'vertical'
                    limiter += 1
        limiter = 0

        Movimiento()
        RandomPoints()
        LifeControl()
        campo = pygame.image.load(os.path.join('recursos/sprites', 'overlay.png')).convert_alpha()
        screen.blit(campo, (0, 0))
        DrawHighScore(W/6, 50)
        DrawScore(W/1.4, 50)
        Line()

        print(GetHeaderPos().x, ' ', GetHeaderPos().y)
        pygame.display.update()
        clock.tick(10)
    if count > HIGHSCORE:
        HIGHSCORE = count
    SaveScore()

def HighScore():
    global changed
    changed = False
    while not changed:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    changed = True

        path = 'score' + '.jpg'
        fondo = pygame.image.load(os.path.join('recursos/sprites', 'scores.jpg')).convert_alpha()
        screen.blit(fondo, (0, 0))
        DrawHighScore(W/2.7, H/2)
        pygame.display.update()



def MainMenu():
    global changed
    global index

    changed = False
    index = 1
    while not changed:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    index = 1
                elif event.key == pygame.K_DOWN:
                    index = 2
                elif event.key == pygame.K_RETURN:
                    changed = True

        index = str(index)
        path = 'fondo' + index + '.jpg'
        fondo = pygame.image.load(os.path.join('recursos/sprites', path)).convert_alpha()
        screen.blit(fondo, (0, 0))
        pygame.display.update()

    pass

def main():
    global index
    index = 1

    MainMenu()
    if int(index) == 1:
        print('xd')
        Juego()
    if int(index) == 2:
        print('xy')
        HighScore()
    main()
# ----- Main Scene -----
if __name__ == '__main__':
    main()

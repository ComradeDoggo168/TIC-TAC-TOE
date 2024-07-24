import pygame
from pygame.locals import *

pygame.init()
wd_w = 1000
wd_h = 800

n = 3
cell_size = 150
mar_x = (wd_w - n * cell_size) / 2
mar_y = 150

col_White = (255, 255, 255)
col_Black = (0, 0, 0)
col_Grey = (188, 188, 188)
col_Orange = (255, 183, 50)
col_P1 = (255, 0, 0)
col_P2 = (0, 0, 255)


current_player = 1
score_p1 = 0
score_p2 = 0
SedangAnnounceWinner = False
winner = None


window = pygame.display.set_mode((wd_w, wd_h))
window.fill(col_White)
clock = pygame.time.Clock()
pygame.display.set_caption('TIC TAC TOE')


font = pygame.font.SysFont("Arial", 38, True)

def input():
    pass


def draw_text(text, font, text_col, flg_HAllign, x, y, col_Back = col_White):
    img = font.render(text, True, text_col, col_Back)
    img_rect = img.get_rect()
    img_w = img_rect.width
    img_h = img_rect.height

    if flg_HAllign == -1:
        tempel_x = x
    elif flg_HAllign == 0:
        tempel_x = x - img_w / 2
    elif flg_HAllign == 1:
        tempel_x = x - img_w

    tempel_y = y

    rect_VisOverwrite = pygame.rect.Rect(tempel_x, tempel_y, img_w, img_h)
    pygame.draw.rect(window, col_Back, rect_VisOverwrite)
    window.blit(img, (tempel_x, tempel_y))


class button():
    def __init__(self, i, j):
        self.xo = 0

        self.cell_c = i
        self.cell_r = j

        self.x = mar_x + i * cell_size
        self.y = mar_y + j * cell_size
        self.w = cell_size
        self.h = cell_size
        self.rect = pygame.rect.Rect(self.x, self.y, cell_size, cell_size)

        self.Redraw()

    def Redraw(self):
        pygame.draw.rect(window, col_White, self.rect)

        pygame.draw.line(window,col_Black, (self.x, self.y), (self.x, self.y + cell_size), 4)
        pygame.draw.line(window,col_Black, (self.x + cell_size, self.y), (self.x + cell_size, self.y + cell_size), 4)

        pygame.draw.line(window,col_Black, (self.x, self.y), (self.x + cell_size, self.y), 4)
        pygame.draw.line(window,col_Black, (self.x, self.y + cell_size), (self.x + cell_size, self.y + cell_size), 4)
        
        if self.xo == 1:
            pygame.draw.line(window, col_P1,  (self.x + 5, self.y + 5),(self.x + cell_size - 10, self.y + cell_size - 10), 5 )
            pygame.draw.line(window, col_P1, (self.x + cell_size - 10, self.y + 5), (self.x + 5, self.y + cell_size - 10), 5 )
        elif self.xo == 2:
            pygame.draw.circle(window, col_P2, (self.x + self.w/2, self.y + self.h/2), (cell_size - 10)/2, 5)
    def ResetButton(self):
        self.xo = 0
        self.Redraw()
    def MarkXO(self, set_xo):
        self.xo = set_xo
        self.Redraw()



def CheckButtonPressed():
    pos_click = pygame.mouse.get_pos()
    for i in range(n):
        for j in range(n):
            if arr[i][j].rect.collidepoint((pos_click)):
                if arr[i][j].xo == 0:
                    return arr[i][j]
    return None


arr = []
for j in range(n):
    row = []
    for i in range(n):
        row.append(button(i, j))
    arr.append(row)


def UpdateTextPlayerScore():
    global current_player

    txt1 = "Player 1 (X) : " + str(score_p1)
    txt2 = str(score_p2) + " : Player 2 (O)"

    if current_player == 1:
        draw_text(txt1, font, col_P1, -1, 0, 30)
        draw_text(txt2, font, col_Grey, 1, wd_w, 30)
    else:
        draw_text(txt1, font, col_Grey, -1, 0, 30)
        draw_text(txt2, font, col_P2, 1, wd_w, 30)

def TogglePlayer():
    global current_player

    if current_player == 2:
        current_player = 1
    else:
        current_player = 2
    UpdateTextPlayerScore()


def CheckAnyWinner(btn_LastPressed):
    c = btn_LastPressed.cell_c
    r = btn_LastPressed.cell_r

    JmlMark = 0
    for j in range(n):
        if arr[j][c].xo == current_player:
            JmlMark += 1
    if JmlMark == n:
        return current_player

    JmlMark = 0
    for i in range(n):
        if arr[r][i].xo == current_player:
            JmlMark += 1
    if JmlMark == n:
        return current_player

    if c == r:
        JmlMark = 0
        for i in range(n):
            if arr[i][i].xo == current_player:
                JmlMark += 1
        if JmlMark == n:
            return current_player

    if c + r == n - 1:
        JmlMark = 0
        for i in range(n):
            if arr[n-1-i][i].xo == current_player:
                JmlMark += 1
        if JmlMark == n:
            return current_player
    return None

def ProcessWinner(winner):
    if winner == 1:
        global score_p1
        score_p1 += 1
        print("Player 1 menang.")
    elif winner == 2:
        global score_p2
        score_p2 += 1
        print("Player 2 menang.")
    UpdateTextPlayerScore()

    pygame.draw.rect(window,col_Orange, (100, 100, wd_w-200, wd_h-200))
    if winner == 1:
        str_Menang = "Player 1 (X) menang."
    else:
        str_Menang = "Player 2 (O) menang."

    draw_text(str_Menang, font, col_Black, 0, wd_w/2, wd_h/2.25, col_Orange)
    draw_text("Click to continue", font, col_Black, 0, wd_w/2, wd_h-350, col_Orange)

def check_draw():
    count = 0
    for i in range(n):
        for j in range(n):
            if arr[i][j].xo != 0:
                count += 1
    if count == n*n:
        return True
    else:
        return False
                

UpdateTextPlayerScore()

win_sfx = pygame.mixer.Sound("win.wav")

run = True   

while run:
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        elif event.type == MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if not SedangAnnounceWinner:
                    btn = CheckButtonPressed()
                    if btn != None:
                        btn.MarkXO(current_player)
                        winner = CheckAnyWinner(btn)
                        if winner != None:
                            ProcessWinner(winner)
                            SedangAnnounceWinner = True
                            win_sfx.play()
                        else:
                            if check_draw():
                                for i in range(n):
                                    for j in range(n):
                                        arr[i][j].xo = 0
                                        arr[i][j].Redraw()
                            else:
                                TogglePlayer()
                else:
                    if winner == 1:
                        current_player = 2
                    elif winner == 2:
                        current_player = 1

                    window.fill(col_White)
                    UpdateTextPlayerScore()
                    for j in range(n):
                        for i in range(n):
                            arr[j][i].xo = 0
                            arr[j][i].Redraw()
                    SedangAnnounceWinner = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()
import os
import sys
import pygame as pg
import random
import time

WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,+5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(+5,0),
    }
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(obj_rct: pg.Rect)  -> tuple[bool,bool] :
    """
    引数:こうかとんRect or 爆弾Rect 
    戻り値:真理値タプル(横判定結果,縦判定結果)（True:画面内/False:画面外）
    Rectオブジェクトのleft, right, top, bottomの値から画面内・外を判断する
    """
    yoko, tate = True,True
    if obj_rct.left < 0 or WIDTH  < obj_rct.right:
        yoko = False
    if obj_rct.top  < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate




def gameover(screen:  pg.display):

    """
    gameover画面を作成し、コウカトンと爆弾が接触したら表示する関数
    """

    cry_kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 5)
    b_rect=pg.Surface((WIDTH, HEIGHT))  #b_rect作成
    pg.draw.rect(b_rect,(0,0,0),(0,0,WIDTH,HEIGHT))  #GAMEOVER時のブラックアウトを作成
    b_rect.set_alpha(200)  #透過設定
    font = pg.font.Font(None, 150)  #フォント取得
    txt = font.render(f"GAME OVER", True, (255, 0, 0))  #文字作成
    screen.blit(b_rect,[0,0])  #作成したb_rectをscreenに貼り付ける
    screen.blit(txt, [400, 300]) #作成した文字をscreenに貼り付ける
    screen.blit(cry_kk_img, [100, 200])  #泣いているコウカトンをscreenに貼り付ける
    pg.display.update()
    time.sleep(5)



def timer(screen: pg.display,timer):

    """
    ゲームの進行時間を計測し表示する関数
    """

    font = pg.font.Font(None, 80)  #フォント取得
    timer = font.render(f"time={timer}", True, (0, 0, 0))  #時間を取得し文字に変換
    screen.blit(timer, [0, 0])  #screenに貼り付ける

def kasoku()  ->tuple[list,list]:
    """
    timeが大きくなるにつれて爆弾の速度と大きさを大きくする関数
    """
    saccs = [a for a in range(1, 11)]
    bomb_imgs=[]
    for r in range(1, 11): 
        bomb_img = pg.Surface((20*r, 20*r))   #加速の計算
        pg.draw.circle(bomb_img, (255, 0, 0), (10*r, 10*r), 10*r)  #拡大の計算
        bomb_img.set_colorkey((0, 0, 0))
        bomb_imgs.append(bomb_img)
    return saccs,bomb_imgs


def main():

    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bomb_accs,bomb_imgs=kasoku()  #kasoku関数呼び出し


    bomb_img = pg.Surface((20,20))   #空のsurface
    pg.draw.circle(bomb_img,(255,0,0),(10,10),10)


    bomb_rct =  bomb_img.get_rect()  #爆弾rectの抽出
    bomb_rct.centerx = random.randint(0,WIDTH)
    bomb_rct.centery = random.randint(0,HEIGHT)
    vx,vy= +5,+5

    bomb_img.set_colorkey((0,0,0))
    clock = pg.time.Clock()
    tmr = 0


    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bomb_rct):  #コウカトンと爆弾が重なっていたら
            gameover(screen)
            return
            
        

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5

        for key,tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[1] +=tpl[1]
                sum_mv[0] +=tpl[0]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        screen.blit(kk_img, kk_rct)

        avx = vx*bomb_accs[min(tmr//500, 9)]
        avy = vy*bomb_accs[min(tmr//500, 9)]

        bomb_rct.move_ip(avx,avy)
        yoko ,tate = check_bound(bomb_rct)
        if not yoko :
            vx *= -1
        if not tate :
            vy *= -1

        bomb_img = bomb_imgs[min(tmr//500, 9)]

        screen.blit(bomb_img, bomb_rct)

        timer(screen,tmr)  #逃げ切っている時間表示

        pg.display.update()
        tmr += 1
        clock.tick(50)



if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

import pygame
from pygame.locals import *
import time
import random

SIZE = 40 #ukuran pixel ular&kodok
panjang = 800
lebar = 720


class makanan_bonus:
    def __init__(self, tampil_layar):
        self.tampil_layar = tampil_layar
        self.gambar_hadiah = pygame.image.load("diamon.png").convert() #import gambar kodok
        self.x = 120
        self.y = 120
        

    def draw(self):
        self.tampil_layar.blit(self.gambar_hadiah, (self.x, self.y)) #gambar letak kodok
        pygame.display.flip() #update display

    def move(self): #random tampil kodok
        self.x = random.randint(1,18)*SIZE # pixel window : ukuran kodok
        self.y = random.randint(1,16)*SIZE

class Kodok:
    def __init__(self, tampil_layar):
        self.tampil_layar = tampil_layar
        self.gambar_kodok = pygame.image.load("kodok2.jpg").convert() #import gambar kodok
        self.x = 120
        self.y = 120
        

    def draw(self):
        self.tampil_layar.blit(self.gambar_kodok, (self.x, self.y)) #gambar letak kodok
        pygame.display.flip() #update display

    def move(self): #random tampil kodok
        self.x = random.randint(1,18)*SIZE # pixel window : ukuran kodok
        self.y = random.randint(1,16)*SIZE

class Ular:
    def __init__(self, tampil_layar):
        self.tampil_layar = tampil_layar
        self.gambar_pala = pygame.image.load("palaular.png").convert() #import gambar ular
        self.gambar_badan = pygame.image.load("badanular.png").convert() #import gambar ular
        self.arah = 'bawah'
        self.score = 0
        self.tambah_waktu = False

        self.length = 1 
        self.x = [40]
        self.y = [40]


    def arah_kiri(self):
        self.arah = 'kiri'

    def arah_kanan(self):
        self.arah = 'kanan'

    def arah_atas(self):
        self.arah = 'atas'

    def arah_bawah(self):
        self.arah = 'bawah'

    def gerak_ular(self):
        # update body
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        # update head
        if self.arah == 'kiri':
            self.x[0] -= SIZE

        if self.arah == 'kanan':
            self.x[0] += SIZE

        if self.arah == 'atas':
            self.y[0] -= SIZE

        if self.arah == 'bawah':
            self.y[0] += SIZE

        self.draw()

    def draw(self):
        for i in range(self.length):
            if ( i == 0 ):
                self.tampil_layar.blit(self.gambar_pala, (self.x[0], self.y[0]))
            
            else :
                self.tampil_layar.blit(self.gambar_badan, (self.x[i], self.y[i]))

        pygame.display.flip()

    def nambah_length(self,score):
        if ( self.length % 10 == 0 and self.length != 0):
            self.tambah_waktu = True
            
        self.score += score
            
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)
  

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("TUBES GAME ULAR")
        
        self.count = 0
        self.layar_utama = pygame.display.set_mode((panjang, lebar)) #ukuran layar
        self.tampil_ular = Ular(self.layar_utama)
        self.tampil_ular.draw()
        self.tampil_kodok = Kodok(self.layar_utama)
        self.tampil_kodok.draw()
        self.tampil_hadiah = makanan_bonus(self.layar_utama)
        self.tampil_hadiah.draw()
        self.waktu = 0.15


    def reset(self):
        self.tampil_ular = Ular(self.layar_utama)
        self.tampil_kodok = Kodok(self.layar_utama)
        self.tampil_hadiah = makanan_bonus(self.layar_utama)

    def makan_kodok(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE: 
                return True
            return False

    def makan_hadiah(self,x1,y1,x2,y2):
        if x1 == x2 and y1 == y2: 
            return True
        else:
            return False

    def tampil_background(self):
        bg = pygame.image.load("background.jpg")
        self.layar_utama.blit(bg, (0,0))

    def play(self):
        self.tampil_background()
        self.tampil_ular.gerak_ular()
       

       #kondisi kemunculan makanan bonus
        if (self.count % 6) == 0 and self.count:
            self.tampil_hadiah.draw()
        else:
            self.tampil_kodok.draw()

        self.tampil_skor()
        pygame.display.flip()
        # print(self.count)

        if self.tampil_ular.x[0] > panjang - 40 or self.tampil_ular.y[0] > lebar - 40 or self.tampil_ular.x[0] < 0 or self.tampil_ular.y[0] < 0:
            raise "Cek Berhasil Nabrak Badan"

        #makan nambah panjang
        if self.makan_kodok(self.tampil_ular.x[0], self.tampil_ular.y[0], self.tampil_kodok.x, self.tampil_kodok.y): #tabrakan dikepala dan kodok
            self.count += 1
            self.tampil_ular.nambah_length(1)
            self.tampil_kodok.move()
            self.tampil_hadiah.move()

            if self.count %6 != 0:
                self.tampil_hadiah.x = (-60)
                self.tampil_hadiah.y = (-60)
            else:
                self.tampil_kodok.x = (-60)
                self.tampil_kodok.y = (-60)
        
        elif self.makan_hadiah(self.tampil_ular.x[0], self.tampil_ular.y[0], self.tampil_hadiah.x, self.tampil_hadiah.y):
            self.count += 1
            self.tampil_ular.nambah_length(5)
            self.tampil_kodok.move()
            

        for i in range(1, self.tampil_ular.length):
            if self.makan_kodok(self.tampil_ular.x[0], self.tampil_ular.y[0], self.tampil_ular.x[i], self.tampil_ular.y[i]):
                raise "Cek Berhasil Nabrak Badan"


    def tampil_skor(self):
        font = pygame.font.SysFont('arial',30)
        skor = font.render(f"Skor: {self.tampil_ular.score}",True,(200,200,200))
        self.layar_utama.blit(skor,(660,10))


    def tampil_gameover(self):
        self.tampil_background()
        font = pygame.font.SysFont('arial', 25)
        ket1 = font.render(f"Permainan Berakhir! Skor mu : {self.tampil_ular.score}", True, (255, 255, 255))
        self.layar_utama.blit(ket1, (100, 300))
        ket2 = font.render("Tekan Enter untuk bermain lagi . Tekan Esc untuk Keluar Game!", True, (255, 255, 255))
        self.layar_utama.blit(ket2, (100, 350))
        pygame.display.flip()

    def run(self):
        running = True
        pause = False


        #keyboard input
        while running:
            for event in pygame.event.get():  #membuat antrian inputan
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pause = False

                    if not pause:
                        if event.key == K_LEFT:
                            self.tampil_ular.arah_kiri()

                        if event.key == K_RIGHT:
                            self.tampil_ular.arah_kanan()

                        if event.key == K_UP:
                            self.tampil_ular.arah_atas()

                        if event.key == K_DOWN:
                            self.tampil_ular.arah_bawah()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()

            except Exception as e:
                self.tampil_gameover()
                pause = True
                self.reset()

            if self.tampil_ular.tambah_waktu :
                self.waktu -= 0.02
                self.tampil_ular.tambah_waktu = False

            time.sleep(self.waktu)

if __name__ == '__main__':
    game = Game()
    game.run()

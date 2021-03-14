import arcade as ar
import random 

WIDTH = 640
HEIGHT = 640
TITLE = 'физика'


# список возможных скоростей
speed_list = [-3,3]
#отвечает за врагов
class Enemy(ar.Sprite):
    def __init__(self,x,y):
        super().__init__(x,y)

        self.scale = 0.5 #размер 
    
        self.texture = ar.load_texture('character_zombie_idle.png')

        self.center_x = x
        self.center_y = y
 
        i = random.randrange(0,1) # выбор скорости
        self.change_x = speed_list[i]

        j = random.randrange(0,1)
        self.change_y = speed_list[j]       

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        # условие ходьбы только по оси Х
        if self.change_x != 0 and random.randint(0,10) < 5:
            self.change_y = 0 

        # условие ходьбы только по оси У
        if self.change_y != 0 and random.randint(0,10) >= 5:
            self.change_x = 0

        # условие смены направления
        if random.randint(0,50) == 0:
            self.change_x = 0
            self.change_y = 0 
            if random.randint(0,1) == 1:
                i = random.randint(0,1) # выбор скорости
                self.change_x = speed_list[i]

            else:
                j = random.randint(0,1) # выбор скорости
                self.change_y = speed_list[j]
   
# основной class
class Mygame(ar.Window):
    # метод(функция) инициализации (создания переменных)
    def __init__(self,w,h,t):
        super().__init__(w,h,t)

        self.player = None #игрок

        self.wall_list = None   #Коробки

        self.coin_list = None  #монетки

        self.enemy_list = None   #враги

        self.Physics_engine = None   #физика

        self.predmet_list = None

        self.coin_sound = ar.Sound("Catch.mp3")   #звук

    # метод установки начальных значений
    def setup(self):
        ar.set_background_color(ar.color.BLUE_SAPPHIRE)  
        #счет
        self.count = 0 
        #переменная жизни 
        self.hp = 3


        self.wall_list = ar.SpriteList()  # присвоение к списку
        self.coin_list = ar.SpriteList()
        self.enemy_list = ar.SpriteList()
        self.predmet_list = ar.SpriteList()
        

       

        self.player = ar.Sprite('igrok.png',0.5)
        self.player.center_x = 300
        self.player.center_y = 300

        coordinate_list = [[100,100],[100,550],[550,100],[550,550], [400,450]]
        #цикл для добавления наших врагов в эти координаты

        for coordinate in coordinate_list:
            enemy = Enemy(coordinate[0], coordinate[1])
            self.enemy_list.append(enemy)
        
        

        # вывод одного блока
        wall = ar.Sprite('platform.png',0.5)
        wall.center_x = 200
        wall.center_y = 200 
        self.wall_list.append(wall)

        for i in range(19): #0,1,2,3,4,5,6...18
            wall = ar.Sprite("platform.png", 0.5)
            wall.center_x = 16
            wall.center_y = 16 + i * 32
            self.wall_list.append(wall)

        # код для вывода большого количества блоков
        # нижняя стенка
        for i in range(19):  # 0,1,2,3,4,5,6,7,8,9
            wall = ar.Sprite('platform.png',0.5)
            wall.center_x = 16 + i * 32   # 32 - размер нашего блока
            wall.center_y = 16
            self.wall_list.append(wall)

        # левая нижняя стенка
        for i in range(9):  # 0,1,2,3,4,5,6,7,8,9
            wall = ar.Sprite('platform.png',0.5)
            wall.center_x = 16    # 32 - размер нашего блока
            wall.center_y = 16 + i * 32  
            self.wall_list.append(wall)

        # левая верхняя стенка
        for i in range(9):  # 0,1,2,3,4,5,6,7,8,9
            wall = ar.Sprite('platform.png',0.5)
            wall.center_x = 16    # 32 - размер нашего блока
            wall.center_y = 368 + i * 32  
            self.wall_list.append(wall)

        # верхняя стенка
        for i in range(19):  # 0,1,2,3,4,5,6,7,8,9
            wall = ar.Sprite('platform.png',0.5)
            wall.center_x = 16 + i * 32   # 32 - размер нашего блока
            wall.center_y = 624
            self.wall_list.append(wall)

        # правая нижняя стенка
        for i in range(9):  # 0,1,2,3,4,5,6,7,8,9
            wall = ar.Sprite('platform.png',0.5)
            wall.center_x = 624    # 32 - размер нашего блока
            wall.center_y = 16 + i * 32  
            self.wall_list.append(wall)

        # правая верхняя стенка
        for i in range(9):  # 0,1,2,3,4,5,6,7,8,9
            wall = ar.Sprite('platform.png',0.5)
            wall.center_x = 624   # 32 - размер нашего блока
            wall.center_y = 368 + i * 32  
            self.wall_list.append(wall)

    # блоки по центру
        # правая  стенка
        for i in range(10):  # 0,1,2,3,4,5,6,7,8,9
            wall = ar.Sprite('platform.png',0.5)
            wall.center_x = 480   # 32 - размер нашего блока
            wall.center_y = 200 + i * 32  
            self.wall_list.append(wall)

        # левая стенка
        for i in range(10):  # 0,1,2,3,4,5,6,7,8,9
            wall = ar.Sprite('platform.png',0.5)
            wall.center_x = 160   # 32 - размер нашего блока
            wall.center_y = 200 + i * 32  
            self.wall_list.append(wall)

        # верхняя стенка
        for i in range(11):  # 0,1,2,3,4,5,6,7,8,9
            wall = ar.Sprite('platform.png',0.5)
            wall.center_x = 160 + i * 32   # 32 - размер нашего блока
            wall.center_y = 520
            self.wall_list.append(wall)

        # нижняя левая стенка
        for i in range(4):  # 0,1,2,3,4,5,6,7,8,9
            wall = ar.Sprite('platform.png',0.5)
            wall.center_x = 160 + i * 32   # 32 - размер нашего блока
            wall.center_y = 200
            self.wall_list.append(wall)

        # нижняя левая стенка
        for i in range(4):  # 0,1,2,3,4,5,6,7,8,9
            wall = ar.Sprite('platform.png',0.5)
            wall.center_x = 380 + i * 32   # 32 - размер нашего блока
            wall.center_y = 200
            self.wall_list.append(wall)
        
        # нижняя левая стенка
        for i in range(4):  # 0,1,2,3,4,5,6,7,8,9
            predmet = ar.Sprite('ghost2.png',0.5)
            predmet.center_x = 380 + i * 32   # 32 - размер нашего блока
            predmet.center_y = 200
            self.predmet_list.append(predmet)

        # вывод монеток
        for i in range(10):  # 0,1,2,3,4,5,6,7,8,9
            for j in range(10): # 0,1,2,3,4,5,6,7,8,9
                coin = ar.Sprite('gold_1.png',0.15)
                coin.center_x = 48 + i * 64   # 32 - размер нашего блока
                coin.center_y = 48 + j * 64
                self.coin_list.append(coin)
        
        
    
        
        
        

        # Задание: вывести на экран симмитрично правую стенку и верхнюю

        self.Physics_engine = ar.PhysicsEngineSimple(self.player,self.wall_list)


        # Задание: 
        # 1) создать переменную для врагов self.enemy_list = None (в def init)
        # 2) присваиваем переменную к списку self.enemy_list = ar.SpriteList() (в def setup)
        # 3) создаем список координат врагов coordinate_list = [[100,100],[100,550],[550,100]] (в def setup)
        # 4) создаем врагов 
        # for coordinate in coordinate_list:
        #     enemy = Enemy(coordinate[0], coordinate[1])
        #     self.enemy_list.append(enemy)
        # 5)записываем код зарисовки self.enemy_list.draw() (в def on_draw) запускаем
        # 6)записываем код обновления self.enemy_list.update() (в def update)
        
        
    # метод зарисовки
    def on_draw(self):
        ar.start_render()

        fon = ar.load_texture("background.jpg")
        ar.draw_texture_rectangle(WIDTH/2, HEIGHT/2, WIDTH, HEIGHT, fon)

        self.player.draw()
        self.wall_list.draw()
        self.coin_list.draw()
        self.enemy_list.draw()
        self.predmet_list.draw()

        ar.draw_text(f"cчет: {self.count}", 50, 550, ar.color.BLACK, 18)
        ar.draw_text(f"жизнь: {self.hp}", 50, 500, ar.color.BLACK, 18)

        #условие проигрыша 
        if self.hp <= 0:
            ar.draw_text(f"YOU LOSE", 250, 300, ar.color.BLACK, 18)

        #условие выигрыша
        if self.count >= 36:
            ar.draw_text(f"Ты выиграл", 250, 300, ar.color.BLACK, 18)


    # метод обновления внутри игры
    def update(self,delta_time):
        if self.hp <=0:
            return
        
        self.Physics_engine.update()
        self.enemy_list.update()
       

        for coin in self.coin_list:
            # условие соприкосновения монеток с блоками
            if ar.check_for_collision_with_list(coin,self.wall_list):
                coin.remove_from_sprite_lists()

            # условие сбора монеток
            if ar.check_for_collision(coin,self.player):
                coin.remove_from_sprite_lists()
                self.count +=1 
                self.coin_sound.play(0.005)
        for predmet in self.predmet_list:
            # условие соприкосновения монеток с блоками
            if ar.check_for_collision(predmet,self.player):
                predmet.remove_from_sprite_lists()
                self.hp -=3
                self.coin_sound.play(0.005)
            

           

        for enemy in self.enemy_list:
            #условие соприкосновение врага с коробками 
            if ar.check_for_collision_with_list(enemy,self.wall_list):
                if enemy.change_x > 0: 
                    enemy.change_x =  speed_list[0]  # -3
                elif enemy.change_x < 0:
                    enemy.change_x = speed_list[1]  # 3

                if enemy.change_y > 0: 
                    enemy.change_y = speed_list[0]
                elif enemy.change_y < 0:
                    enemy.change_y = speed_list[1]
             
            #условие соприкосновения игрока и врагов

            if ar.check_for_collision(enemy, self.player):

                self.hp -=1
                self.player.center_x = 300
                self.player.center_y = 300
       
                

    # метод управления клавиатурой
    def on_key_press(self,key,modifiers):
        # условие нажатия
        if key == ar.key.W:
            self.player.change_y = 5
        if key == ar.key.S:
            self.player.change_y = -5
        if key == ar.key.A:
            self.player.change_x = -5
        if key == ar.key.D:
            self.player.change_x = 5
        if key == ar.key.SPACE and self.hp <=0:
            self.setup()
           


    # метод для остановки игрока если нет нажатия
    def on_key_release(self,key,modifiers):
        # условие нажатия
        if key == ar.key.W:
            self.player.change_y = 0
        if key == ar.key.S:
            self.player.change_y = 0
        if key == ar.key.A:
            self.player.change_x = 0
        if key == ar.key.D:
            self.player.change_x = 0
     
# основная функция
def main():
    # присвоение к переменной основнго класса
    window = Mygame(WIDTH,HEIGHT,TITLE)
    window.setup()
    window.WINDOW_STYLE_DIALOG
    ar.run()

# вызов функции
main()

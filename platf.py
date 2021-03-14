import arcade as ar
import random

WIDTH = 640
HEIGHT = 640
TITLE = 'физика'

map_scale = 0.8  # масштаб карты

GRAVITY = 0.5  # гравитация
UPDATES_PER_SECOND = 4 # обновление анимации 

RIGHT_FACING = 0  # переменная поворота лица вправо
LEFT_FACING = 1 # переменная поворота лица влево
def load_texture_pair(filename):
    return[
        ar.load_texture(filename),
        ar.load_texture(filename,mirrored=True)
    ]
# класс player
class Player(ar.Sprite):
    def __init__(self):
        super().__init__()

        self.scale = 0.5  # масштаб

        self.cur_texture = 0  # начальная текстуры ходьбы

        # основной путь к изображениям
        main_path  = "module 6/images/male_person/character_maleAdventurer" # _idle.png

        self.stand_texture_pair = load_texture_pair(f'{main_path}_idle.png') # стоячая текстура
        self.jump_texture_pair = load_texture_pair(f'{main_path}_jump.png') #текстура, когда он прыгает
        self.fall_texture_pair = load_texture_pair(f'{main_path}_fall.png') #текстура, когда он падает
        
        self.direction = RIGHT_FACING  # направление игрока вправо
        #специальный алгоритм для загрузки изображений для ходьбы нашего главного героя
        #список текстур ходьбы для того чтобы хранить в нем все изображения
        self.walk_textures = []
        #загрузка изображения
        for i in range(8): #0,1,2,3,..7
            texture = load_texture_pair(f'{main_path}_walk{i}.png')
            self.walk_textures.append(texture)
        
        #установка первого изображения
        self.texture = self.stand_texture_pair[self.direction]

    def update_animation(self,delta_time = 1/60):

        # условие смены направления изображения
        if self.change_x < 0 and self.direction == RIGHT_FACING:  # движение вправо
            self.direction = LEFT_FACING

        # условие смены направления изображения
        if self.change_x > 0 and self.direction == LEFT_FACING:  # движение влево
            self.direction = RIGHT_FACING
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.stand_texture_pair[self.direction]
            return

       #условие смены изображения при прыжке
        if self.change_y > 0:
           self.texture = self.jump_texture_pair[self.direction]

        #условие смены изображения при падении

        if  self.change_y < 0:
           self.texture = self.fall_texture_pair[self.direction]

       #алгоритм для загрузки всех изображений 
        self.cur_texture +=1
        if self.cur_texture > 7*UPDATES_PER_SECOND:
            self.cur_texture = 0

        self.texture = self.walk_textures[self.cur_texture//UPDATES_PER_SECOND][self.direction]
class Mygame(ar.Window):
    # метод(функция) инициализации (создания переменных)
    def __init__(self,w,h,t):
        super().__init__(w,h,t)

        self.coin_list = None

        self.wall_list = None
        self.all_wall_list = None
        self.ground_list = None
        self.broken_walls_list = None  
        self.enemy_list = None
        self.collision_list = None

        self.player = None

        self.Physics_engine = None
      

        self.view_left = 0
        self.view_bottom = 0 
        

    # метод установки начальных значений
    def setup(self):
        ar.set_background_color(ar.color.BLUE_SAPPHIRE)  

        self.wall_list = ar.SpriteList()
        self.coin_list = ar.SpriteList()
        self.all_wall_list = ar.SpriteList()
        self.ground_list = ar.SpriteList()
        self.broken_walls_list = ar.SpriteList()
        self.enemy_list = ar.SpriteList()
        self.collision_list = ar.SpriteList()

        # чтение карты  и  присвоение карты
        # 1) присвоение слоев в переменной
        # 2) присвоение слоев к списку 

        my_map = ar.tilemap.read_tmx('module 6/maps/map_10.tmx')

        coins_layer_name = 'coins'
        walls_layer_name = 'walls'
        broken_walls_layer_name = 'broken_walls'

        self.coin_list = ar.tilemap.process_layer(my_map,coins_layer_name, map_scale)  
        self.wall_list = ar.tilemap.process_layer(my_map,walls_layer_name, map_scale)
        self.broken_walls_list = ar.tilemap.process_layer(my_map,broken_walls_layer_name, map_scale)

        self.enemy_list = ar.tilemap.process_layer(my_map,'enemy',map_scale)
        self.collision_list = ar.tilemap.process_layer(my_map,'collision_blocks',map_scale)

        # создание скорости для врагов
        for enemy in self.enemy_list:
            enemy.change_x = random.randrange(-3,3,2)
      

        # добавление в общий список блоков
        for wall in self.wall_list:
            self.all_wall_list.append(wall)
       
        # добавление в общий список блоков
        for wall in self.broken_walls_list:
            self.all_wall_list.append(wall)

        #создание игрока
        self.player = Player()
        self.player.center_x = 300
        self.player.center_y = 300

        # добавление физики для всех блоков
        self.Physics_engine = ar.PhysicsEnginePlatformer(self.player, self.all_wall_list, GRAVITY)

    # метод зарисовки
    def on_draw(self):
        ar.start_render()
        self.coin_list.draw()
        self.all_wall_list.draw()
        self.enemy_list.draw()
        
        self.collision_list.draw()

        self.player.draw()        

    # метод обновления внутри игры
    def update(self,delta_time):
        self.Physics_engine.update()
        self.enemy_list.update_animation()
        self.enemy_list.update()
        self.player.update_animation()

        # код для отскока
        for enemy in self.enemy_list:
            # учет соприкосновения
            if ar.check_for_collision_with_list(enemy,self.collision_list):
                # код выполнения отскока
                enemy.change_x *= -1

        # команда для передвижения экрана
        if True:
            # движение экрана с игроком
            ar.set_viewport(self.view_left,WIDTH + self.view_left,self.view_bottom ,HEIGHT +self.view_bottom)

            # движение экрана влево
            left_boundary = self.view_left + 200        
            if self.player.left < left_boundary:
                # if self.player.left > 200:  # условие остановки передвижения экрана
                    self.view_left -= left_boundary - self.player.left

            # движение экрана вправо
            right_boundary = self.view_left + WIDTH - 200
            if self.player.right > right_boundary:
                # if self.player.right < 984: # условие остановки передвижения экрана
                    self.view_left += self.player.right - right_boundary

            # движение экрана влево
            bottom_boundary = self.view_bottom + 100    
            if self.player.bottom < bottom_boundary:
                # if self.player.left > 200:  # условие остановки передвижения экрана
                    self.view_bottom -= bottom_boundary - self.player.bottom

            # движение экрана вправо
            top_boundary = self.view_bottom + HEIGHT - 200
            if self.player.top > top_boundary:
                # if self.player.right < 984: # условие остановки передвижения экрана
                    self.view_bottom += self.player.top - top_boundary


    # метод управления клавиатурой
    def on_key_press(self,key,modifiers):
        if key == ar.key.LEFT:
            self.player.change_x = -5    # ctrl + H       для быстрой смены слова
        elif key == ar.key.RIGHT:
            self.player.change_x = 5
        if key == ar.key.UP:
            if self.Physics_engine.can_jump():
                self.player.change_y = 13           

    # метод для остановки игрока если нет нажатия
    def on_key_release(self,key,modifiers):
        if key == ar.key.LEFT:
            self.player.change_x = 0
        elif key == ar.key.RIGHT:
            self.player.change_x = 0

     
# основная функция
def main():
    # присвоение к переменной основнго класса
    window = Mygame(WIDTH,HEIGHT,TITLE)
    window.setup()
    ar.run()

# вызов функции
main()

import pygame,random

pygame.init()

screen = pygame.display.set_mode((800,800))

pygame.display.set_caption("Maze")

cell_size = 20

class Cell:
    cell_size = 20
    def __init__(self,x,y,row,col):
        self.row = row
        self.col = col
        self.x = x
        self.y = y
        self.surface = pygame.Surface((self.cell_size,self.cell_size))
        self.rect = self.surface.get_rect(topleft=(x,y))
        self.has_north_edge =  self.has_east_edge = True


    def draw(self):

        pygame.draw.rect(screen,(0,0,0),self.rect,1)
        if not self.has_north_edge:
            pygame.draw.line(screen,(255,255,255),(self.x + self.cell_size,self.y),(self.x + self.cell_size,self.y + self.cell_size),10)
        elif not self.has_east_edge:
            pygame.draw.line(screen,(255,255,255),(self.x,self.y),(self.x + self.cell_size,self.y),10)



class Wall(pygame.sprite.Sprite):

    def __init__(self,x,y,width,height):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.Surface([width,height])
        self.rect = self.image.get_rect(topleft=(x,y))
    

class Player(pygame.sprite.Sprite):

    def __init__(self,x,y,size,walls):
        super().__init__()

        self.image =pygame.Surface((size,size))
        self.walls = walls
        self.rect = self.image.get_rect(topleft=(x,y))
        self.speed = 2
        self.moving_vertical = False
        self.moving_horizontal = False
        
    
    def draw(self):
        pygame.draw.rect(screen,(255,0,0),self.rect)
    
    def change_speed(self,x,y):
        self.x_speed = x
        self.y_speed = y
    def update(self,pressed_keys):
        
        number = 0
        previous_x,previous_y = self.rect.x,self.rect.y 
        moving_horizontal = False
        if pressed_keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            number =1 
            moving_horizontal = True
        if pressed_keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            number = 2
            moving_horizontal = True
        

        if not moving_horizontal:
            if pressed_keys[pygame.K_UP]:
                self.rect.y -= self.speed
                number = 3
            if pressed_keys[pygame.K_DOWN]:
                self.rect.y += self.speed
                number = 4
        

        if self.rect.right > 800:
            self.rect.right = 800

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.bottom > 800:
            self.rect.bottom = 800

        if self.rect.top < 0:
            self.rect.top = 0

        block_hit_list = pygame.sprite.spritecollide(self,self.walls,False)

        for block in block_hit_list:
            if number == 1:
                self.rect.right = block.rect.left
            elif number ==2:
                self.rect.left = block.rect.right
            elif number ==3:
                self.rect.top = block.rect.bottom
            elif number == 4:
                self.rect.bottom = block.rect.top
        

rows = cols = 40


def binary_tree():
    '''binary tree'''
    walls = pygame.sprite.Group()
    for col in range(cols - 1,-1,-1):
        for row in range(rows):
            print(row,col)
            if row == 0:
                walls.add(Wall(col * cell_size,row * cell_size,cell_size,1))
            elif col == cols - 1:
                walls.add(Wall(col * cell_size + cell_size,row * cell_size,1,cell_size))
            elif row != 0:
                number = random.randint(1,2)
                if number == 1:
                    walls.add(Wall(col * cell_size,row * cell_size,cell_size,1))
                else:
                    walls.add(Wall(col * cell_size + cell_size,row * cell_size,1,cell_size))

    return walls

def side_winder():
    walls = pygame.sprite.Group()

    for row in range(rows - 1,-1,-1):
        current_run = []
        if row == 0:
            continue
        for col in range(cols):
            current_run.append(Wall(col * cell_size,row * cell_size,cell_size,1))
            number = random.randint(1,2)
            if number ==1 or col == cols - 1:
                wall = random.choice(current_run)
                current_run.remove(wall)
                for wall in current_run:
                    walls.add(wall)
                current_run = []
                walls.add(Wall(col * cell_size + cell_size,row * cell_size,1,cell_size))

    
    return walls

walls = side_winder()

player = Player(0,0,5,walls)

done = False
clock = pygame.time.Clock()


goal_row,goal_col = 20,cols -1


while done == False:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.change_speed(-2,0)
            
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
        
    
    screen.fill((255,255,255))
    walls.draw(screen)
    player.draw()
    pygame.draw.line(screen,(0,255,0),(goal_row * cell_size,goal_col * cell_size),(goal_row *cell_size + cell_size,goal_col * cell_size + cell_size),2)
    pygame.draw.line(screen,(0,255,0),(goal_row * cell_size + cell_size,goal_col * cell_size),(goal_row *cell_size,goal_col * cell_size + cell_size),2)
    pygame.display.update()
    clock.tick(60)

    





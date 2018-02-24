# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600

SHIP_ANGULAR_VEL = 0.1
SHIP_LINEAR_ACC = 0.1
FRICTION = 0.01
score = 0
lives = 0
time = 0
started = False 

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

# Resolve Collision of two groups of objects
def group_group_collide(group1, group2):
    collisions = 0
    for sprite in set(group1):
        if group_collide(sprite, group2):
            group1.remove(sprite)
            collisions += 1
    return collisions
        

# Resolve Collision of an object and a groups of objects
def group_collide(sprite, group):
        collision_found = False
        items_to_remove = set([])
        for sp in group:
            if (sp.collide(sprite)):
                items_to_remove.add(sp)
                explosion_group.add(Sprite(sp.get_position(), [0,0], 0, 0, explosion_image, explosion_info))
                collision_found = True
        group.difference_update(items_to_remove)
        return collision_found

# Create a random float such that: float >= lower and float < upper
def random_float(lower, upper):
    import random

    range_width = upper - lower
    return random.random() * range_width + lower

# helper functions for controls
def rotate_anticlockwise():
    my_ship.set_angle_vel(-SHIP_ANGULAR_VEL)
    
def rotate_clockwise():
    my_ship.set_angle_vel(SHIP_ANGULAR_VEL)
    
def move_forward():
    my_ship.set_thrust(True)
    my_ship.set_linear_acc(SHIP_LINEAR_ACC)
    ship_thrust_sound.play()
    
def move_backward():
    pass

def stop_rotation():
    my_ship.set_angle_vel(0)
    
def stop_linear_motion():
    my_ship.set_thrust(False)
    my_ship.set_linear_acc(0)
    ship_thrust_sound.rewind()

#Helper to draw and update group of rocks 
def process_sprite_group(canvas, sprite_group):
    for sprite in set(sprite_group):
        sprite.draw(canvas)
        if sprite.update():
            sprite_group.remove(sprite)
    
# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.linear_acc = 0
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_center_thrust_on = (self.image_center[0] * 3, self.image_center[1])
        self.image_size = info.get_size()
        self.radius = info.get_radius()
    
    def set_angle_vel(self, angle_vel):
        self.angle_vel = angle_vel
        
    def set_linear_acc(self, linear_acc):
        self.linear_acc = float(linear_acc)
        
    def set_thrust(self, thrust):
        self.thrust = thrust
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
        
    def shoot(self):
        global missile_group
        const = 3
        ship_cannon = 45
        direction = angle_to_vector(self.angle)
        vel = [self.vel[0] + (direction[0] * const),
              self.vel[1] + (direction[1] * const)]
        pos = [self.pos[0] + (direction[0] * ship_cannon),
               self.pos[1] + (direction[1] * ship_cannon)]
        missile_group.add(Sprite(pos, vel, 0, 0, missile_image, missile_info, missile_sound))

    def draw(self,canvas):
        self.pos[0] %= WIDTH
        self.pos[1] %= HEIGHT
        if self.thrust:            
            canvas.draw_image(self.image, self.image_center_thrust_on, self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        self.angle += self.angle_vel
        
        direction = angle_to_vector(self.angle)
        self.vel[0] += (direction[0] * self.linear_acc) - (FRICTION * self.vel[0])
        self.vel[1] += (direction[1] * self.linear_acc) - (FRICTION * self.vel[1])
        self.pos = [self.pos[0] + self.vel[0], self.pos[1] + self.vel[1]]
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
            
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
   
    def draw(self, canvas):
        if (self.animated):
            i_center = [self.image_center[0] + (self.image_size[0] * self.age),
                      self.image_center[1]]
            canvas.draw_image(self.image, i_center, self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        self.age += 1
        self.angle += self.angle_vel
        self.pos[0] %= WIDTH
        self.pos[1] %= HEIGHT
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        if (self.age >= self.lifespan):
            return True
        else:
            return False
    
    def collide(self, other_object):
        radius_sum = self.radius + other_object.get_radius()
        distance = dist(self.pos, other_object.get_position())
        if (distance > radius_sum):
            return False
        else:
            return True
        
    
def draw(canvas):
    global time, lives, score, started, rock_group, missile_group, explosion_group
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship
    my_ship.draw(canvas)
    
    # update ship
    my_ship.update()
    
    #Draw lives
    canvas.draw_text('Lives: ' + str(lives), (20, 20), 24, 'White')
    
    #Draw score
    canvas.draw_text('Score: ' + str(score), (WIDTH - 100, 20), 24, 'White')
    
    if (started == True and lives > 0):
        #Draw and update the rocks and missiles
        process_sprite_group(canvas, rock_group)
        process_sprite_group(canvas, missile_group)   
        process_sprite_group(canvas, explosion_group)   

        if group_collide(my_ship, rock_group):
            lives += -1

        #Resolve collisions of missiles and rocks   
        score += group_group_collide(missile_group, rock_group)
    else:
        started = False
        missile_group = set([])
        rock_group = set([])
        explosion_group = set([])
        
        #Draw splash screen
        if not started:
            canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), (WIDTH / 2, HEIGHT / 2), splash_info.get_size())


# Controls handler
def keydown_handler(key):
    for control in KEYDOWN_CONTROLS:
        if simplegui.KEY_MAP[control] == key:
            KEYDOWN_CONTROLS[control]()

def keyup_handler(key):
    for control in KEYUP_CONTROLS:
        if simplegui.KEY_MAP[control] == key:
            KEYUP_CONTROLS[control]()
            
def mouse_handler(position):
    global started, lives
    if not started:
        lives = 3
        started = True
        soundtrack.rewind()
        soundtrack.play()
            
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group, my_ship
    
    #square area in which rocks should not be spawned
    ship_pos = my_ship.get_position()
    boundary_left = ship_pos[0] - 90
    boundary_right = ship_pos[0] + 90
    boundary_top = ship_pos[1] - 90
    boundary_bottom = ship_pos[1] + 90
    
    if len(rock_group) < 12:
        pos = (random.randrange(WIDTH), random.randrange(HEIGHT))
        vel = (random_float(-1, 1), random_float(-1, 1))
        angle_vel = random_float(0.03, 0.1)
        
        if (not (boundary_left < pos[0] < boundary_right and
            boundary_top < pos[1] < boundary_bottom)):
            rock_group.add(Sprite(pos, vel, 0, angle_vel, asteroid_image, asteroid_info))
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

missile_group = set([])
rock_group = set([])
explosion_group = set([])

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown_handler)
frame.set_keyup_handler(keyup_handler)
frame.set_mouseclick_handler(mouse_handler)

timer = simplegui.create_timer(1000, rock_spawner)

# get things rolling
timer.start()
frame.start()

#Control Keys    
KEYDOWN_CONTROLS = {
    "left" : rotate_anticlockwise,
    "right" : rotate_clockwise,
    "up" : move_forward,
    "down": move_backward,
    "space": my_ship.shoot
}

KEYUP_CONTROLS = {
    "left" : stop_rotation,
    "right" : stop_rotation,
    "up" : stop_linear_motion,
    "down": stop_linear_motion
}

from drawable import Drawable
from collisionbody import CollisionBody, CollisionSide
import pygame
from pygame import Vector2, Color, Rect
from drawable import Drawable
from tilemap import Tilemap
from renderrect import RenderRect
from frect import FRect
from sprite import Sprite
import engine as engine
from enum import Enum, auto
from utils import clamp, frange
from animation import Animation
from copy import copy
from fireball import Fireball

TERMINAL_FALL_SPEED = 6
TERMINAL_WALK_SPEED = 2.4
TERMINAL_RUN_SPEED = 4.4
GRAVITY = 0.5
WALK_SPEED = 0.40
RUN_SPEED = 0.40
DEACCEL = 0.1
COYOTE_TIME_MAX = 4
JUMP_POWER = 2.6
RETURN_FRAME_PERCENT = 300
RUN_FPS = 40
RUN_MAX_FPS_TICKS = 750
AIR_DEACCEL_PERCENT = 1
AIR_SPEED_PERCENT = 1
INVINCIBILITY_FRAMES_MAX = 100
RUN_RESET_TICKS = 2500
FIREBALL_COOLDOWN_TICKS = 150


class PowerupState(Enum):
    Small = 0,
    Normal = 1,
    Fire = 2

class MarioState(Enum):
    Null = auto(),
    Idle = auto(),
    Walking = auto(),
    Running = auto(),
    Jumping = auto(),
    Falling = auto(),
    Returning = auto(),
    PoweringUp = auto(),
    PoweringDown = auto(),
    Crouching = auto()

ANIMATIONS = {
    PowerupState.Small: {
        MarioState.Idle: Animation([FRect(1, 1, 16, 16)], 1),
        MarioState.Walking: Animation([FRect(18, 1, 16, 16), FRect(35, 1, 16, 16), FRect(52, 1, 16, 16), FRect(18, 1, 16, 16)], 20),
        MarioState.Returning:  Animation([FRect(69, 1, 16, 16)], 1),
        MarioState.Running: Animation([FRect(18, 1, 16, 16), FRect(35, 1, 16, 16), FRect(52, 1, 16, 16), FRect(18, 1, 16, 16)], RUN_FPS),
        MarioState.Falling: Animation([FRect(35, 1, 16, 16)], 1),
        MarioState.Jumping: Animation([FRect(86, 1, 16, 16)], 1),
        MarioState.PoweringUp: Animation([FRect(137, 18, 16, 32), FRect(120, 18, 16, 32), FRect(137, 18, 16, 32), FRect(120, 18, 16, 32), FRect(137, 18, 16, 32), FRect(120, 18, 16, 32), FRect(137, 18, 16, 32), FRect(1, 18, 16, 32), FRect(137, 18, 16, 32), FRect(1, 18, 16, 32)], 11)
    },
    PowerupState.Normal: {
        MarioState.Idle: Animation([FRect(1, 18, 16, 32)], 1),
        MarioState.Walking: Animation([FRect(18, 18, 16, 32), FRect(35, 18, 16, 32), FRect(52, 18, 16, 32), FRect(18, 18, 16, 32)], 20),
        MarioState.Returning: Animation([FRect(69, 18, 16, 32)], 1),
        MarioState.Running: Animation([FRect(18, 18, 16, 32), FRect(35, 18, 16, 32), FRect(52, 18, 16, 32), FRect(18, 18, 16, 32)], RUN_FPS),
        MarioState.Falling: Animation([FRect(35, 18, 16, 32)], 1),
        MarioState.Jumping: Animation([FRect(86, 18, 16, 32)], 1),
        MarioState.PoweringDown: Animation([FRect(86, 18, 16, 32), FRect(154, 18, 16, 32), FRect(86, 18, 16, 32), FRect(154, 18, 16, 32), FRect(86, 18, 16, 32), FRect(154, 18, 16, 32), FRect(86, 18, 16, 32), FRect(154, 18, 16, 32), FRect(188, 18, 16, 32), FRect(154, 18, 16, 32), FRect(171, 18, 16, 32), FRect(154, 18, 16, 32), FRect(171, 18, 16, 32), FRect(154, 18, 16, 32), FRect(188, 18, 16, 32), FRect(188, 18, 16, 32), FRect(188, 18, 16, 32), FRect(188, 18, 16, 32), FRect(188, 18, 16, 32)], 15),
        MarioState.PoweringUp: Animation([FRect(324, 18, 16, 32), FRect(341, 18, 16, 32), FRect(358, 18, 16, 32), FRect(1, 18, 16, 32), FRect(324, 18, 16, 32), FRect(341, 18, 16, 32), FRect(358, 18, 16, 32), FRect(1, 18, 16, 32), FRect(324, 18, 16, 32), FRect(341, 18, 16, 32)], 11),
        MarioState.Crouching: Animation([FRect(103, 18, 16, 32)], 1)
    },
    PowerupState.Fire: {
        MarioState.Idle: Animation([FRect(1, 51, 16, 32)], 1),
        MarioState.Walking: Animation([FRect(18, 51, 16, 32), FRect(35, 51, 16, 32), FRect(52, 51, 16, 32), FRect(18, 51, 16, 32)], 20),
        MarioState.Returning: Animation([FRect(69, 51, 16, 32)], 1),
        MarioState.Running: Animation([FRect(18, 51, 16, 32), FRect(35, 51, 16, 32), FRect(52, 51, 16, 32), FRect(18, 51, 16, 32)], RUN_FPS),
        MarioState.Falling: Animation([FRect(35, 51, 16, 32)], 1),
        MarioState.Jumping: Animation([FRect(86, 51, 16, 32)], 1),
        MarioState.PoweringDown: Animation([FRect(86, 51, 16, 32), FRect(154, 51, 16, 32), FRect(86, 51, 16, 32), FRect(154, 51, 16, 32), FRect(86, 51, 16, 32), FRect(154, 51, 16, 32), FRect(86, 51, 16, 32), FRect(154, 51, 16, 32), FRect(188, 51, 16, 32), FRect(154, 51, 16, 32), FRect(171, 51, 16, 32), FRect(154, 51, 16, 32), FRect(171, 51, 16, 32), FRect(154, 51, 16, 32), FRect(188, 51, 16, 32), FRect(188, 51, 16, 32), FRect(188, 51, 16, 32), FRect(188, 51, 16, 32), FRect(188, 51, 16, 32), FRect(188, 18, 16, 32)], 15),
        MarioState.Crouching: Animation([FRect(103, 51, 16, 32)], 1)
    }
}

SIZES = {
    PowerupState.Small: Vector2(32, 32),
    PowerupState.Normal: Vector2(32, 66),
    PowerupState.Fire: Vector2(32, 66),
}

class Mario(Drawable):
    def draw(self) -> None:
        if not (self.crouching or self.crouch_jumping):
            self.body.size.y = (7.54/8) * self.sprite.size.y
        self.sprite.position.x = self.body.position.x - self.sprite.size.x / 5
        self.sprite.position.y = self.body.position.y + self.body.size.y - self.sprite.size.y
        
        if self.direction == -1:
            self.sprite.h_flip = True
        else:
            self.sprite.h_flip = False
        
        self.sprite.draw()
    
    def change_powerup_state(self, state: PowerupState) -> None:
        self.next_powerup_state = state
    
    def _change_powerup_state(self, state: PowerupState) -> None:
        if self.lock_state:
            return
        if state == PowerupState.Small:
            self.invincibility_frames = INVINCIBILITY_FRAMES_MAX
            
            if not self.crouching:
                self.stored_position = Vector2(self.body.position.x, self.body.position.y + (self.sprite.size.y - SIZES[PowerupState.Small].y))
            else:
                self.stored_position = copy(self.body.position)
            self.state = MarioState.PoweringDown
            self.stored_velocity = self.body.velocity
            self.stored_sprite_size = SIZES[state]
            self.lock_state = True
            ANIMATIONS[self.powerup_state][MarioState.PoweringDown].play()
            
        elif (state == PowerupState.Normal or state == PowerupState.Fire) and self.powerup_state == PowerupState.Small:
            self.state = MarioState.PoweringUp
            self.stored_sprite_size = SIZES[state]
            self.body.position.y -= SIZES[PowerupState.Small].y
            self.stored_position = self.body.position
            self.stored_velocity = self.body.velocity
            self.lock_state = True
            ANIMATIONS[self.powerup_state][MarioState.PoweringUp].play()
        
        elif state == PowerupState.Fire and self.powerup_state == PowerupState.Normal:
            self.state = MarioState.PoweringUp
            self.stored_sprite_size = SIZES[state]
            self.stored_position = self.body.position
            self.stored_velocity = self.body.velocity
            self.lock_state = True
            ANIMATIONS[self.powerup_state][MarioState.PoweringUp].play()
          
        self.stored_powerup_state = state
    
    def update_input(self) -> None:
        self.state = MarioState.Idle
        self.holding_run = False
        speed = WALK_SPEED
        
        keys = engine.instance.input_manager.get_keys_pressed()
        keys_just_pressed = engine.instance.input_manager.get_keys_just_pressed()
        
        if 'down' in keys and self.is_grounded and self.powerup_state != PowerupState.Small and not self.lock_state:
            self.state = MarioState.Crouching
            if not self.crouching:
                self.crouching = True
                self.body.size.y = (1/2) * self.sprite.size.y
                self.body.position.y += self.sprite.size.y / 2
        elif not ('down' in keys) and not self.lock_state:
            if self.crouching == True and ((not self.crouch_jumping) or (self.crouch_jumping and self.is_grounded)):
                self.body.position.y -= self.sprite.size.y / 2
                self.body.size.y = (7.54/8) * self.sprite.size.y
            self.crouching = False
        if engine.instance.input_manager.is_key_pressed('x') and ('left' in keys or 'right' in keys) and self.state != MarioState.Crouching:
            if self.time_of_run == -1:
                self.time_of_run = pygame.time.get_ticks()
            
            percentage = min(0.2 + (pygame.time.get_ticks() - self.time_of_run) / (RUN_MAX_FPS_TICKS), 1)     
            ANIMATIONS[self.powerup_state][MarioState.Running].fps = int(percentage * RUN_FPS)
            self.state = MarioState.Running
            speed = RUN_SPEED * percentage
            self.holding_run = True
        if 'x' in keys_just_pressed and self.powerup_state == PowerupState.Fire and self.state != MarioState.Crouching:
            if self.time_of_last_fireball == -1:
                self.time_of_last_fireball = pygame.time.get_ticks()
                fireball = Fireball(self.world.tilemap)
            
                fireball.body.position.y = self.body.position.y + (1/4) * self.sprite.size.y

                if self.direction == -1:
                    fireball.body.position.x = self.body.position.x
                else:
                    fireball.body.position.x = self.body.position.x + self.body.size.x
            
                fireball.direction = self.direction
            
                self.world.fireballs.append(fireball)
            elif (pygame.time.get_ticks() - self.time_of_last_fireball) >= FIREBALL_COOLDOWN_TICKS:
                self.time_of_last_fireball = -1
                            
        
        if engine.instance.input_manager.is_key_pressed('left') and self.return_frame == -1:
            
            if (self.state == MarioState.Crouching):
                self.direction = -1
                
                if not self.is_grounded:
                    self.body.velocity.x += -speed * (AIR_SPEED_PERCENT/100)
                
            else:
                if self.state != MarioState.Running:
                    self.state = MarioState.Walking
             
                self.return_frames = abs(self.body.velocity.x) * (RETURN_FRAME_PERCENT / 100)
                if self.direction == 1:
                    self.return_frame = 0
            
                self.direction = -1
            
                if self.is_grounded: 
                    self.body.velocity.x += -speed
                else:
                    self.body.velocity.x += -speed * (AIR_SPEED_PERCENT/100)
        elif engine.instance.input_manager.is_key_pressed('right') and self.return_frame == -1:
            if (self.state == MarioState.Crouching):
                self.direction = 1
                
                if not self.is_grounded:
                    self.body.velocity.x += -speed * (AIR_SPEED_PERCENT/100)
            else:
                if self.state != MarioState.Running:
                    self.state = MarioState.Walking
            
                self.return_frames = abs(self.body.velocity.x) * (RETURN_FRAME_PERCENT / 100)
                if self.direction == -1:
                    self.return_frame = 0
            
                self.direction = 1
            
                if self.is_grounded:
                    self.body.velocity.x += speed
                else:
                    self.body.velocity.x += speed * (AIR_SPEED_PERCENT/100)
        if 'z' in keys_just_pressed and self.coyote_time > 0:
            self.body.velocity.y += -JUMP_POWER
            self.jumped = True
        
            if self.crouching:
                self.crouch_jumping = True
        elif 'z' in keys and self.coyote_time > 0 and not self.is_grounded:
            self.body.velocity.y += -JUMP_POWER
        if engine.instance.input_manager.is_key_pressed('down') and not self.is_grounded and not self.crouch_jumping:
            self.body.velocity.y += GRAVITY
        
    def collide_with_tilemap(self):
        rect = self.tilemap.get_body_bounds(self.body)
        self.is_grounded = False
        tiles_collided_with = []
        for x in range(rect[0], rect[0] + rect[2]):
            for y in range(rect[1], rect[1] + rect[3]):
                tile = self.tilemap.tiles[x][y]
                
                if tile != -1:
                    tile_body = self.tilemap.get_tile_collision_body((x,y))
                    tiles_collided_with.append(tile_body)
        
        tiles_collided_with.sort(key = lambda tile: (tile.position + tile.size / 2).distance_to(self.body.position + self.body.size / 2))
        for tile in tiles_collided_with:
            side = self.body.get_collision_side(tile)
            self.body.solve_collision(tile, side)
            if side == CollisionSide.Bottom:
                if self.body.velocity.y >= 0:
                    self.is_grounded = True
                    self.jumped = False

    def update_state(self):
        if self.return_frame != -1:
            self.state = MarioState.Returning
        if self.jumped and not self.is_grounded:
            self.state = MarioState.Jumping
            self.return_frame = -1
        if not self.is_grounded and not self.jumped:
            self.state = MarioState.Falling
            self.return_frame = -1
        elif round(self.body.velocity.x, 2) in frange(0.0, 0.1, 0.01) and self.is_grounded and not self.state == MarioState.Crouching:
            self.state = MarioState.Idle
        
        if not self.jumped:
            self.crouch_jumping = False
        
        if self.return_frame > -1 and self.return_frame < self.return_frames:
            self.return_frame += 1
        elif self.return_frame >= self.return_frames:
            self.return_frame = -1

        if self.state != MarioState.Running and (pygame.time.get_ticks() - self.time_of_run) >= RUN_RESET_TICKS and self.time_of_run != -1:
            self.time_of_run = -1

    def update_physics(self):
        if self.is_grounded:
            if self.state == MarioState.Idle or self.state == MarioState.Returning or self.state == MarioState.Crouching:
                if self.body.velocity.x != 0:
                    self.body.velocity.x += -self.body.velocity.x * DEACCEL
        else:
            if self.body.velocity.x != 0:
                self.body.velocity.x += -self.body.velocity.x * DEACCEL * (AIR_DEACCEL_PERCENT/100)
        self.body.velocity.y += GRAVITY
    
        if not self.is_grounded:
            self.coyote_time = max(self.coyote_time-1,0)
        else:
            self.coyote_time = COYOTE_TIME_MAX

        self.body.velocity.y = min(self.body.velocity.y, TERMINAL_FALL_SPEED)
        
        speed_limit = TERMINAL_RUN_SPEED if self.holding_run else TERMINAL_WALK_SPEED
        
        self.body.velocity.x = clamp(self.body.velocity.x, -speed_limit, speed_limit)
        self.collide_with_tilemap()
        self.body.update()

    def update_animations(self):
        anim_dict = ANIMATIONS[self.powerup_state]

        match self.state:
            case MarioState.Idle:
                anim = anim_dict[self.state]
                anim.play()
                self.sprite.area = anim.get_frame()
            case MarioState.Walking:
                anim = anim_dict[self.state]
                if not anim.playing:
                    anim.play()
                self.sprite.area = anim.get_frame()
            case MarioState.Returning:
                anim = anim_dict[self.state]
                anim.play()
                self.sprite.area = anim.get_frame()
            case MarioState.Jumping:
                anim = anim_dict[MarioState.Crouching] if self.crouch_jumping else anim_dict[self.state]
                anim.play()
                self.sprite.area = anim.get_frame()
            case MarioState.Falling:
                anim = anim_dict[self.state]
                anim.play()
                self.sprite.area = anim.get_frame()
            case MarioState.Running:
                anim = anim_dict[self.state]
                if not anim.playing:
                    self.run_max_fps_time = pygame.time.get_ticks() + RUN_MAX_FPS_TICKS
                    anim.play()
                self.sprite.area = anim.get_frame()
            case MarioState.PoweringUp:
                anim = anim_dict[self.state]
                self.sprite.size = self.stored_sprite_size
                self.sprite.area = anim.get_frame()
            case MarioState.PoweringDown:
                anim = anim_dict[self.state]
                self.sprite.area = anim.get_frame()
            case MarioState.Crouching:
                anim = anim_dict[self.state]
                anim.play()
                self.sprite.area = anim.get_frame()

    def update(self) -> None:
        if not self.alive:
            return
        
        if self.next_powerup_state != None:
            self._change_powerup_state(self.next_powerup_state)
            self.next_powerup_state = None
        
        if not self.lock_state:
            self.update_input()
            self.update_state()
            self.update_physics()
                
        self.update_animations()
        
        if self.lock_state == True:
            anim = ANIMATIONS[self.powerup_state][self.state]
            if not anim.playing:
                anim.reset()
                self.powerup_state = copy(self.stored_powerup_state)
                self.stored_powerup_state = None
                self.sprite.size = copy(self.stored_sprite_size)
                self.body.velocity = copy(self.stored_velocity)
                self.body.position = copy(self.stored_position)
                self.lock_state = False
                self.state = MarioState.Idle
    
        if self.invincibility_frames > 0:
            self.sprite.alpha = 150
            self.invincibility_frames -= 1
        else:
            self.sprite.alpha = 255
    def __init__(self, world):
        super().__init__()
        self.body = CollisionBody(Vector2(0, 0), Vector2(20,20))
        self.is_grounded = False
        self.tilemap = world.tilemap
        self.coyote_time = COYOTE_TIME_MAX
        self.direction = 1
        self.body.color = Color(255,255,255,255)
        self.alive = True
        self.powerup_state = PowerupState.Small
        self.return_frame = -1
        self.return_frames = 0
        self.holding_run = False
        self.jumped = False
        self.state = MarioState.Idle
        self.time_of_run = -1
        self.stored_position = Vector2(0,0)
        self.sprite = Sprite(engine.instance.surface_manager.get_surface("atlas_mario"), self.body.position, SIZES[self.powerup_state], FRect(1, 1, 16, 16))
        self.invincibility_frames = 0
        self.lock_state = False
        self.stored_velocity = Vector2(0,0)
        self.next_powerup_state = None
        self.fire_debounce = False
        self.crouch_jumping = False
        self.crouching = False
        self.time_of_last_fireball = -1
        self.world = world

DEAD_RETURN_DISTANCE = 100
DEAD_FALL_SPEED = 7
DEAD_OFFSET = 500
UPWARDS_FALL_DELAY = 1000

class DeadMario(Drawable):
    def update(self):
        time_since_death = pygame.time.get_ticks() - self.time_of_death
        
        if round(self.sprite.position.y - self.target_position, 1) < 4 and self.flag == 'up':
            self.target_position = engine.instance.window.size.y + DEAD_OFFSET
            self.flag = 'down'
            self.multiplier = 0.1
        
        if round(self.target_position - self.sprite.position.y, 1) < 2 and self.flag == 'down':
            self.reset_flag = 1
        
        if self.flag == 'up':
            self.sprite.position.y += (self.target_position - self.sprite.position.y) * self.multiplier
        else:
            self.sprite.position.y += TERMINAL_FALL_SPEED
    
    def draw(self):
        self.sprite.draw()
        pass
    
    def __init__(self, position):
        self.multiplier = 0.099
        self.flag = 'up'
        self.spawn_position = position
        self.position = position
        self.sprite = Sprite(engine.instance.surface_manager.get_surface("atlas_mario"), position, Vector2(32,32), FRect(6 * 16 + 7, 1, 16, 16))
        self.reset_flag = 0
        self.time_of_death = pygame.time.get_ticks()
        self.target_position = self.spawn_position.y - DEAD_RETURN_DISTANCE
        self.yvel = 0
        pass
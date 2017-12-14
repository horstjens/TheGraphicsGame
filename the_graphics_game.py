# -*- coding: utf-8 -*-

import random
import pygame 
import operator
import math

import vectorclass2d as v



class Shape():
    number = 0
    
    def __init__(self, screen, startpoint, pointlist, zoom=1, angle=0, color=(255,0,0), width=1, borderBounce=True, friction=0.5, move=v.Vec2d(0,0)):
        self.startpoint = startpoint
        self.pointlist = pointlist
        self.rotationpoint = v.Vec2d(0,0)
        self.zoom = zoom
        self.angle = angle
        self.color = color
        self.width = width
        self.screen = screen
        self.hitpoints = 1000
        self.number = Shape.number
        Shape.number += 1
        self.borderBounce = borderBounce
        #--- friction: 0 means no frictoin, 1 means no gliding
        self.friction = friction #0.1 # 0 or False means no friction
        self.move = v.Vec2d(move.x, move.y)
        
        
    
    def forward(self, delta=1):
        deltavec = v.Vec2d(delta, 0)
        deltavec.rotate(self.angle)
        #self.startpoint += deltavec
        self.move += deltavec
    
    def rotate(self, delta_angle=1):
        """alters pointlist by rotation with angle from rotationpoint"""
        self.angle += delta_angle
        #print(self.angle)
        for point in self.pointlist:
            point.rotate(delta_angle)    
        
    def update(self, seconds):
        """update movement. gets the seconds passed since last frame as parameter"""
        self.startpoint += self.move * seconds
        if self.friction:
            self.move *= (1-self.friction)
        if self.borderBounce:
            if self.startpoint.x < 0:
                self.startpoint.x = 0
                self.move.x = 0
            if self.startpoint.x > PygView.width :
                self.startpoint.x = PygView.width
                self.move.x = 0
            if self.startpoint.y < 0:
                self.startpoint.y = 0
                self.move.y = 0
            if self.startpoint.y > PygView.height:
                self.startpoint.y = PygView.height
                self.move.y = 0
        
    def draw(self):
        oldpoint = self.pointlist[0]
        #pygame.draw.line(self.screen, self.color, (0,0),(100,10),2)
        #pygame.draw.line(self.screen, self.color, (100,10),(10,150),2)
        self.color = (random.randint(0, 255) ,random.randint(0, 255) ,random.randint(0, 255) ) 
        for point in self.pointlist:
            #print("painting from point", oldpoint.x, oldpoint.y, "to", point.x, point.y)
            pygame.draw.line(self.screen, self.color,
                (self.startpoint.x + oldpoint.x * self.zoom,
                 self.startpoint.y + oldpoint.y * self.zoom),
                (self.startpoint.x + point.x * self.zoom,
                 self.startpoint.y + point.y * self.zoom)
                 ,self.width)
            oldpoint = point
                              

                              
class VectorSprite(pygame.sprite.Sprite):
    pointlist = []
    
    def __init__(self, pos=v.Vec2d(100,100), move=v.Vec2d(50,0),
                 color=(255,0,0)):
        self._layer = 1
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.pos = v.Vec2d(pos.x, pos.y)
        self.move = v.Vec2d(move.x, move.y)
        self.color = color
        self.create_image()
        self.rect = self.image.get_rect()
        self.rect.center = self.pos.x, self.pos.y
        self.lifetime = None
        self.age = 0
        
    
    
    def update(self, seconds):
        self.age += seconds
        self.pos += self.move * seconds
        self.rect.center = (self.pos.x, self.pos.y)
        if self.lifetime is not None:
            self.lifetime -= seconds
            if self.lifetime < 0:
                self.kill()
        
    def create_image(self):
        minx = 0
        miny = 0
        maxx = 5
        maxy = 5
        for point in self.pointlist:
            if point.x < minx:
                minx = point.x
            if point.x > maxx:
                maxx = point.x
            if point.y < miny:
                miny = point.y
            if point.y > maxy:
                maxy = point.y
        self.image = pygame.Surface((maxx, maxy))
        pygame.draw.circle(self.image, self.color, (2,2), 2)
        self.image.convert_alpha()  
  
class Ufo(VectorSprite):
  
    def update(self, seconds):
        # --- animate ------
        # new image each 1/10th second, i have 3 images total
        i = (self.age*10) % 3 # modulo = rest of division by 3
        self.image = self.images[int(i)]
        # --- chance to change move vector ---
        if random.random() < 0.001:
            self.move=v.Vec2d(random.randint(-80,80),
                              random.randint(-80,80))
        # --- bounce on screen edge ---
        if self.pos.x < 0:
            self.pos.x = 0
            self.move.x *= -1
        elif self.pos.x > PygView.width:
            self.pos.x = PygView.width
            self.move.x *= -1
        if self.pos.y < 0:
            self.pos.y = 0
            self.move.y *= -1
        elif self.pos.y > PygView.height:
            self.pos.y = PygView.height
            self.pos.y *= -1
        VectorSprite.update(self, seconds)
  
    def create_image(self):
        # ---- image0 -----
        self.image0 = pygame.Surface((100, 100))
        pygame.draw.line(self.image0, self.color, (15, 50), (85, 50),1)
        pygame.draw.line(self.image0, self.color, (15, 50), (25, 25),3)
        pygame.draw.line(self.image0, self.color, (15, 50), (25, 75),3)
        pygame.draw.line(self.image0, self.color, (85, 50), (75, 25),3)
        pygame.draw.line(self.image0, self.color, (85, 50), (75, 75),3)
        pygame.draw.line(self.image0, self.color, (25, 25), (75, 25),3)
        pygame.draw.line(self.image0, self.color, (25, 75), (75, 75),3)
        self.image0.set_colorkey((0,0,0))
        self.image0.convert_alpha() 
        # ----- image1 ------
        self.image1 = pygame.Surface((100, 100))
        pygame.draw.line(self.image1, self.color, (15, 50), (85, 50),1)
        pygame.draw.line(self.image1, self.color, (15, 50), (25, 25),3)
        pygame.draw.line(self.image1, self.color, (15, 50), (25, 75),3)
        pygame.draw.line(self.image1, self.color, (85, 50), (75, 25),3)
        pygame.draw.line(self.image1, self.color, (85, 50), (75, 75),3)
        pygame.draw.line(self.image1, self.color, (25, 25), (75, 25),3)
        pygame.draw.line(self.image1, self.color, (25, 75), (75, 75),3)
        self.image1.set_colorkey((0,0,0))
        self.image1.convert_alpha() 
        # ----- image2 ---------
        self.image2 = pygame.Surface((100, 100))
        pygame.draw.line(self.image2, self.color, (15, 50), (85, 50),1)
        pygame.draw.line(self.image2, self.color, (15, 50), (25, 25),3)
        pygame.draw.line(self.image2, self.color, (15, 50), (25, 75),3)
        pygame.draw.line(self.image2, self.color, (85, 50), (75, 25),3)
        pygame.draw.line(self.image2, self.color, (85, 50), (75, 75),3)
        pygame.draw.line(self.image2, self.color, (25, 25), (75, 25),3)
        pygame.draw.line(self.image2, self.color, (25, 75), (75, 75),3)
        self.image2.set_colorkey((0,0,0))
        self.image2.convert_alpha() 
        # ------------------------
        self.images = [self.image0, self.image1, self.image2]
        self.image = self.images[0]
    
        
class Fragment(VectorSprite):
    def __init__(self, pos=v.Vec2d(100,100), move=None, color=None, gravity=None, lifetime=None, clone=False, radius=2):
        self.radius = radius
        if gravity is not None:
            self.gravity = v.Vec2d(gravity.x, gravity.y)
        else:
            self.gravity = gravity
        if color is not None:
            self.color = color
        else:
            self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        if move is not None:
            self.move = v.Vec2d(move.x, move.y)
        else:
            self.move = v.Vec2d(0,random.randint(5,250))
            self.move.rotate(random.randint(0,360))
        self.clone = clone
        VectorSprite.__init__(self, pos, self.move, color=self.color)
        if lifetime is not None:
            self.lifetime = lifetime
        else:
            self.lifetime = 0.1 + random.random() * 3
            
    def update(self, seconds):
        VectorSprite.update(self, seconds)
        if self.gravity is not None:
            self.move += self.gravity * seconds
        if self.clone and random.random() < 0.5:
            Smoke(pos=self.pos, move=v.Vec2d(0,0), color=self.color, lifetime=0.8)
        
    def create_image(self):
        self.image = pygame.Surface((self.radius*2,self.radius*2))
        pygame.draw.circle(self.image, self.color, (self.radius,self.radius), self.radius)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        
class Spark(Fragment):
    
    def create_image(self):
        self.image = pygame.Surface((50,50))
        self.color = (random.randint(200, 255), random.randint(128, 220), 50)
        pygame.draw.circle(self.image, self.color, (25,25), 2)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        
    def update(self, seconds):
        VectorSprite.update(self, seconds)
        if self.gravity is not None:
            self.move += self.gravity * seconds
        
        if self.age / 10 > 2:
            self.radius = self.age // 10
            self.create_image(self)


class Flashlight(Fragment):
    
    def __init__(self, pos, radius=15, delay=None, lifetime=None, expand=False):
        self.radius = radius
        Fragment.__init__(self, v.Vec2d(pos.x, pos.y), v.Vec2d(0,0),
                          color=(255,255,255), radius=self.radius)
        if delay is None:
            self.delay = random.random() * 0.25
        else:
            self.delay = delay
        if lifetime is None:
            self.lifetime = random.random() * 0.01 + self.delay
        else:
            self.lifetime = lifetime + self.delay
        self.expand = expand
        
    def create_image(self):
        self.image = pygame.Surface((2*self.radius,2*self.radius))
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius )
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        
    def update(self, seconds):
        self.age += seconds
        if self.age > self.delay:
            Fragment.update(self, seconds)
        else:
            self.lifetime -= seconds
            
    def kill(self):
        if self.expand and self.radius < 100:
            Flashlight(self.pos, self.radius+10, 0.0, 0.1, True)
        Fragment.kill(self)
        

            
class Smoke(Fragment):
    def create_image(self):
        self.image = pygame.Surface((50,50))
        pygame.draw.circle(self.image, self.color, (25,25), 2)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        
    def update(self, seconds):
        VectorSprite.update(self, seconds)
        if self.gravity is not None:
            self.move += self.gravity * seconds
        if self.age / 10 > 2:
            self.radius = self.age // 10
            self.create_image(self)
        
class Rocket(Fragment):
    def __init__(self, startpos, target, speed=None, color=(150,99,0), ex=None):
            #leftcorner = v.Vec2d(0,self.height)
            #rightcorner = v.Vec2d(self.width,self.height)
            if speed is not None:
                self.speed = speed
            else:
                self.speed = random.randint(130,180)
            rocketcolor = color
            #speed = random.randint(150,180)
            rocketmove = target - startpos
            rockettime = rocketmove.length / self.speed
            rocketmove = rocketmove.normalized() * self.speed
            #leftmove = pos-leftcorner
            #lefttime = leftmove.length / speed
            #leftmove = leftmove.normalized() * speed
            Fragment.__init__(self, pos=startpos, move=rocketmove, color=rocketcolor, gravity=None, lifetime=rockettime)
            if ex is None:
                self.ex = random.randint(1,7)
            else:
                self.ex = ex
     
    def update(self, seconds):
          self.pos += self.move * seconds
          self.rect.center = (self.pos.x, self.pos.y)
          self.lifetime -= seconds
          if self.lifetime > 0:
              # black smoke
              if random.random() < 1:
                  Smoke(self.pos, move=self.move* -0.1, color=(19,0,0))  
              m = self.move * -1
              m.rotate(random.randint(-5, 5))
              Spark(self.pos, move = m)
          else:
          #if self.lifetime < 0:
                # explosion
                c1 = random.randint(0,255)
                c2 = random.randint(0,255)
                c3 = random.randint(0,255)
                c4 = random.randint(0,255)
                g = v.Vec2d(0,random.randint(100,250))
                
                explosion = self.ex 
                if explosion == 0:
                    for x in range(50):
                        Fragment(self.pos, gravity=None, color=(c1,c2,c3))
                
                elif explosion == 1:
                    for x in range(50):
                        Fragment(self.pos, gravity=g, color=(c1,c2,c3))
                
                elif explosion == 2:
                    m = v.Vec2d(random.randint(100,200), 0)
                    for x in range(72):
                        Fragment(self.pos, move=m, gravity=g, color=(c1,c2,c3))
                        m.rotate(5)
                
                elif explosion == 3:
                    m = v.Vec2d(random.randint(100,200), 0)
                    for x in range(72):
                        Fragment(self.pos, move=m, gravity=g, color=(c1,c2,c3), clone=True)
                        m.rotate(5)
                    
                elif explosion == 4:
                    m = v.Vec2d(100,0)
                    wieoft = random.randint(1,4)
                    winkel = random.randint(1,360)
                    for x in range(wieoft):
                        Rocket(self.pos, target=self.pos+m)
                        m.rotate(winkel)
                        
                elif explosion == 5:
                    m = v.Vec2d(100,0)
                    wieoft = random.randint(1,10)
                    winkel = random.randint(1,360)
                    for x in range(wieoft):
                        Rocket(self.pos, target=self.pos+m)
                        m.rotate(winkel)
                        
                elif explosion == 6:
                    m = v.Vec2d(random.randint(150,200), 0)
                    for x in range(36):
                        Fragment(self.pos, move=m)
                        m.rotate(10)
                        m *= 0.92 
                        
                elif explosion == 7:
                    m = v.Vec2d(random.randint(100,200), 0)
                    wieoft = random.randint(1,10)
                    winkel = random.randint(1,360)
                    wieoft2 = random.randint(1,2)
                    for x in range(wieoft):
                        Fragment(self.pos, move=m)
                        m.rotate(winkel)
                        m *= wieoft2
                
                elif explosion == 8:
                    for x in range(5):
                        s = v.Vec2d(random.randint(0,50), 0)
                        s.rotate(random.randint(0,360))
                        Flashlight( self.pos + s )
                
                elif explosion == 9:
                    Flashlight( self.pos, 2, 0.1, 0.1, True )
                                   
                self.kill()
                
      

            
  

class Ball():
    
    group = []
    number = 0
    maxage = 400
    """this is not a native pygame sprite but instead a pygame surface"""
    def __init__(self, screen, startpoint=v.Vec2d(5,5), move=v.Vec2d(1,0), radius = 50, color=(0,0,255), bossnumber=0):
        """create a (black) surface and paint a blue ball on it"""
        self.number = Ball.number
        Ball.number += 1
        #Ball.group[self.number] = self
        Ball.group.append(self)
        self.radius = radius
        self.color = color
        self.bossnumber = bossnumber # 
        self.screen = screen
        self.startpoint = v.Vec2d(startpoint.x, startpoint.y) # make a copy of the startpoint vector
        self.move = move
        self.age = 0
        # create a rectangular surface for the ball 100x100
        self.surface = pygame.Surface((2*self.radius,2*self.radius))    
        # pygame.draw.circle(Surface, color, pos, radius, width=0) # from pygame documentation
        #pygame.draw.circle(self.surface, color, (radius, radius), radius) # draw blue filled circle on ball surface
        width = 1
        pygame.draw.line(self.surface, self.color, (50,50),
                    (50+self.move.x * 10, 50+self.move.y*10),width)
        self.startpoint.x -= 50
        self.startpoint.y -= 50
        self.surface.set_colorkey((0,0,0)) # make black transparent
        self.surface = self.surface.convert_alpha() # for faster blitting. 
        
    #def blit(self, background):
        #"""blit the Ball on the background"""
        #background.blit(self.surface, ( self.x, self.y))
        
    def draw(self):
        self.screen.blit(self.surface, (self.startpoint.x, self.startpoint.y))
        self.startpoint += self.move
        self.age += 1
        

        

class PygView(object):
  
    width = 0
    height = 0
  
    def __init__(self, width=1440, height=850, fps=30):
        """Initialize pygame, window, background, font,...
           default arguments 
        """
        pygame.init()
        pygame.display.set_caption("Press ESC to quit.")
        PygView.width = width    # also self.width 
        PygView.height = height  # also self.height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()  
        self.background.fill((255, 255, 255)) # yannik hier hintergrund färben
        # fill background white
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
        self.font = pygame.font.SysFont('mono', 24, bold=True)
        self.allgroup = pygame.sprite.LayeredUpdates()
        VectorSprite.groups = self.allgroup
        Fragment.groups = self.allgroup
        self.ufo1 = Ufo()

    def paint(self):
        """painting ships on the surface"""

        self.yanniks_ship = Shape(self.screen, v.Vec2d(100, 80),
                                       (
                                        v.Vec2d(0, 0),
                                        v.Vec2d(-25, 25),
                                        v.Vec2d(25, 0),
                                        v.Vec2d(-25, -25),
                                        v.Vec2d(0, 0)))
        self.yanniks_ship.draw()
        self.pixelhirn = Shape(self.screen, v.Vec2d(self.width-100, self.height-100),
                                       (
                                        v.Vec2d(0, 0),
                                        v.Vec2d(-25, 25),
                                        v.Vec2d(75, 0),
                                        v.Vec2d(-25, -25),
                                        v.Vec2d(0, 0)))
        self.pixelhirn.rotate(180)
        self.pixelhirn.draw()
        
        

    def run(self):
        """The mainloop
        """
        self.paint() 
        running = True
        while running:
            # --------- update time -------------            
            
            milliseconds = self.clock.tick(self.fps)
            seconds = milliseconds / 1000.0
            self.playtime += seconds
            text_time = "FPS: {:4.3} TIME: {:6.3} sec".format(self.clock.get_fps(), self.playtime)
            text_player1 = "Player1: HP: {}".format(self.yanniks_ship.hitpoints)
            text_player2 = "Player2: HP: {}".format(self.pixelhirn.hitpoints)
            self.draw_text(text_player1, x=50, y=30, color=(200,20,0))
            self.draw_text(text_time, x = self.width//2-200, y=30, color=(100,0,100))
            self.draw_text(text_player2, x=self.width-300, y=30, color=(0,20,200))
            
            
            # ------------ event handler: keys pressed and released -----
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_c:
                        self.background.fill((255,255,255))
                    #if event.key == pygame.K_RIGHT:
                    #    self.africa.startpoint = v.Vec2d(self.africa.startpoint.x + 20 ,self.africa.startpoint.y)
                    # ----- reset to start position ------
                    if event.key == pygame.K_1:
                        self.yanniks_ship.startpoint.x = 100
                        self.yanniks_ship.startpoint.y = 425
                    if event.key == pygame.K_2:
                        self.pixelhirn.startpoint.x = 1340
                        self.pixelhirn.startpoint.y = 425                    
            # --------- pressed key handler --------------            
            pressed = pygame.key.get_pressed()            
            #self.yanniks_ship.move = v.Vec2d(0,0)
            if pressed[pygame.K_w]:
                self.yanniks_ship.forward(150)
            if pressed[pygame.K_s]:
                self.yanniks_ship.forward(-50)
            if pressed[pygame.K_a]:
                self.yanniks_ship.rotate(-5)
            if pressed[pygame.K_d]:
                self.yanniks_ship.rotate(5)
           
                
            #if pressed[pygame.K_t]:
            #    self.yanniks_ship.zoom += 0.25
            #if pressed[pygame.K_f]:
            #    self.yanniks_ship.zoom -= 0.25
            #-------- pixelhirn ---------
            #self.pixelhirn.move = v.Vec2d(0,0)
            if pressed[pygame.K_UP]:
                self.pixelhirn.forward(150)
            if pressed[pygame.K_DOWN]:
                self.pixelhirn.forward(-50)
            if pressed[pygame.K_LEFT]:
                self.pixelhirn.rotate(-5)
            if pressed[pygame.K_RIGHT]:
                self.pixelhirn.rotate(5)
            
            #if pressed[pygame.K_PLUS]:
            #    self.pixelhirn.zoom += 0.25
            #if pressed[pygame.K_MINUS]:
            #    self.pixelhirn.zoom -= 0.25
            # ----------update ships ------
            self.yanniks_ship.update(seconds)
            self.pixelhirn.update(seconds)
            # ----------draw ships ----------------
            self.yanniks_ship.draw()
            self.pixelhirn.draw()
            
            # -----draw balls-----
            for b in Ball.group:
                b.draw()
            # ---- delete old balls ----
            
            Ball.group = [b for b in Ball.group if b.age < Ball.maxage]
            
            # ----- collision detection -----
            critical_distance = 20
            for b in Ball.group:
                if b.bossnumber != self.pixelhirn.number:
                    if (b.startpoint - self.pixelhirn.startpoint).get_length() < critical_distance:
                        self.pixelhirn.hitpoints -= 1
                if b.bossnumber != self.yanniks_ship.number:
                    if (b.startpoint - self.yanniks_ship.startpoint).get_length() < critical_distance:
                        self.yanniks_ship.hitpoints -= 1
            
            # -------- draw cannons ------------
            # cannon yannik aiming at pixelhirn 
            c =  self.pixelhirn.startpoint - self.yanniks_ship.startpoint 
            c = c.normalized()
            c *= 35
            pygame.draw.line(self.screen, (0,0,0), (self.yanniks_ship.startpoint.x,
                                                    self.yanniks_ship.startpoint.y),
                                                    (self.yanniks_ship.startpoint.x + c.x,
                                                    self.yanniks_ship.startpoint.y + c.y),
                                                    8) 
            
            

            # cannon yannik aiming at pixelhirn
            d =  self.yanniks_ship.startpoint - self.pixelhirn.startpoint 
            d = d.normalized()
            d *= 35
            pygame.draw.line(self.screen, (0,0,0), (self.pixelhirn.startpoint.x,
                                                    self.pixelhirn.startpoint.y),
                                                    (self.pixelhirn.startpoint.x + d.x,
                                                    self.pixelhirn.startpoint.y + d.y),
                                                    8)                                             
                                                    
                                                            
            # --------- (auto)fire -------
            #c *= 0.05
            #d *= 0.05
            speedfactor = 0.05
            if pressed[pygame.K_LCTRL]:
            #if random.random() < 0.1:
                move = c * speedfactor # + self.yanniks_ship.move
                Ball(self.screen, self.yanniks_ship.startpoint+c, move, color=(200,20,0), bossnumber=self.yanniks_ship.number)                      
            
            if pressed[pygame.K_RSHIFT]:                                                
            #if random.random() < 0.1:
                move = d * speedfactor 
                Ball(self.screen, self.pixelhirn.startpoint+d,  move, color=(0,0,200), bossnumber=self.pixelhirn.number)   
            # ------ sentry guns in corner
            p1 = v.Vec2d(0,0)
            distance1 = self.pixelhirn.startpoint - p1
            #Ball(self.screen, (
            
            
            
            # ---------- update screen ----------- 
            #pygame.display.flip()
            #self.screen.blit(self.background, (0, 0))
            
            # ---------- update screen ----------- 
            self.screen.blit(self.background, (0, 0))
            # ------ sprite ------
            self.allgroup.update(seconds)
            self.allgroup.draw(self.screen)
            # ------ flip screen ------
            pygame.display.flip()
            
        pygame.quit()


    def draw_text(self, text, x=50, y=150, color=(0,0,0)):
        """Center text in window
        """
        fw, fh = self.font.size(text)
        surface = self.font.render(text, True, color)
        self.screen.blit(surface, (x,y))


    
####

if __name__ == '__main__':
    PygView().run()

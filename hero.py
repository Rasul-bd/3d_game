# напиши свой код здесь
class Hero():
    def __init__(self, pos, land):
        self.land = land
        self.hero = loader.loadModel('smiley')
        self.hero.setColor(1, 0.5, 0)
        self.hero.setScale(0.3)
        self.hero.setPos(pos)
        self.hero.reparentTo(render)
        self.cameraBind()
        self.accept_events()
        self.mode = True

    def accept_events(self):
        base.accept('m', self.turn_right)
        base.accept('m'+'-repeat', self.turn_right)
        base.accept('n', self.turn_left)
        base.accept('n'+'-repeat', self.turn_left)

        base.accept('w', self.forward)
        base.accept('w' + '-repeat', self.forward)
        base.accept('s', self.back)
        base.accept('s' + '-repeat', self.back)
        base.accept('a', self.left)
        base.accept('a' + '-repeat', self.left)
        base.accept('d', self.right)
        base.accept('d' + '-repeat', self.right)

        base.accept('e', self.up)
        base.accept('e' + '-repeat', self.up)

        base.accept('q', self.down)
        base.accept('q' + '-repeat', self.down)

        base.accept( 'b', self.build )
        base.accept( 'v', self.destroy )


        base.accept('z', self.changeMode)

        base.accept('k', self.land.saveMap)
        base.accept('l', self.land.loadMap)


        base.accept('c', self.changeView)

    def turn_right(self):
        self.hero.setH((self.hero.getH() - 5) % 360)

    def turn_left(self):
        self.hero.setH((self.hero.getH() + 5) % 360)

    def changeView(self):
        if self.cameraOn:
            self.cameraUp()
        else:
            self.cameraBind()
    
    def changeMode(self):
        if self.mode == True:
            self.mode = False
        else:
            self.mode = True

    def cameraUp(self):
        pos = self.hero.getPos()
        base.mouseInterfaceNode.setPos(-pos[0], -pos[1], -pos[2] - 3 )
        base.camera.reparentTo(render)
        base.enableMouse()
        self.cameraOn = False
    def cameraBind(self):
        base.disableMouse()
        base.camera.setH(180)
        base.camera.reparentTo(self.hero)
        base.camera.setPos(0, 0, 1.5)
        self.cameraOn = True
    
    def just_move(self, angle):
        pos = self.look_at(angle)
        self.hero.setPos(pos)

    def try_move(self, angle):
        pos = self.look_at(angle)
        if self.land.isEmpty(pos):
            pos = self.land.findHighestEmpty(pos)
            self.hero.setPos(pos)
        else:
            pos = pos[0], pos[1], pos[2] + 1
        if self.land.isEmpty(pos):
            self.hero.setPos(pos)

    def move_to(self, angle):
        if self.mode:
            self.just_move(angle)
        else:
            self.try_move(angle)


    def look_at(self, angle):
        from_x = round(self.hero.getX())
        from_y = round(self.hero.getY())
        from_z = round(self.hero.getZ())
        dx, dy = self.check_dir(angle)
        x_to = from_x + dx
        y_to = from_y + dy
        return x_to, y_to, from_z

    def check_dir(self, angle):
        if angle >= 0 and angle <= 20:
           return (0, -1)
        elif angle <= 65:
           return (1, -1)
        elif angle <= 110:
           return (1, 0)
        elif angle <= 155:
           return (1, 1)
        elif angle <= 200:
           return (0, 1)
        elif angle <= 245:
           return (-1, 1)
        elif angle <= 290:
           return (-1, 0)
        elif angle <= 335:
           return (-1, -1)
        else:
           return (0, -1)
    
    def up(self):
        self.hero.setZ( self.hero.getZ() + 1)
    def down(self):
        self.hero.setZ( self.hero.getZ() - 1)

    def forward(self):
        angle =(self.hero.getH()+0) % 360
        self.move_to(angle)
    def back(self):
        angle =(self.hero.getH()+180) % 360
        self.move_to(angle)
    def left(self):
        angle =(self.hero.getH()+90) % 360
        self.move_to(angle)
    def right(self):
        angle =(self.hero.getH()+270) % 360
        self.move_to(angle)
    
    def build(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.addBlock(pos)
        else:
            self.land.buildBlock(pos)
    
    def destroy(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.delBlock(pos)
        else:
            self.land.delBlockFrom(pos)

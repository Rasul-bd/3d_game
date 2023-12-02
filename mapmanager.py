# напиши здесь код создания и управления картой
import pickle

class Mapmanager():
    def __init__(self):
        self.model = 'block.egg'
        self.texture = 'block.png'
        self.colors = [(0.2, 0.2, 0.35, 1), (0.2, 0.2, 0.3, 1), (0.5, 0.5, 0.2, 1), (0, 0.6, 0, 1)]
        self.startNew()
        #self.addBlock((0, 10, 0 ))
        
    def addBlock(self, position):
        self.block = loader.loadModel(self.model)
        self.block.setTexture(loader.loadTexture(self.texture))

        self.block.setPos(position)
        self.color = self.getColor(int(position[2]))
        self.block.setColor(self.color)
        self.block.reparentTo(self.land)
        self.block.setTag("at", str(position))
    
    def getColor(self, z):
        if z < len(self.colors):
            return self.colors[z]
        else:
            return self.colors[len(self.colors) - 1]

    def startNew(self):
        self.land = render.attachNewNode("Land")

    def clear(self):
        self.land.removeNode()
        self.startNew()

    def loadLand(self, filename):
        self.clear()
        with open(filename, 'r') as file:
            y = 0
            for string in file:
                x = 0
                string_list = string.split(' ')
                for z in string_list:
                    for z0 in range(int(z)+1):
                        block = self.addBlock((x, y, z0))
                    x = x + 1
                y = y + 1
        return x,y
    
    def findBlocks(self,pos):
        return self.land.findAllMatches("=at=" + str(pos))
    
    def findHighestEmpty(self,pos):
        x, y, z = pos
        z = 1
        while not self.isEmpty((x, y, z)):
            z += 1
        return (x, y, z)
    
    def isEmpty(self, pos):
        blocks = self.findBlocks(pos)
        if blocks:
            return False
        else:
            return True
    
    def delBlock(self, position):
        blocks = self.findBlocks(position)
        for block in blocks:
            block.removeNode()
    
    def buildBlock(self, pos):
        x, y, z = pos
        new = self.findHighestEmpty(pos)
        if new[2] <= z + 1:
            self.addBlock(new)
    
    def delBlockFrom(self, pos):
        x, y, z = self.findHighestEmpty(pos)
        pos = x, y, z-1
        blocks = self.findBlocks(pos)
        for block in blocks:
            block.removeNode()
    
    def saveMap(self):
        blocks = self.land.getChildren()
        with open('my_map.dat', 'wb') as f:
            pickle.dump(len(blocks), f)
            for block in blocks:
                x, y, z = block.getPos()
                pos = (int(x), int(y), int(z))
                pickle.dump(pos, f)

                
    def loadMap(self):
        self.clear()
        with open('my_map.dat', 'rb') as f:
            length = pickle.load(f)
            for i in range(length):
                pos = pickle.load(f)
                block = self.addBlock(pos)
                

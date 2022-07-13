

class BaseLevel:
    def __init__(self, app, width, height):
        self.app = app
        self.width = width
        self.height = height
        

        self.map = None

    
    def update(self):
        if self.map:
            self.map.update()
            self.map.draw(self.app.screen)



def TestLevel(BaseLevel):
    def __init__(self, app, width, height):
        super().__init__(app, width, height)
        
        self.map = LevelCreator.generateBasicLevel(self, self.width-30, self.height-10)


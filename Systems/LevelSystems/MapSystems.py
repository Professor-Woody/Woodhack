from Systems.BaseSystem import BaseSystem


class UpdateMapSystem(BaseSystem):
    priority=190

    def run(self):
        self.level.map.update()


class RenderMapSystem(BaseSystem):
    priority=200

    def run(self):
        self.level.map.draw(self.level.app.screen)
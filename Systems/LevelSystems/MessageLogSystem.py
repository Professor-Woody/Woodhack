from Components import Position, Render, Target
from Systems.BaseSystem import BaseSystem


class MessageLogSystem(BaseSystem):
    actions = ['log']
    update = True
    title = "History"
    alwaysActive=False
    priority=210

    def __init__(self, level, entity):
        super().__init__(level)
        # message format: [ [colour, message]  ]
        self.history = []
        self.log = entity

    def run(self):
        if self._actionQueue:
            renderComponents = self.getComponents(Render)

            for action in self.actionQueue:
                # colour could be one of two things
                #   it could be an int, in which case it's the entity fg we need
                #   it could be a tuple, in which case we use it straight
                if type(action['colour']) == int:
                    action['colour'] = renderComponents[action['colour']]['fg']

                # the message may have entityIDs embedded in it. filter them and replace with names, positions, and colours
                message = action['message']
                entities = []
                
                pos = message.find('£')
                while pos != -1:
                    entity = int(message[message.find('£')+1 : message.find('$')])
                    entities.append([renderComponents[entity]['name'], renderComponents[entity]['fg'], pos])

                    message = \
                        message[:message.find('£')] + \
                        renderComponents[entity]['name'] + \
                        message[message.find('$')+1:]                

                    pos = message.find('£')
                self.history.append([action['colour'], message, entities])
            
            self.history = self.history[-10:]
            positionComponents = self.getComponents(Position)

            self.level.app.screen.drawFrame(
                positionComponents[self.log]['x'],
                positionComponents[self.log]['y'],
                positionComponents[self.log]['width'],
                positionComponents[self.log]['height'],
                self.title
            )

            for i in range(len(self.history)):
                message = self.history[i][1]
                entities = self.history[i][2]

                self.level.app.screen.printLine(
                    positionComponents[self.log]['x'] + 2,
                    positionComponents[self.log]['y'] + 1 + i,
                    'o ' + message,
                    self.history[i][0]
                )

                for entity in entities:
                        self.level.app.screen.printLine(
                            positionComponents[self.log]['x'] + 4 + entity[2],
                            positionComponents[self.log]['y'] + 1 + i,
                            entity[0],
                            entity[1]
                        )

    def find_all(self, a_str, sub):
        start = 0
        while True:
            start = a_str.find(sub, start)
            if start == -1: return
            yield start
            start += len(sub)                


class CombatLogSystem(MessageLogSystem):
    actions = ['clog']
    title = "Combat"
    priority=220

        

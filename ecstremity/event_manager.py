class EventManager:
    def __init__(self, queries):
        self._events = []
        self._backlog = []
        self._queries = queries
        self._running = False

    def post(self, event):
        if not self._running:
            self._events.append(event)
        else:
            self._backlog.append(event)

    def update(self):
        self._running = True
        for event in self._events:
            # run on:
            #   target (if there is one)
            #   a query's worth of entities (if it's a string)
            #   the original poster (all other cases)

            if event.target and type(event.target) != str and not event.target.is_destroyed:
                event.target.fire(event)
            elif type(event.target) == str:
                for entity in self._queries[event.target].result:
                    if not entity.is_destroyed:
                        entity.fire(event)

            else:
                if not event.source.is_destroyed:
                    event.source.fire(event)

        self._events.clear()
        self._events = self._backlog.copy()
        self._running = False
        self._backlog.clear()

        if self._events:
            self.update()

        for entity in self._queries['dead'].result:
            entity.destroy()

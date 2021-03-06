import sqlite3

class DB:

    conn = None

    def __init__(self, settings):
        self.conn = sqlite3.connect(settings['PATH'])
        self.conn.row_factory = self.dictFactory
        self.c = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def dictFactory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    # example
    def getUserByLogin(self, login):
        self.c.execute("SELECT * FROM user WHERE login=:login", {"login": login})
        return self.c.fetchone()

    # получить карту (граф и метки)
    def getMap(self, id):
        self.c.execute("SELECT * FROM map WHERE id=:id", { "id": id })
        return self.c.fetchone()

    # получить для карты вершины графа
    def getVertexes(self, map_id):
        self.c.execute("SELECT id, type, name, x, y, z FROM vertex WHERE map_id=:map_id", { "map_id": map_id })
        return self.c.fetchall()

    # получить для карты ребра графа
    def getEdges(self, map_id):
        self.c.execute("SELECT id, vertex1, vertex2, weight FROM edge WHERE map_id=:map_id", { "map_id": map_id })
        return self.c.fetchall()

    # получить конкретный маршрут
    def getPathway(self, id):
        self.c.execute("SELECT id, path, priority, task FROM pathway WHERE id=:id AND status='open'", { "id": id })
        return self.c.fetchone()

    # получить открытый маршрут
    def getLaunchPathway(self):
        self.c.execute("SELECT id, path, priority, task FROM pathway WHERE status='launch'")
        return self.c.fetchone()

    # получить все открытые маршруты
    def getPathways(self, map_id, priority = None):
        if priority:
            query = "SELECT id, path, priority, task FROM pathway WHERE map_id=:map_id AND priority=:priority AND status='open'"
            params = { "map_id": map_id, "priority": priority }
        else:
            query = "SELECT id, path, priority, task FROM pathway WHERE map_id=:map_id AND status='open'"
            params = { "map_id": map_id }
        self.c.execute(query, params)
        return self.c.fetchall()

    # записать путь
    def setPathway(self, map_id, path, priority, task):
        query = "INSERT INTO pathway (map_id, path, priority, task, status) VALUES (:map_id, :path, :priority, :task, 'open')"
        self.c.execute(query, { "map_id": map_id, "path": path, "priority": priority, "task": task })
        return self.conn.commit()

    # изменить статус пути
    def updatePathwayStatus(self, id, status = None):
        if status:
            query = "UPDATE pathway SET status=:status WHERE id=:id"
            params = { "id": id, "status": status }
        else:
            query = "UPDATE pathway SET status='close' WHERE id=:id"
            params = { "id": id }
        self.c.execute(query, params)
        return self.conn.commit()

    # завершить путь
    def closePathway(self, id, status = None):
        return self.updatePathwayStatus(id, 'close')


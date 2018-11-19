SETTINGS = {
    # настройки БД
    'DB': {
        'PATH': 'application/modules/db/map.db'
    },
    # используемая карта
    'MAP_ID': 1,
    # маршрут
    'PATHWAY': {
        # приоритетность маршрута
        'PRIORITY': { 
            'NORMAL': 'normal',
            'HIGH': 'high',
            'URGENT': 'urgent'
        },
        # полетное задание
        'TASK': {
            'FLY': 'fly', # полет с зависанием
            'DELIVERY': 'delivery', # полет с разгрузкой
            'LANDING': 'landing' # полет с посадкой
        }
    },
    # список событий медиатора
    'MEDIATOR_EVENTS': {
        'TEST': 'TEST',
        'MAKE_PATHWAY': 'MAKE_PATHWAY', # задать полетное задание (маршрут)
        'NEW_PATHWAY': 'NEW_PATHWAY', # новое полетное задание создано
        'START_NEXT_PATHWAY': 'START_NEXT_PATHWAY' # начать выполнение следующего полетного задания
    }
}
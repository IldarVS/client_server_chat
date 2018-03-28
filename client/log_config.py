import logging
from datetime import datetime

logger = logging.getLogger('app.main')
# logger = logging.getLogger('DOCTOR')
# Создаём объект форматирования:
# formatter = logging.Formatter('%(created)s %(name)s - %(levelname)s - %(message)s')
formatter = logging.Formatter('%(asctime)s %(levelname)-10s %(module)s %(funcName)s %(message)s')

# Создаём файловый обработчик логгирования (можно задать кодировку):
fh = logging.FileHandler(datetime.now().strftime("%Y%m%d") + '.log', encoding ='utf-8')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)


# Добавляем в логгер новый обработчик событий и устанавливаем уровень логгирования
logger.addHandler(fh)
logger.setLevel(logging.DEBUG)


if __name__ == '__main__':
    # Создаём потоковый обработчик логгирования (по умолчанию sys.stderr):
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    logger.addHandler(console)
    # В логгирование передаем имя текущей функции и имя вызвавшей функции
    logger.info('Тестовый запуск логгирования')


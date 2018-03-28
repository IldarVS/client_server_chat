import logging
import log_config

logger = logging.getLogger('app.main')

def log(func):
    def decorated(*args, **kwargs):
        res = func(*args, **kwargs)
        logger.debug('обработана функция {}'.format(func.__name__))
        return res
    return decorated

def main():
    ''' Тестовая главная функция
    '''
    logger.debug('Старт приложения')

if __name__ == '__main__':
    main()
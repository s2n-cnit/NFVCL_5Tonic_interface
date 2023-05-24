import logging


def create_logger(name: str) -> logging.getLogger:
    # create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(ch)
    return logger


class SstConvertion():
    sstType = {"EMBB": "eMBB", "URLCC": "URLCC", "MMTC": "mMTC"}

    @classmethod
    def to5Tonic(cls, value: str = None):
        return next((v for k,v in cls.sstType.items() if k == value.upper()), None)
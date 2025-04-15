from logger import Logger
from chrono import Chrono
import os
import time

l = Logger("logs", log_name="TEST")
c = Chrono(l)

l.custom("debug", os.getpid())


@c.time_function(name="testing name")
def test():
    result = 0

    for i in range(0, 100):
        result += i

    return result


test()
l.info(c.get_function_timings())

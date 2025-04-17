from Orange.widgets.orangecontrib.AAIT.utils import MetManagement
import time
time0 = MetManagement.get_second_from_1970()
time.sleep(10)
time1 = MetManagement.get_second_from_1970()

print(time0, time1)


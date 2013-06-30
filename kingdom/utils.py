from datetime import datetime
import time


def toTimestamp(localtime):
	return time.mktime(localtime.timetuple()) * 1000 if localtime is not None else None

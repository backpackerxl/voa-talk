import time

# 起始时间戳，可自定义，这里以 2020-01-01 00:00:00 为例
START_TIMESTAMP = 1577836800000

# 数据中心 ID 所占位数
DATA_CENTER_ID_BITS = 5
# 机器 ID 所占位数
WORKER_ID_BITS = 5
# 序列号所占位数
SEQUENCE_BITS = 12

# 数据中心 ID 最大值
MAX_DATA_CENTER_ID = -1 ^ (-1 << DATA_CENTER_ID_BITS)
# 机器 ID 最大值
MAX_WORKER_ID = -1 ^ (-1 << WORKER_ID_BITS)
# 序列号最大值
MAX_SEQUENCE = -1 ^ (-1 << SEQUENCE_BITS)

# 机器 ID 向左移位数
WORKER_ID_SHIFT = SEQUENCE_BITS
# 数据中心 ID 向左移位数
DATA_CENTER_ID_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS
# 时间戳向左移位数
TIMESTAMP_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS + DATA_CENTER_ID_BITS


class Snowflake:
    def __init__(self, data_center_id, worker_id):
        if data_center_id > MAX_DATA_CENTER_ID or data_center_id < 0:
            raise ValueError(f"Data center ID must be between 0 and {MAX_DATA_CENTER_ID}")
        if worker_id > MAX_WORKER_ID or worker_id < 0:
            raise ValueError(f"Worker ID must be between 0 and {MAX_WORKER_ID}")

        self.data_center_id = data_center_id
        self.worker_id = worker_id
        self.sequence = 0
        self.last_timestamp = -1

    def _get_current_timestamp(self):
        return int(time.time() * 1000)

    def _wait_for_next_millis(self, last_timestamp):
        timestamp = self._get_current_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._get_current_timestamp()
        return timestamp

    def next_id(self):
        timestamp = self._get_current_timestamp()

        if timestamp < self.last_timestamp:
            raise Exception("Clock moved backwards. Refusing to generate id for %d milliseconds" % (
                    self.last_timestamp - timestamp))

        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & MAX_SEQUENCE
            if self.sequence == 0:
                timestamp = self._wait_for_next_millis(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        id_num = ((timestamp - START_TIMESTAMP) << TIMESTAMP_SHIFT) | \
                 (self.data_center_id << DATA_CENTER_ID_SHIFT) | \
                 (self.worker_id << WORKER_ID_SHIFT) | \
                 self.sequence

        return id_num

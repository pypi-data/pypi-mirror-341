from enum import Enum


class OverviewWebsocketChannelEnum(str, Enum):
    OVER_ALL = "over_all"  # 儀表板
    RECEPTION_CENTER = "reception_center"  # 接待中心
    CAR_MOVEMENT = "car_movement"  # 車輛動態

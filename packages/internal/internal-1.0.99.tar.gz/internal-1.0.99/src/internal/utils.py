# -*- coding: utf-8 -*-
import json
from datetime import datetime, timezone

import arrow

from .base_config import BaseConfig
from .const import STR_EMPTY, ARR_EXPORT_DATETIME_FMT, STR_DASH, REDIS_LPR_DATA_LIST_PREFIX


def is_today(time, system_time_zone):
    if not time:
        return False

    return arrow.now(system_time_zone).floor("day") == arrow.get(time).to(system_time_zone).floor("day")


def get_tz_day_boundary(date_time, time_zone, out_tz="UTC"):
    """
    傳入date_time，取其在dt_tz時區的當天的floor與ceil，以out_tz時區回傳
    比對區間需使用gte/lte
    """
    date_time = arrow.get(date_time) if date_time else arrow.get()
    tz_time = date_time.to(time_zone)
    return tz_time.floor("day").to(out_tz), tz_time.ceil("day").to(out_tz)


def timestamp_interval(start, end, interval_sec):
    while start < end:
        yield start
        start += interval_sec


def export_time_format(date, time_zone, fmt=ARR_EXPORT_DATETIME_FMT):
    if not date:
        return STR_EMPTY

    return arrow.get(date).to(time_zone).format(fmt)


def update_dict_with_cast(curr_settings: BaseConfig, new_conf: dict):
    if issubclass(type(curr_settings), BaseConfig):
        for key, value in new_conf.items():
            if hasattr(curr_settings, key):
                key_type = type(getattr(curr_settings, key))
                cast_func = key_type if key_type in (str, int) else json.loads
                setattr(curr_settings, key, cast_func(value))


def sanitize_plate_no(plate_no):
    return plate_no.replace(STR_DASH, STR_EMPTY).upper()


def get_current_utc() -> datetime:
    return datetime.now(timezone.utc)


def get_lpr_data_list_redis_key(organization_id, plate_no):
    return f"{REDIS_LPR_DATA_LIST_PREFIX}_{organization_id}_{plate_no}"

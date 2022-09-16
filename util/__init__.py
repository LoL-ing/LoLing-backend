import unicodedata
from typing import List
from datetime import datetime, timedelta

import json
import logging


def group_by_json_list(data: List[dict], key: str):
    result = dict()

    for row in data:
        channel_id = row.get(key)

        if not result.get(channel_id):
            result[channel_id] = [row]
        else:
            result[channel_id].append(row)

    return result


# def xml_to_dict(xml: str):
#     try:
#         if not xml:
#             return dict()

#         parsed_xml = xmltodict.parse(xml, process_namespaces=True)

#         return json.loads(json.dumps(parsed_xml, ensure_ascii=True))

#     except Exception as err:
#         print("파싱 실패: ", repr(err))
#         return {}


def get_daterange_iterator(
    p_start_date: datetime, p_end_date: datetime, format: str = "%Y-%m-%d"
) -> datetime:
    start_date = p_start_date
    end_date = p_end_date

    if isinstance(p_start_date, str):
        start_date = datetime.strptime(p_start_date, format)

    if isinstance(p_end_date, str):
        end_date = datetime.strptime(p_end_date, format)

    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)


def get_daterange(
    p_start_date: datetime, p_end_date: datetime, format: str = "%Y-%m-%d"
) -> datetime:
    start_date = p_start_date
    end_date = p_end_date

    if isinstance(p_start_date, str):
        start_date = datetime.strptime(p_start_date, format)

    if isinstance(p_end_date, str):
        end_date = datetime.strptime(p_end_date, format)

    return int((end_date - start_date).days)


def ljust_print_by_unciode_len(
    p_str: str,
    p_len: int,
    blank_char: str = " ",
    new_line=False,
    color="",
):
    ljust_len = p_len - len(
        list(
            filter(lambda char: unicodedata.east_asian_width(char) in ["W", "F"], p_str)
        )
    )

    print(p_str.ljust(ljust_len, blank_char), end=" | ")

    if new_line:
        print("\n")


def center_print_by_unciode_len(
    p_str: str,
    p_len: int,
    blank_char: str = " ",
    end_char: str = "\n",
    new_line=False,
):

    print(center_str_by_unciode_len(p_str, p_len, blank_char), end=end_char)

    if new_line:
        print("\n")


def center_str_by_unciode_len(
    p_str: str,
    p_len: int,
    blank_char: str = " ",
    color="",
):

    # linux 는 syntax 가 달라서
    # text color 가 python 에서만 먹힘

    # if color != "":
    #     print(
    #         f"\x1b[{color}m" + p_str.center(center_len, blank_char) + "\x1b[0m",
    #         end=" | ",
    #     )

    center_len = p_len - len(
        list(
            filter(lambda char: unicodedata.east_asian_width(char) in ["W", "F"], p_str)
        )
    )

    return p_str.center(center_len, blank_char)


def get_customized_logger():

    # 로그 생성
    logger = logging.getLogger()

    # 로그의 출력 기준 설정
    logger.setLevel(logging.INFO)

    # log 출력 형식
    formatter = logging.Formatter("[ %(asctime)s ] %(message)s")

    # log 출력
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # log를 파일에 출력
    # file_handler = logging.FileHandler('my.log')
    # file_handler.setFormatter(formatter)
    # logger.addHandler(file_handler)

    return logger


if __name__ == "__main__":
    pass

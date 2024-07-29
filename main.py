import os
from typing import Dict, List, Union, Type, Callable

import pymysql
import uvicorn
from fastapi import FastAPI, Query
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()
# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有 HTTP 头
)

# 判断当前操作系统
is_windows = os.name == 'nt'

# 数据库配置
db_config = {
    # 'host': 'mysql.superxiang.com',
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'Lx284190056!' if is_windows else 'Lx284190056!',
    'database': 'lottery'
}


def get_db_connection():
    return pymysql.connect(**db_config)


# 定义响应模型
class NumberFrequency(BaseModel):
    number: str
    frequency: int


class NumberProbability(BaseModel):
    number: str
    probability: float


class CombinedResponse(BaseModel):
    numbers: List[Dict[str, str]]


class ProbabilityResponse(BaseModel):
    numbers: List[Dict[str, str]]


class DetailResponse(BaseModel):
    detail: Dict[str, List[NumberFrequency]]


class ProbabilityDetailResponse(BaseModel):
    detail: Dict[str, List[NumberProbability]]


class CombinedAllResponse(BaseModel):
    numbers: str
    detail: Dict[str, List[Union[NumberFrequency, NumberProbability]]]


@app.get("/")
async def root():
    return {"message": "Hello World"}


def execute_query(query: str) -> List[Dict[str, Union[int, float]]]:
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()
    finally:
        connection.close()


def fetch_data(position: str, count_condition: str, field: str) -> List[Dict[str, Union[int, float]]]:
    query = f"""
        SELECT {position} as number, COUNT(*) as {field}
        FROM (SELECT * FROM ssq {count_condition}) AS sub
        GROUP BY {position}
        ORDER BY {field} DESC
        LIMIT 5;
    """
    return execute_query(query)


def fetch_probability_data(position: str, count_condition: str, field: str) -> List[Dict[str, float]]:
    query = f"""
        SELECT {position} as number, COUNT(*) / (SELECT COUNT(*) FROM (SELECT * FROM ssq {count_condition}) AS sub) as {field}
        FROM (SELECT * FROM ssq {count_condition}) AS sub
        GROUP BY {position}
        ORDER BY {field} DESC
        LIMIT 5;
    """
    return execute_query(query)


def get_combined_response(fetch_function: Callable[[str, str, str], List[Dict[str, Union[int, float]]]],
                          field: str) -> CombinedResponse:
    count_conditions = {
        "全量": "",
        "50": "ORDER BY issue_number DESC LIMIT 50",
        "100": "ORDER BY issue_number DESC LIMIT 100",
        "200": "ORDER BY issue_number DESC LIMIT 200",
        "300": "ORDER BY issue_number DESC LIMIT 300",
        "400": "ORDER BY issue_number DESC LIMIT 400",
        "500": "ORDER BY issue_number DESC LIMIT 500",
    }

    result = []

    for label, count_condition in count_conditions.items():
        positions = ['red1', 'red2', 'red3', 'red4', 'red5', 'red6', 'blue']
        result_numbers = []
        chosen_numbers = set()

        for position in positions:
            data = fetch_function(position, count_condition, field)
            for number, _ in data:
                if number not in chosen_numbers:
                    result_numbers.append(number)
                    chosen_numbers.add(number)
                    break

        numbers = " ".join(result_numbers)
        result.append({label: numbers})

    return CombinedResponse(numbers=result)


def get_detail_response(fetch_function: Callable[[str, str, str], List[Dict[str, Union[int, float]]]], count: int,
                        field: str, response_model: Type[BaseModel]) -> BaseModel:
    positions = ['red1', 'red2', 'red3', 'red4', 'red5', 'red6', 'blue']
    detail = {}
    count_condition = f"ORDER BY issue_number DESC LIMIT {count}" if count > 0 else ""

    for position in positions:
        data = fetch_function(position, count_condition, field)
        detail[position] = [{"number": number, field: value} for number, value in data]

    return response_model(detail=detail)


def get_combined_all_response(fetch_function: Callable[[str, str, str], List[Dict[str, Union[int, float]]]], count: int,
                              field: str) -> CombinedAllResponse:
    count_condition = f"ORDER BY issue_number DESC LIMIT {count}" if count > 0 else ""
    positions = ['red1', 'red2', 'red3', 'red4', 'red5', 'red6', 'blue']
    result_numbers = []
    chosen_numbers = set()
    detail = {}

    for position in positions:
        data = fetch_function(position, count_condition, field)
        for number, _ in data:
            if number not in chosen_numbers:
                result_numbers.append(number)
                chosen_numbers.add(number)
                break
        detail[position] = [{"number": number, field: value} for number, value in data]

    numbers = " ".join(result_numbers)
    return CombinedAllResponse(numbers=numbers, detail=detail)


@app.get("/frequency_numbers", response_model=CombinedResponse)
async def frequency_numbers() -> CombinedResponse:
    return get_combined_response(fetch_data, "frequency")


@app.get("/frequency_detail", response_model=DetailResponse)
async def frequency_detail(count: int = Query(0, description="Number of latest records to consider")) -> BaseModel:
    return get_detail_response(fetch_data, count, "frequency", DetailResponse)


@app.get("/probability_numbers", response_model=ProbabilityResponse)
async def probability_numbers() -> CombinedResponse:
    return get_combined_response(fetch_probability_data, "probability")


@app.get("/probability_detail", response_model=ProbabilityDetailResponse)
async def probability_detail(
        count: int = Query(0, description="Number of latest records to consider")) -> BaseModel:
    return get_detail_response(fetch_probability_data, count, "probability", ProbabilityDetailResponse)


@app.get("/frequency_all", response_model=CombinedAllResponse)
async def frequency_all(
        count: int = Query(0, description="Number of latest records to consider")) -> CombinedAllResponse:
    return get_combined_all_response(fetch_data, count, "frequency")


@app.get("/probability_all", response_model=CombinedAllResponse)
async def probability_all(
        count: int = Query(0, description="Number of latest records to consider")) -> CombinedAllResponse:
    return get_combined_all_response(fetch_probability_data, count, "probability")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=11021)

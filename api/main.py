import uvicorn
from fastapi import FastAPI, Response, UploadFile, File, HTTPException
import pandas as pd
from pydantic import BaseModel
from typing import Any, Dict, List
from fastapi.staticfiles import StaticFiles
import os
from fastapi.responses import JSONResponse

app = FastAPI()
app.mount("/app", StaticFiles(directory="app", html=True), name="app")


# get the dataset
@app.get("/data")
def get_iris_dataset():
    # load the iris dataset
    data = pd.read_csv('data/master.csv')

    return Response(data.to_json(orient="records"), media_type="application/json")


# Создаем папку, если она не существует
if not os.path.exists('refactored_data'):
    os.makedirs('refactored_data')


class DataFrameModel(BaseModel):
    data: List[List[Any]]  # Исправлено на List[List[Any]]
    columns: List[str]     # Добавлена типизация для columns
    index: List[Any]       # Добавлена типизация для index


@app.post("/upload-dataframe/")
async def upload_dataframe(df: DataFrameModel):
    try:
        # Преобразуем полученные данные в DataFrame
        dataframe = pd.DataFrame(data=df.data, columns=df.columns, index=df.index)

        # Определяем имя файла, например, с использованием текущего времени
        filename = f"dataframe_refactored.csv"
        file_path = os.path.join('refactored_data', filename)

        # Сохраняем DataFrame как CSV
        dataframe.to_csv(file_path, index=True)

        return {"filename": filename, "detail": "DataFrame успешно сохранен."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обработке DataFrame: {e}")

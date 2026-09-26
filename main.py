from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import re
import time

app = FastAPI()

templates = Jinja2Templates(directory="templates")


def counting_sort(arr):
    if not arr:
        return []
    min_val = min(arr)
    max_val = max(arr)
    count = [0] * (max_val - min_val + 1)
    for num in arr:
        count[num - min_val] += 1
    result = []
    for i, c in enumerate(count):
        result.extend([min_val + i] * c)
    return result


def parse_numbers(s):
    nums = re.findall(r'-?\d+', s)
    return [int(x) for x in nums]


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "show_result": False,
        "numbers_input": "5 3 8 1 9 2",
        "error": None,
        "original_arr": [],
        "sorted_arr": [],
        "time_ms": 0
    })


@app.post("/sort", response_class=HTMLResponse)
async def sort_numbers(request: Request, numbers: str = Form(...)):
    try:
        arr = parse_numbers(numbers)
        if not arr:
            return templates.TemplateResponse("index.html", {
                "request": request,
                "show_result": False,
                "numbers_input": numbers,
                "error": "Введите числа!",
                "original_arr": [],
                "sorted_arr": [],
                "time_ms": 0
            })
        
        original = arr.copy()
        start = time.time()
        sorted_arr = counting_sort(arr)
        elapsed = (time.time() - start) * 1000
        
        return templates.TemplateResponse("index.html", {
            "request": request,
            "show_result": True,
            "numbers_input": numbers,
            "original_arr": original,
            "sorted_arr": sorted_arr,
            "time_ms": round(elapsed, 3),
            "error": None
        })
    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "show_result": False,
            "numbers_input": numbers,
            "error": str(e),
            "original_arr": [],
            "sorted_arr": [],
            "time_ms": 0
        })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
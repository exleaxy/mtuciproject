from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, crud, database

app = FastAPI()

# Настройка CORS для разрешения запросов с любых источников
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Обновите этот список для разрешенных доменов
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Создание таблиц в базе данных при запуске приложения
models.Base.metadata.create_all(bind=database.engine)

# Инициализация шаблонов Jinja2
templates = Jinja2Templates(directory="templates")

# Главная страница, возвращает index.html из папки templates
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Endpoint для создания кандидата
@app.post("/candidates/")
def create_candidate(candidate: schemas.CandidateCreate, db: Session = Depends(database.get_db)):
    return crud.create_candidate(db=db, candidate=candidate)

# Endpoint для создания вакансии
@app.post("/vacancies/")
def create_vacancy(vacancy: schemas.VacancyCreate, db: Session = Depends(database.get_db)):
    return crud.create_vacancy(db=db, vacancy=vacancy)

# Endpoint для получения аналитики
@app.get("/analytics/")
def get_analytics(db: Session = Depends(database.get_db)):
    return crud.get_analytics(db=db)

# Endpoint для парсинга данных о вакансиях с HH.ru
@app.post("/fetch_vacancies/", response_model=schemas.VacancyQuery)
def fetch_vacancies(query: schemas.VacancyQuery, db: Session = Depends(database.get_db)):
    try:
        crud.create_vacancy_from_hh_and_save(db=db, query=query)
        return {"message": "Vacancies fetched and saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Endpoint для получения всех вакансий
@app.get("/vacancies/")
def read_vacancies(db: Session = Depends(database.get_db)):
    vacancies = crud.get_vacancies(db)
    return {"vacancies": vacancies}

# Endpoint для отображения вакансий на странице
@app.get("/vacancies_page/")
def vacancies_page(request: Request, db: Session = Depends(database.get_db)):
    vacancies = crud.get_vacancies(db)
    return templates.TemplateResponse("vacancies.html", {"request": request, "vacancies": vacancies})


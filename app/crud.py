import requests
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal

def create_candidate(db: Session, candidate: schemas.CandidateCreate):
    db_candidate = models.Candidate(
        full_name=candidate.full_name,
        skills=candidate.skills,
        experience=candidate.experience,
        education=candidate.education
    )
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    return db_candidate

def create_vacancy(db: Session, vacancy: schemas.VacancyCreate):
    db_vacancy = models.Vacancy(
        job_title=vacancy.job_title,
        requirements=vacancy.requirements,
        salary=vacancy.salary,
        work_format=vacancy.work_format
    )
    db.add(db_vacancy)
    db.commit()
    db.refresh(db_vacancy)
    return db_vacancy

def fetch_vacancies_from_hh(query: schemas.VacancyQuery):
    url = "https://api.hh.ru/vacancies"
    params = {
        "text": query.text,
        "area": query.area,
        "per_page": query.per_page
    }
    response = requests.get(url, params=params)
    return response.json()

def create_vacancy_from_hh(db: Session, query: schemas.VacancyQuery):
    data = fetch_vacancies_from_hh(query)
    for item in data.get("items", []):
        salary_info = item.get("salary", {})
        salary = None
        if salary_info:
            if salary_info.get("from") and salary_info.get("to"):
                salary = f"{salary_info['from']} - {salary_info['to']} {salary_info['currency']}"
            elif salary_info.get("from"):
                salary = f"от {salary_info['from']} {salary_info['currency']}"
            elif salary_info.get("to"):
                salary = f"до {salary_info['to']} {salary_info['currency']}"
        else:
            salary = "нет"
        vacancy = schemas.VacancyCreate(
            job_title=item["name"],
            requirements=item.get("snippet", {}).get("requirement", ""),
            salary=salary,
            work_format=item.get("employment", {}).get("name", "")
        )
        create_vacancy(db, vacancy)

def get_analytics(db: Session):
    candidate_count = db.query(models.Candidate).count()
    vacancy_count = db.query(models.Vacancy).count()
    return {"candidates": candidate_count, "vacancies": vacancy_count}

def get_vacancies(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Vacancy).offset(skip).limit(limit).all()

def create_vacancy_from_hh_and_save(db: Session, query: schemas.VacancyQuery):
    vacancies = parse_vacancies_from_hh(query.query)  # Предполагаемая функция для парсинга
    for vacancy in vacancies:
        db_vacancy = models.Vacancy(**vacancy.dict())
        db.add(db_vacancy)
    db.commit()
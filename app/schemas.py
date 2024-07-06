from pydantic import BaseModel

class CandidateBase(BaseModel):
    full_name: str
    skills: str
    experience: str
    education: str

class CandidateCreate(CandidateBase):
    pass

class Candidate(CandidateBase):
    id: int

    class Config:
        orm_mode = True

class VacancyBase(BaseModel):
    job_title: str
    requirements: str
    salary: str
    work_format: str

class VacancyCreate(VacancyBase):
    pass

class VacancyQuery(BaseModel):
    query: str

class Vacancy(BaseModel):
    id: int
    title: str
    description: str
    company: str

    class Config:
        orm_mode = True

from fastapi import APIRouter, BackgroundTasks
from services import jobService

router = APIRouter()

@router.get('/jobs', tags=['jobs'])
def get_jobs():
    return { 'jobs': jobService.jobs_cache}

@router.post('/jobs/update', tags=['jobs'])
def scrape_jobs(background_tasks: BackgroundTasks):
    background_tasks.add_task(jobService.start_scrape)
    return { 'message': 'Job scraping started'}
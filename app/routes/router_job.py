
from fastapi import APIRouter, BackgroundTasks
from services import jobService

router = APIRouter()
scraper = jobService.JobScraper()

@router.get('/jobs', tags=['jobs'])
def get_jobs():
    return { 'jobs': scraper.jobs_cache}

@router.post('/jobs/update', tags=['jobs'])
def scrape_jobs(background_tasks: BackgroundTasks):
    background_tasks.add_task(scraper.start_scrape)
    return { 'message': 'Job scraping started'}
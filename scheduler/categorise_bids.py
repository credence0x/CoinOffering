from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from Bid import allocate
import apscheduler.schedulers.blocking


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(allocate.run, 'interval', seconds=20,id='bid_scheduler_id')
    scheduler.start()
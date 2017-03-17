import os
import sys

from celery import Celery

import library.XmlMovers as XmlMovers
import library.SqlWriters as SqlWriters

app = Celery('CeleryTasks', broker='pyamqp://guest@localhost//')

@app.task(bind=True, max_retries=3)
def extract_inning(self, gid_url):
    try:
        res = XmlMovers.InningWriter(gid_url).process()
    except:
        self.retry(exc=sys.exc_info()[0])

@app.task(bind=True, max_retries=3)
def extract_boxscore(self, gid_url):
    try:
        XmlMovers.BoxscoreWriter(gid_url).process()
    except:
        self.retry(exc=sys.exc_info()[0])

@app.task(bind=True, max_retries=3)
def extract_linescore(self, gid_url):
    try:
        XmlMovers.LinescoreWriter(gid_url).process()
    except:
        self.retry(exc=sys.exc_info()[0])

@app.task(bind=True, max_retries=3)
def extract_player(self, gid_url):
    try:
        XmlMovers.PlayersWriter(gid_url).process()
    except:
        self.retry(exc=sys.exc_info()[0])

@app.task(bind=True, max_retries=3)
def table_inning(self, _, gid_path):
    try:
        SqlWriters.InningWriter(gid_path).process()
    except:
        self.retry(exc=sys.exc_info()[0])

@app.task(bind=True, max_retries=3)
def table_boxscore(self, _, gid_path):
    try:
        SqlWriters.RawBoxscoreWriter(gid_path).process()
    except:
        self.retry(exc=sys.exc_info()[0])

@app.task(bind=True, max_retries=3)
def table_player(self, _, gid_path):
    try:
        SqlWriters.PlayerWriter(gid_path).process()
    except:
        self.retry(exc=sys.exc_info()[0])

@app.task(bind=True, max_retries=3)
def table_linescore(self, _, gid_path):
    try:
        SqlWriters.LinescoreWriter(gid_path).process()
    except:
        self.retry(exc=sys.exc_info()[0])

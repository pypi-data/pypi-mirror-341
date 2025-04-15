import sqlite3
from typing import List, Dict
import os

class PatentDatabase:
    def __init__(self, db_path: str = 'patents.db'):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """
        Initialize the database with the required schema
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS patents (
                    document_no TEXT PRIMARY KEY,
                    title TEXT,
                    country_code TEXT,
                    current_assignee TEXT,
                    document_status TEXT,
                    application_status TEXT,
                    cpc_first TEXT,
                    cpc_inventive TEXT,
                    file_date TEXT,
                    grant_date TEXT,
                    pscore REAL,
                    cscore REAL,
                    lscore REAL,
                    tscore REAL,
                    prior_art_score REAL,
                    pendency INTEGER,
                    category TEXT
                )
            """)
            conn.commit()

    async def store_patents(self, patents: List[Dict]):
        """
        Store patent records in the database
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            for patent in patents:
                cursor.execute("""
                    INSERT OR REPLACE INTO patents (
                        document_no, title, country_code, current_assignee,
                        document_status, application_status, cpc_first,
                        cpc_inventive, file_date, grant_date, pscore,
                        cscore, lscore, tscore, prior_art_score,
                        pendency, category
                    ) VALUES (
                        :document_no, :title, :country_code, :current_assignee,
                        :document_status, :application_status, :cpc_first,
                        :cpc_inventive, :file_date, :grant_date, :pscore,
                        :cscore, :lscore, :tscore, :prior_art_score,
                        :pendency, :category
                    )
                """, patent)
            conn.commit()
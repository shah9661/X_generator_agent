import os
from datetime import datetime
from dotenv import load_dotenv
import psycopg2
import psycopg2.extras

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    """Return a new psycopg2 connection."""
    return psycopg2.connect(DATABASE_URL)


def init_db():
    """
    Create the tweets table if it doesn't exist.
    Call this once at server startup.
    """
    sql = """
        CREATE TABLE IF NOT EXISTS tweets (
            id               SERIAL PRIMARY KEY,
            topic            TEXT        NOT NULL,
            final_tweet      TEXT        NOT NULL,
            status           TEXT        NOT NULL,
            iterations_used  INT         NOT NULL,
            max_iteration    INT         NOT NULL,
            tweet_history    TEXT[]      NOT NULL DEFAULT '{}',
            feedback_history TEXT[]      NOT NULL DEFAULT '{}',
            created_at       TIMESTAMP   NOT NULL DEFAULT NOW()
        );
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()
    finally:
        conn.close()



def save_tweet(result: dict) -> int:
    """
    Save a pipeline result to the tweets table.
    Returns the new row's id.
    """
    sql = """
        INSERT INTO tweets
            (topic, final_tweet, status, iterations_used, max_iteration,
             tweet_history, feedback_history)
        VALUES
            (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (
                result["topic"],
                result["final_tweet"],
                result["status"],
                result["iterations_used"],
                result["max_iteration"],
                result["tweet_history"],
                result["feedback_history"],
            ))
            new_id = cur.fetchone()[0]
        conn.commit()
        return new_id
    finally:
        conn.close()


def get_history(limit: int = 20) -> list[dict]:
    """
    Fetch the most recent tweets, newest first.
    Returns a list of dicts ready to send as JSON.
    """
    sql = """
        SELECT
            id, topic, final_tweet, status,
            iterations_used, max_iteration,
            tweet_history, feedback_history,
            created_at
        FROM tweets
        ORDER BY created_at DESC
        LIMIT %s;
    """
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, (limit,))
            rows = cur.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


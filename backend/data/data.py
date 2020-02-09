from typing import NewType, List
import sqlite3

Trust = NewType('Trust', float)

database = sqlite3.connect('data.db')

def configure_db():
    c = database.cursor()
    c.execute("CREATE TABLE Source (url, trust)")
    c.execute("CREATE TABLE Classification (url, source, trust, time)")
    c.execute("CREATE TABLE Document (url, source, vectors, time)")
    c.close()
    database.commit()

class Source:
    url: str
    trust: Trust

    def __init__(self, url: str, trust: Trust):
        self.url = url
        self.trust = trust

    def __eq__(self, other):
        return isinstance(other, Source) \
            and self.url == other.url \
            and self.trust == other.trust

    @classmethod
    def retrieve(cls, url):
        cursor = database.cursor()
        try:
            cursor.execute(f"SELECT Source.url, Source.trust FROM Source")
            fetched = cursor.fetchone()
            if not fetched: return
            (url, trust) = cursor.fetchone()
            return Source(url, trust)
        finally:
            cursor.close()

    @classmethod
    def new(cls, url: str, trust: Trust):
        cursor = database.cursor()
        try:
            cursor.execute(f"INSERT INTO Source (url, trust) VALUES (\"{url}\", \"{trust}\")")
            database.commit()
            return cls(url, trust)
        finally:
            cursor.close()


class Document:
    url: str
    source: Source
    time: int
    vector: List[int]

    def __init__(self, source: Source, url: str, time: int, vector: List[int]):
        self.url = url
        self.source = source
        self.time = time
        self.vector = vector

    @classmethod
    def retrieve(cls, url):
        cursor = database.cursor()
        try:
            cursor.execute("SELECT Document.url, Document.vectors, Document.time, Source.url, Source.trust FROM Document, Source WHERE Document.source = Source.url")
            fetched = cursor.fetchone()
            if not fetched: return
            (url, vector, time, source_url, source_trust) = fetched
            return cls(Source(source_url, source_trust), url, time, (v.split(",") for v in vector.split("|")))
        finally:
            cursor.close()

    @classmethod
    def new(cls, source, url, time, vectors):
        cursor = database.cursor()
        try:
            cursor.execute(f"""INSERT INTO Document(url, source, time, vectors) 
                                VALUES ("{url}", "{source}", "{time}", "{'|'.join(','.join(str(e) for e in v) for v in vectors)}")
                                """)
            database.commit()
            return cls(source, url, time, vectors)
        finally:
            cursor.close()

class Classification:
    source: Source
    url: str
    trust: Trust
    time: int
    
    def __init__(self, source: Source, url: str, trust: Trust, time: int):
        self.source = source
        self.url = url
        self.trust = trust
        self.time = time

    @classmethod
    def retrieve(cls, url):
        cursor = database.cursor()
        try:
            cursor.execute(
                f"""SELECT Classification.url, Classification.trust, Classification.time, Source.url, Source.trust
                FROM Classification, Source 
                WHERE Classification.source == Source.url AND Classification.url = \"{url}\""""
                )
            fetched = cursor.fetchone()
            if not fetched: return
            (url, trust, time, source, source_trust) = fetched
            return cls(Source(source, Trust(float(source_trust))), url, Trust(float(trust)), int(time))
        finally:
            cursor.close()

    @classmethod
    def retrieve_all(cls):
        cursor = database.cursor()
        try:
            cursor.execute(
                """SELECT Classification.url, Classification.trust, Classification.time, Source.url, Source.trust
                FROM Classification, Source 
                WHERE Classification.source == Source.url"""
                )
            for (url, trust, time, source, source_trust) in cursor.fetchall():
                yield cls(Source(source, Trust(float(source_trust))), url, Trust(float(trust)), int(time))
        finally:
            cursor.close()

    @classmethod
    def new(cls, source, url, trust, time):
        cursor = database.cursor()
        try:
            cursor.execute(f"""INSERT INTO Classification(source, url, trust, time) 
                            VALUES ("{source}", "{url}", "{trust}", "{time}")
                            """)
            database.commit()
            return cls(source, url, time, time)
        finally:
            cursor.close()

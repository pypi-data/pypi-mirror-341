import json
import os
import sqlite3
import threading
import uuid
from concurrent.futures import ThreadPoolExecutor

import pandas as pd

from .progress import tqdm

DBFILE = "/tmp/maputil.db"

SCHEMA = """
create table if not exists item(key text primary key, val text);
create table if not exists run(name text primary key, size integer, created_at timestamp default current_timestamp);
"""


def conn():
    create_tables = False
    if not os.path.exists(DBFILE):
        create_tables = True

    db = sqlite3.connect(DBFILE, check_same_thread=False)
    if create_tables:
        db.executescript(SCHEMA)
        db.commit()
    return db


def clear():
    try:
        os.remove(DBFILE)
    except FileNotFoundError:
        pass


def newid():
    return uuid.uuid4().hex


def to_run(row):
    if row is None:
        return None
    name, size = row
    return {"name": name, "size": size}


def new_run(db, resume, size):
    assert isinstance(db, sqlite3.Connection)
    assert isinstance(resume, bool) or isinstance(resume, str)
    assert isinstance(size, int)

    run = None
    if resume is True:
        # if resume is True, automatically use the last run.
        cur = db.execute("select name,size from run order by created_at desc limit 1")
        run = to_run(cur.fetchone())
        if run is None:
            # if there is no last run, create a new one.
            resume = newid()
    elif isinstance(resume, str):
        # if resume is a string, use the run with that name. If it doesn't exist, create a new one.
        cur = db.execute("select name,size from run where name=?", (resume,))
        run = to_run(cur.fetchone())
    else:
        # otherwise always create a new run.
        resume = newid()

    if run is None:
        db.execute("insert into run(name,size) values(?,?)", (resume, size))
        db.commit()
        return resume
    else:
        # if run is not None, check that the size matches.
        assert run["size"] == size
        return run["name"]


def set_item(db, key, jsonval):
    assert isinstance(db, sqlite3.Connection)
    assert isinstance(key, str)
    assert isinstance(jsonval, str)

    db.execute("insert into item(key,val) values(?,?)", (key, jsonval))
    db.commit()


def get_item(db, key):
    assert isinstance(db, sqlite3.Connection)
    assert isinstance(key, str)

    cur = db.execute("select val from item where key=?", (key,))
    row = cur.fetchone()
    if row is None:
        return None
    (jsonval,) = row
    return jsonval


def select(fn, inputs, resume=False, progress=False, concurrency=1):
    """
    Apply a function to a collection of inputs with caching and optional concurrency.

    Parameters:
    -----------
    fn : callable
        The function to apply to each input element.
    inputs : list or pandas.Series
        The collection of input values to process.
    resume : bool or str, default=False
        If True, resume the last run. If a string, resume the run with that name.
        If False, create a new run with a random identifier.
    progress : bool, default=False
        Whether to display a progress bar during execution.
    concurrency : int, default=1
        Number of concurrent workers. If greater than 1, processing is done in parallel.

    Returns:
    --------
    list or pandas.Series
        If inputs was a list, returns a list of results.
        If inputs was a pandas.Series, returns a pandas.Series with the same index.

    Notes:
    ------
    Results are cached in a SQLite database based on the resume identifier and input position.
    Subsequent calls with the same resume identifier will use cached results without recomputation.
    The caching is persistent across program restarts, making it useful for long-running or failure-prone processes.
    """
    assert callable(fn)
    assert isinstance(inputs, list) or isinstance(inputs, pd.Series)
    assert isinstance(resume, bool) or isinstance(resume, str)
    assert isinstance(progress, bool)
    assert isinstance(concurrency, int) and concurrency > 0

    index = None
    if isinstance(inputs, pd.Series):
        index = inputs.index
        inputs = inputs.tolist()

    pbar = None
    if progress:
        pbar = tqdm(total=len(inputs))

    dblock = threading.Lock()
    with conn() as db:
        runid = new_run(db, resume, len(inputs))
        print("runid:", runid)

        def memfn(item):
            idx, input = item
            key = f"{runid}:{idx}"

            with dblock:
                # try to get cached result
                jsonval = get_item(db, key)

            if jsonval is None:
                # if not cached, compute result
                val = fn(input)

                with dblock:
                    # save result to cache
                    jsonval = json.dumps(val)
                    set_item(db, key, jsonval)
            else:
                # if cached, load result
                val = json.loads(jsonval)

            if progress:
                pbar.update(1)
            return val

        if concurrency == 1:
            outputs = [memfn(item) for item in enumerate(inputs)]
        else:
            with ThreadPoolExecutor(max_workers=concurrency) as executor:
                outputs = list(executor.map(memfn, enumerate(inputs)))

    if progress:
        pbar.close()

    # return either a list or Series which should match the input type
    if index is None:
        return outputs
    else:
        return pd.Series(outputs, index=index)

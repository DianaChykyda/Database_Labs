import psycopg2
import threading
import time

DB_PARAMS = {
    'dbname': 'mydatabase',       
    'user': 'myuser',             
    'password': 'mypassword',     
    'host': 'localhost',          
    'port': 5432                  
}


def get_counter_value():
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()
    cur.execute("SELECT counter FROM user_counter WHERE user_id = 1;")
    counter = cur.fetchone()[0]
    cur.close()
    conn.close()
    return counter


def reset_counter():
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()
    cur.execute("UPDATE user_counter SET counter = 0 WHERE user_id = 1;")
    conn.commit()
    cur.close()
    conn.close()


def measure_time(func, name, threads=10, updates_per_thread=10000):
    reset_counter()  
    start_time = time.time()
    
    thread_list = []
    for _ in range(threads):
        t = threading.Thread(target=func, args=(updates_per_thread,))
        thread_list.append(t)
        t.start()
    for t in thread_list:
        t.join()
    
    elapsed_time = time.time() - start_time
    final_counter = get_counter_value() 
    
    print(f"{name}: {elapsed_time:.2f} сек, Кінцеве значення counter: {final_counter}")


def lost_update(updates):
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()
    for _ in range(updates):
        cur.execute("SELECT counter FROM user_counter WHERE user_id = 1;")
        counter = cur.fetchone()[0] + 1
        cur.execute("UPDATE user_counter SET counter = %s WHERE user_id = 1;", (counter,))
        conn.commit()
    cur.close()
    conn.close()


def in_place_update(updates):
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()
    for _ in range(updates):
        cur.execute("UPDATE user_counter SET counter = counter + 1 WHERE user_id = 1;")
        conn.commit()
    cur.close()
    conn.close()


def row_level_locking(updates):
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()
    for _ in range(updates):
        cur.execute("SELECT counter FROM user_counter WHERE user_id = 1 FOR UPDATE;")
        counter = cur.fetchone()[0] + 1
        cur.execute("UPDATE user_counter SET counter = %s WHERE user_id = 1;", (counter,))
        conn.commit()
    cur.close()
    conn.close()


def optimistic_concurrency_control(updates):
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()
    for _ in range(updates):
        while True:
            cur.execute("SELECT counter, version FROM user_counter WHERE user_id = 1;")
            counter, version = cur.fetchone()
            counter += 1
            cur.execute("UPDATE user_counter SET counter = %s, version = %s WHERE user_id = 1 AND version = %s;", 
                        (counter, version + 1, version))
            conn.commit()
            if cur.rowcount > 0:
                break
    cur.close()
    conn.close()


if __name__ == "__main__":
    print("Виконання тестів:")
    measure_time(lost_update, "Lost Update")
    measure_time(in_place_update, "In-Place Update")
    measure_time(row_level_locking, "Row-Level Locking")
    measure_time(optimistic_concurrency_control, "Optimistic Concurrency Control")
    print("-------------")

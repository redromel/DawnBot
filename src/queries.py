CREATE_BIRTHDAYS_TABLE = '''
    CREATE TABLE IF NOT EXISTS birthdays (
        user_id BIGINT PRIMARY KEY,
        month INTEGER NOT NULL,
        day INTEGER NOT NULL
    )
'''

INSERT_BIRTHDAY = '''
    INSERT INTO birthdays (user_id, month, day)
    VALUES (%s, %s, %s)
    ON CONFLICT (user_id) DO UPDATE
    SET month = EXCLUDED.month, day = EXCLUDED.day
'''

SELECT_BIRTHDAY = '''
    SELECT month, day FROM birthdays WHERE user_id = %s
'''

CHECK_BIRTHDAY = '''
    SELECT user_id, month, day FROM birthdays WHERE month = %s AND day = %s
'''

ALL_BIRTHDAYS = '''
    SELECT user_id, month, day FROM birthdays
'''

UPCOMING_BIRTHDAYS = '''
    SELECT user_id, month, day FROM birthdays
    WHERE 
        (month = %s AND day >= %s)
        OR
        (month = %s)
'''

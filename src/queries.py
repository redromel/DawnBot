CREATE_BIRTHDAYS_TABLE = '''
    CREATE TABLE IF NOT EXISTS birthdays (
        user_id BIGINT PRIMARY KEY,
        month INTEGER NOT NULL,
        day INTEGER NOT NULL
    )
'''

CREATE_ANNOUNCEMENT_CHANNELS_TABLE = '''
    CREATE TABLE IF NOT EXISTS announcement_channels (
        guild_id BIGINT PRIMARY KEY,
        channel_id BIGINT NOT NULL
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

DELETE_BIRTHDAY = '''
    DELETE FROM birthdays WHERE user_id = %s
'''

INSERT_ANNOUNCEMENT_CHANNEL = '''
    INSERT INTO announcement_channels (guild_id, channel_id)
    VALUES (%s, %s)
    ON CONFLICT (guild_id) DO UPDATE
    SET channel_id = EXCLUDED.channel_id
'''

DELETE_ANNOUNCEMENT_CHANNEL = '''
    DELETE FROM announcement_channels WHERE guild_id = %s
''' 

CHECK_ANNOUNCEMENT_CHANNEL = '''
    SELECT channel_id FROM announcement_channels WHERE guild_id = %s
'''

GET_ALL_ANNOUNCEMENT_CHANNELS = '''
    SELECT guild_id, channel_id FROM announcement_channels
'''
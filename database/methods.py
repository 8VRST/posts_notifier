import logging
from datetime import timezone, datetime, timedelta, date

from database.connection import connect_to_db


def create_database(name):
    connect = connect_to_db(create_db=True)
    connect.autocommit = True
    cursor = connect.cursor()
    cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = '%s'" % (name,))
    exists = cursor.fetchone()
    if not exists:
        cursor.execute("CREATE DATABASE %s" % (name,))
        connect.close()
        logging.info(msg="Database %s has been successfully created" % (name,))
    else:
        connect.close()
        logging.info(msg="Database with name %s is already exists" % (name,))


def create_table(name, columns):
    connect = connect_to_db()
    cursor = connect.cursor()
    table_to_create = "create table if not exists %s " % (name,)
    columns_to_set = "(%s)" % (", ".join(columns))
    cursor.execute("%s %s" % (table_to_create, columns_to_set))
    connect.commit()
    connect.close()
    logging.info(msg="Table %s has been successfully created" % (name,))


def select_data(table, column, condition=None, condition_column=None, check_if_exists=None, user_settings=None,
                by_timestamp=None, date_min=None, date_max=None):
    connect = connect_to_db()
    cursor = connect.cursor()
    if condition:
        sql = "select %s from %s where %s = %s" % (column, table, condition_column, condition,)
    else:
        sql = "select %s from %s" % (column, table,)
        if by_timestamp:
            sql = "%s where timestamp between date '%s' and date '%s'" % (sql, date_min, date_max,)
        else:
            sql = sql
    cursor.execute(sql)
    if check_if_exists:
        exists = cursor.fetchone()
        connect.close()
        if exists:
            return True
        else:
            return False
    if user_settings:
        setting = cursor.fetchone()[0]
        connect.close()
        return setting
    rows = cursor.fetchall()
    data = [row[0] for row in rows]
    connect.close()
    return data


def insert_posts(new_posts):
    send_posts = []
    connect = connect_to_db()
    cursor = connect.cursor()
    data = select_data(table="links", column="link")
    for post in new_posts:
        if post not in data:
            send_posts.append(post)
            cursor.execute("insert into links (link, timestamp) values ('%s', '%s')" % (post, datetime.now(timezone.utc),))
    connect.commit()
    connect.close()
    logging.info(msg="Data %s has been successfully set in table links" % (new_posts,))
    return send_posts


def insert_user(user_id):
    connect = connect_to_db()
    cursor = connect.cursor()
    cursor.execute("insert into users (telegram_id, last_action) values (%s, '%s')" % (user_id, datetime.now(timezone.utc),))
    connect.commit()
    connect.close()
    logging.info(msg="User %s has been successfully added" % (user_id,))


def update_user(user_id, status=None, lang=None, greet_status=None):
    connect = connect_to_db()
    cursor = connect.cursor()
    if status==True or status==False:
        sql = "update users set status = (%s), last_action = ('%s') where telegram_id = (%s)" % (status, datetime.now(timezone.utc), user_id,)
        user_exists = select_data(table="users", column="telegram_id", condition=user_id, condition_column="telegram_id", check_if_exists=True)
        if user_exists==True:
            cursor.execute(sql)
        else:
            insert_user(user_id)
            cursor.execute(sql)
    elif greet_status==True or greet_status==False:
        sql = "update users set greet_status = (%s), last_action = ('%s') where telegram_id = (%s)" % (greet_status, datetime.now(timezone.utc), user_id,)
        cursor.execute(sql)
    elif lang:
        sql = "update users set lang = ('%s'), last_action = ('%s') where telegram_id = (%s)" % (lang, datetime.now(timezone.utc), user_id,)
        cursor.execute(sql)
    else:
        logging.error(msg="No action where provided for this method")
    connect.commit()
    connect.close()
    logging.info(msg="Data for user %s was successfully changed to %s" % (user_id, status,))


def delete_old_posts():
    connect = connect_to_db()
    cursor = connect.cursor()
    sql = "delete from links where timestamp <= timestamp '%s 00:00:00'" % (date.today() - timedelta(days=14)).strftime("%Y-%m-%d")
    cursor.execute(sql)
    connect.commit()
    connect.close()
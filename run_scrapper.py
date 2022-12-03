import time
from datetime import date
import random

from scrappers.posts_scrapper import ScrapPosts
from database.methods import insert_posts, select_data, delete_old_posts
from telegram.push_msg import push_posts


current_day = None


while True:
    new_posts = ScrapPosts().new_posts()
    send_posts = insert_posts(new_posts)
    select_users = select_data(table="users", column="telegram_id", condition=True, condition_column="status")
    if send_posts!=[]:
        for user in select_users:
            push_posts(user=user, posts=send_posts)
    else:
        pass
    if current_day != date.today().strftime("%d"):
        delete_old_posts()
        current_day = date.today().strftime("%d")
    else:
        pass
    time.sleep(random.randint(250, 350))
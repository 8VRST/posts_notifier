import logging

import requests
from bs4 import BeautifulSoup

from utils.json_pocessing import open_json_file


class ScrapPosts:

    def __init__(self):
        config = open_json_file("scrappers/config.json")
        urls = config["urls"]

        self.kufar_url = urls["kufar"]
        self.realtby_url = urls["realtby"]
        self.gohome_url = urls["gohome"]
        self.hataby_url = urls["hataby"]
        self.irrby_url = urls["irrby"]
        self.forumgrodno_url = urls["forumgrodno"]
        self.vkcom_url = urls["vkcom"]
        self.spam_words = config["spam_words"]
        self.headers = config["headers"]
        self.not_200_status_msg = "{} response from {}"

    def new_posts(self):
        empty_urls_types = [[], ""]

        kufar = self.__kufar() if self.kufar_url not in empty_urls_types else []
        realt_by = self.__realtby() if self.realtby_url not in empty_urls_types else []
        gohomeby = self.__gohomeby() if self.gohome_url not in empty_urls_types else []
        hataby = self.__hataby() if self.hataby_url not in empty_urls_types else []
        irrby = self.__irrby() if self.irrby_url not in empty_urls_types else []
        forumgrodno = self.__forumgrodno() if self.forumgrodno_url not in empty_urls_types else []
        vkcom = self.__vkcom() if self.vkcom_url not in empty_urls_types else []

        posts = kufar + realt_by + gohomeby + hataby + irrby + forumgrodno + vkcom

        return posts

    def __data_from_request(self, link, verify=None, headers=None):
        if headers:
            response = requests.get(link, headers=self.headers)
        elif verify:
            response = requests.get(link, verify=verify)
        else:
            response = requests.get(link)
        status_code = response.status_code
        data = BeautifulSoup(response.text, "html.parser")
        return data, status_code

    def __kufar(self):
        posts_list = []
        data, status_code = self.__data_from_request(self.kufar_url, headers=True)
        if status_code==200:
            try:
                anchor_tag = data.find_all("section")
                for post in anchor_tag:
                    post_link = str(post.find("a").get("href"))
                    if "?rank=" in post_link:
                        post_link = post_link.split("?rank=")[0]
                    posts_list.append(post_link)
                return posts_list[:11]
            except Exception as error:
                logging.info(msg=error)
                return []
        else:
            logging.info(msg=self.not_200_status_msg.format(status_code, "Kufar"))
            return []

    def __realtby(self):
        posts_list = []
        data, status_code = self.__data_from_request(self.realtby_url, headers=True)
        if status_code==200:
            try:
                posts_div_list = data.find("div", {"class": "listing view-format"}).find_all("a",  {"class": "teaser-title"})
                for post in posts_div_list:
                    post_link = str(post.get("href"))
                    posts_list.append(post_link)
                return posts_list
            except Exception as error:
                logging.info(msg=error)
                return []
        else:
            logging.info(msg=self.not_200_status_msg.format(status_code, "Realtby"))
            return []

    def __gohomeby(self):
        posts_list = []
        data, status_code = self.__data_from_request(self.gohome_url, verify=False)
        if status_code == 200:
            try:
                posts_div_list = data.find_all("div", {"class": "w-name"})
                for post in posts_div_list:
                    post_link = "https://gohome.by" + str(post.find("a").get("href"))
                    posts_list.append(post_link)
                return posts_list
            except Exception as error:
                logging.info(msg=error)
                return []
        else:
            logging.info(msg=self.not_200_status_msg.format(status_code, "Gohomeby"))
            return []

    def __hataby(self):
        posts_list = []
        data, status_code = self.__data_from_request(self.hataby_url, headers=True)
        if status_code == 200:
            try:
                posts_div_list = data.find_all("div", {"class": "text"})
                for post in posts_div_list:
                    post_link = str(post.find("a").get("href"))
                    posts_list.append(post_link)
                return posts_list
            except Exception as error:
                logging.info(msg=error)
                return []
        else:
            logging.info(msg=self.not_200_status_msg.format(status_code, "Hataby"))
            return []

    def __irrby(self):
        posts_list = []
        data, status_code = self.__data_from_request(self.irrby_url, headers=True)
        if status_code == 200:
            try:
                for post_position in range(1, 5):
                    post_anchor_div = data.find("div", {"class": "adds_cont clear"}).find("div", {"data-position": str(post_position)})
                    post_link = post_anchor_div.find("a").get("href")
                    posts_list.append(post_link)
                return posts_list
            except Exception as error:
                logging.info(msg=error)
                return []
        else:
            logging.info(msg=self.not_200_status_msg.format(status_code, "Irrby"))
            return []

    def __forumgrodno(self):
        posts_list = []
        data, status_code = self.__data_from_request(self.forumgrodno_url, headers=True)
        if status_code == 200:
            try:
                posts_div_list = data.find_all("span", {"class": "topic_name"})
                for post in posts_div_list:
                    post_link = str(post.find("a").get("href"))
                    if "PHPSESSID=" in post_link:
                        post_link = post_link.split("PHPSESSID=")[0] + post_link.split("&")[1]
                    posts_list.append(post_link)
                return posts_list[1:11]
            except Exception as error:
                logging.info(msg=error)
                return []
        else:
            logging.info(msg=self.not_200_status_msg.format(status_code, "ForumGrodno"))
            return []

    def __vkcom(self):
        posts_list = []
        filtered_posts = []
        for url in self.vkcom_url:
            data_wall, status_code = self.__data_from_request(url, headers=True)
            if status_code == 200:
                try:
                    posts_div_list = data_wall.find_all("div", {"class": "post_date"})
                    for post in posts_div_list:
                        post_link = "https://vk.com" + str(post.find("a").get("href"))
                        filtered_posts.append(post_link)
                except Exception as error:
                    logging.info(msg=error)
                    continue
            else:
                logging.info(msg=self.not_200_status_msg.format(status_code, url))
                continue

        filtered_posts = set(filtered_posts)

        if filtered_posts!=():
            for post in filtered_posts:
                data, status_code = self.__data_from_request(post, headers=True)
                if status_code == 200:
                    try:
                        try:
                            post_text = str.lower(data.find("div", {"class": "wall_post_text zoom_text"}).text)
                        except Exception:
                            post_text = None

                        if post_text==None:
                            pass
                        else:
                            if [spam_word for spam_word in self.spam_words if spam_word in post_text.split()]!=[]:
                                pass
                            else:
                                posts_list.append(post)
                    except Exception as error:
                        logging.info(msg=error)
                        continue
                else:
                    logging.info(msg=self.not_200_status_msg.format(status_code, post))
                    continue
            return posts_list
        else:
            return []
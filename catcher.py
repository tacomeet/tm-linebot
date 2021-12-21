import random
import sys

import requests

import question

BASE_URL = 'https://teenmakers.jp/wp-json/wp/v2/'
DEFAULT_PER_PAGE = 10


class Catcher:
    def __init__(self, uid, tags, age):
        self.id = uid
        self.tags = tags
        self.age = age

    def add_tag(self, tag):
        self.tags.append(tag)


class Catchers:
    def __init__(self):
        self.catchers = {}
        self.candidates = []
        self.cand_by_user = {}
        self.used_tags = {}
        res_num = DEFAULT_PER_PAGE
        offset = 0
        while res_num == DEFAULT_PER_PAGE:
            res = requests.get(BASE_URL + 'posts?offset=' + str(offset), timeout=5)
            if res.status_code != requests.codes.ok:
                print('Error: ' + str(res.status_code))
                break
            js = res.json()
            res_num = len(js)
            offset += DEFAULT_PER_PAGE
            for j in js:
                uid = j['id']
                age = j['acf']['age']
                tags = j['tags']
                c = Catcher(uid, tags, age)
                self.catchers[uid] = c
                self.candidates.append(uid)

    def register(self, user_id):
        self.cand_by_user[user_id] = self.candidates.copy()
        self.used_tags[user_id] = []

    def get_question(self, used_id) -> (int, str):
        cand = self.cand_by_user[used_id]
        cand_tag = set()
        for c in cand:
            cand_tag.update(self.catchers[c].tags)
        for t in self.used_tags[used_id]:
            if t in cand_tag:
                cand_tag.remove(t)
        if len(cand_tag) == 0:
            return None, None
        t = random.choice(list(cand_tag))
        q = question.questions[t]
        self.used_tags[used_id].append(t)
        return t, random.choice(q)

    def exclude_tag(self, used_id, tag):
        cand = self.cand_by_user[used_id]
        new = []
        for c in cand:
            if tag not in self.catchers[c].tags:
                new.append(c)
        self.cand_by_user[used_id] = new

    def include_tag(self, used_id, tag):
        cand = self.cand_by_user[used_id]
        new = []
        for c in cand:
            if tag in self.catchers[c].tags:
                new.append(c)
        self.cand_by_user[used_id] = new

    def is_determined(self, used_id):
        return len(self.cand_by_user[used_id]) == 1




def yes_no():
    return random.choice(['yes', 'no'])


def main():
    user_id = 'userid'
    cs = Catchers()
    cs.register(user_id)
    while True:
        tag, q = cs.get_question(user_id)
        if not tag:
            if len(cs.cand_by_user[user_id]) == 0:
                print('Sorry, no one can satisfy your needs, right now. Please try again.')
                sys.exit()
            else:
                rec = random.choice(cs.cand_by_user[user_id])
        text = yes_no()
        print(q, text, tag)
        if text == 'yes':
            cs.include_tag(user_id, tag)
        else:
            cs.exclude_tag(user_id, tag)
        if cs.is_determined(user_id):
            rec = cs.cand_by_user[user_id]
            break

    print(rec[0])
    print(cs.catchers[rec[0]].age)
    print(cs.catchers[rec[0]].tags)


if __name__ == '__main__':
    main()

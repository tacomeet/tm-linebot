import logging
import random

import requests
import slack

from const import question
from database.database import db
from models import CatcherCandidate, UsedTag, CatcherTag

BASE_URL = 'https://teenmakers.jp/wp-json/wp/v2/'
DEFAULT_PER_PAGE = 10

logger = logging.getLogger('app.flask')


def register(user_id):
    cand = set(ct.catcher_id for ct in CatcherTag.query.all())
    for c in cand:
        db.session.add(CatcherCandidate(user_id, c))
    db.session.commit()


def reset(user_id):
    CatcherCandidate.query.filter_by(user_id=user_id).delete()
    UsedTag.query.filter_by(user_id=user_id).delete()
    db.session.commit()


def get_candidates(user_id):
    return CatcherCandidate.query.filter_by(user_id=user_id).all()


def get_question(user_id) -> (int, str):
    cand = get_candidates(user_id)
    cand_tags = set()
    for c in cand:
        cand_tags.update(c.tag_id for c in CatcherTag.query.filter_by(catcher_id=c.catcher_id).all())
    used_tags = set(t.tag_id for t in UsedTag.query.filter_by(user_id=user_id).all())
    cand_tags -= set(used_tags)
    while True:
        if len(cand_tags) == 0:
            return None, None
        t = random.choice(list(cand_tags))
        try:
            q = question.questions[t]
            break
        except KeyError:
            db.session.add(UsedTag(user_id, t))
            exclude_tag(user_id, t)
            cand_tags -= {t}
            slack.tag_missing(t)
    db.session.add(UsedTag(user_id, t))
    return t, q


def setup_catcher_tag():
    res_num = DEFAULT_PER_PAGE
    offset = 0
    while res_num == DEFAULT_PER_PAGE:
        res = requests.get(BASE_URL + 'posts?offset=' + str(offset), timeout=5)
        if res.status_code != requests.codes.ok:
            logger.error('Error: ' + str(res.status_code))
            break
        js = res.json()
        res_num = len(js)
        offset += DEFAULT_PER_PAGE
        for j in js:
            uid = j['id']
            for tag in j['tags']:
                ct = CatcherTag(uid, tag)
                db.session.add(ct)
        db.session.commit()


def refresh_catcher_tag():
    CatcherTag.__table__.drop(db.get_engine())
    CatcherTag.__table__.create(db.get_engine())
    setup_catcher_tag()


def exclude_tag(user_id, tag_id):
    cand = get_candidates(user_id)
    for c in cand:
        tag_ids = {ct.tag_id for ct in CatcherTag.query.filter_by(catcher_id=c.catcher_id).all()}
        if tag_id in tag_ids:
            CatcherCandidate.query.filter_by(user_id=user_id, catcher_id=c.catcher_id).delete()


def exclude_catcher(user_id, catcher_id):
    CatcherCandidate.query.filter_by(user_id=user_id, catcher_id=catcher_id).delete()


def get_rec(user_id):
    cand = get_candidates(user_id)
    used_tags = set(t.tag_id for t in UsedTag.query.filter_by(user_id=user_id).all())
    for c in cand:
        satis = True
        tag_ids = [ct.tag_id for ct in CatcherTag.query.filter_by(catcher_id=c.catcher_id).all()]
        for tag_id in tag_ids:
            if tag_id not in used_tags:
                satis = False
                break
        if satis:
            return c.catcher_id


def get_catcher_tags(user_id, catcher_id):
    catcher_tags = set(ct.tag_id for ct in CatcherTag.query.filter_by(catcher_id=catcher_id).all())
    return catcher_tags

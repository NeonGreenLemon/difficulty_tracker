import re

from typing import Any, Dict, Tuple, Literal
from aqt import gui_hooks, mw
from anki.cards import Card
from aqt.reviewer import Reviewer
from aqt.utils import tooltip


def check_difficulty_tag_on_answer(tuple_ans: Tuple, reviewer: Reviewer,
                                   card: Card) -> "Tuple[bool, Literal[1, 2, 3, 4]]":
    config = mw.addonManager.getConfig(__name__)
    proceed, ease = tuple_ans
    type_info = get_card_typ_info(card)

    if config["increase_only_on_review"] and not type_info["Review"]:
        return tuple_ans

    is_leech = card.note().hasTag(config["only_leech_tag_name"])
    if config["only_leech"] and not is_leech:
        return tuple_ans

    cur_difficulty = 0
    pattern = re.compile(config["tag_name"] + "(\d+)")
    if any((match := pattern.match(tag)) for tag in card.note().tags):
        cur_difficulty = int(match.group(1))

    # when tag exist delete tag
    if cur_difficulty > 0:
        card.note().delTag(config["tag_name"] + str(cur_difficulty))

    if ease > 1:
        if type_info["Review"]:  # reset and reduce should only happen when review! (tag delete rollbacks no flush)
            if not config["good_reset_all"]:
                next_dif = (cur_difficulty - 1)
                if next_dif > 0:  # when result 0 then we need no tag
                    if config["show_tooltip"]:
                        tooltip("Decrease to: " + str(next_dif))
                    card.note().addTag(config["tag_name"] + str(next_dif))
            card.note().flush()
        return tuple_ans

    next_dif = cur_difficulty + 1
    if next_dif > config["max_difficulty"]:
        next_dif = config["max_difficulty"]

    if config["show_tooltip"]:
        tooltip("Increase to: " + str(next_dif))
    card.note().addTag(config["tag_name"] + str(next_dif))
    card.note().flush()

    if config["again_is_good"] and is_leech:
        tuple_ans = (tuple_ans[0], 2)  # set answer to good!

    return tuple_ans


gui_hooks.reviewer_will_answer_card.append(check_difficulty_tag_on_answer)


def get_card_typ_info(card):
    typeInfo: Dict[str, Any] = {}
    typeInfo["Review"] = True if card.type == 2 and card.queue == 2 else False  # only if in queue 2 it is a real review
    typeInfo["New"] = True if card.type == 0 else False
    typeInfo["Learning"] = True if card.type == 1 else False
    typeInfo["TodayLearning"] = (
        True if card.type == 1 and card.queue == 1 else False
    )
    typeInfo["DayLearning"] = (
        True if card.type == 1 and card.queue == 3 else False
    )
    return typeInfo

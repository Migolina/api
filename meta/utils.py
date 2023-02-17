
def get_actions_dict(insights):
    actions = {}
    for ad in insights:
        if ad.get("actions", None):
            for _type in ad["actions"]:
                actions[_type["action_type"]] = _type["value"]

    return actions










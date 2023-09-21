from collections import OrderedDict


async def service_normalize_tags(body):
    tags = [tag[:25].strip() for tag_str in body.tags for tag in tag_str.split(",") if tag]
    correct_tags = list(OrderedDict.fromkeys(tags))
    return correct_tags

from itertools import groupby


def group_tags(tags):
    tag_list = []
    for k, g in groupby(tags, key=lambda x: x.name.capitalize()[:1]):
        tag_list.append((k, list(g)))

    return tag_list

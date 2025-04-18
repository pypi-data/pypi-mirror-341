'''
get_list_repeat: 获取列表中重复的元素
'''
def get_list_repeat(data):
    if not data or not isinstance(data, list):
        return []
    if len(data) == 1:
        return []
    sdata = sorted(data)
    cur = sdata[0]
    repeats = []
    rnum = 0
    for e in sdata[1:]:
        if e == cur:
            rnum += 1
            if rnum == 1:
                repeats.append(e)
        else:
            cur = e
            rnum = 0
    return repeats
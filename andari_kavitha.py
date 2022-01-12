class GlobVariables:
    sep = "|"
    typ = int
    start = "s"
    end = "e"
    indicator = "!"
    cont = "c"
    file_ = "andari_kavitha.txt"
    limit = 200
    start_kavitha = "started noting kavitha with id "
    print_kavitha = "current poem {} \n-----\n{}".format
    end_kavitha = "Enjaai the community kavitha \n ---------- \n{} \n --------- \n Authors: {}".format
    avialable_kavitha = "currently, poems with ids {} are open".format
    channels = [930490931935858711, # bot_kavithvam_test
    930795638495514664, #complete-the-kavithvam
    ]
    available = "a"


def get_int(x):
    try:
        return int(x)
    except:
        return


def find_small_num(arr_):
    "find the smallest missing number from an unsorted array"
    arr = arr_.copy()
    size = len(arr)
    for i in range(size):
        if (arr[i] < size) and (arr[arr[i]] > 0):
            arr[arr[i]] = -arr[arr[i] - 1]

    for i in range(size):
        if (arr[i] > 0):
            return i
    return size


def get_poem(messages, id):
    """a little confusion whether the messages are upside down or downside up. Currently consider them downside up. i.e, more recenet message is the first element"""
    res = []
    authors = set()
    i = 0
    found = False
    #print([mes.content for mes in messages])
    while i < (len(messages)-1) and (not found):
        #print(messages[i].content.strip(" \n"), GlobVariables.indicator, id)
        if messages[i].content.strip(" \n").startswith("{}{}".format(GlobVariables.indicator, id)):
            #print("adding to res", res)
            res.append(messages[i].content.strip(" \n").strip("{}{}".format(GlobVariables.indicator, id)).strip(" \n"))
            if hasattr(messages[i].author, "nick") and messages[i].author.nick:
              authors.add(messages[i].author.nick)
            else:
              authors.add(str(messages[i].author).split("#")[0])
        i += 1
        if "{}{}".format(GlobVariables.start_kavitha, id) in messages[i].content:
            found = True
    if not found:
        return 0, "poem not started bruh!"
    return 1, "\n".join(reversed(res)), ",".join([str(x) for x in authors if x])


async def get_kavitha(message):
    """
    :param message: expected to start with a !number or !s. if not, it is deleted
    # recent messages are like literally the recent
    message.channel bot-test
    ['!b most recent msg', 'recent messig', '!b bigbit', '!b bittid', '!b tidbit']
    :return:
    """
    msg = message.content.strip(" \n")
    hist_messages = await message.channel.history(limit=GlobVariables.limit).flatten()
    # hist_messages = [x.content for x in hist_messages]
    f = open(GlobVariables.file_, "r+")
    ids = [GlobVariables.typ(x) for x in f.read().split(GlobVariables.sep)]
    if msg.startswith(GlobVariables.indicator):
        msg = msg.strip(GlobVariables.indicator)
        #print("get int method", msg.split()[0])
        #print(get_int(msg.split()[0]))
        if msg[0].lower() == GlobVariables.start:
            if get_int(msg.rsplit(GlobVariables.start, 1)[-1].strip(" \n")):
                new_id = get_int(msg.rsplit(GlobVariables.start, 1)[-1].strip(" \n"))
            else:
                new_id = find_small_num(ids)
            f.write("{}{}".format(GlobVariables.sep, new_id))
            f.close()
            await message.channel.send("{}{}. use this id to continue/end".format(GlobVariables.start_kavitha, new_id))
        elif get_int(msg.split()[0]):
            if get_int(msg.split()[0]) not in ids:
              await message.channel.send("no one started the poem with id {} bruh".format(get_int(msg.split()[0])))
            else:
              success, build_poem, _ = get_poem(hist_messages, get_int(msg.split()[0]))
              if success:
                  await message.channel.send(GlobVariables.print_kavitha(get_int(msg.split()[0]), build_poem))
              else:
                  await message.channel.send("Exception occurred: {}".format(build_poem))
        elif msg[0].lower() == GlobVariables.end:
            if get_int(msg.rsplit(GlobVariables.end, 1)[-1].strip(" \n")):
                success, build_poem, authors = get_poem(hist_messages, get_int(msg.rsplit(GlobVariables.end, 1)[-1].strip(" \n")))
                if success:
                    end_msg = await message.channel.send(GlobVariables.end_kavitha(build_poem, authors))
                    await end_msg.pin()
                else:
                    await message.channel.send("Exception occurred: {}".format(build_poem))
                try:
                    ids.remove(get_int(msg.rsplit(GlobVariables.end, 1)[-1].strip(" \n")))
                    f.seek(0)
                    f.truncate(0)
                    f.write(GlobVariables.sep.join([str(x) for x in ids]))
                    f.close()
                except Exception as e:
                    await message.channel.send("Exception occured: {}".format(e))
        elif msg[0].lower() == GlobVariables.available:
          ids.remove(0)
          await message.channel.send(",".join([str(x) for x in ids]))
    else:
        await message.delete()

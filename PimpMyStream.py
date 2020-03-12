import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import utils.LiveChat as lc


def run_poll(delay, choices_string, url, title):
    # Variables - EnterByUser
    choices = choices_string.split(';')
    choices[-1] = choices[-1][0:len(choices[-1])-1]
    live_chat = lc.LiveChat(url)
    period = int(delay)
    # Variables - Construct
    vote = [1 for k in choices]
    voteRate = [100 / len(vote) for k in vote]
    participant = []
    fig = plt.figure()

    def calcul_vote_rate():
        s = 0
        for i in vote:
            s += i
        for j in range(len(voteRate)):
            voteRate[j] = (vote[j] / s) * 100

    def index_of_max(liste):
        p = 0
        index = 0
        max = liste[0]
        for i in liste:
            if i > max:
                index = p
                max = i
            p += 1
        return index

    def contain_vote(message):
        for choice in choices:
            if choice in message:
                choix = choice
                contain = True
                return contain, choix
        return None

    def calculVote():
        liste = live_chat.get_messages()
        for elem in liste:
            par = elem[0]
            message = elem[1]
            tmp = contain_vote(message)
            if tmp is not None:
                if (par not in participant) and tmp[0]:
                    participant.append(par)
                    i = choices.index(tmp[1])
                    vote[i] += 1

    def run_animation():
        start = time.time()

        def animFunc(i):
            now = time.time()

            if now - start >= period:
                anim.event_source.stop()
                index_max = index_of_max(vote)
                return choices[index_max]
            else:
                calculVote()
                # vote[random.randint(0, 2)] += 1
                calcul_vote_rate()
                index = np.arange(len(choices))
                plt.clf()
                plt.ylim(0, 100)
                plt.bar(index, voteRate)
                plt.title(title)
                plt.xlabel('Choix')
                plt.ylabel('Votes en %')
                plt.xticks(index, choices)
                for c in range(len(choices)):
                    plt.annotate(round(voteRate[c], 2), (c, voteRate[c]))

        anim = animation.FuncAnimation(fig, animFunc, fargs=(), interval=500)
        plt.show()

    run_animation()
    print(choices[index_of_max(vote)])
    return choices[index_of_max(vote)]


if __name__ == "__main__":
    """
    # Variables - EnterByUser
    period = 300
    choices = "lol;cs;wow"
    url = ""
    # Variables - Construct
    vote = [0 for k in choices]
    voteRate = [100 / len(vote) for k in vote]
    participant = []
    fig = plt.figure()

    pageToken = None
    run_poll(period, choices, url, "titre")
        """


import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import glob

k1, k2 = 0, 0


half_total_times = 720
def cluster():
    log = np.append(np.random.normal(33, 2, half_total_times),
                    np.random.normal(27, 2, half_total_times))
    plt.hist(log, 80, histtype='bar', facecolor='yellowgreen', alpha=0.75)
    plt.ylabel('Frequentness')
    plt.xlabel('Temperature')
    plt.xticks(np.arange(20, 42, 1))
    plt.title("Raw Temperature Stats.")
    plt.show()

    np.random.shuffle(log)
    t1, t2 = log[:half_total_times], log[half_total_times:]
    global k1
    global k2
    k1, k2 = np.mean(t1), np.mean(t2)

    while True:
        flag = True
        i, j = 0, 0
        while i < len(t1):
            tmp = t1[i]
            if abs(tmp-k1) > abs(tmp-k2):
                t2 = np.append(t2, tmp)
                t1 = np.delete(t1, i)
                flag = False
                print(tmp, "has been moved to 2")
                continue
            i = i + 1
        while j < len(t2):
            tmp = t2[j]
            if abs(tmp-k1) < abs(tmp-k2):
                t1 = np.append(t1, tmp)
                t2 = np.delete(t2, j)
                flag = False
                print(tmp, "has been moved to 1")
                continue
            j = j + 1
        if flag:
            break
        k1 = np.mean(t1)
        k2 = np.mean(t2)
        # print(k1, k2)
    print("final k-means:", k1, k2, "# htt =", half_total_times)
    n1, bins1, patches1 = plt.hist(
        t1, 80, histtype='bar', density=1, facecolor='blue', alpha=0.75)  # according to P21
    n2, bins2, patches2 = plt.hist(
        t2, 80, histtype='bar', density=1, facecolor='green', alpha=0.75)
    y1 = stats.norm.pdf(bins1, np.mean(t1), np.std(t1))
    y2 = stats.norm.pdf(bins2, np.mean(t2), np.std(t2))
    plt.plot(bins1, y1, 'r--')
    plt.plot(bins2, y2, 'r--')
    plt.ylabel('Proportion')
    plt.xlabel('Temperature')
    plt.xticks(np.arange(20, 42, 1))
    plt.title("2-Means Clustering")
    plt.show()


def judge():
    try:
        while True:
            for name in glob.glob('/sys/bus/w1/devices/28*'):
                name += '/w1_slave'
                with open(name, 'r') as f:
                    contents = f.readlines()
                    s = contents[1].find('t=') + 2
                    temp = int(contents[1][s:]) / 1000
                    print('current temperature:', temp)
                    if abs(temp - k1) < abs(temp - k2):
                        print("It's person 1 here")
                    else:
                        print("It's person 2 here")
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    cluster()
    # judge()

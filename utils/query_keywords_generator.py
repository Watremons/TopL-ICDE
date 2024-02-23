
import random
import numpy as np
from scipy.stats import zipf

if __name__ == "__main__":
    distribution = "unifrom"
    size = 50000
    keyword_size = 5
    keyword_domain_size = 20
    per_vertex_keyword = 3
    for _ in range(15):
        if distribution == "unifrom":
            keywords_set = range(0, keyword_domain_size)
            keywords = random.sample(keywords_set, keyword_size)
        elif distribution == "zipf":
            # Zipf
            a = 2  # param
            zipf_dist = zipf(a)
            keywords_set = zipf_dist.rvs(size * per_vertex_keyword)
        elif distribution == "gauss":
            mean = 10  # 均值
            stddev = 3  # 标准差
            keywords_set = np.random.normal(mean, stddev, size)
        keywords_set = np.clip(keywords_set, 0, keyword_domain_size-1).astype(int)
        # print(keywords_set)
        keywords = np.random.choice(keywords_set, keyword_size)
        while len(set(keywords)) != len(keywords):
            keywords = np.random.choice(keywords_set, keyword_size)
        for keyword in keywords:
            print(keyword, end=",")
        print()

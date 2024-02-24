import os

if __name__ == "__main__":
    # folder_path = "/home/yons/projects/influential-community-detection/dataset/"
    folder_path = "/home/yons/projects/influential-community-detection/dataset_atindex/"
    # 10000-28675-20-3
    # 25000-72201-20-3
    # 50000-145648-20-3
    # 100000-295840-20-3
    # 250000-768545-20-3
    # 500000-1616753-20-3
    # 1000000-3500118-20-3
    # 334863-925872-20-3
    # 317080-1049866-20-3
    folder_path = os.path.join(folder_path, "manual", "50000-145648-20-3")
    print("------{}------".format(folder_path))

    uni_result_list = []
    gau_result_list = []
    zipf_result_list = []

    uni_file_list = os.listdir(folder_path)
    gau_file_list = os.listdir(os.path.join(folder_path, "gauss"))
    zipf_file_list = os.listdir(os.path.join(folder_path, "zipf"))

    for file_name in uni_file_list:
        file_path = os.path.join(folder_path, file_name)
        if os.path.splitext(file_path)[-1] == ".txt":
            refine_type = "Unknown"
            obtain_time = 0
            refine_time = 0
            sampling_ratio = 1
            with open(file_path, encoding='utf-8') as file_obj:
                lines = file_obj.readlines()
            for line in lines:
                if line.startswith("Refine Type:"):
                    refine_type = line.rstrip().split(' ')[2]
                if line.startswith("Obtainment time:"):
                    obtain_time = line.rstrip().split(' ')[2]
                if line.startswith("Refinement Increment Compute Time:"):
                    refine_time = line.rstrip().split(' ')[4]
                if line.startswith("Optimal Sampling Ratio:"):
                    sampling_ratio = line.rstrip().split(' ')[3]
            refine_time = float(refine_time) * (float(sampling_ratio) if float(sampling_ratio) > 1 else 1)
            uni_result_list.append([refine_type, obtain_time, refine_time])

    for file_name in gau_file_list:
        file_path = os.path.join(folder_path, "gauss", file_name)
        if os.path.splitext(file_path)[-1] == ".txt":
            total_score = "Unknown"
            obtain_time = 0
            refine_time = 0
            sampling_ratio = 1
            with open(file_path, encoding='utf-8') as file_obj:
                lines = file_obj.readlines()
            for line in lines:
                if line.startswith("Total Score:"):
                    total_score = line.rstrip().split(' ')[2]
                if line.startswith("Obtainment time:"):
                    obtain_time = line.rstrip().split(' ')[2]
                if line.startswith("Refinement Increment Compute Time:"):
                    refine_time = line.rstrip().split(' ')[4]
                if line.startswith("Optimal Sampling Ratio:"):
                    sampling_ratio = line.rstrip().split(' ')[3]
            refine_time = float(refine_time) * (float(sampling_ratio) if float(sampling_ratio) > 1 else 1)
            gau_result_list.append([total_score, obtain_time, refine_time])

    for file_name in zipf_file_list:
        file_path = os.path.join(folder_path, "zipf", file_name)
        if os.path.splitext(file_path)[-1] == ".txt":
            total_score = "Unknown"
            obtain_time = 0
            refine_time = 0
            sampling_ratio = 1
            with open(file_path, encoding='utf-8') as file_obj:
                lines = file_obj.readlines()
            for line in lines:
                if line.startswith("Total Score:"):
                    total_score = line.rstrip().split(' ')[2]
                if line.startswith("Obtainment time:"):
                    obtain_time = line.rstrip().split(' ')[2]
                if line.startswith("Refinement Increment Compute Time:"):
                    refine_time = line.rstrip().split(' ')[4]
                if line.startswith("Optimal Sampling Ratio:"):
                    sampling_ratio = line.rstrip().split(' ')[3]
            refine_time = float(refine_time) * (float(sampling_ratio) if float(sampling_ratio) > 1 else 1)
            zipf_result_list.append([total_score, obtain_time, refine_time])

    print("uni")
    for uni_result in uni_result_list:
        print(uni_result[0], uni_result[1], uni_result[2], sep="\t")
    print("gau")
    for gau_result in gau_result_list:
        print(gau_result[0], gau_result[1], gau_result[2], sep="\t")
    print("zipf")
    for zipf_result in zipf_result_list:
        print(zipf_result[0], zipf_result[1], zipf_result[2], sep="\t")

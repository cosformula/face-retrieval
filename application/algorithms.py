import random


def AnsDisConTgt2(i, distance, options, answer, theta_a=0.8, theta_b=58):
    p_sum = 0
    prob = 0
    for option in options:
        distance_from_i_to_result = distance[i][option]
        # print(distance_from_i_to_result)
        prob_i = (1+theta_a*distance_from_i_to_result) / \
            (1+theta_b*distance_from_i_to_result)
        # print(prob_i)
        p_sum += prob_i
        if answer == option:
            prob = prob_i
    prob = prob / p_sum
    return prob
    #   if (gfFbmDis[iPntInd, result_indexs[i]] > fTheta1)
    #   {
    #       fPhi = fTheta2;
    #   }
    #   else  
    #   {
    #       fPhi = (float)1 - gfFbmDis[iPntInd, result_indexs[i]] * (1 - fTheta2) / fTheta1;
    #   }
    #   fPsum = fPsum + fPhi;


#  enropy a = 0.8 b = 58 |  a = 1.8 b = 18.5
#  else a = 1.8 b = 18.5 |  a= 0.115 0.149

def update_probability_distribution(distance, distribution, options, answer):
    p_sum = 0
    # print(distribution)
    for i in range(len(distribution)):
        if i in options:
            distribution[i] = 0
        else:
            distribution[i] *= AnsDisConTgt2(i, distance, options, answer)
        p_sum += distribution[i]
    for i in range(len(distribution)):
        distribution[i] /= p_sum
    return distribution


def get_next_iteration_random(no, distribution, max_iteration_faces):
    index_list = list(range(len(distribution)))
    dis_index = list(zip(distribution, index_list))

    filtered_index = list(filter(
        lambda x: x[0] > 0, dis_index))

    if len(filtered_index) > max_iteration_faces:
        return random.sample(filtered_index, max_iteration_faces)
    else:
        return filtered_index


def get_next_iteration_similarity(no, distribution, max_iteration_faces):
    index_list = list(range(len(distribution)))
    dis_index = list(zip(distribution, index_list))

    filtered_index = filter(
        lambda x: x[0] > 0, dis_index)

    sorted_index = list(sorted(filtered_index, key=lambda x: x[0], reverse=True))
    options = sorted_index[:max_iteration_faces]

    if len(sorted_index) > max_iteration_faces:
        return sorted_index[:max_iteration_faces]
    else:
        return sorted_index


def get_next_iteration_entropy(no, distribution, max_iteration_faces, distances):
    index_list = list(range(len(distribution)))
    dis_index = list(zip(distribution, index_list))

    filtered_index = filter(
        lambda x: x[0] > 0, dis_index)

    sorted_index = list(sorted(filtered_index, key=lambda x: x[1], reverse=True))
    # sorted_index = list(map(sorted_index,lambda x:x[1]))

    DELTA = 1e-10
    thresh = 1 / max_iteration_faces
    p_sum = 0
    results = []
    index_pointer = 0
    index_available = [1 for i in range(len(distribution))]

    def get_similar_index_list(distances, index):
        distance = distances[index]
        distance_index = list(zip(distance, index_list))
        sorted_index = list(sorted(distance_index, key=lambda x: x[0]))
        # print(sorted_index)
        return list(map(lambda x: x[1], sorted_index))

    for i in range(max_iteration_faces):
        current_index = sorted_index[index_pointer][1]
        while index_available[current_index] == 0:
            index_pointer += 1
            current_index = sorted_index[index_pointer][1]

        current_index = sorted_index[index_pointer][1]

        index_available[current_index] = 0
        index_pointer += 1
        p_sum_t = distribution[current_index]

        if p_sum_t < thresh:
            similar_index_list = get_similar_index_list(
                distances, current_index)
            for index in similar_index_list:
                if index_available[index] == 0:
                    continue
                p_sum_t += distribution[index]
                index_available[index] = 0
                if p_sum_t >= thresh - DELTA:
                    break

        results.append((p_sum_t, sorted_index[index_pointer][1]))

        if i < max_iteration_faces - 1:
            p_sum += p_sum_t
            thresh = (1.0-p_sum)/(max_iteration_faces-i-1)
    return results

    # options = sorted_index[:max_iteration_faces]

    # if len(sorted_index) > max_iteration_faces:
    #     return sorted_index[:max_iteration_faces]
    # else:
    #     return sorted_index

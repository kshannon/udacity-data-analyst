# #!/usr/bin/python


def outlierCleaner(predictions, ages, net_worths):
    """
        Clean away the 10 percent of points that have the largest
        residual errors (difference between the prediction
        and the actual net worth).

        Return a list of tuples named cleaned_data where 
        each tuple is of the form (age, net_worth, error).
    """


    cleaned_data = []
    index_count = 0
    while index_count < len(ages):
        error = abs(predictions[index_count] - net_worths[index_count])
        temp_tuple = (ages[index_count][0], net_worths[index_count][0], error[0])
        cleaned_data.append(temp_tuple)
        index_count += 1


    return sorted(cleaned_data, key=lambda erra: erra[2])[:81]

# Create your own code here
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# this program has a large amount of redundancy (especially around nan) but seems  to function for everything I need it to.


def main():
    dataset = parse()
    dataset = clean_data(dataset)
    selection = []
    for i in dataset[0]:
        selection.append(i)

    running = 1
    while running == 1:
        print("Options to select from: " + str(selection))
        x = input("Please select which stat you want for the x-axis: ")
        y = input("Please select which stat you want for the y-axis: ")
        m, B = regression(x, y, dataset)
        graph_regression(x, y, dataset, m, B)
        plt.savefig("./output/output.png")
        if input("If you would to exit, press q. Otherwise press enter\n") == "q":
            running = 0




def parse():
    df = pd.read_csv("lol_champions.csv", encoding="iso-8859-1", delimiter=";", header=None)
    # removed 142 since all of Udyrs data is missing, causing errors
    df.drop(142, inplace=True)
    df.fillna({"numeric_col": 0, "string_col": ""}, inplace=True)

    data = df.values.tolist()
    return data


# This function removes columns that don't have impact on statistics like winrate or popularity
# this includes things like Champ ID and ability descriptions
def clean_data(unclean):
    index = 0
    nums_to_keep = [3, 6, 7, 8, 9, 10, 13, 14, 15, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38]
    new_data = [["" for _ in range(27)] for row in unclean]
    for row in range(len(unclean)):
        for column in range(len(unclean[row])):
            if column + 1 in nums_to_keep:
                new_data[row][index] = unclean[row][column]
                index += 1
        index = 0
    return new_data


# graphs data on a scatter plot with labeled data
def graph_data(x_target, y_target, data):
    x_data = []
    y_data = []
    champ = []
    x_found = False
    y_found = False

    # create fig and axis for labels later
    fig = plt.figure(figsize=(10, 10))
    axis = fig.add_subplot(111)

    for header in range(len(data[0])):
        # looks for data type
        if x_target in data[0][header]:
            x_col = header
            x_found = True
        if y_target in data[0][header]:
            y_col = header
            y_found = True
    if x_found and y_found:
        # [:1] to skip first entry (the header)

        for row in data[1:]:
            if row[x_col] != "nan":
                champ.append(row[0])
                x_data.append(str_conversion(row[x_col]))
                y_data.append(str_conversion(row[y_col]))

        plt.scatter(x_data, y_data)
        plt.xlabel(x_target)
        plt.ylabel(y_target)

        # add text to each data point (followed this: https://medium.com/@marvelouskgc/three-ways-to-add-labels-to-each-data-point-in-a-scatter-plot-in-python-matplotlib-eugene-tsai-42e4094dc07e)
        for i, txt in enumerate(champ):
            axis.text(x_data[i], y_data[i], txt)
        return x_data, y_data
    else:
        print("Error: columns not found, check entered columns are correct and try again.")


# graphs data on a scatter plot, then adds regression line
# once again referenced https://textbooks.math.gatech.edu/ila/least-squares.html
def graph_regression(x_target, y_target, data, m, B):
    x_data, y_data = graph_data(x_target, y_target, data)
    x_line = [min(x_data), max(x_data)]

    # y=mx+B
    y_line = [m * x + B for x in x_line]
    plt.plot(x_line, y_line, color="red")


# converts strings to floats so they can be placed on a scatter plot without cluttering the x/y labels
def str_conversion(incoming_str):
    if type(incoming_str) is not str:
        pass
    elif "%" in incoming_str:
        incoming_str = float(incoming_str.strip("%"))
    else:
        incoming_str = float(incoming_str)
    return incoming_str


# regression to see how data correlates
# referenced notes, as well as https://textbooks.math.gatech.edu/ila/least-squares.html
def regression(x, y, data):
    A = []
    b = []
    # reusing, it would be better practice to just turn this into a function, but considering the scope of this project
    # I'm not worried about tech debt
    for header in range(len(data[0])):
        if x in data[0][header]:
            x_col = header
            x_found = True
        if y in data[0][header]:
            y_col = header
            y_found = True

    if x_found and y_found:
        # [:1] to skip first entry (the header)
        for row in data[1:]:

            if row[x_col] != float("nan") and row[y_col] != float("nan"):


                A.append([str_conversion(row[x_col]), 1])
                b.append(str_conversion(row[y_col]))
        A_t = transpose(A)
        A_t_A = multiply(A_t, A)
        A_t_A_inv = pseudo_inverse(A_t_A)
        # if something doesn't work COME BACK HERE
        # this implementation is awful
        A_t_b = second_is_vector(A_t, b)
        x = second_is_vector(A_t_A_inv, A_t_b)

        m = x[0]
        B = x[1]
        return m, B


    else:
        print("Error: columns not found, check entered columns are correct and try again.")



def pseudo_inverse(A):

    U, Sigma, V_t = np.linalg.svd(A)
    U_t = transpose(U)
    V = transpose(V_t)
    # fix sigma
    m = len(U)
    n = len(V_t)
    new_s = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(len(Sigma)):
        new_s[i][i] = Sigma[i]
    Sigma = new_s
    pseudo_sigma = find_pseudo_sigma(Sigma)
    # multiply together
    U_t_PSigma = multiply(U_t, pseudo_sigma)
    pseudo_A = multiply(U_t_PSigma, V)
    return pseudo_A

# transpose function from summative assignment
def transpose(A):
    # initialize matrix (forgot I could do it this way)

    new_lst = [["" for _ in range(len(A))] for _ in range(len(A[0]))]
    for row_index in range(len(A)):
        for col_index in range(len(A[0])):
            new_lst[col_index][row_index] = A[row_index][col_index]
    return new_lst


# new pseudo sigma function
def find_pseudo_sigma(sigma):

    sig_t = transpose(sigma)

    # place all non-zero numbers under 1
    for row in range(len(sig_t)):
        for col in range(len(sig_t[row])):
            if sig_t[row][col] != 0:
                sig_t[row][col] = 1/float(sig_t[row][col])
    return sig_t

# mult function from summative assignment
def multiply(A, B):
    new_row_len = len(A)
    new_col_len = len(B[0])

    new_matrix = []
    # initialize matrix
    for row in range(new_row_len):
        new_matrix.append([])
        for col in range(new_col_len):
            new_matrix[row].append("")
    # solve using for loops
    for a_index in range(len(A)):
        for b_index in range(len(B[0])):
            total = 0
            for col in range(len(A[0])):
                # col index in row pos since the axis a and b move on are opposite during multiplication
                # a_index tracks A's rows
                # b_index tracks b's columns, together these identify the position on the final array
                # col tracks a's column and b's row

                total += A[a_index][col] * B[col][b_index]
            new_matrix[a_index][b_index] = total
    return new_matrix


# This is an incredibly hard coded and lazy solution, but this is an easy workaround from an oversight in the
# summative assignment
def second_is_vector(A, B):

    new_row_len = len(A)
    new_col_len = 0

    new_matrix = []
    # initialize matrix
    for row in range(new_row_len):
        new_matrix.append([])
        for col in range(new_col_len):
            new_matrix[row].append("")
    # solve using for loops
    for a_index in range(len(A)):

        total = 0
        for col in range(len(A[0])):
            # col index in row pos since the axis a and b move on are opposite during multiplication
            # a_index tracks A's rows
            # b_index tracks b's columns, together these identify the position on the final array
            # col tracks a's column and b's row
            total += A[a_index][col] * B[col]
        new_matrix[a_index] = total

    return new_matrix







if __name__ == "__main__":
    main()

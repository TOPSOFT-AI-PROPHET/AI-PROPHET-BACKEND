import tensorflow as tf
import numpy as np
from sklearn import *
from sklearn.model_selection import train_test_split
from joblib import dump, load
from sklearn.tree import DecisionTreeClassifier
from math import log
import operator
import matplotlib.pyplot as plt

dig_set = datasets.load_digits()
X = dig_set.data   #get features and classes from the dataset
y = dig_set.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

mytree = []

#pre-process data
z = dig_set.images
p = z.reshape(1797,8,8,1).astype('float32')

Xi_train, Xi_test, yi_train, yi_test = train_test_split(p, y, test_size=0.3, random_state=0)

def calculate_entropy(data_set,lable_list):
    num_features = data_set.shape[0]
    label_count = {}
    for Vec in lable_list:

        if Vec not in label_count.keys():
            label_count[Vec] = 0

        label_count[Vec] += 1

    entropy = 0.0

    for key in label_count:
        probability = float(label_count[key]) / num_features #entropy for a single label

        entropy = entropy - probability * log(probability,2) #cumulatively adding entropies up for the entire set

    return entropy

def splitDataset(dataset,axis,value,part=0): #part 0 for left 1 for right
    retDataset = []

    for featvec in dataset:
        if part == 0 and float(featvec[axis]) <= value:
            reduceFeatVec = list(featvec[:axis])
            reduceFeatVec.extend(list(featvec[axis + 1:]))
            retDataset.append(reduceFeatVec)

        if part == 1 and float(featvec[axis]) > value:
            reduceFeatVec = list(featvec[:axis])
            reduceFeatVec.extend(list(featvec[axis+1:]))
            retDataset.append(reduceFeatVec)

    return np.array(retDataset)

def find_relativeLabelSet(dataset,label_set,axis,value,part=0):
    retDataset = []
    for idx in range(dataset.shape[0]):
        if part == 0 and float(dataset[idx][axis]) <= value:
            retDataset.append(label_set[idx])

        if part == 1 and float(dataset[idx][axis]) > value:
            retDataset.append(label_set[idx])

    return np.array(retDataset);


def chooseBestFeatureToSplit(dataset,label_list):

    num_of_features = dataset.shape[1]

    #base entropy
    info_d = calculate_entropy(dataset,label_list)
    max_gain_rate = 0.0
    bestFeature = -1
    best_point_split = None

    for i in range(num_of_features):

        featlist = [example[i] for example in list(dataset)]  #create a set with unique values of a single feature


        featlist.sort()
        temp_set = set(featlist)
        featlist = [attr for attr in temp_set]
        split_points = []

        for index in range(len(featlist) - 1):
            split_points.append( (float(featlist[index]) + float(featlist[index + 1])) / 2)

        for split_point in split_points:
            info_A_D = 0.0
            split_info_D = 0.0

            for part in range(2):
                sub_data_set = splitDataset(dataset,i,split_point,part)
                sub_label_list = find_relativeLabelSet(dataset,label_list,i,split_point,part)
                prob = sub_data_set.shape[0] / float(dataset.shape[0])
                info_A_D += prob * calculate_entropy(sub_data_set,sub_label_list)
                split_info_D -= prob * log(prob,2)
            if split_info_D == 0:
                split_info_D += 1

            gainrate = (info_d - info_A_D) / split_info_D
            if gainrate > max_gain_rate:
                max_gain_rate = gainrate
                best_point_split = split_point
                bestFeature = i



    return bestFeature,best_point_split

def confidency_vote(classlist):
    counter_dic = {}
    for vote in classlist:
        if vote not in counter_dic.keys():
            counter_dic[vote] = 0
        counter_dic[vote] += 1

    sortedcounter = sorted(counter_dic.items(),key=operator.itemgetter(1),reverse=True)

    return sortedcounter[0][0]

def treegrow(dataset,label_list,labels):


    classlist = list(label_list)

    #stop classifiy if all in same class
    if classlist.count(classlist[0]) == len(classlist):
        return classlist[0]

    #stop classifiy if all features has been done and return the most common feature
    if (len(list(dataset[0])) == 0):
        return confidency_vote(classlist)





    bestFeat,bestpoint = chooseBestFeatureToSplit(dataset,label_list)
    bestFeatLabel = labels[bestFeat]
    dcTree = {bestFeatLabel:{}}
    del(labels[bestFeat])


    sub_labels = labels[:]
    sub_label_list = find_relativeLabelSet(dataset,label_list,bestFeat,bestpoint,0)
    #left
    dcTree[bestFeatLabel]["<=" + str(bestpoint)] = treegrow(splitDataset(dataset,bestFeat,bestpoint,0),sub_label_list,sub_labels)


    sub_label_list = find_relativeLabelSet(dataset, label_list, bestFeat, bestpoint,1)
    #right
    dcTree[bestFeatLabel][">" + str(bestpoint)] = treegrow(splitDataset(dataset, bestFeat, bestpoint, 1),sub_label_list, sub_labels)
    return dcTree

def dc_classify(tree,featlabels,testvec):

    firstSides = list(tree.keys())
    firstStr = firstSides[0]
    secoundDic = tree[firstStr]

    featIdex = featlabels.index(firstStr)

    for key in secoundDic.keys():
        if key[0] == '<':
            value = float(key[2:])
            if float(testvec[featIdex]) <= value:
                if type(secoundDic[key]).__name__ == 'dict':
                    classLabel = dc_classify(secoundDic[key], featlabels, testvec)
                else:
                    classLabel = secoundDic[key]  # leaf reached

        elif key[0] == '>':
            value = float(key[1:])
            if float(testvec[featIdex]) > value:
                if type(secoundDic[key]).__name__ == 'dict':
                    classLabel = dc_classify(secoundDic[key], featlabels, testvec)
                else:
                    classLabel = secoundDic[key]  # leaf reached


    return classLabel

def dc_predict(data,tree,featlabels):
    retset = []

    for i in range(data.shape[0]):
        retset.append(dc_classify(tree,featlabels,data[i]))

    return retset

def compute_error(ture_data,predicted_data):
    correct_count = 0
    for i in range(ture_data.shape[0]):
        if (ture_data[i] == predicted_data[i]):
            correct_count = correct_count + 1
    return 1-(correct_count/ture_data.shape[0])

### end of code form assignemt_1 ###



def CNN_model(xt,yt):
    print("\n********-Constructing CNN structure...")
    model_2 = tf.keras.Sequential([
        tf.keras.layers.Conv2D(64, kernel_size=(4, 4), activation='relu', input_shape=(8, 8, 1), padding='same'),
        tf.keras.layers.MaxPool2D(pool_size=(2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')]
    )

    model_2.compile(optimizer='adam',
                    loss='sparse_categorical_crossentropy')



    model_2.fit(xt, yt, epochs=50,verbose=0)
    

    return model_2


def NN_model(xt,yt):
    print("\n********-Constructing NN structure...")
    model = tf.keras.Sequential([tf.keras.layers.Dense(1000, input_shape=(64,), activation='relu'),
                                 tf.keras.layers.Dense(10, activation='softmax')]
                                )

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy')



    model.fit(xt, yt, epochs=50,verbose=0)

    return model






def find_best_prediction(predicted_set):
    y = []

    for i in range(len(predicted_set)):
        localmax = 0
        for m in range(len(predicted_set[i])):
            if( predicted_set[i][m] > predicted_set[i][localmax] ):
                localmax = m
        y.append(localmax)

    return np.array(y)


def cross_val(data_set,target_set,probability_flag):

    subsamples = [data_set[0:359],data_set[359:718],data_set[718:1077],data_set[1077:1436],data_set[1436:1796]] #spliting data
    subtargets = [target_set[0:359],target_set[359:718],target_set[718:1077],target_set[1077:1436],target_set[1436:1796]]

    conmulicative_val = 0

    print("\n******Cross validation result:")
    for i in range(4):
        if(probability_flag == 1):
            dtree = DecisionTreeClassifier(criterion='entropy', max_depth=10, random_state=0)
            dtree.fit(np.array(subsamples[i]), np.array(subtargets[i]))
            result_tem = 1 - compute_error(np.array(subtargets[4]),dtree.predict(np.array(subsamples[4])))
            conmulicative_val = conmulicative_val + result_tem
            print("Subsample:" + str(i) + " , Accuracy:" + str(result_tem)  )
        elif (probability_flag == 2):
            global mytree
            z = ["f" + str(i) for i in range(64)]
            prediction = dc_predict(np.array(subsamples[4]), mytree, z)
            result_tem = 1 - compute_error(np.array(subtargets[4]), prediction)
            conmulicative_val = conmulicative_val + result_tem
            print("Subsample:" + str(i) + " , Accuracy:" + str(result_tem))
        elif (probability_flag == 3):
            model = NN_model(np.array(subsamples[i]), np.array(subtargets[i]))
            result_tem = 1 - compute_error(np.array(subtargets[4]),find_best_prediction(model.predict(np.array(subsamples[4]))))
            conmulicative_val = conmulicative_val + result_tem
            print("Subsample:" + str(i) + " , Accuracy:" + str(result_tem))
        elif (probability_flag == 4):
            model = CNN_model(np.array(subsamples[i]), np.array(subtargets[i]))
            result_tem = 1 - compute_error(np.array(subtargets[4]),find_best_prediction(model.predict(
                                                                                   np.array(subsamples[4]))))
            conmulicative_val = conmulicative_val + result_tem
            print("Subsample:" + str(i) + " , Accuracy:" + str(result_tem))

    print("Average accuracy : " + str(conmulicative_val/4))


def plot_confusion_matrix(matrix):
    labels = ['0','1','2','3','4','5','6','7','8','9']

    plt.imshow(matrix, cmap=plt.cm.Blues)

    indices = range(len(matrix))

    plt.xticks(indices, labels)
    plt.yticks(indices, labels)

    plt.colorbar()

    plt.xlabel('predicted values')
    plt.ylabel('ture values')
    plt.title('Confusion Matrix')

    # 显示数据
    for first_index in range(len(matrix)):
        for second_index in range(len(matrix[first_index])):
            plt.text(first_index, second_index, matrix[first_index][second_index])

    plt.show()



def confusion_matrix(data_set,target_set,probability_flag):

    matrix = [[0,0,0,0,0,0,0,0,0,0],    #10x10 matrix
              [0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0],]

    if (probability_flag == 1):
        dtree = DecisionTreeClassifier(criterion='entropy', max_depth=10, random_state=0)
        dtree.fit(np.array(X_train), np.array(y_train))
        prediction = dtree.predict(data_set)
        for i in range(len(prediction)):
            if(prediction[i] == target_set[i]):
                matrix[prediction[i]][prediction[i]] = matrix[prediction[i]][prediction[i]] + 1
            else:
                matrix[target_set[i]][prediction[i]] = matrix[target_set[i]][prediction[i]] + 1
    elif (probability_flag == 2):
        global mytree
        z = ["f" + str(i) for i in range(64)]
        prediction = dc_predict(data_set, mytree, z)
        for i in range(len(prediction)):
            if (prediction[i] == target_set[i]):
                matrix[prediction[i]][prediction[i]] = matrix[prediction[i]][prediction[i]] + 1
            else:
                matrix[target_set[i]][prediction[i]] = matrix[target_set[i]][prediction[i]] + 1
    elif (probability_flag == 3):
        model = NN_model(np.array(X_train), np.array(y_train))
        prediction = find_best_prediction(model.predict(data_set))
        for i in range(len(prediction)):
            if (prediction[i] == target_set[i]):
                matrix[prediction[i]][prediction[i]] = matrix[prediction[i]][prediction[i]] + 1
            else:
                matrix[target_set[i]][prediction[i]] = matrix[target_set[i]][prediction[i]] + 1
    elif (probability_flag == 4):
        model = CNN_model(Xi_train, yi_train)
        prediction = find_best_prediction(model.predict(data_set))
        for i in range(len(prediction)):
            if (prediction[i] == target_set[i]):
                matrix[prediction[i]][prediction[i]] = matrix[prediction[i]][prediction[i]] + 1
            else:
                matrix[target_set[i]][prediction[i]] = matrix[target_set[i]][prediction[i]] + 1
    #print matrix
    for i in matrix:
        print(i)
    plot_confusion_matrix(np.array(matrix))


def roc_draw(predict, ground_truth):
    nums = len(predict)

    x, y = 1, 1

    index = np.argsort(predict)
    ground = ground_truth[index]

    x_step = 1.0 / (nums - sum(ground_truth))  # 负样本步长
    y_step = 1. / sum(ground_truth)

    res_x = []
    res_y = []

    for i in range(nums):
        if ground[i] == 1:
            y -= y_step
        else:
            x -= x_step

        res_x.append(x)
        res_y.append(y)
    return res_x, res_y







def function_1():

    print("\nIn this program I have built 2 deep learning networks, one with convenutionl one without;")
    print("The dataset I am using is Optical recognition of handwritten digits dataset;")


    ui = input("choose one to view the structure of each: \n a.NN \n b.CNN \n :")

    if (ui == "a"):
        model = NN_model(X_train,y_train)
        model.summary()
    elif (ui == "b"):
        model = CNN_model(Xi_train, yi_train)
        model.summary()


def function_2():

    print("\n --- Choose one from below, which method you would like to use:\n a.Cross validation \n b.Confusion matrix \n c.ROC curve")
    usr_input = input("\n Enter a or b or c :")
    if(usr_input == "a"):
        print("\n --- Choose one from below, which model you would like to evaluate: \n a.sklearn-DC model \n b.self-DC model \n c.NN model \n d.CNN model ")
        usr_input = input("\n Enter a or b or c or d:")
        if(usr_input == "a"):
            cross_val(X,y,1)
        elif(usr_input == "b"):
            z = ["f" + str(i) for i in range(64)]
            global mytree
            mytree = treegrow(X_train, y_train, z)
            cross_val(X,y,2)
        elif (usr_input == "c"):
            cross_val(X,y,3)
        elif (usr_input == "d"):
            cross_val(p,y,4)
    elif(usr_input == "b"):
        print("\n --- Choose one from below, which model you would like to evaluate: \n a.sklearn-DC model \n b.self-DC model \n c.NN model \n d.CNN model ")
        usr_input = input("\n Enter a or b or c or d:")
        if (usr_input == "a"):
            confusion_matrix(X,y,1)
        elif (usr_input == "b"):
            z = ["f" + str(i) for i in range(64)]
            mytree = treegrow(X_train, y_train, z)
            confusion_matrix(X,y,2)
        elif (usr_input == "c"):
            confusion_matrix(X,y,3)
        elif (usr_input == "d"):
            confusion_matrix(p,y,4)

    elif(usr_input == "c"):
        print("\n --- Choose one from below, which model you would like to evaluate: \n a.sklearn-DC model \n b.self-DC model \n c.NN model \n d.CNN model ")
        usr_input = input("\n Enter a or b or c or d:")
        if(usr_input == "a"):
            dtree = DecisionTreeClassifier(criterion='entropy', max_depth=10, random_state=0)
            dtree.fit(np.array(X_train), np.array(y_train))
            prediction = dtree.predict(X_test)
            x, yb = roc_draw(prediction, y_test)
            plt.plot(x, yb)
            plt.show()

        elif(usr_input == "b"):
            z = ["f" + str(i) for i in range(64)]
            mytree = treegrow(X_train, y_train, z)
            prediction = dc_predict(X_test, mytree, z)
            x, yb = roc_draw(prediction, y_test)
            plt.plot(x, yb)
            plt.show()

        elif (usr_input == "c"):
            model = NN_model(np.array(X_train), np.array(y_train))
            prediction = find_best_prediction(model.predict(X_test))
            x, yb = roc_draw(prediction, y_test)
            plt.plot(x, yb)
            plt.show()

        elif (usr_input == "d"):
            model = CNN_model(Xi_train, yi_train)
            prediction = find_best_prediction(model.predict(Xi_test))
            x, yb = roc_draw(prediction, yi_test)
            plt.plot(x, yb)
            plt.show()



#user interface
while(1):
    print("\n| Functionality Menu |\n")
    print("f1 -- Check f1")
    print("f2 -- Check f2")
    print("quit -- Terminate the program\n")
    user_input = input("Choose of the above to continue:")
    if(user_input == "f1"):
        function_1()
    elif(user_input == "f2"):
        function_2()
    elif (user_input == "quit"):
        break



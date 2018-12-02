import csv
from caserec.recommenders.rating_prediction.userknn import UserKNN as CFlick
import pickle

class coffeeFlick:
    def __init__(self):
        pass

    def printPrediction(self):

        for i in range(1,6):
            nam1 = "train" + str(i) + ".dat"
            nam2 = "test" + str(i) + ".dat"
            tr = "/home/souravghai/Desktop/courses/cf/assignment/assignment3/encoder/" + nam1
            te = "/home/souravghai/Desktop/courses/cf/assignment/assignment3/encoder/" + nam2

            # # Simple
            CFlick(tr, te).compute()

# mira.py
# -------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

# Mira implementation
import util

PRINT = True


class MiraClassifier:
    """
    Mira classifier.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to a raw samples.Datum).
    """

    def __init__(self, legalLabels, max_iterations):
        self.legalLabels = legalLabels
        self.type = "mira"
        self.automaticTuning = False
        self.C = 0.001
        self.legalLabels = legalLabels
        self.max_iterations = max_iterations
        self.initializeWeightsToZero()

    def initializeWeightsToZero(self):
        "Resets the weights of each label to zero vectors"
        self.weights = {}
        for label in self.legalLabels:
            self.weights[label] = util.Counter()  # this is the data-structure you should use

    def train(self, trainingData, trainingLabels, validationData, validationLabels):
        "Outside shell to call your method. Do not modify this method."

        self.features = trainingData[0].keys()  # this could be useful for your code later...

        if (self.automaticTuning):
            Cgrid = [0.002, 0.004, 0.008]
        else:
            Cgrid = [self.C]

        return self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, Cgrid)

    def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, Cgrid):
        """
        This method sets self.weights using MIRA.  Train the classifier for each value of C in Cgrid,
        then store the weights that give the best accuracy on the validationData.

        Use the provided self.weights[label] data structure so that
        the classify method works correctly. Also, recall that a
        datum is a counter from features to values for those features
        representing a vector of values.
        """
        "*** YOUR CODE HERE ***"
        """ Basically perceptron with the weights adjusted using an additional parameter
        for incorrect classifications we use weight^correct label += t * data and
        weight^prediction -= t * data. Where t is the min of the following equation

        t = min{c = 0.001, (weight[prediction] - weight[actual]) * data + 1 / 2 * (data * data)} """

        # same code as perceptron..... except for the calculation of t
        number_of_errors = 0
        for iteration in range(self.max_iterations):
            if iteration > 0:
                print "Number of Errors: ", number_of_errors
                # print the number of errors after each iteration
                number_of_errors = 0  # reset for next iteration
            print "Starting iteration ", iteration, "..."

            for i in range(len(trainingData)):
                "*** YOUR CODE HERE ***"
                # idea is the find the label that best represents
                # each datum (image)

                top_score = -1
                best_label = None
                current_image = trainingData[i]  # current image

                for label in self.legalLabels:
                    # Calculate the prediction on the current image for every labels weights (0-9)
                    result = current_image * self.weights[label]
                    if result > top_score:
                        # save the result with the largest value - i.e most likely to be correct
                        top_score = result
                        best_label = label

                actual_label = trainingLabels[i]

                if best_label != actual_label:  # prediction is incorrect
                    number_of_errors += 1
                    data = current_image.copy()
                    t = min(0.001, (self.weights[best_label] - self.weights[actual_label]) * data + 1.0 / 2.0 * (data * data))
                    data.multiply_all(t)  # method I wrote for Counter that multiplies every value by a scalar
                    # update weights
                    self.weights[actual_label] = self.weights[actual_label] + data  # under predicted
                    self.weights[best_label] = self.weights[best_label] - data  # over predicted

    def classify(self, data):
        """
        Classifies each datum as the label that most closely matches the prototype vector
        for that label.  See the project description for details.

        Recall that a datum is a util.counter...
        """
        guesses = []
        for datum in data:
            vectors = util.Counter()
            for l in self.legalLabels:
                vectors[l] = self.weights[l] * datum
            guesses.append(vectors.argMax())
        return guesses

    def findHighOddsFeatures(self, label1, label2):
        """
        Returns a list of the 100 features with the greatest difference in feature values
                         w_label1 - w_label2

        """
        featuresOdds = []

        "*** YOUR CODE HERE ***"

        return featuresOdds

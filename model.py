def classify():
    # import the necessary packages
    import numpy as np
    import argparse
    import time
    import cv2

    # construct the argument parse and parse the arguments
    # ap = argparse.ArgumentParser()
    # ap.add_argument("-i", "--image", required=True,
    #                 help="path to input image")
    # ap.add_argument("-p", "--prototxt", required=True,
    #                 help="path to Caffe 'deploy' prototxt file")
    # ap.add_argument("-m", "--model", required=True,
    #                 help="path to Caffe pre-trained model")
    # ap.add_argument("-l", "--labels", required=True,
    #                 help="path to ImageNet labels (i.e., syn-sets)")
    # args = vars(ap.parse_args())
    args = {'image': 'images/image.jpg', 'prototxt': 'bvlc_googlenet.prototxt',
            'model': 'bvlc_googlenet.caffemodel', 'labels': 'synset_words.txt'}

    # load the input image from disk
    image = cv2.imread(args["image"])

    # load the class labels from disk
    rows = open(args["labels"]).read().strip().split("\n")
    classes = [r[r.find(" ") + 1:].split(",")[0] for r in rows]

    # our CNN requires fixed spatial dimensions for our input image(s)
    # so we need to ensure it is resized to 224x224 pixels while
    # performing mean subtraction (104, 117, 123) to normalize the input;
    # after executing this command our "blob" now has the shape:
    # (1, 3, 224, 224)
    blob = cv2.dnn.blobFromImage(image, 1, (224, 224), (104, 117, 123))

    # load our serialized model from disk
    print("[INFO] loading model...")
    net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

    # set the blob as input to the network and perform a forward-pass to
    # obtain our output classification
    net.setInput(blob)
    start = time.time()
    preds = net.forward()
    end = time.time()
    print("[INFO] classification took {:.5} seconds".format(end - start))

    # sort the indexes of the probabilities in descending order (higher
    # probabilitiy first) and grab the top-5 predictions
    idxs = np.argsort(preds[0])[::-1][:5]

    classification = None
    confidence = 0
    for (i, idx) in enumerate(idxs):
        if i == 0:
            classification = classes[idx]
            confidence = preds[0][idx]
            break

    print(classification)
    print(confidence)

    return classification

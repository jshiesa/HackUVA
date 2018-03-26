def classify():
    import numpy as np
    import time
    import cv2

    args = {'image': 'images/image.jpg', 'prototxt': 'bvlc_googlenet.prototxt',
            'model': 'bvlc_googlenet.caffemodel', 'labels': 'synset_words.txt'}

    image = cv2.imread(args["image"])

    rows = open(args["labels"]).read().strip().split("\n")
    classes = [r[r.find(" ") + 1:].split(",")[0] for r in rows]

    blob = cv2.dnn.blobFromImage(image, 1, (224, 224), (104, 117, 123))

    print("[INFO] loading model...")
    net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

    net.setInput(blob)
    start = time.time()
    preds = net.forward()
    end = time.time()
    print("[INFO] classification took {:.5} seconds".format(end - start))

    idxs = np.argsort(preds[0])[::-1][:5]

    classification, confidence = None, None
    for (i, idx) in enumerate(idxs):
        if i == 0:
            classification = classes[idx]
            confidence = preds[0][idx]
        print("[INFO] {}. label: {}, probability: {:.5}".format(i + 1,
                                                                classes[idx], preds[0][idx]))

    print(classification, confidence)

    return classification

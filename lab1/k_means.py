"""
    Adapted from https://code.likeagirl.io/finding-dominant-colour-on-an-image-b4e075f98097
"""
import cv2
import numpy as np
from sklearn.cluster import KMeans

def find_histogram(clt):
    """
    create a histogram with k clusters
    :param: clt
    :return:hist
    """
    num_labels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=num_labels)

    hist = hist.astype("float")
    hist /= hist.sum()

    return hist

def plot_colors2(hist, centroids):
    bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0

    for (percent, color) in zip(hist, centroids):
        # plot the relative percentage of each cluster
        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                      color.astype("uint8").tolist(), -1)
        startX = endX

    # return the bar chart
    return bar

DOMAIN_DIM = 50
cap = cv2.VideoCapture(0)

while True:
    _, bgr_img = cap.read()
    rgb_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)

    # Define domain for KMeans Clustering
    y,x,_ = rgb_img.shape
    cx, cy = x//2, y//2
    (dx1, dy1) = cx - DOMAIN_DIM, cy - DOMAIN_DIM
    (dx2, dy2) = cx + DOMAIN_DIM, cy + DOMAIN_DIM

    domain = rgb_img[dy1:dy2, dx1:dx2, :]

    cv2.rectangle(bgr_img, (dx1, dy1), (dx2, dy2), (0, 255, 0), 4)

    domain = domain.reshape((domain.shape[0] * domain.shape[1],3)) #represent as row*column,channel number
    clt = KMeans(n_clusters=1, n_init=3)
    clt.fit(domain)

    histogram = find_histogram(clt)
    bar = plot_colors2(histogram, clt.cluster_centers_)

    # Convert RGB to BGR
    bar = np.flip(bar)

    cv2.imshow("Camera", bgr_img)
    cv2.imshow("Dominant Color", bar)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
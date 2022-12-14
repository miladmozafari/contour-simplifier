import cv2
import numpy as np
from typing import Sequence

def distance2line(p1: Sequence[int], p2: Sequence[int], p3: Sequence[int]) -> float:
    """
    Returns the distance of the point `p3` to the line passing through `p1` and `p2`.
    Args:
        `p1`: The first point on the line
        `p2`: The second point on the line
        `p3`: The point to compute its distance to the line

    Returns:
        The distance of `p3` to the line
    """
    dist = np.abs((p2[0]-p1[0]) * (p1[1]-p3[1]) - (p1[0]-p3[0]) * (p2[1]-p1[1]))
    dist = dist / np.sqrt((p2[0]-p1[0])*(p2[0]-p1[0]) + (p2[1]-p1[1])*(p2[1]-p1[1]))
    return dist

def simplify_contour(contours: Sequence[Sequence[Sequence[int]]], d:float) -> Sequence[Sequence[Sequence[int]]]:
    """
    Given a contour as a sequence of points, it returns a simplified version based on the distance parameter `d`.
    Larger valued of `d` results in simpler contours but less similar to the original contour.
    Args:
        `contours`: a sequence of contours generated by opencv
        `d`: the tuning parameter for the amount of simplification
    
    Returns:
        A sequence of simplified contours
    """

    simp = []
    for contour in contours:
        left  = 0
        right = 2
        res = [contour[0]]

        while right < len(contour):
            p1 = contour[left][0]
            p2 = contour[right][0]
            p3 = contour[right-1][0]
            dist = distance2line(p1,p2,p3)
            if dist > d:
                left = right - 1
                res.append(contour[left])
            right += 1
        simp.append(np.array(res))
    return tuple(simp)

if __name__ == "__main__":

    # load an image to find its contour
    image = cv2.imread('bdancer.jpg')

    # opencv contour algorithm only works with grayscale images
    # image = cv2.bitwise_not(image)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # it works better with binary images
    ret, thresh = cv2.threshold(image_gray, 150, 255, cv2.THRESH_BINARY)

    # finding original contours using opencv
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    print(f"number of points (original): {contours[0].shape[0]}")
    
    # draw the original contour in green for comparison
    contour_orig = image.copy()
    cv2.drawContours(contour_orig, contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
    
    # simplify the contours
    simp_contours = simplify_contour(contours, 0.6)
    print(f"number of points (original): {simp_contours[0].shape[0]}")

    # draw the simplified contour in green and save
    cv2.drawContours(contour_orig, simp_contours, contourIdx=-1, color=(0, 0, 255), thickness=2, lineType=cv2.LINE_AA)
    cv2.imwrite(f'countours.jpg', contour_orig)
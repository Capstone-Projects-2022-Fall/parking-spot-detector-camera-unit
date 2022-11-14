import cv2
import operator
import math

def pixelset(open_spots_mask, coords):
    return (open_spots_mask[coords] == [255, 255, 255]).all()

def find_next(spot_vector, coords):
    # height, width
    height, width, d = spot_vector.shape

    offsets = [
        (-1, 0),
        (-1, 1),
        (0, 1),
        (1, 1)
    ]

    for o in offsets:
        curr_coords = tuple(map(operator.add, coords, o))

        # check if curr_coords in picture
        if(curr_coords[0] >= height or curr_coords[1] >= width):
            break

        if((spot_vector[curr_coords] == [255, 255, 255]).all()):
            return curr_coords

    return None


def find_open_segments(open_spots_mask, spot_vector):
    # find num vectors

    # find init red pixels

    image_sz = spot_vector.shape
    height = image_sz[0]
    width = image_sz[1]

    # list of line starts
    line_starts = []

    for y in range(height):
        for x in range(width):
            if((spot_vector[y, x] == [0, 0, 255]).all()):
                line_starts.append((y, x))

    segments = []

    for coords in line_starts:
        curr_coords = coords
        in_spot = False
        curr_segment = []
        last_coords = None

        while curr_coords:
            if(pixelset(open_spots_mask, curr_coords)):
                if(not in_spot):
                    curr_segment.append(curr_coords)
                    in_spot = True
            else:
                if(in_spot):
                    curr_segment.append(curr_coords)
                    segments.append(curr_segment)
                    curr_segment = []
                    in_spot = False

            last_coords = curr_coords
            curr_coords = find_next(spot_vector, curr_coords)

        if(in_spot):
            curr_segment.append(last_coords)
            segments.append(curr_segment)
            curr_segment = []
            in_spot = False

    return segments


def find_mid_points_and_size(segments, mpp=1, px_threshold=0, meter_threshold=0):
    points_and_size = []

    for segment in segments:
        a, b = segment

        midpoint = (int((b[0] + a[0]) / 2), int((b[1] + a[1]) / 2))
        # slope * dX
        size = math.sqrt(abs((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2))

        if(size < px_threshold):
            continue

        m_size = size * mpp

        if(m_size < meter_threshold):
            continue

        point_and_size = (midpoint, m_size)
        points_and_size.append(point_and_size)

        print(point_and_size)


test_mask = cv2.imread("test.png")
test_vectors = cv2.imread("vectors.png")
print(test_mask.size)
segments = find_open_segments(test_mask, test_vectors)
find_mid_points_and_size(segments, mpp=2/70, meter_threshold=1)

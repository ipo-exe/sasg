import numpy as np
import pandas as pd


def create_rectangle_wkt(x_min, x_max, y_min, y_max):
    """
    Returns a WKT representation of a rectangular polygon.

    :param x_min: Minimum x-coordinate (left boundary)
    :param x_max: Maximum x-coordinate (right boundary)
    :param y_min: Minimum y-coordinate (bottom boundary)
    :param y_max: Maximum y-coordinate (top boundary)
    :return: WKT string representing the rectangle as a POLYGON
    """
    wkt = (
        f"POLYGON(({x_min} {y_min}, {x_min} {y_max}, {x_max} {y_max}, "
        f"{x_max} {y_min}, {x_min} {y_min}))"
    )
    return wkt

def retrieve_number(s_number):
    """
    Converts a string representation of a geographical coordinate with hemisphere
    information into a signed float.

    :param s_number: A string of the geographical number with direction (e.g., "N45p67")
    :return: A signed float representing the geographical coordinate.
    """
    # Convert the input string to lowercase to ensure consistent processing
    s_number = s_number.lower()
    # Dictionary to convert compass direction to mathematical sign
    d_signal = {
        "w": "-",
        "s": "-",
        "n": "+",
        "e": "+"
    }
    # Replace 'p' with '.' to conform to float formatting
    s_number = s_number.replace("p", ".")
    # Apply the sign based on the first character (direction) and concatenate with the number
    s_number = d_signal[s_number[0]] + s_number[1:]
    # Convert the string to a float and return it
    return float(s_number)


def format_number(f_number, axis="y"):
    """
    Formats a numerical geographic coordinate into a string with hemisphere indication.

    :param f_number: The coordinate value as a float.
    :param axis: Specifies the axis ('x' for longitude, 'y' for latitude) for correct hemisphere encoding.
    :return: String formatted with hemisphere and coordinate.
    """
    # Dictionaries to map positive and negative values to hemisphere indicators
    d_signal_positive = {
        "y": "n",
        "x": "e"
    }
    d_signal_negative = {
        "y": "s",
        "x": "w"
    }
    # Determine hemisphere based on the sign of the number
    if f_number >= 0:
        s_hem = d_signal_positive[axis]
    else:
        s_hem = d_signal_negative[axis]

    # Convert number to positive and format to replace '.' with 'p'
    f_abs = abs(f_number)
    s_abs = str(f_abs).replace(".", "p")

    if axis is None:
        s_hem = ""
    # Return the hemisphere followed by the absolute value of the coordinate
    return s_hem + s_abs


def get_code(x_min, x_max, y_min, y_max):
    """
    Generates a unique code string based on the geographical bounds of a rectangle.

    :param x_min: Minimum longitude value.
    :param x_max: Maximum longitude value.
    :param y_min: Minimum latitude value.
    :param y_max: Maximum latitude value.
    :return: A unique code combining formatted coordinates with '-' as a delimiter.
    """
    # Format each boundary value and collect them into a list
    ls = [
        format_number(f_number=x_min, axis="x"),
        format_number(f_number=x_max, axis="x"),
        format_number(f_number=y_min, axis="y"),
        format_number(f_number=y_max, axis="y")
    ]
    # Concatenate formatted values into a single string with dashes
    s = "-".join(ls)
    return s


def get_grid_df(step, xs_min=-110, xs_max=-18, ys_min=-60, ys_max=18):
    """
    Generates a grid of rectangular polygons defined by a step size and geographic bounds.

    :param step: The size of the step for the grid.
    :param xs_min: Minimum x-coordinate of the grid.
    :param xs_max: Maximum x-coordinate of the grid.
    :param ys_min: Minimum y-coordinate of the grid.
    :param ys_max: Maximum y-coordinate of the grid.
    :return: A DataFrame containing the grid polygons and their corresponding codes and IDs.
    """
    # Create arrays for the x and y coordinates using the given step size
    xs = np.arange(xs_min, xs_max, step)
    ys = np.arange(ys_min, ys_max, step)

    # Lists to store grid data
    lst_ids = []
    lst_codes = []
    lst_xmin = []
    lst_xmax = []
    lst_ymin = []
    lst_ymax = []
    lst_wkt = []

    # Counter for unique polygon IDs
    c_id = 1
    # Nested loops to create polygons and their codes
    for i in range(len(xs) - 1):
        for j in range(len(ys) - 1):
            xmin = xs[i]
            xmax = xs[i + 1]
            ymin = ys[j]
            ymax = ys[j + 1]

            # Generate WKT for the polygon and collect grid data
            s = create_rectangle_wkt(xmin, xmax, ymin, ymax)
            lst_ids.append(c_id)
            lst_xmin.append(xmin)
            lst_xmax.append(xmax)
            lst_ymin.append(ymin)
            lst_ymax.append(ymax)
            lst_wkt.append(s)
            lst_codes.append(get_code(xmin, xmax, ymin, ymax))
            c_id = c_id + 1

    # Assemble data into a DataFrame
    d = {
        "Id": lst_ids,
        "tile_code": lst_codes,
        "x_min": lst_xmin,
        "x_max": lst_xmax,
        "y_min": lst_ymin,
        "y_max": lst_ymax,
        "geometry": lst_wkt
    }
    df = pd.DataFrame(d)
    return df


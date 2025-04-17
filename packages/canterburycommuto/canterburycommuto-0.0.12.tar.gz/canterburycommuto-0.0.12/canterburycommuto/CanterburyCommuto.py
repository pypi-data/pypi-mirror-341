import csv
import datetime
import math
import os
import random
from typing import Dict, List, Tuple
from multiprocessing.dummy import Pool

import folium
import polyline
import requests
from IPython.display import display, IFrame
from pyproj import Geod, Transformer
from shapely.geometry import LineString, Polygon, mapping, MultiLineString, Point, GeometryCollection, MultiPoint

# Global function to generate URL
def generate_url(origin: str, destination: str, api_key: str) -> str:
    """
    Generates the Google Maps Directions API URL with the given parameters.

    Parameters:
    - origin (str): The starting point of the route (latitude,longitude).
    - destination (str): The endpoint of the route (latitude,longitude).
    - api_key (str): The API key for accessing the Google Maps Directions API.

    Returns:
    - str: The full URL for the API request.
    """
    return f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={api_key}"


# Function to read a csv file and then asks the users to manually enter their corresponding column variables with respect to OriginA, DestinationA, OriginB, and DestinationB.
def read_csv_file(
    csv_file: str, colorna: str, coldesta: str, colorib: str, colfestb: str
) -> List[Dict[str, str]]:
    """
    Reads a CSV file and maps user-specified column names to standardized names
    (OriginA, DestinationA, OriginB, DestinationB). Returns a list of dictionaries
    with standardized column names.

    Parameters:
    - csv_file (str): Path to the CSV file.
    - colorna (str): Column name for the origin of route A.
    - coldesta (str): Column name for the destination of route A.
    - colorib (str): Column name for the origin of route B.
    - colfestb (str): Column name for the destination of route B.

    Returns:
    - List[Dict[str, str]]: List of dictionaries with standardized column names.
    """
    with open(csv_file, mode="r") as file:
        reader = csv.DictReader(file)
        csv_columns = reader.fieldnames  # Extract column names from the CSV header

        # Validate column names
        required_columns = [colorna, coldesta, colorib, colfestb]
        for column in required_columns:
            if column not in csv_columns:
                raise ValueError(f"Column '{column}' not found in the CSV file.")

        # Map specified column names to standardized names
        column_mapping = {
            colorna: "OriginA",
            coldesta: "DestinationA",
            colorib: "OriginB",
            colfestb: "DestinationB",
        }

        # Replace original column names with standardized names in each row
        mapped_data = []
        for row in reader:
            mapped_row = {
                column_mapping.get(col, col): value for col, value in row.items()
            }
            mapped_data.append(mapped_row)

        return mapped_data


# Function to write results to a CSV file
def write_csv_file(output_csv: str, results: list, fieldnames: list) -> None:
    """
    Writes the results to a CSV file.

    Parameters:
    - output_csv (str): The path to the output CSV file.
    - results (list): A list of dictionaries containing the data to write.
    - fieldnames (list): A list of field names for the CSV file.

    Returns:
    - None
    """
    with open(output_csv, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


def get_route_data(origin: str, destination: str, api_key: str) -> tuple:
    """
    Fetches route data from the Google Maps Directions API and decodes it.

    Parameters:
    - origin (str): The starting point of the route (latitude,longitude).
    - destination (str): The endpoint of the route (latitude,longitude).
    - api_key (str): The API key for accessing the Google Maps Directions API.

    Returns:
    - tuple:
        - list: A list of (latitude, longitude) tuples representing the route.
        - float: Total route distance in kilometers.
        - float: Total route time in minutes.
    """
    # Use the global function to generate the URL
    url = generate_url(origin, destination, api_key)
    response = requests.get(url)
    directions_data = response.json()

    if directions_data["status"] == "OK":
        route_polyline = directions_data["routes"][0]["overview_polyline"]["points"]
        coordinates = polyline.decode(route_polyline)
        total_distance = (
            directions_data["routes"][0]["legs"][0]["distance"]["value"] / 1000
        )  # kilometers
        total_time = (
            directions_data["routes"][0]["legs"][0]["duration"]["value"] / 60
        )  # minutes
        return coordinates, total_distance, total_time
    else:
        print("Error fetching directions:", directions_data["status"])
        return [], 0, 0


# Function to find common nodes
def find_common_nodes(coordinates_a: list, coordinates_b: list) -> tuple:
    """
    Finds the first and last common nodes between two routes.

    Parameters:
    - coordinates_a (list): A list of (latitude, longitude) tuples representing route A.
    - coordinates_b (list): A list of (latitude, longitude) tuples representing route B.

    Returns:
    - tuple:
        - tuple or None: The first common node (latitude, longitude) or None if not found.
        - tuple or None: The last common node (latitude, longitude) or None if not found.
    """
    first_common_node = next(
        (coord for coord in coordinates_a if coord in coordinates_b), None
    )
    last_common_node = next(
        (coord for coord in reversed(coordinates_a) if coord in coordinates_b), None
    )
    return first_common_node, last_common_node


# Function to split route segments
def split_segments(coordinates: list, first_common: tuple, last_common: tuple) -> tuple:
    """
    Splits a route into 'before', 'overlap', and 'after' segments.

    Parameters:
    - coordinates (list): A list of (latitude, longitude) tuples representing the route.
    - first_common (tuple): The first common node (latitude, longitude).
    - last_common (tuple): The last common node (latitude, longitude).

    Returns:
    - tuple:
        - list: The 'before' segment of the route.
        - list: The 'overlap' segment of the route.
        - list: The 'after' segment of the route.
    """
    index_first = coordinates.index(first_common)
    index_last = coordinates.index(last_common)
    return (
        coordinates[: index_first + 1],
        coordinates[index_first : index_last + 1],
        coordinates[index_last:],
    )


# Function to compute percentages
def compute_percentages(segment_value: float, total_value: float) -> float:
    """
    Computes the percentage of a segment relative to the total.

    Parameters:
    - segment_value (float): The value of the segment (e.g., distance or time).
    - total_value (float): The total value (e.g., total distance or time).

    Returns:
    - float: The percentage of the segment relative to the total, or 0 if total_value is 0.
    """
    return (segment_value / total_value) * 100 if total_value > 0 else 0


# Function to generate unique file names for storing the outputs and maps
def generate_unique_filename(base_name: str, extension: str = ".csv") -> str:
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    random_id = random.randint(10000, 99999)
    return f"{base_name}-{timestamp}_{random_id}{extension}"


# Function to save the maps
def save_map(map_object, base_name: str) -> str:
    os.makedirs("results", exist_ok=True)
    filename = generate_unique_filename(os.path.join("results", base_name), ".html")
    map_object.save(filename)
    print(f"Map saved to: {os.path.abspath(filename)}")
    return filename

# Function to plot routes to display on maps
def plot_routes(
    coordinates_a: list, coordinates_b: list, first_common: tuple, last_common: tuple
) -> None:
    """
    Plots routes A and B with common nodes highlighted over an OpenStreetMap background.

    Parameters:
    - coordinates_a (list): A list of (latitude, longitude) tuples for route A.
    - coordinates_b (list): A list of (latitude, longitude) tuples for route B.
    - first_common (tuple): The first common node (latitude, longitude).
    - last_common (tuple): The last common node (latitude, longitude).

    Returns:
    - None
    """

    # If the routes completely overlap, set Route B to be the same as Route A
    if not coordinates_b:
        coordinates_b = coordinates_a

    # Calculate the center of the map
    avg_lat = sum(coord[0] for coord in coordinates_a + coordinates_b) / len(
        coordinates_a + coordinates_b
    )
    avg_lon = sum(coord[1] for coord in coordinates_a + coordinates_b) / len(
        coordinates_a + coordinates_b
    )

    # Create a map centered at the average location of the routes
    map_osm = folium.Map(location=[avg_lat, avg_lon], zoom_start=13)

    # Add Route A to the map
    folium.PolyLine(
        locations=coordinates_a, color="blue", weight=5, opacity=1, tooltip="Route A"
    ).add_to(map_osm)

    # Add Route B to the map
    folium.PolyLine(
        locations=coordinates_b, color="red", weight=5, opacity=1, tooltip="Route B"
    ).add_to(map_osm)

    # Add circular marker for the first common node (Cadet Blue)
    if first_common:
        folium.CircleMarker(
            location=[first_common[0], first_common[1]],
            radius=8,  
            color="cadetblue",  
            fill=True,
            fill_color="cadetblue",  
            fill_opacity=1,
            tooltip="First Common Node",
        ).add_to(map_osm)

    # Add circular marker for the last common node (Pink)
    if last_common:
        folium.CircleMarker(
            location=[last_common[0], last_common[1]],
            radius=8,
            color="pink",
            fill=True,
            fill_color="pink",
            fill_opacity=1,
            tooltip="Last Common Node",
        ).add_to(map_osm)

    # Add origin markers for Route A (Red) and Route B (Green)
    folium.Marker(
        location=coordinates_a[0],  
        icon=folium.Icon(color="red", icon="info-sign"), 
        tooltip="Origin A"
    ).add_to(map_osm)

    folium.Marker(
        location=coordinates_b[0],  
        icon=folium.Icon(color="green", icon="info-sign"), 
        tooltip="Origin B"
    ).add_to(map_osm)

    # Add destination markers as stars using DivIcon
    folium.Marker(
        location=coordinates_a[-1],
        icon=folium.DivIcon(
            html=f"""
            <div style="font-size: 16px; color: red; transform: scale(1.4);">
                <i class='fa fa-star'></i>
            </div>
            """
        ),
        tooltip="Destination A",
    ).add_to(map_osm)

    folium.Marker(
        location=coordinates_b[-1],
        icon=folium.DivIcon(
            html=f"""
            <div style="font-size: 16px; color: green; transform: scale(1.4);">
                <i class='fa fa-star'></i>
            </div>
            """
        ),
        tooltip="Destination B",
    ).add_to(map_osm)

    # Save the map using the save_map function
    map_filename = save_map(map_osm, "routes_map")

    # Display the map inline (only for Jupyter Notebooks)
    try:
        display(IFrame(map_filename, width="100%", height="500px"))
    except NameError:
        print(f"Map saved as '{map_filename}'. Open it in a browser.")

def wrap_row(args):
    row, api_key, row_function = args
    return row_function((row, api_key))

def process_rows(data, api_key, row_function, processes=None):
    args = [(row, api_key, row_function) for row in data]
    with Pool(processes=processes) as pool:
        results = pool.map(wrap_row, args)
    return results

def process_row_overlap(row_and_api_key):
    row, api_key = row_and_api_key
    origin_a, destination_a = row["OriginA"], row["DestinationA"]
    origin_b, destination_b = row["OriginB"], row["DestinationB"]

    if origin_a == origin_b and destination_a == destination_b:
        coordinates_a, a_dist, a_time = get_route_data(origin_a, destination_a, api_key)
        plot_routes(coordinates_a, [], None, None)
        return {
            "OriginA": origin_a, "DestinationA": destination_a,
            "OriginB": origin_b, "DestinationB": destination_b,
            "aDist": a_dist, "aTime": a_time,
            "bDist": a_dist, "bTime": a_time,
            "overlapDist": a_dist, "overlapTime": a_time,
            "aBeforeDist": 0.0, "aBeforeTime": 0.0,
            "bBeforeDist": 0.0, "bBeforeTime": 0.0,
            "aAfterDist": 0.0, "aAfterTime": 0.0,
            "bAfterDist": 0.0, "bAfterTime": 0.0,
        }

    coordinates_a, total_distance_a, total_time_a = get_route_data(origin_a, destination_a, api_key)
    coordinates_b, total_distance_b, total_time_b = get_route_data(origin_b, destination_b, api_key)

    first_common_node, last_common_node = find_common_nodes(coordinates_a, coordinates_b)

    if not first_common_node or not last_common_node:
        plot_routes(coordinates_a, coordinates_b, None, None)
        return {
            "OriginA": origin_a, "DestinationA": destination_a,
            "OriginB": origin_b, "DestinationB": destination_b,
            "aDist": total_distance_a, "aTime": total_time_a,
            "bDist": total_distance_b, "bTime": total_time_b,
            "overlapDist": 0.0, "overlapTime": 0.0,
            "aBeforeDist": 0.0, "aBeforeTime": 0.0,
            "bBeforeDist": 0.0, "bBeforeTime": 0.0,
            "aAfterDist": 0.0, "aAfterTime": 0.0,
            "bAfterDist": 0.0, "bAfterTime": 0.0,
        }

    before_a, overlap_a, after_a = split_segments(coordinates_a, first_common_node, last_common_node)
    before_b, overlap_b, after_b = split_segments(coordinates_b, first_common_node, last_common_node)

    _, before_a_distance, before_a_time = get_route_data(origin_a, f"{before_a[-1][0]},{before_a[-1][1]}", api_key)
    _, overlap_a_distance, overlap_a_time = get_route_data(
        f"{overlap_a[0][0]},{overlap_a[0][1]}", f"{overlap_a[-1][0]},{overlap_a[-1][1]}", api_key)
    _, after_a_distance, after_a_time = get_route_data(f"{after_a[0][0]},{after_a[0][1]}", destination_a, api_key)

    _, before_b_distance, before_b_time = get_route_data(origin_b, f"{before_b[-1][0]},{before_b[-1][1]}", api_key)
    _, after_b_distance, after_b_time = get_route_data(f"{after_b[0][0]},{after_b[0][1]}", destination_b, api_key)

    plot_routes(coordinates_a, coordinates_b, first_common_node, last_common_node)


    return {
        "OriginA": origin_a, "DestinationA": destination_a,
        "OriginB": origin_b, "DestinationB": destination_b,
        "aDist": total_distance_a, "aTime": total_time_a,
        "bDist": total_distance_b, "bTime": total_time_b,
        "overlapDist": overlap_a_distance, "overlapTime": overlap_a_time,
        "aBeforeDist": before_a_distance, "aBeforeTime": before_a_time,
        "bBeforeDist": before_b_distance, "bBeforeTime": before_b_time,
        "aAfterDist": after_a_distance if after_a else 0.0,
        "aAfterTime": after_a_time if after_a else 0.0,
        "bAfterDist": after_b_distance if after_b else 0.0,
        "bAfterTime": after_b_time if after_b else 0.0,
    }

def process_routes_with_csv(
    csv_file: str,
    api_key: str,
    output_csv: str = "output.csv",
    colorna: str = None,
    coldesta: str = None,
    colorib: str = None,
    colfestb: str = None,
) -> list:
    data = read_csv_file(
        csv_file=csv_file,
        colorna=colorna,
        coldesta=coldesta,
        colorib=colorib,
        colfestb=colfestb,
    )

    # Use multiprocessing to process rows in parallel
    results = process_rows(data, api_key, process_row_overlap)
    
    fieldnames = [
        "OriginA", "DestinationA", "OriginB", "DestinationB",
        "aDist", "aTime", "bDist", "bTime",
        "overlapDist", "overlapTime",
        "aBeforeDist", "aBeforeTime", "bBeforeDist", "bBeforeTime",
        "aAfterDist", "aAfterTime", "bAfterDist", "bAfterTime",
    ]

    write_csv_file(output_csv, results, fieldnames)
    return results

def process_row_only_overlap(row_and_api_key):
    row, api_key = row_and_api_key
    origin_a, destination_a = row["OriginA"], row["DestinationA"]
    origin_b, destination_b = row["OriginB"], row["DestinationB"]

    if origin_a == origin_b and destination_a == destination_b:
        coordinates_a, a_dist, a_time = get_route_data(origin_a, destination_a, api_key)
        plot_routes(coordinates_a, [], None, None)
        return {
            "OriginA": origin_a, "DestinationA": destination_a,
            "OriginB": origin_b, "DestinationB": destination_b,
            "aDist": a_dist, "aTime": a_time,
            "bDist": a_dist, "bTime": a_time,
            "overlapDist": a_dist, "overlapTime": a_time,
        }

    coordinates_a, total_distance_a, total_time_a = get_route_data(origin_a, destination_a, api_key)
    coordinates_b, total_distance_b, total_time_b = get_route_data(origin_b, destination_b, api_key)

    first_common_node, last_common_node = find_common_nodes(coordinates_a, coordinates_b)

    if not first_common_node or not last_common_node:
        plot_routes(coordinates_a, coordinates_b, None, None)
        return {
            "OriginA": origin_a, "DestinationA": destination_a,
            "OriginB": origin_b, "DestinationB": destination_b,
            "aDist": total_distance_a, "aTime": total_time_a,
            "bDist": total_distance_b, "bTime": total_time_b,
            "overlapDist": 0.0, "overlapTime": 0.0,
        }

    before_a, overlap_a, after_a = split_segments(coordinates_a, first_common_node, last_common_node)
    before_b, overlap_b, after_b = split_segments(coordinates_b, first_common_node, last_common_node)

    _, overlap_a_distance, overlap_a_time = get_route_data(
        f"{overlap_a[0][0]},{overlap_a[0][1]}", f"{overlap_a[-1][0]},{overlap_a[-1][1]}", api_key)

    overlap_b_distance, overlap_b_time = overlap_a_distance, overlap_a_time

    plot_routes(coordinates_a, coordinates_b, first_common_node, last_common_node)

    return {
        "OriginA": origin_a, "DestinationA": destination_a,
        "OriginB": origin_b, "DestinationB": destination_b,
        "aDist": total_distance_a, "aTime": total_time_a,
        "bDist": total_distance_b, "bTime": total_time_b,
        "overlapDist": overlap_a_distance, "overlapTime": overlap_a_time,
    }

def process_routes_only_overlap_with_csv(
    csv_file: str,
    api_key: str,
    output_csv: str = "output.csv",
    colorna: str = None,
    coldesta: str = None,
    colorib: str = None,
    colfestb: str = None,
) -> list:
    data = read_csv_file(
        csv_file=csv_file,
        colorna=colorna,
        coldesta=coldesta,
        colorib=colorib,
        colfestb=colfestb,
    )

    results = process_rows(data, api_key, process_row_only_overlap)

    fieldnames = [
        "OriginA", "DestinationA", "OriginB", "DestinationB",
        "aDist", "aTime", "bDist", "bTime",
        "overlapDist", "overlapTime",
    ]
    write_csv_file(output_csv, results, fieldnames)

    return results

##The following functions are used for finding approximations around the first and last common node. The approximation is probably more relevant when two routes crosses each other. The code can still be improved.
def great_circle_distance(
    coord1, coord2
):  # Function from Urban Economics and Real Estate course, taught by Professor Benoit Schmutz, Homework 1.
    """
    Compute the great-circle distance between two points using the provided formula.

    Parameters:
    - coord1: tuple of (latitude, longitude)
    - coord2: tuple of (latitude, longitude)

    Returns:
    - float: Distance in meters
    """
    OLA, OLO = coord1
    DLA, DLO = coord2

    # Convert latitude and longitude from degrees to radians
    L1 = OLA * math.pi / 180
    L2 = DLA * math.pi / 180
    DLo = abs(OLO - DLO) * math.pi / 180

    # Apply the great circle formula
    cosd = (math.sin(L1) * math.sin(L2)) + (math.cos(L1) * math.cos(L2) * math.cos(DLo))
    cosd = min(1, max(-1, cosd))  # Ensure cosd is in the range [-1, 1]

    # Take the arc cosine
    dist_degrees = math.acos(cosd) * 180 / math.pi

    # Convert degrees to miles
    dist_miles = 69.16 * dist_degrees

    # Convert miles to kilometers
    dist_km = 1.609 * dist_miles

    return dist_km * 1000  # Convert to meters


def calculate_distances(segment: list, label_prefix: str) -> list:
    """
    Calculates distances and creates labeled segments for a given list of coordinates.

    Parameters:
    - segment (list): A list of (latitude, longitude) tuples.
    - label_prefix (str): The prefix for labeling segments (e.g., 't' or 'T').

    Returns:
    - list: A list of dictionaries, each containing:
        - 'label': The label of the segment (e.g., t1, t2, ...).
        - 'start': Start coordinates of the segment.
        - 'end': End coordinates of the segment.
        - 'distance': Distance (in meters) for the segment.
    """
    segment_details = []
    for i in range(len(segment) - 1):
        start = segment[i]
        end = segment[i + 1]
        distance = great_circle_distance(start, end)
        label = f"{label_prefix}{i + 1}"
        segment_details.append(
            {"label": label, "start": start, "end": end, "distance": distance}
        )
    return segment_details


def calculate_segment_distances(before: list, after: list) -> dict:
    """
    Calculates the distance between each consecutive pair of coordinates in the
    'before' and 'after' segments from the split_segments function.
    Labels the segments as t1, t2, ... for before, and T1, T2, ... for after.

    Parameters:
    - before (list): A list of (latitude, longitude) tuples representing the route before the overlap.
    - after (list): A list of (latitude, longitude) tuples representing the route after the overlap.

    Returns:
    - dict: A dictionary with two keys:
        - 'before_segments': A list of dictionaries containing details about each segment in the 'before' route.
        - 'after_segments': A list of dictionaries containing details about each segment in the 'after' route.
    """
    # Calculate labeled segments for 'before' and 'after'
    before_segments = calculate_distances(before, label_prefix="t")
    after_segments = calculate_distances(after, label_prefix="T")

    return {"before_segments": before_segments, "after_segments": after_segments}


def calculate_rectangle_coordinates(start, end, width: float) -> list:
    """
    Calculates the coordinates of the corners of a rectangle for a given segment.

    Parameters:
    - start (tuple): The starting coordinate of the segment (latitude, longitude).
    - end (tuple): The ending coordinate of the segment (latitude, longitude).
    - width (float): The width of the rectangle in meters.

    Returns:
    - list: A list of 5 tuples representing the corners of the rectangle,
            including the repeated first corner to close the polygon.
    """
    # Calculate unit direction vector of the segment
    dx = end[1] - start[1]
    dy = end[0] - start[0]
    magnitude = (dx**2 + dy**2) ** 0.5
    unit_dx = dx / magnitude
    unit_dy = dy / magnitude

    # Perpendicular vector for the rectangle width
    perp_dx = -unit_dy
    perp_dy = unit_dx

    # Convert width to degrees (approximately)
    half_width = width / 2 / 111_111  # 111,111 meters per degree of latitude

    # Rectangle corner offsets
    offset_x = perp_dx * half_width
    offset_y = perp_dy * half_width

    # Define rectangle corners
    bottom_left = (start[0] - offset_y, start[1] - offset_x)
    top_left = (start[0] + offset_y, start[1] + offset_x)
    bottom_right = (end[0] - offset_y, end[1] - offset_x)
    top_right = (end[0] + offset_y, end[1] + offset_x)

    return [bottom_left, top_left, top_right, bottom_right, bottom_left]


def create_segment_rectangles(segments: list, width: float = 100) -> list:
    """
    Creates rectangles for each segment, where the length of the rectangle is the segment's distance
    and the width is the given default width.

    Parameters:
    - segments (list): A list of dictionaries, each containing:
        - 'label': The label of the segment (e.g., t1, t2, T1, T2).
        - 'start': Start coordinates of the segment.
        - 'end': End coordinates of the segment.
        - 'distance': Length of the segment in meters.
    - width (float): The width of the rectangle in meters (default: 100).

    Returns:
    - list: A list of dictionaries, each containing:
        - 'label': The label of the segment.
        - 'rectangle': A Shapely Polygon representing the rectangle.
    """
    rectangles = []
    for segment in segments:
        start = segment["start"]
        end = segment["end"]
        rectangle_coords = calculate_rectangle_coordinates(start, end, width)
        rectangle_polygon = Polygon(rectangle_coords)
        rectangles.append({"label": segment["label"], "rectangle": rectangle_polygon})

    return rectangles


def find_segment_combinations(rectangles_a: list, rectangles_b: list) -> dict:
    """
    Finds all combinations of segments between two routes (A and B).
    Each combination consists of one segment from A and one segment from B.

    Parameters:
    - rectangles_a (list): A list of dictionaries, each representing a rectangle segment from Route A.
        - Each dictionary contains:
            - 'label': The label of the segment (e.g., t1, t2, T1, T2).
            - 'rectangle': A Shapely Polygon representing the rectangle.
    - rectangles_b (list): A list of dictionaries, each representing a rectangle segment from Route B.

    Returns:
    - dict: A dictionary with two keys:
        - 'before_combinations': A list of tuples, each containing:
            - 'segment_a': The label of a segment from Route A.
            - 'segment_b': The label of a segment from Route B.
        - 'after_combinations': A list of tuples, with the same structure as above.
    """
    before_combinations = []
    after_combinations = []

    # Separate rectangles into before and after overlap based on labels
    before_a = [rect for rect in rectangles_a if rect["label"].startswith("t")]
    after_a = [rect for rect in rectangles_a if rect["label"].startswith("T")]
    before_b = [rect for rect in rectangles_b if rect["label"].startswith("t")]
    after_b = [rect for rect in rectangles_b if rect["label"].startswith("T")]

    # Find all combinations for "before" segments
    for rect_a in before_a:
        for rect_b in before_b:
            before_combinations.append((rect_a["label"], rect_b["label"]))

    # Find all combinations for "after" segments
    for rect_a in after_a:
        for rect_b in after_b:
            after_combinations.append((rect_a["label"], rect_b["label"]))

    return {
        "before_combinations": before_combinations,
        "after_combinations": after_combinations,
    }


def calculate_overlap_ratio(polygon_a, polygon_b) -> float:
    """
    Calculates the overlap area ratio between two polygons.

    Parameters:
    - polygon_a: A Shapely Polygon representing the first rectangle.
    - polygon_b: A Shapely Polygon representing the second rectangle.

    Returns:
    - float: The ratio of the overlapping area to the smaller polygon's area, as a percentage.
    """
    intersection = polygon_a.intersection(polygon_b)
    if intersection.is_empty:
        return 0.0

    overlap_area = intersection.area
    smaller_area = min(polygon_a.area, polygon_b.area)
    return (overlap_area / smaller_area) * 100 if smaller_area > 0 else 0.0


def filter_combinations_by_overlap(
    rectangles_a: list, rectangles_b: list, threshold: float = 50
) -> dict:
    """
    Finds and filters segment combinations based on overlapping area ratios.
    Retains only those combinations where the overlapping area is greater than
    the specified threshold of the smaller rectangle's area.

    Parameters:
    - rectangles_a (list): A list of dictionaries representing segments from Route A.
        - Each dictionary contains:
            - 'label': The label of the segment (e.g., t1, t2, T1, T2).
            - 'rectangle': A Shapely Polygon representing the rectangle.
    - rectangles_b (list): A list of dictionaries representing segments from Route B.
    - threshold (float): The minimum percentage overlap required (default: 50).

    Returns:
    - dict: A dictionary with two keys:
        - 'before_combinations': A list of tuples with retained combinations for "before overlap".
        - 'after_combinations': A list of tuples with retained combinations for "after overlap".
    """
    filtered_before_combinations = []
    filtered_after_combinations = []

    # Separate rectangles into before and after overlap
    before_a = [rect for rect in rectangles_a if rect["label"].startswith("t")]
    after_a = [rect for rect in rectangles_a if rect["label"].startswith("T")]
    before_b = [rect for rect in rectangles_b if rect["label"].startswith("t")]
    after_b = [rect for rect in rectangles_b if rect["label"].startswith("T")]

    # Process "before overlap" combinations
    for rect_a in before_a:
        for rect_b in before_b:
            overlap_ratio = calculate_overlap_ratio(
                rect_a["rectangle"], rect_b["rectangle"]
            )
            if overlap_ratio >= threshold:
                filtered_before_combinations.append(
                    (rect_a["label"], rect_b["label"], overlap_ratio)
                )

    # Process "after overlap" combinations
    for rect_a in after_a:
        for rect_b in after_b:
            overlap_ratio = calculate_overlap_ratio(
                rect_a["rectangle"], rect_b["rectangle"]
            )
            if overlap_ratio >= threshold:
                filtered_after_combinations.append(
                    (rect_a["label"], rect_b["label"], overlap_ratio)
                )

    return {
        "before_combinations": filtered_before_combinations,
        "after_combinations": filtered_after_combinations,
    }


def get_segment_by_label(rectangles: list, label: str) -> dict:
    """
    Finds a segment dictionary by its label.

    Parameters:
    - rectangles (list): A list of dictionaries, each representing a segment.
        - Each dictionary contains:
            - 'label': The label of the segment.
            - 'rectangle': A Shapely Polygon representing the rectangle.
    - label (str): The label of the segment to find.

    Returns:
    - dict: The dictionary representing the segment with the matching label.
    - None: If no matching segment is found.
    """
    for rect in rectangles:
        if rect["label"] == label:
            return rect
    return None


def find_overlap_boundary_nodes(
    filtered_combinations: dict, rectangles_a: list, rectangles_b: list
) -> dict:
    """
    Finds the first node of overlapping segments before the overlap and the last node of overlapping
    segments after the overlap for both Route A and Route B.

    Parameters:
    - filtered_combinations (dict): The filtered combinations output from filter_combinations_by_overlap.
        Contains 'before_combinations' and 'after_combinations'.
    - rectangles_a (list): A list of dictionaries representing segments from Route A.
    - rectangles_b (list): A list of dictionaries representing segments from Route B.

    Returns:
    - dict: A dictionary containing:
        - 'first_node_before_overlap': The first overlapping node and its label for Route A and B.
        - 'last_node_after_overlap': The last overlapping node and its label for Route A and B.
    """
    # Get the first combination before the overlap
    first_before_combination = (
        filtered_combinations["before_combinations"][0]
        if filtered_combinations["before_combinations"]
        else None
    )
    # Get the last combination after the overlap
    last_after_combination = (
        filtered_combinations["after_combinations"][-1]
        if filtered_combinations["after_combinations"]
        else None
    )

    first_node_before = None
    last_node_after = None

    if first_before_combination:
        # Extract labels from the first before overlap combination
        label_a, label_b, _ = first_before_combination

        # Find the corresponding segments
        segment_a = get_segment_by_label(rectangles_a, label_a)
        segment_b = get_segment_by_label(rectangles_b, label_b)

        # Get the first node of the segment
        if segment_a and segment_b:
            first_node_before = {
                "label_a": segment_a["label"],
                "node_a": segment_a["rectangle"].exterior.coords[0],
                "label_b": segment_b["label"],
                "node_b": segment_b["rectangle"].exterior.coords[0],
            }

    if last_after_combination:
        # Extract labels from the last after overlap combination
        label_a, label_b, _ = last_after_combination

        # Find the corresponding segments
        segment_a = get_segment_by_label(rectangles_a, label_a)
        segment_b = get_segment_by_label(rectangles_b, label_b)

        # Get the last node of the segment
        if segment_a and segment_b:
            last_node_after = {
                "label_a": segment_a["label"],
                "node_a": segment_a["rectangle"].exterior.coords[
                    -2
                ],  # Second-to-last for the last node
                "label_b": segment_b["label"],
                "node_b": segment_b["rectangle"].exterior.coords[
                    -2
                ],  # Second-to-last for the last node
            }

    return {
        "first_node_before_overlap": first_node_before,
        "last_node_after_overlap": last_node_after,
    }

def wrap_row_multiproc(args):
    row, api_key, row_function, *extra_args = args
    return row_function((row, api_key, *extra_args))

def process_rows_multiproc(data, api_key, row_function, processes=None, extra_args=()):
    args = [(row, api_key, row_function, *extra_args) for row in data]
    with Pool(processes=processes) as pool:
        results = pool.map(wrap_row_multiproc, args)
    return results

def process_row_overlap_rec_multiproc(row_and_args):
    row, api_key, width, threshold = row_and_args
    origin_a, destination_a = row["OriginA"], row["DestinationA"]
    origin_b, destination_b = row["OriginB"], row["DestinationB"]

    if origin_a == origin_b and destination_a == destination_b:
        coordinates_a, a_dist, a_time = get_route_data(origin_a, destination_a, api_key)
        plot_routes(coordinates_a, [], None, None)
        return {
            "OriginA": origin_a, "DestinationA": destination_a,
            "OriginB": origin_b, "DestinationB": destination_b,
            "aDist": a_dist, "aTime": a_time,
            "bDist": a_dist, "bTime": a_time,
            "overlapDist": a_dist, "overlapTime": a_time,
            "aBeforeDist": 0.0, "aBeforeTime": 0.0,
            "bBeforeDist": 0.0, "bBeforeTime": 0.0,
            "aAfterDist": 0.0, "aAfterTime": 0.0,
            "bAfterDist": 0.0, "bAfterTime": 0.0,
        }

    coordinates_a, total_distance_a, total_time_a = get_route_data(origin_a, destination_a, api_key)
    coordinates_b, total_distance_b, total_time_b = get_route_data(origin_b, destination_b, api_key)

    first_common_node, last_common_node = find_common_nodes(coordinates_a, coordinates_b)

    if not first_common_node or not last_common_node:
        plot_routes(coordinates_a, coordinates_b, None, None)
        return {
            "OriginA": origin_a, "DestinationA": destination_a,
            "OriginB": origin_b, "DestinationB": destination_b,
            "aDist": total_distance_a, "aTime": total_time_a,
            "bDist": total_distance_b, "bTime": total_time_b,
            "overlapDist": 0.0, "overlapTime": 0.0,
            "aBeforeDist": 0.0, "aBeforeTime": 0.0,
            "bBeforeDist": 0.0, "bBeforeTime": 0.0,
            "aAfterDist": 0.0, "aAfterTime": 0.0,
            "bAfterDist": 0.0, "bAfterTime": 0.0,
        }

    before_a, overlap_a, after_a = split_segments(coordinates_a, first_common_node, last_common_node)
    before_b, overlap_b, after_b = split_segments(coordinates_b, first_common_node, last_common_node)

    a_segment_distances = calculate_segment_distances(before_a, after_a)
    b_segment_distances = calculate_segment_distances(before_b, after_b)

    rectangles_a = create_segment_rectangles(
        a_segment_distances["before_segments"] + a_segment_distances["after_segments"], width=width)
    rectangles_b = create_segment_rectangles(
        b_segment_distances["before_segments"] + b_segment_distances["after_segments"], width=width)

    filtered_combinations = filter_combinations_by_overlap(
        rectangles_a, rectangles_b, threshold=threshold)

    boundary_nodes = find_overlap_boundary_nodes(
        filtered_combinations, rectangles_a, rectangles_b)

    if (
        not boundary_nodes["first_node_before_overlap"]
        or not boundary_nodes["last_node_after_overlap"]
    ):
        boundary_nodes = {
            "first_node_before_overlap": {
                "node_a": first_common_node,
                "node_b": first_common_node,
            },
            "last_node_after_overlap": {
                "node_a": last_common_node,
                "node_b": last_common_node,
            },
        }

    _, before_a_dist, before_a_time = get_route_data(
        origin_a,
        f"{boundary_nodes['first_node_before_overlap']['node_a'][0]},{boundary_nodes['first_node_before_overlap']['node_a'][1]}",
        api_key,
    )

    _, overlap_a_dist, overlap_a_time = get_route_data(
        f"{boundary_nodes['first_node_before_overlap']['node_a'][0]},{boundary_nodes['first_node_before_overlap']['node_a'][1]}",
        f"{boundary_nodes['last_node_after_overlap']['node_a'][0]},{boundary_nodes['last_node_after_overlap']['node_a'][1]}",
        api_key,
    )

    _, after_a_dist, after_a_time = get_route_data(
        f"{boundary_nodes['last_node_after_overlap']['node_a'][0]},{boundary_nodes['last_node_after_overlap']['node_a'][1]}",
        destination_a,
        api_key,
    )

    _, before_b_dist, before_b_time = get_route_data(
        origin_b,
        f"{boundary_nodes['first_node_before_overlap']['node_b'][0]},{boundary_nodes['first_node_before_overlap']['node_b'][1]}",
        api_key,
    )

    _, overlap_b_dist, overlap_b_time = get_route_data(
        f"{boundary_nodes['first_node_before_overlap']['node_b'][0]},{boundary_nodes['first_node_before_overlap']['node_b'][1]}",
        f"{boundary_nodes['last_node_after_overlap']['node_b'][0]},{boundary_nodes['last_node_after_overlap']['node_b'][1]}",
        api_key,
    )

    _, after_b_dist, after_b_time = get_route_data(
        f"{boundary_nodes['last_node_after_overlap']['node_b'][0]},{boundary_nodes['last_node_after_overlap']['node_b'][1]}",
        destination_b,
        api_key,
    )

    plot_routes(coordinates_a, coordinates_b, first_common_node, last_common_node)

    return {
        "OriginA": origin_a, "DestinationA": destination_a,
        "OriginB": origin_b, "DestinationB": destination_b,
        "aDist": total_distance_a, "aTime": total_time_a,
        "bDist": total_distance_b, "bTime": total_time_b,
        "overlapDist": overlap_a_dist, "overlapTime": overlap_a_time,
        "aBeforeDist": before_a_dist, "aBeforeTime": before_a_time,
        "bBeforeDist": before_b_dist, "bBeforeTime": before_b_time,
        "aAfterDist": after_a_dist, "aAfterTime": after_a_time,
        "bAfterDist": after_b_dist, "bAfterTime": after_b_time,
    }

def overlap_rec(
    csv_file: str,
    api_key: str,
    output_csv: str = "outputRec.csv",
    threshold: int = 50,
    width: int = 100,
    colorna: str = None,
    coldesta: str = None,
    colorib: str = None,
    colfestb: str = None,
) -> list:
    data = read_csv_file(
        csv_file=csv_file,
        colorna=colorna,
        coldesta=coldesta,
        colorib=colorib,
        colfestb=colfestb,
    )

    results = process_rows_multiproc(
        data, api_key, process_row_overlap_rec_multiproc, extra_args=(width, threshold)
    )

    fieldnames = [
        "OriginA", "DestinationA", "OriginB", "DestinationB",
        "aDist", "aTime", "bDist", "bTime",
        "overlapDist", "overlapTime",
        "aBeforeDist", "aBeforeTime", "bBeforeDist", "bBeforeTime",
        "aAfterDist", "aAfterTime", "bAfterDist", "bAfterTime",
    ]
    write_csv_file(output_csv, results, fieldnames)

    return results

def process_row_only_overlap_rec(row_and_args):
    row, api_key, width, threshold = row_and_args
    origin_a, destination_a = row["OriginA"], row["DestinationA"]
    origin_b, destination_b = row["OriginB"], row["DestinationB"]

    if origin_a == origin_b and destination_a == destination_b:
        coordinates_a, a_dist, a_time = get_route_data(origin_a, destination_a, api_key)
        plot_routes(coordinates_a, [], None, None)
        return {
            "OriginA": origin_a,
            "DestinationA": destination_a,
            "OriginB": origin_b,
            "DestinationB": destination_b,
            "aDist": a_dist,
            "aTime": a_time,
            "bDist": a_dist,
            "bTime": a_time,
            "overlapDist": a_dist,
            "overlapTime": a_time,
        }

    coordinates_a, total_distance_a, total_time_a = get_route_data(origin_a, destination_a, api_key)
    coordinates_b, total_distance_b, total_time_b = get_route_data(origin_b, destination_b, api_key)

    first_common_node, last_common_node = find_common_nodes(coordinates_a, coordinates_b)

    if not first_common_node or not last_common_node:
        plot_routes(coordinates_a, coordinates_b, None, None)
        return {
            "OriginA": origin_a,
            "DestinationA": destination_a,
            "OriginB": origin_b,
            "DestinationB": destination_b,
            "aDist": total_distance_a,
            "aTime": total_time_a,
            "bDist": total_distance_b,
            "bTime": total_time_b,
            "overlapDist": 0.0,
            "overlapTime": 0.0,
        }

    before_a, overlap_a, after_a = split_segments(coordinates_a, first_common_node, last_common_node)
    before_b, overlap_b, after_b = split_segments(coordinates_b, first_common_node, last_common_node)

    a_segment_distances = calculate_segment_distances(before_a, after_a)
    b_segment_distances = calculate_segment_distances(before_b, after_b)

    rectangles_a = create_segment_rectangles(
        a_segment_distances["before_segments"] + a_segment_distances["after_segments"], width=width)
    rectangles_b = create_segment_rectangles(
        b_segment_distances["before_segments"] + b_segment_distances["after_segments"], width=width)

    filtered_combinations = filter_combinations_by_overlap(
        rectangles_a, rectangles_b, threshold=threshold)

    boundary_nodes = find_overlap_boundary_nodes(
        filtered_combinations, rectangles_a, rectangles_b)

    if (
        not boundary_nodes["first_node_before_overlap"]
        or not boundary_nodes["last_node_after_overlap"]
    ):
        boundary_nodes = {
            "first_node_before_overlap": {
                "node_a": first_common_node,
                "node_b": first_common_node,
            },
            "last_node_after_overlap": {
                "node_a": last_common_node,
                "node_b": last_common_node,
            },
        }

    _, overlap_a_dist, overlap_a_time = get_route_data(
        f"{boundary_nodes['first_node_before_overlap']['node_a'][0]},{boundary_nodes['first_node_before_overlap']['node_a'][1]}",
        f"{boundary_nodes['last_node_after_overlap']['node_a'][0]},{boundary_nodes['last_node_after_overlap']['node_a'][1]}",
        api_key,
    )

    _, overlap_b_dist, overlap_b_time = get_route_data(
        f"{boundary_nodes['first_node_before_overlap']['node_b'][0]},{boundary_nodes['first_node_before_overlap']['node_b'][1]}",
        f"{boundary_nodes['last_node_after_overlap']['node_b'][0]},{boundary_nodes['last_node_after_overlap']['node_b'][1]}",
        api_key,
    )

    plot_routes(coordinates_a, coordinates_b, first_common_node, last_common_node)

    return {
        "OriginA": origin_a,
        "DestinationA": destination_a,
        "OriginB": origin_b,
        "DestinationB": destination_b,
        "aDist": total_distance_a,
        "aTime": total_time_a,
        "bDist": total_distance_b,
        "bTime": total_time_b,
        "overlapDist": overlap_a_dist,
        "overlapTime": overlap_a_time,
    }

def only_overlap_rec(
    csv_file: str,
    api_key: str,
    output_csv: str = "outputRec.csv",
    threshold: float = 50,
    width: float = 100,
    colorna: str = None,
    coldesta: str = None,
    colorib: str = None,
    colfestb: str = None,
) -> list:
    data = read_csv_file(
        csv_file=csv_file,
        colorna=colorna,
        coldesta=coldesta,
        colorib=colorib,
        colfestb=colfestb,
    )

    results = process_rows_multiproc(
        data, api_key, process_row_only_overlap_rec, extra_args=(width, threshold)
    )

    fieldnames = [
        "OriginA", "DestinationA", "OriginB", "DestinationB",
        "aDist", "aTime", "bDist", "bTime",
        "overlapDist", "overlapTime",
    ]
    write_csv_file(output_csv, results, fieldnames)

    return results

## The following functions create buffers along the commuting routes to find the ratios of buffers' intersection area over the two routes' total buffer areas.
def calculate_geodetic_area(polygon: Polygon) -> float:
    """
    Calculate the geodetic area of a polygon or multipolygon in square meters using the WGS84 ellipsoid.

    Args:
        polygon (Polygon or MultiPolygon): A shapely Polygon or MultiPolygon object in geographic coordinates (latitude/longitude).

    Returns:
        float: The total area of the polygon or multipolygon in square meters (absolute value).
    """
    geod = Geod(ellps="WGS84")

    if polygon.geom_type == "Polygon":
        lon, lat = zip(*polygon.exterior.coords)
        area, _ = geod.polygon_area_perimeter(lon, lat)
        return abs(area)

    elif polygon.geom_type == "MultiPolygon":
        total_area = 0
        for single_polygon in polygon.geoms:
            lon, lat = zip(*single_polygon.exterior.coords)
            area, _ = geod.polygon_area_perimeter(lon, lat)
            total_area += abs(area)
        return total_area

    else:
        raise ValueError(f"Unsupported geometry type: {polygon.geom_type}")

def create_buffered_route(
    route_coords: List[Tuple[float, float]],
    buffer_distance_meters: float,
    projection: str = "EPSG:3857",
) -> Polygon:
    """
    Create a buffer around a geographic route (lat/lon) by projecting to a Cartesian plane.

    Args:
        route_coords (List[Tuple[float, float]]): List of (latitude, longitude) coordinates representing the route.
        buffer_distance_meters (float): Buffer distance in meters.
        projection (str): EPSG code for the projection (default: Web Mercator - EPSG:3857).

    Returns:
        Polygon: Buffered polygon around the route in geographic coordinates (lat/lon), or None if not possible.
    """
    if not route_coords or len(route_coords) < 2:
        print("Warning: Not enough points to create buffer. Returning None.")
        return None

    transformer = Transformer.from_crs("EPSG:4326", projection, always_xy=True)
    inverse_transformer = Transformer.from_crs(projection, "EPSG:4326", always_xy=True)

    projected_coords = [transformer.transform(lon, lat) for lat, lon in route_coords]

    if len(projected_coords) < 2:
        print("Error: Not enough points after projection to create LineString.")
        return None

    projected_line = LineString(projected_coords)
    buffered_polygon = projected_line.buffer(buffer_distance_meters)

    return Polygon([
        inverse_transformer.transform(x, y)
        for x, y in buffered_polygon.exterior.coords
    ])

def plot_routes_and_buffers(
    route_a_coords: List[Tuple[float, float]],
    route_b_coords: List[Tuple[float, float]],
    buffer_a: Polygon,
    buffer_b: Polygon,
) -> None:
    """
    Plot two routes and their respective buffers over an OpenStreetMap background and display it inline.

    Args:
        route_a_coords (List[Tuple[float, float]]): Route A coordinates (latitude, longitude).
        route_b_coords (List[Tuple[float, float]]): Route B coordinates (latitude, longitude).
        buffer_a (Polygon): Buffered polygon for Route A.
        buffer_b (Polygon): Buffered polygon for Route B.

    Returns:
        None
    """

    # Calculate the center of the map
    avg_lat = sum(coord[0] for coord in route_a_coords + route_b_coords) / len(
        route_a_coords + route_b_coords
    )
    avg_lon = sum(coord[1] for coord in route_a_coords + route_b_coords) / len(
        route_a_coords + route_b_coords
    )

    # Create a map centered at the average location of the routes
    map_osm = folium.Map(location=[avg_lat, avg_lon], zoom_start=13)

    # Add Route A to the map
    folium.PolyLine(
        locations=route_a_coords, color="red", weight=5, opacity=1, tooltip="Route A"
    ).add_to(map_osm)

    # Add Route B to the map
    folium.PolyLine(
        locations=route_b_coords, color="orange", weight=5, opacity=1, tooltip="Route B"
    ).add_to(map_osm)

    # Add Buffer A to the map
    buffer_a_geojson = mapping(buffer_a)
    folium.GeoJson(
        buffer_a_geojson,
        style_function=lambda x: {
            "fillColor": "blue",
            "color": "blue",
            "fillOpacity": 0.5,
            "weight": 2,
        },
        tooltip="Buffer A",
    ).add_to(map_osm)

    # Add Buffer B to the map
    buffer_b_geojson = mapping(buffer_b)
    folium.GeoJson(
        buffer_b_geojson,
        style_function=lambda x: {
            "fillColor": "darkred",
            "color": "darkred",
            "fillOpacity": 0.5,
            "weight": 2,
        },
        tooltip="Buffer B",
    ).add_to(map_osm)

    # Add markers for O1 (Origin A) and O2 (Origin B)
    folium.Marker(
        location=route_a_coords[0],  
        icon=folium.Icon(color="red", icon="info-sign"), 
        tooltip="O1 (Origin A)"
    ).add_to(map_osm)

    folium.Marker(
        location=route_b_coords[0],  
        icon=folium.Icon(color="green", icon="info-sign"), 
        tooltip="O2 (Origin B)"
    ).add_to(map_osm)

    # Add markers for D1 (Destination A) and D2 (Destination B) as stars
    folium.Marker(
        location=route_a_coords[-1],
        tooltip="D1 (Destination A)",
        icon=folium.DivIcon(
            html="""
            <div style="font-size: 16px; color: red; transform: scale(1.4);">
                <i class='fa fa-star'></i>
            </div>
            """
        ),
    ).add_to(map_osm)

    folium.Marker(
        location=route_b_coords[-1],
        tooltip="D2 (Destination B)",
        icon=folium.DivIcon(
            html="""
            <div style="font-size: 16px; color: green; transform: scale(1.4);">
                <i class='fa fa-star'></i>
            </div>
            """
        ),
    ).add_to(map_osm)

    # Save the map using save_map function
    map_filename = save_map(map_osm, "routes_with_buffers_map")

    # Display the map inline
    display(IFrame(map_filename, width="100%", height="600px"))
    print(f"Map has been displayed inline and saved as '{map_filename}'.")


def calculate_area_ratios(
    buffer_a: Polygon, buffer_b: Polygon, intersection: Polygon
) -> Dict[str, float]:
    """
    Calculate the area ratios for the intersection relative to buffer A and buffer B.

    Args:
        buffer_a (Polygon): Buffered polygon for Route A.
        buffer_b (Polygon): Buffered polygon for Route B.
        intersection (Polygon): Intersection polygon of buffers A and B.

    Returns:
        Dict[str, float]: Dictionary containing the area ratios and intersection area.
    """
    # Calculate areas using geodetic area function
    intersection_area = calculate_geodetic_area(intersection)
    area_a = calculate_geodetic_area(buffer_a)
    area_b = calculate_geodetic_area(buffer_b)

    # Compute ratios
    ratio_over_a = (intersection_area / area_a) * 100 if area_a > 0 else 0
    ratio_over_b = (intersection_area / area_b) * 100 if area_b > 0 else 0

    # Return results
    return {
        "IntersectionArea": intersection_area,
        "aAreaRatio": ratio_over_a,
        "bAreaRatio": ratio_over_b,
    }

def process_row_route_buffers(row_and_args):
    row, api_key, buffer_distance = row_and_args
    origin_a, destination_a = row["OriginA"], row["DestinationA"]
    origin_b, destination_b = row["OriginB"], row["DestinationB"]

    if origin_a == destination_a and origin_b == destination_b:
        return {
            "OriginA": origin_a, "DestinationA": destination_a,
            "OriginB": origin_b, "DestinationB": destination_b,
            "aDist": 0, "aTime": 0, "bDist": 0, "bTime": 0,
            "aIntersecRatio": 0.0, "bIntersecRatio": 0.0,
        }

    if origin_a == destination_a and origin_b != destination_b:
        route_b_coords, b_dist, b_time = get_route_data(origin_b, destination_b, api_key)
        return {
            "OriginA": origin_a, "DestinationA": destination_a,
            "OriginB": origin_b, "DestinationB": destination_b,
            "aDist": 0, "aTime": 0, "bDist": b_dist, "bTime": b_time,
            "aIntersecRatio": 0.0, "bIntersecRatio": 0.0,
        }

    if origin_a != destination_a and origin_b == destination_b:
        route_a_coords, a_dist, a_time = get_route_data(origin_a, destination_a, api_key)
        return {
            "OriginA": origin_a, "DestinationA": destination_a,
            "OriginB": origin_b, "DestinationB": destination_b,
            "aDist": a_dist, "aTime": a_time, "bDist": 0, "bTime": 0,
            "aIntersecRatio": 0.0, "bIntersecRatio": 0.0,
        }

    route_a_coords, a_dist, a_time = get_route_data(origin_a, destination_a, api_key)
    route_b_coords, b_dist, b_time = get_route_data(origin_b, destination_b, api_key)

    if origin_a == origin_b and destination_a == destination_b:
        buffer_a = create_buffered_route(route_a_coords, buffer_distance)
        buffer_b = buffer_a
        plot_routes_and_buffers(route_a_coords, route_b_coords, buffer_a, buffer_b)
        return {
            "OriginA": origin_a, "DestinationA": destination_a,
            "OriginB": origin_b, "DestinationB": destination_b,
            "aDist": a_dist, "aTime": a_time,
            "bDist": a_dist, "bTime": a_time,
            "aIntersecRatio": 1.0, "bIntersecRatio": 1.0,
        }

    buffer_a = create_buffered_route(route_a_coords, buffer_distance)
    buffer_b = create_buffered_route(route_b_coords, buffer_distance)
    intersection = buffer_a.intersection(buffer_b)

    plot_routes_and_buffers(route_a_coords, route_b_coords, buffer_a, buffer_b)

    if intersection.is_empty:
        return {
            "OriginA": origin_a, "DestinationA": destination_a,
            "OriginB": origin_b, "DestinationB": destination_b,
            "aDist": a_dist, "aTime": a_time,
            "bDist": b_dist, "bTime": b_time,
            "aIntersecRatio": 0.0, "bIntersecRatio": 0.0,
        }

    intersection_area = intersection.area
    a_area = buffer_a.area
    b_area = buffer_b.area
    a_intersec_ratio = intersection_area / a_area
    b_intersec_ratio = intersection_area / b_area

    return {
        "OriginA": origin_a, "DestinationA": destination_a,
        "OriginB": origin_b, "DestinationB": destination_b,
        "aDist": a_dist, "aTime": a_time,
        "bDist": b_dist, "bTime": b_time,
        "aIntersecRatio": a_intersec_ratio,
        "bIntersecRatio": b_intersec_ratio,
    }

def process_routes_with_buffers(
    csv_file: str,
    output_csv: str,
    api_key: str,
    buffer_distance: float = 100,
    colorna: str = None,
    coldesta: str = None,
    colorib: str = None,
    colfestb: str = None,
) -> None:
    data = read_csv_file(
        csv_file=csv_file,
        colorna=colorna,
        coldesta=coldesta,
        colorib=colorib,
        colfestb=colfestb,
    )

    results = process_rows_multiproc(
        data, api_key, process_row_route_buffers, extra_args=(buffer_distance,)
    )

    fieldnames = [
        "OriginA", "DestinationA", "OriginB", "DestinationB",
        "aDist", "aTime", "bDist", "bTime",
        "aIntersecRatio", "bIntersecRatio",
    ]

    write_csv_file(output_csv, results, fieldnames)

def calculate_precise_travel_segments(
    route_coords: List[List[float]],
    intersections: List[List[float]],
    api_key: str
) -> Dict[str, float]:
    """
    Calculates travel distances and times for segments of a route before, during,
    and after overlaps using Google Maps Directions API.
    Returns a dictionary with travel segment details.
    All coordinates are in the format [latitude, longitude].
    """

    if len(intersections) < 2:
        print(f"Only {len(intersections)} intersection(s) found, skipping during segment calculation.")
        if len(intersections) == 1:
            start = intersections[0]
            before_data = get_route_data(
                f"{route_coords[0][0]},{route_coords[0][1]}",
                f"{start[0]},{start[1]}",
                api_key
            )
            after_data = get_route_data(
                f"{start[0]},{start[1]}",
                f"{route_coords[-1][0]},{route_coords[-1][1]}",
                api_key
            )
            return {
                "before_distance": before_data[1],
                "before_time": before_data[2],
                "during_distance": 0.0,
                "during_time": 0.0,
                "after_distance": after_data[1],
                "after_time": after_data[2],
            }
        else:
            return {
                "before_distance": 0.0,
                "before_time": 0.0,
                "during_distance": 0.0,
                "during_time": 0.0,
                "after_distance": 0.0,
                "after_time": 0.0,
            }

    start = intersections[0]
    end = intersections[-1]

    before_data = get_route_data(
        f"{route_coords[0][0]},{route_coords[0][1]}",
        f"{start[0]},{start[1]}",
        api_key
    )
    during_data = get_route_data(
        f"{start[0]},{start[1]}",
        f"{end[0]},{end[1]}",
        api_key
    )
    after_data = get_route_data(
        f"{end[0]},{end[1]}",
        f"{route_coords[-1][0]},{route_coords[-1][1]}",
        api_key
    )

    print(f"Before segment: {before_data}")
    print(f"During segment: {during_data}")
    print(f"After segment: {after_data}")

    return {
        "before_distance": before_data[1],
        "before_time": before_data[2],
        "during_distance": during_data[1],
        "during_time": during_data[2],
        "after_distance": after_data[1],
        "after_time": after_data[2],
    }

def get_buffer_intersection(buffer1: Polygon, buffer2: Polygon) -> Polygon:
    """
    Returns the intersection of two buffer polygons.

    Args:
        buffer1 (Polygon): First buffer polygon.
        buffer2 (Polygon): Second buffer polygon.

    Returns:
        Polygon: Intersection polygon of the two buffers, or None if no intersection or invalid input.
    """
    if buffer1 is None or buffer2 is None:
        print("Warning: One or both buffer polygons are None. Cannot compute intersection.")
        return None

    intersection = buffer1.intersection(buffer2)
    return intersection if not intersection.is_empty else None

def get_route_polygon_intersections(route_coords: List[Tuple[float, float]], polygon: Polygon) -> List[Tuple[float, float]]:
    """
    Finds exact intersection points between a route LineString and a polygon.

    Args:
        route_coords (List[Tuple[float, float]]): The route as list of (lat, lon).
        polygon (Polygon): Polygon to intersect with.

    Returns:
        List[Tuple[float, float]]: List of intersection points in (lat, lon).
    """
    route_line = LineString([(lon, lat) for lat, lon in route_coords])  # shapely uses (x, y) = (lon, lat)
    intersection = route_line.intersection(polygon)

    if intersection.is_empty:
        return []
    
    # Handle different geometry types
    if isinstance(intersection, Point):
        return [(intersection.y, intersection.x)]
    elif isinstance(intersection, MultiPoint):
        return [(pt.y, pt.x) for pt in intersection.geoms]
    elif isinstance(intersection, LineString):
        return [(pt[1], pt[0]) for pt in intersection.coords]
    else:
        # Can include cases like MultiLineString or GeometryCollection
        return [
            (pt.y, pt.x) for geom in getattr(intersection, 'geoms', []) 
            if isinstance(geom, Point) for pt in [geom]
        ]
# The function calculates travel metrics and overlapping segments between two routes based on their closest nodes and shared buffer intersection.
def process_row_closest_nodes(row_and_args):
    row, api_key, buffer_distance = row_and_args
    origin_a, destination_a = row["OriginA"], row["DestinationA"]
    origin_b, destination_b = row["OriginB"], row["DestinationB"]

    if origin_a == destination_a and origin_b == destination_b:
        return {"OriginA": origin_a, "DestinationA": destination_a, "OriginB": origin_b, "DestinationB": destination_b,
                "aDist": 0.0, "aTime": 0.0, "bDist": 0.0, "bTime": 0.0, "aoverlapDist": 0.0, "aoverlapTime": 0.0,
                "boverlapDist": 0.0, "boverlapTime": 0.0, "aBeforeDist": 0.0, "aBeforeTime": 0.0, "aAfterDist": 0.0,
                "aAfterTime": 0.0, "bBeforeDist": 0.0, "bBeforeTime": 0.0, "bAfterDist": 0.0, "bAfterTime": 0.0}

    if origin_a == destination_a and origin_b != destination_b:
        coords_b, b_dist, b_time = get_route_data(origin_b, destination_b, api_key)
        return {"OriginA": origin_a, "DestinationA": destination_a, "OriginB": origin_b, "DestinationB": destination_b,
                "aDist": 0.0, "aTime": 0.0, "bDist": b_dist, "bTime": b_time, "aoverlapDist": 0.0, "aoverlapTime": 0.0,
                "boverlapDist": 0.0, "boverlapTime": 0.0, "aBeforeDist": 0.0, "aBeforeTime": 0.0, "aAfterDist": 0.0,
                "aAfterTime": 0.0, "bBeforeDist": 0.0, "bBeforeTime": 0.0, "bAfterDist": 0.0, "bAfterTime": 0.0}

    if origin_a != destination_a and origin_b == destination_b:
        coords_a, a_dist, a_time = get_route_data(origin_a, destination_a, api_key)
        return {"OriginA": origin_a, "DestinationA": destination_a, "OriginB": origin_b, "DestinationB": destination_b,
                "aDist": a_dist, "aTime": a_time, "bDist": 0.0, "bTime": 0.0, "aoverlapDist": 0.0, "aoverlapTime": 0.0,
                "boverlapDist": 0.0, "boverlapTime": 0.0, "aBeforeDist": 0.0, "aBeforeTime": 0.0, "aAfterDist": 0.0,
                "aAfterTime": 0.0, "bBeforeDist": 0.0, "bBeforeTime": 0.0, "bAfterDist": 0.0, "bAfterTime": 0.0}

    if origin_a == origin_b and destination_a == destination_b:
        coords_a, a_dist, a_time = get_route_data(origin_a, destination_a, api_key)
        buffer_a = create_buffered_route(coords_a, buffer_distance)
        coords_b = coords_a
        buffer_b = buffer_a
        plot_routes_and_buffers(coords_a, coords_b, buffer_a, buffer_b)
        return {"OriginA": origin_a, "DestinationA": destination_a, "OriginB": origin_b, "DestinationB": destination_b,
                "aDist": a_dist, "aTime": a_time, "bDist": a_dist, "bTime": a_time, "aoverlapDist": a_dist,
                "aoverlapTime": a_time, "boverlapDist": a_dist, "boverlapTime": a_time, "aBeforeDist": 0.0,
                "aBeforeTime": 0.0, "aAfterDist": 0.0, "aAfterTime": 0.0, "bBeforeDist": 0.0, "bBeforeTime": 0.0,
                "bAfterDist": 0.0, "bAfterTime": 0.0}

    coords_a, a_dist, a_time = get_route_data(origin_a, destination_a, api_key)
    coords_b, b_dist, b_time = get_route_data(origin_b, destination_b, api_key)
    buffer_a = create_buffered_route(coords_a, buffer_distance)
    buffer_b = create_buffered_route(coords_b, buffer_distance)
    intersection_polygon = get_buffer_intersection(buffer_a, buffer_b)
    plot_routes_and_buffers(coords_a, coords_b, buffer_a, buffer_b)

    if not intersection_polygon:
        overlap_a = overlap_b = {"during_distance": 0.0, "during_time": 0.0, "before_distance": 0.0, "before_time": 0.0,
                                  "after_distance": 0.0, "after_time": 0.0}
    else:
        nodes_inside_a = [pt for pt in coords_a if Point(pt[1], pt[0]).within(intersection_polygon)]
        nodes_inside_b = [pt for pt in coords_b if Point(pt[1], pt[0]).within(intersection_polygon)]

        if len(nodes_inside_a) >= 2:
            entry_a, exit_a = nodes_inside_a[0], nodes_inside_a[-1]
            overlap_a = calculate_precise_travel_segments(coords_a, [entry_a, exit_a], api_key)
        else:
            overlap_a = {"during_distance": 0.0, "during_time": 0.0, "before_distance": 0.0, "before_time": 0.0,
                         "after_distance": 0.0, "after_time": 0.0}

        if len(nodes_inside_b) >= 2:
            entry_b, exit_b = nodes_inside_b[0], nodes_inside_b[-1]
            overlap_b = calculate_precise_travel_segments(coords_b, [entry_b, exit_b], api_key)
        else:
            overlap_b = {"during_distance": 0.0, "during_time": 0.0, "before_distance": 0.0, "before_time": 0.0,
                         "after_distance": 0.0, "after_time": 0.0}

    return {
        "OriginA": origin_a, "DestinationA": destination_a,
        "OriginB": origin_b, "DestinationB": destination_b,
        "aDist": a_dist, "aTime": a_time, "bDist": b_dist, "bTime": b_time,
        "aoverlapDist": overlap_a["during_distance"], "aoverlapTime": overlap_a["during_time"],
        "boverlapDist": overlap_b["during_distance"], "boverlapTime": overlap_b["during_time"],
        "aBeforeDist": overlap_a["before_distance"], "aBeforeTime": overlap_a["before_time"],
        "aAfterDist": overlap_a["after_distance"], "aAfterTime": overlap_a["after_time"],
        "bBeforeDist": overlap_b["before_distance"], "bBeforeTime": overlap_b["before_time"],
        "bAfterDist": overlap_b["after_distance"], "bAfterTime": overlap_b["after_time"]
    }

def process_routes_with_closest_nodes(
    csv_file: str,
    api_key: str,
    buffer_distance: float = 100.0,
    output_csv: str = "output_closest_nodes.csv",
    colorna: str = None,
    coldesta: str = None,
    colorib: str = None,
    colfestb: str = None,
) -> list:
    data = read_csv_file(
        csv_file=csv_file,
        colorna=colorna,
        coldesta=coldesta,
        colorib=colorib,
        colfestb=colfestb,
    )

    results = process_rows_multiproc(
        data, api_key, process_row_closest_nodes, extra_args=(buffer_distance,)
    )

    if results:
        fieldnames = list(results[0].keys())
        with open(output_csv, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

    return results

def process_row_closest_nodes_simple(row_and_args):
    row, api_key, buffer_distance = row_and_args
    origin_a, destination_a = row["OriginA"], row["DestinationA"]
    origin_b, destination_b = row["OriginB"], row["DestinationB"]

    if origin_a == destination_a and origin_b == destination_b:
        return {
            "OriginA": origin_a, "DestinationA": destination_a,
            "OriginB": origin_b, "DestinationB": destination_b,
            "aDist": 0.0, "aTime": 0.0, "bDist": 0.0, "bTime": 0.0,
            "aoverlapDist": 0.0, "aoverlapTime": 0.0,
            "boverlapDist": 0.0, "boverlapTime": 0.0,
        }

    if origin_a == destination_a and origin_b != destination_b:
        coords_b, b_dist, b_time = get_route_data(origin_b, destination_b, api_key)
        return {
            "OriginA": origin_a, "DestinationA": destination_a,
            "OriginB": origin_b, "DestinationB": destination_b,
            "aDist": 0.0, "aTime": 0.0, "bDist": b_dist, "bTime": b_time,
            "aoverlapDist": 0.0, "aoverlapTime": 0.0,
            "boverlapDist": 0.0, "boverlapTime": 0.0,
        }

    if origin_a != destination_a and origin_b == destination_b:
        coords_a, a_dist, a_time = get_route_data(origin_a, destination_a, api_key)
        return {
            "OriginA": origin_a, "DestinationA": destination_a,
            "OriginB": origin_b, "DestinationB": destination_b,
            "aDist": a_dist, "aTime": a_time, "bDist": 0.0, "bTime": 0.0,
            "aoverlapDist": 0.0, "aoverlapTime": 0.0,
            "boverlapDist": 0.0, "boverlapTime": 0.0,
        }

    coords_a, a_dist, a_time = get_route_data(origin_a, destination_a, api_key)
    coords_b, b_dist, b_time = get_route_data(origin_b, destination_b, api_key)

    if origin_a == origin_b and destination_a == destination_b:
        buffer_a = create_buffered_route(coords_a, buffer_distance)
        buffer_b = buffer_a
        plot_routes_and_buffers(coords_a, coords_b, buffer_a, buffer_b)
        return {
            "OriginA": origin_a, "DestinationA": destination_a,
            "OriginB": origin_b, "DestinationB": destination_b,
            "aDist": a_dist, "aTime": a_time, "bDist": a_dist, "bTime": a_time,
            "aoverlapDist": a_dist, "aoverlapTime": a_time,
            "boverlapDist": a_dist, "boverlapTime": a_time,
        }

    buffer_a = create_buffered_route(coords_a, buffer_distance)
    buffer_b = create_buffered_route(coords_b, buffer_distance)
    intersection_polygon = get_buffer_intersection(buffer_a, buffer_b)

    plot_routes_and_buffers(coords_a, coords_b, buffer_a, buffer_b)

    if not intersection_polygon:
        print(f"No intersection for {origin_a} → {destination_a} and {origin_b} → {destination_b}")
        overlap_a_dist = overlap_a_time = overlap_b_dist = overlap_b_time = 0.0
    else:
        nodes_inside_a = [pt for pt in coords_a if Point(pt[1], pt[0]).within(intersection_polygon)]
        nodes_inside_b = [pt for pt in coords_b if Point(pt[1], pt[0]).within(intersection_polygon)]

        if len(nodes_inside_a) >= 2:
            entry_a, exit_a = nodes_inside_a[0], nodes_inside_a[-1]
            segments_a = calculate_precise_travel_segments(coords_a, [entry_a, exit_a], api_key)
            overlap_a_dist = segments_a.get("during_distance", 0.0)
            overlap_a_time = segments_a.get("during_time", 0.0)
        else:
            overlap_a_dist = overlap_a_time = 0.0

        if len(nodes_inside_b) >= 2:
            entry_b, exit_b = nodes_inside_b[0], nodes_inside_b[-1]
            segments_b = calculate_precise_travel_segments(coords_b, [entry_b, exit_b], api_key)
            overlap_b_dist = segments_b.get("during_distance", 0.0)
            overlap_b_time = segments_b.get("during_time", 0.0)
        else:
            overlap_b_dist = overlap_b_time = 0.0

    return {
        "OriginA": origin_a, "DestinationA": destination_a,
        "OriginB": origin_b, "DestinationB": destination_b,
        "aDist": a_dist, "aTime": a_time,
        "bDist": b_dist, "bTime": b_time,
        "aoverlapDist": overlap_a_dist, "aoverlapTime": overlap_a_time,
        "boverlapDist": overlap_b_dist, "boverlapTime": overlap_b_time,
    }

def process_routes_with_closest_nodes_simple(
    csv_file: str,
    api_key: str,
    buffer_distance: float = 100.0,
    output_csv: str = "output_closest_nodes_simple.csv",
    colorna: str = None,
    coldesta: str = None,
    colorib: str = None,
    colfestb: str = None,
) -> list:
    data = read_csv_file(
        csv_file=csv_file,
        colorna=colorna,
        coldesta=coldesta,
        colorib=colorib,
        colfestb=colfestb,
    )

    results = process_rows_multiproc(
        data, api_key, process_row_closest_nodes_simple, extra_args=(buffer_distance,)
    )

    if results:
        fieldnames = list(results[0].keys())
        with open(output_csv, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

    return results

def wrap_row_multiproc_exact(args):
    row, api_key, buffer_distance = args
    return process_row_exact_intersections(row, api_key, buffer_distance)

def process_row_exact_intersections(row, api_key, buffer_distance):
    origin_a, destination_a = row["OriginA"], row["DestinationA"]
    origin_b, destination_b = row["OriginB"], row["DestinationB"]

    if origin_a == destination_a and origin_b == destination_b:
        print(f"Skipping row: Origin A == Destination A and Origin B == Destination B ({origin_a}, {destination_a})")
        return {
            "OriginA": origin_a, "DestinationA": destination_a,
            "OriginB": origin_b, "DestinationB": destination_b,
            "aDist": 0.0, "aTime": 0.0, "bDist": 0.0, "bTime": 0.0,
            "aoverlapDist": 0.0, "aoverlapTime": 0.0,
            "boverlapDist": 0.0, "boverlapTime": 0.0,
            "aBeforeDist": 0.0, "aBeforeTime": 0.0,
            "aAfterDist": 0.0, "aAfterTime": 0.0,
            "bBeforeDist": 0.0, "bBeforeTime": 0.0,
            "bAfterDist": 0.0, "bAfterTime": 0.0,
        }

    if origin_a == destination_a and origin_b != destination_b:
        coords_b, b_dist, b_time = get_route_data(origin_b, destination_b, api_key)
        return {
            "OriginA": origin_a, "DestinationA": destination_a,
            "OriginB": origin_b, "DestinationB": destination_b,
            "aDist": 0.0, "aTime": 0.0, "bDist": b_dist, "bTime": b_time,
            "aoverlapDist": 0.0, "aoverlapTime": 0.0,
            "boverlapDist": 0.0, "boverlapTime": 0.0,
            "aBeforeDist": 0.0, "aBeforeTime": 0.0,
            "aAfterDist": 0.0, "aAfterTime": 0.0,
            "bBeforeDist": 0.0, "bBeforeTime": 0.0,
            "bAfterDist": 0.0, "bAfterTime": 0.0,
        }

    if origin_a != destination_a and origin_b == destination_b:
        coords_a, a_dist, a_time = get_route_data(origin_a, destination_a, api_key)
        return {
            "OriginA": origin_a, "DestinationA": destination_a,
            "OriginB": origin_b, "DestinationB": destination_b,
            "aDist": a_dist, "aTime": a_time, "bDist": 0.0, "bTime": 0.0,
            "aoverlapDist": 0.0, "aoverlapTime": 0.0,
            "boverlapDist": 0.0, "boverlapTime": 0.0,
            "aBeforeDist": 0.0, "aBeforeTime": 0.0,
            "aAfterDist": 0.0, "aAfterTime": 0.0,
            "bBeforeDist": 0.0, "bBeforeTime": 0.0,
            "bAfterDist": 0.0, "bAfterTime": 0.0,
        }

    coords_a, a_dist, a_time = get_route_data(origin_a, destination_a, api_key)
    coords_b, b_dist, b_time = get_route_data(origin_b, destination_b, api_key)

    buffer_a = create_buffered_route(coords_a, buffer_distance)
    buffer_b = create_buffered_route(coords_b, buffer_distance)
    intersection_polygon = get_buffer_intersection(buffer_a, buffer_b)

    plot_routes_and_buffers(coords_a, coords_b, buffer_a, buffer_b)

    if not intersection_polygon:
        print(f"No intersection for {origin_a} → {destination_a} and {origin_b} → {destination_b}")
        overlap_a = {
            "during_distance": 0.0, "during_time": 0.0,
            "before_distance": 0.0, "before_time": 0.0,
            "after_distance": 0.0, "after_time": 0.0,
        }
        overlap_b = {
            "during_distance": 0.0, "during_time": 0.0,
            "before_distance": 0.0, "before_time": 0.0,
            "after_distance": 0.0, "after_time": 0.0,
        }
    else:
        points_a = get_route_polygon_intersections(coords_a, intersection_polygon)
        points_b = get_route_polygon_intersections(coords_b, intersection_polygon)

        if len(points_a) >= 2:
            entry_a, exit_a = points_a[0], points_a[-1]
            overlap_a = calculate_precise_travel_segments(coords_a, [entry_a, exit_a], api_key)
        else:
            print("Not enough route A intersections.")
            overlap_a = {
                "during_distance": 0.0, "during_time": 0.0,
                "before_distance": 0.0, "before_time": 0.0,
                "after_distance": 0.0, "after_time": 0.0,
            }

        if len(points_b) >= 2:
            entry_b, exit_b = points_b[0], points_b[-1]
            overlap_b = calculate_precise_travel_segments(coords_b, [entry_b, exit_b], api_key)
        else:
            print("Not enough route B intersections.")
            overlap_b = {
                "during_distance": 0.0, "during_time": 0.0,
                "before_distance": 0.0, "before_time": 0.0,
                "after_distance": 0.0, "after_time": 0.0,
            }

    return {
        "OriginA": origin_a,
        "DestinationA": destination_a,
        "OriginB": origin_b,
        "DestinationB": destination_b,
        "aDist": a_dist,
        "aTime": a_time,
        "bDist": b_dist,
        "bTime": b_time,
        "aoverlapDist": overlap_a["during_distance"],
        "aoverlapTime": overlap_a["during_time"],
        "boverlapDist": overlap_b["during_distance"],
        "boverlapTime": overlap_b["during_time"],
        "aBeforeDist": overlap_a["before_distance"],
        "aBeforeTime": overlap_a["before_time"],
        "aAfterDist": overlap_a["after_distance"],
        "aAfterTime": overlap_a["after_time"],
        "bBeforeDist": overlap_b["before_distance"],
        "bBeforeTime": overlap_b["before_time"],
        "bAfterDist": overlap_b["after_distance"],
        "bAfterTime": overlap_b["after_time"],
    }

def process_routes_with_exact_intersections(
    csv_file: str,
    api_key: str,
    buffer_distance: float = 100.0,
    output_csv: str = "output_exact_intersections.csv",
    colorna: str = None,
    coldesta: str = None,
    colorib: str = None,
    colfestb: str = None,
) -> list:
    data = read_csv_file(
        csv_file=csv_file,
        colorna=colorna,
        coldesta=coldesta,
        colorib=colorib,
        colfestb=colfestb,
    )

    args_list = [(row, api_key, buffer_distance) for row in data]
    with Pool() as pool:
        results = pool.map(wrap_row_multiproc_exact, args_list)

    if results:
        fieldnames = list(results[0].keys())
        with open(output_csv, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

    return results

def wrap_row_multiproc_simple(args):
    row, api_key, buffer_distance = args
    return process_row_exact_intersections_simple((row, api_key, buffer_distance))

def process_row_exact_intersections_simple(row_and_args):
    row, api_key, buffer_distance = row_and_args
    origin_a, destination_a = row["OriginA"], row["DestinationA"]
    origin_b, destination_b = row["OriginB"], row["DestinationB"]

    if origin_a == destination_a and origin_b == destination_b:
        print(f"Skipping row: Origin A == Destination A and Origin B == Destination B ({origin_a}, {destination_a})")
        return {
            "OriginA": origin_a,
            "DestinationA": destination_a,
            "OriginB": origin_b,
            "DestinationB": destination_b,
            "aDist": 0.0,
            "aTime": 0.0,
            "bDist": 0.0,
            "bTime": 0.0,
            "aoverlapDist": 0.0,
            "aoverlapTime": 0.0,
            "boverlapDist": 0.0,
            "boverlapTime": 0.0,
        }

    if origin_a == destination_a and origin_b != destination_b:
        coords_b, b_dist, b_time = get_route_data(origin_b, destination_b, api_key)
        return {
            "OriginA": origin_a,
            "DestinationA": destination_a,
            "OriginB": origin_b,
            "DestinationB": destination_b,
            "aDist": 0.0,
            "aTime": 0.0,
            "bDist": b_dist,
            "bTime": b_time,
            "aoverlapDist": 0.0,
            "aoverlapTime": 0.0,
            "boverlapDist": 0.0,
            "boverlapTime": 0.0,
        }

    if origin_a != destination_a and origin_b == destination_b:
        coords_a, a_dist, a_time = get_route_data(origin_a, destination_a, api_key)
        return {
            "OriginA": origin_a,
            "DestinationA": destination_a,
            "OriginB": origin_b,
            "DestinationB": destination_b,
            "aDist": a_dist,
            "aTime": a_time,
            "bDist": 0.0,
            "bTime": 0.0,
            "aoverlapDist": 0.0,
            "aoverlapTime": 0.0,
            "boverlapDist": 0.0,
            "boverlapTime": 0.0,
        }

    if origin_a == origin_b and destination_a == destination_b:
        coords_a, a_dist, a_time = get_route_data(origin_a, destination_a, api_key)
        buffer_a = create_buffered_route(coords_a, buffer_distance)
        coords_b = coords_a
        buffer_b = buffer_a
        plot_routes_and_buffers(coords_a, coords_b, buffer_a, buffer_b)
        return {
            "OriginA": origin_a,
            "DestinationA": destination_a,
            "OriginB": origin_b,
            "DestinationB": destination_b,
            "aDist": a_dist,
            "aTime": a_time,
            "bDist": a_dist,
            "bTime": a_time,
            "aoverlapDist": a_dist,
            "aoverlapTime": a_time,
            "boverlapDist": a_dist,
            "boverlapTime": a_time,
        }

    coords_a, a_dist, a_time = get_route_data(origin_a, destination_a, api_key)
    coords_b, b_dist, b_time = get_route_data(origin_b, destination_b, api_key)

    buffer_a = create_buffered_route(coords_a, buffer_distance)
    buffer_b = create_buffered_route(coords_b, buffer_distance)
    intersection_polygon = get_buffer_intersection(buffer_a, buffer_b)

    plot_routes_and_buffers(coords_a, coords_b, buffer_a, buffer_b)

    if not intersection_polygon:
        print(f"No intersection for {origin_a} → {destination_a} and {origin_b} → {destination_b}")
        overlap_a_dist = 0.0
        overlap_a_time = 0.0
        overlap_b_dist = 0.0
        overlap_b_time = 0.0
    else:
        points_a = get_route_polygon_intersections(coords_a, intersection_polygon)
        points_b = get_route_polygon_intersections(coords_b, intersection_polygon)

        if len(points_a) >= 2:
            entry_a, exit_a = points_a[0], points_a[-1]
            segments_a = calculate_precise_travel_segments(coords_a, [entry_a, exit_a], api_key)
            overlap_a_dist = segments_a.get("during_distance", 0.0)
            overlap_a_time = segments_a.get("during_time", 0.0)
        else:
            print("Not enough route A intersections.")
            overlap_a_dist = 0.0
            overlap_a_time = 0.0

        if len(points_b) >= 2:
            entry_b, exit_b = points_b[0], points_b[-1]
            segments_b = calculate_precise_travel_segments(coords_b, [entry_b, exit_b], api_key)
            overlap_b_dist = segments_b.get("during_distance", 0.0)
            overlap_b_time = segments_b.get("during_time", 0.0)
        else:
            print("Not enough route B intersections.")
            overlap_b_dist = 0.0
            overlap_b_time = 0.0

    return {
        "OriginA": origin_a,
        "DestinationA": destination_a,
        "OriginB": origin_b,
        "DestinationB": destination_b,
        "aDist": a_dist,
        "aTime": a_time,
        "bDist": b_dist,
        "bTime": b_time,
        "aoverlapDist": overlap_a_dist,
        "aoverlapTime": overlap_a_time,
        "boverlapDist": overlap_b_dist,
        "boverlapTime": overlap_b_time,
    }

def process_routes_with_exact_intersections_simple(
    csv_file: str,
    api_key: str,
    buffer_distance: float = 100.0,
    output_csv: str = "output_exact_intersections_simple.csv",
    colorna: str = None,
    coldesta: str = None,
    colorib: str = None,
    colfestb: str = None,
) -> list:
    data = read_csv_file(
        csv_file=csv_file,
        colorna=colorna,
        coldesta=coldesta,
        colorib=colorib,
        colfestb=colfestb,
    )

    args = [(row, api_key, buffer_distance) for row in data]
    with Pool() as pool:
        results = pool.map(wrap_row_multiproc_simple, args)

    if results:
        fieldnames = list(results[0].keys())
        with open(output_csv, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

    return results

# Function to write txt file for displaying inputs for the package to run.
def write_log(file_path: str, options: dict) -> None:
    """
    Writes a log file summarizing the inputs used for running the package.

    Args:
        file_path (str): Path of the main CSV result file.
        options (dict): Dictionary of options and their values.
    Returns:
        None
    """
    # Ensure results folder exists
    os.makedirs("results", exist_ok=True)
    base_filename = os.path.basename(file_path).replace(".csv", ".log")

    # Force the log file to be saved inside the results folder
    log_file_path = os.path.join("results", base_filename)

    # Write the log file
    with open(log_file_path, "w", encoding="utf-8") as log_file:
        log_file.write("Options:\n")
        for key, value in options.items():
            log_file.write(f"{key}: {value}\n")
        log_file.write(f"Generated on: {datetime.datetime.now()}\n")

    print(f"Log file saved to: {os.path.abspath(log_file_path)}")


## This is the main function with user interaction.
def Overlap_Function(
    csv_file: str,
    api_key: str,
    threshold: float = 50,
    width: float = 100,
    buffer: float = 100,
    approximation: str = "no",
    commuting_info: str = "no",
    colorna: str = None,
    coldesta: str = None,
    colorib: str = None,
    colfestb: str = None,
    output_overlap: str = None,
    output_buffer: str = None,
) -> None:
    os.makedirs("results", exist_ok=True)

    options = {
        "csv_file": csv_file,
        "api_key": "********",
        "threshold": threshold,
        "width": width,
        "buffer": buffer,
        "approximation": approximation,
        "commuting_info": commuting_info,
        "colorna": colorna,
        "coldesta": coldesta,
        "colorib": colorib,
        "colfestb": colfestb,
    }

    if output_overlap:
        output_overlap = os.path.join("results", os.path.basename(output_overlap))
    if output_buffer:
        output_buffer = os.path.join("results", os.path.basename(output_buffer))

    if approximation == "yes":
        if commuting_info == "yes":
            output_overlap = output_overlap or generate_unique_filename("results/outputRec", ".csv")
            overlap_rec(csv_file, api_key, output_csv=output_overlap, threshold=threshold, width=width, colorna=colorna, coldesta=coldesta, colorib=colorib, colfestb=colfestb)
            write_log(output_overlap, options)
        elif commuting_info == "no":
            output_overlap = output_overlap or generate_unique_filename("results/outputRec_only_overlap", ".csv")
            only_overlap_rec(csv_file, api_key, output_csv=output_overlap, threshold=threshold, width=width, colorna=colorna, coldesta=coldesta, colorib=colorib, colfestb=colfestb)
            write_log(output_overlap, options)

    elif approximation == "no":
        if commuting_info == "yes":
            output_overlap = output_overlap or generate_unique_filename("results/outputRoutes", ".csv")
            process_routes_with_csv(csv_file, api_key, output_csv=output_overlap, colorna=colorna, coldesta=coldesta, colorib=colorib, colfestb=colfestb)
            write_log(output_overlap, options)
        elif commuting_info == "no":
            output_overlap = output_overlap or generate_unique_filename("results/outputRoutes_only_overlap", ".csv")
            process_routes_only_overlap_with_csv(csv_file, api_key, output_csv=output_overlap, colorna=colorna, coldesta=coldesta, colorib=colorib, colfestb=colfestb)
            write_log(output_overlap, options)

    elif approximation == "yes with buffer":
        output_buffer = output_buffer or generate_unique_filename("results/buffer_intersection_results", ".csv")
        process_routes_with_buffers(csv_file=csv_file, output_csv=output_buffer, api_key=api_key, buffer_distance=buffer, colorna=colorna, coldesta=coldesta, colorib=colorib, colfestb=colfestb)
        write_log(output_buffer, options)

    elif approximation == "closer to precision":
        if commuting_info == "yes":
            output_buffer = output_buffer or generate_unique_filename("results/closest_nodes_buffer_results", ".csv")
            process_routes_with_closest_nodes(csv_file=csv_file, api_key=api_key, buffer_distance=buffer, output_csv=output_buffer, colorna=colorna, coldesta=coldesta, colorib=colorib, colfestb=colfestb)
            write_log(output_buffer, options)
        elif commuting_info == "no":
            output_buffer = output_buffer or generate_unique_filename("results/closest_nodes_buffer_only_overlap", ".csv")
            process_routes_with_closest_nodes_simple(csv_file=csv_file, api_key=api_key, buffer_distance=buffer, output_csv=output_buffer, colorna=colorna, coldesta=coldesta, colorib=colorib, colfestb=colfestb)
            write_log(output_buffer, options)

    elif approximation == "exact":
        if commuting_info == "yes":
            output_buffer = output_buffer or generate_unique_filename("results/exact_intersection_buffer_results", ".csv")
            process_routes_with_exact_intersections(csv_file=csv_file, api_key=api_key, buffer_distance=buffer, output_csv=output_buffer, colorna=colorna, coldesta=coldesta, colorib=colorib, colfestb=colfestb)
            write_log(output_buffer, options)
        elif commuting_info == "no":
            output_buffer = output_buffer or generate_unique_filename("results/exact_intersection_buffer_only_overlap", ".csv")
            process_routes_with_exact_intersections_simple(csv_file=csv_file, api_key=api_key, buffer_distance=buffer, output_csv=output_buffer, colorna=colorna, coldesta=coldesta, colorib=colorib, colfestb=colfestb)
            write_log(output_buffer, options)

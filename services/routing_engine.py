# WARNING!!!

# THIS MODULE HAS BEEN AI-GENERATED
# AND MAY NOT BE UP TO PROJECT STANDARDS (NOT TESTED)
# AS OF MARCH 2026, A REPLACEMENT ROUTING ENGINE
# IS IN DEVELOPMENT. ETA: 1-5 APRIL 2026
# IMPLEMENTATION IS SUBJECT TO CHANGE!

# (this module is safe to use with live db)

from datetime import datetime, timedelta
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from sqlalchemy.orm import Session
from services.distmatrix_generator import get_time_matrix


def datetime_to_minutes(dt: datetime, base_time: datetime) -> int:
    """Convert and round datetime to minutes for VRPTW solver."""
    if not dt:
        return 0
    delta = dt - base_time
    return int(delta.total_seconds() // 60)


def run_routing_solver(db: Session, orders: list, drivers: list):
    """Initiate and run the Google OR-VRPTW solver."""
    if not orders or not drivers:
        print("Missing orders or drivers. Aborting routing.")
        return

    # ---------------------------------------------------------
    # STEP 1: Node Mapping (Create the Graph)
    # ---------------------------------------------------------
    nodes = []

    for driver in drivers:
        lat = driver.latitude if driver.latitude is not None else 0.0
        lng = driver.longitude if driver.longitude is not None else 0.0
        nodes.append({"lat": lat, "lng": lng, "type": "driver", "obj": driver})

    for order in orders:
        lat = order.latitude if order.latitude is not None else 0.0
        lng = order.longitude if order.longitude is not None else 0.0
        nodes.append({"lat": lat, "lng": lng, "type": "order", "obj": order})

    # ---------------------------------------------------------
    # STEP 2: Fetch OSRM Matrix & Inject "Dummy End Node"
    # ---------------------------------------------------------
    coords = [(n["lat"], n["lng"]) for n in nodes]
    raw_osrm_matrix = get_time_matrix(coords)

    if not raw_osrm_matrix or len(raw_osrm_matrix) != len(nodes):
        print("Failed to get a valid OSRM time matrix! Aborting routing.")
        return

    time_matrix = []
    for row in raw_osrm_matrix:
        time_matrix.append([int(val // 60) for val in row])

    # --- OPEN ROUTING LOGIC: The Dummy End Node ---
    # We add an extra node index that represents the "end of shift".
    # Traveling from anywhere to this dummy node takes 0 minutes.
    dummy_node_index = len(nodes)

    # Add a column of 0s to every existing row (cost to go to the dummy node)
    for row in time_matrix:
        row.append(0)

    # Add a final row of 0s for the dummy node itself (cost to leave dummy node, though unused)
    time_matrix.append([0] * (dummy_node_index + 1))

    # All vehicles start at their respective driver indexes, but ALL end at the dummy node
    starts = list(range(len(drivers)))  # Indexes 0 to len(drivers)-1
    ends = [dummy_node_index] * len(drivers)

    # ---------------------------------------------------------
    # STEP 3: Build Time Windows
    # ---------------------------------------------------------
    time_windows = []
    for node in nodes:
        if node["type"] == "driver":
            time_windows.append((0, 1440))
        else:
            order = node["obj"]
            start_min = datetime_to_minutes(order.startTime, datetime.now()) if order.startTime else 0
            end_min = datetime_to_minutes(order.endTime, datetime.now()) if order.endTime else 1440
            time_windows.append((max(0, start_min), max(0, end_min)))

    # Add wide-open time window for the dummy end node
    time_windows.append((0, 1440))

    # ---------------------------------------------------------
    # STEP 4: Configure OR-Tools Data Model
    # ---------------------------------------------------------
    data = {
        "time_matrix": time_matrix,
        "time_windows": time_windows,
        "num_vehicles": len(drivers),
        "starts": starts,
        "ends": ends
    }

    manager = pywrapcp.RoutingIndexManager(
        len(data["time_matrix"]),
        data["num_vehicles"],
        data["starts"],
        data["ends"]
    )
    routing = pywrapcp.RoutingModel(manager)

    def time_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["time_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(time_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    routing.AddDimension(
        transit_callback_index,
        720,  # max slacking time (12h wait time limit)
        1440,  # max total route time (24h)
        False,
        "Time"
    )
    time_dimension = routing.GetDimensionOrDie("Time")

    for location_idx, time_window in enumerate(data["time_windows"]):
        if location_idx in data["starts"] or location_idx == dummy_node_index:
            continue

        index = manager.NodeToIndex(location_idx)
        time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])

    # ---------------------------------------------------------
    # STEP 5: Solve!
    # ---------------------------------------------------------
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    search_parameters.time_limit.seconds = 10

    solution = routing.SolveWithParameters(search_parameters)

    # ---------------------------------------------------------
    # STEP 6: Parse Output & Update Database
    # ---------------------------------------------------------
    if solution:
        print("\n--- SOLUTION FOUND ---")
        for vehicle_id in range(data["num_vehicles"]):
            driver = drivers[vehicle_id]
            index = routing.Start(vehicle_id)

            route_output = f"Route for Driver {driver.username} (ID: {driver.driverId}):\n"
            route_output += f"  Start: [{driver.latitude}, {driver.longitude}]\n"

            sequence_counter = 1

            while not routing.IsEnd(index):
                node_index = manager.IndexToNode(index)

                if node_index < len(nodes):
                    node = nodes[node_index]
                    time_var = time_dimension.CumulVar(index)
                    eta_minutes = solution.Min(time_var)

                    if node["type"] == "order":
                        assigned_order = node["obj"]

                        route_output += f"  -> [Seq {sequence_counter}] Order {assigned_order.orderId} (ETA: {eta_minutes} mins)\n"

                        # Update DB Objects
                        assigned_order.driverId = driver.driverId
                        assigned_order.status = 1
                        assigned_order.routeSequence = sequence_counter
                        assigned_order.eta = datetime.now() + timedelta(minutes=eta_minutes)

                        sequence_counter += 1

                index = solution.Value(routing.NextVar(index))

            print(route_output)

        db.commit()
        print("Database updated successfully.\n")
    else:
        print("No mathematical solution found for these time windows/locations!")
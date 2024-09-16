

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from metro import GraphM
import traceback

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

g = GraphM()
g.create_metro_map()


@app.route('/')
def index():
    return render_template('index.html')

def future_project():
    return render_template('future.html')

@app.route('/api/stations', methods=['GET'])
def get_stations():
    stations = g.get_stations()
    return jsonify(stations)

@app.route('/api/list_stations', methods=['GET'])
def list_stations():
    return jsonify({'stations': g.get_stations()})

  # Adjust import based on your project structure



@app.route('/api/path_details', methods=['POST'])
def path_details():
    try:
        data = request.json
        print("Received data:", data)  # Debug print
        source = data.get('source')
        destination = data.get('destination')

        print(f"Source: {source}, Destination: {destination}")

        # Check if source and destination are provided
        if not source or not destination:
            raise ValueError("Source or destination is missing")

        # Check if the stations exist in the graph
        if not g.contains_vertex(source):
            raise ValueError(f"Source station '{source}' does not exist in the graph.")
        if not g.contains_vertex(destination):
            raise ValueError(f"Destination station '{destination}' does not exist in the graph.")

        # Calculate distance and time
        print("Calculating distance...")
        distance = g.dijkstra(source, destination, False)
        print(f"Distance calculated: {distance}")

        print("Calculating time...")
        time = g.dijkstra(source, destination, True) // 60
        print(f"Time calculated: {time}")

        print("Calculating path...")
        path_str = g.get_minimum_distance(source, destination)
        print(f"Path calculated: {path_str}")

        # Split the path string to get the stations
        path_parts = path_str.split()
        path = []

        # Clean up path parts
        for part in path_parts:
            if '==' in part or '->' in part:  # Check for interchange or segment separators
                continue
            if part:  # Check if part is not empty
                path.append(part)

        # Calculate total stations
        total_stations = len(path) - 2 if len(path) > 2 else 0  # Exclude source and destination

        # Find stations between source and destination
        stations_between = path[1:-1] if len(path) > 2 else []

        # Check if both source and destination are on the same line
        source_line = g.is_same_line(source)
        destination_line = g.is_same_line(destination)

        # Find interchanges only if the lines are different
        interchanges = []
        if source_line != destination_line:
            interchanges = [station for station in path if '==' in station]

        # Handle direct travel without interchanges
        else:
            interchanges = []  # No interchange needed if on the same line

        result = {
            'source_to_destination': f"From {source} to {destination}",
            'stations_between': {
                'count': len(stations_between),
                'names': stations_between
            },
            'interchanges': {
                'count': len(interchanges),
                'stations': interchanges if interchanges else "No interchange required"
            },
            'distance': f"{distance} KM",
            'time': f"{time} minutes"
        }

        return jsonify(result)
    except KeyError as e:
        print(f"KeyError: {str(e)}")  # Log the missing key
        return jsonify({'error': f'Missing key: {str(e)}'}), 400
    except ValueError as e:
        print(f"ValueError: {str(e)}")  # Log the value error
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f"Error in path_details: {str(e)}")
        print(f"Exception type: {type(e).__name__}")
        print("Traceback:")
        traceback.print_exc()
        error_message = f"An unexpected error occurred: {str(e)}"
        return jsonify({'error': error_message}), 500


@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)



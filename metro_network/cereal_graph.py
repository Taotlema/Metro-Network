# Imports for managing File Handling
import os
import csv

# Imports for instantiating social network
import networkx as nx

# Import for outputting social network
import matplotlib.pyplot as plt

# Define data types for each field
SHIPMENT_ID = str
ORIGIN_STATE = str
ORIGIN_MA = int
ORIGIN_CFS_AREA = str
DEST_STATE = str
DEST_MA = int
DEST_CFS_AREA = str
NAICS = int
QUARTER = int
SCTG = str
MODE = int
SHIPMENT_VALUE = float
SHIPMENT_WGHT = float
SHIPMENT_DIST_GC = float
SHIPMENT_DIST_ROUTED = float
TEMP_CNTL_YN = str
EXPORT_YN = str
EXPORT_CNTRY = str
HAZMAT = str
WGT_FACTOR = float

# Define the Commodity Exchange object
class CommodityExchange:
    def __init__(self, shipment_id, origin_state, origin_ma, origin_cfs_area,
                 dest_state, dest_ma, dest_cfs_area, naics, quarter, sctg, mode,
                 shipment_value, shipment_weight, shipment_dist_gc, shipment_dist_routed,
                 temp_control_yn, export_yn, export_country, hazmat, weight_factor):
        self.shipment_id = shipment_id
        self.origin_state = origin_state
        self.origin_ma = origin_ma
        self.origin_cfs_area = origin_cfs_area
        self.dest_state = dest_state
        self.dest_ma = dest_ma
        self.dest_cfs_area = dest_cfs_area
        self.naics = naics
        self.quarter = quarter
        self.sctg = sctg
        self.mode = mode
        self.shipment_value = shipment_value
        self.shipment_weight = shipment_weight
        self.shipment_dist_gc = shipment_dist_gc
        self.shipment_dist_routed = shipment_dist_routed
        self.temp_control_yn = temp_control_yn
        self.export_yn = export_yn
        self.export_country = export_country
        self.hazmat = hazmat
        self.weight_factor = weight_factor

# cmd_ex_list = empty list to store CommodityExchange objects
cmd_ex_list = []

# File reading process - iterating through each line in CSV File
def process_csv_line(line):
    fields = line.strip().split(",")

    # Check for invalid number of fields
    if len(fields) != 20:
        print(f"Error: Invalid number of fields in line: {line}")
        return

    try:
        # Converts each field to its respective data type
        shipment_id = fields[0]
        origin_state = fields[1]
        origin_ma = int(fields[2])
        origin_cfs_area = fields[3]
        dest_state = fields[4]
        dest_ma = int(fields[5])
        dest_cfs_area = fields[6]
        naics = int(fields[7])
        quarter = int(fields[8])
        sctg = fields[9]
        mode = int(fields[10])
        shipment_value = float(fields[11])
        shipment_weight = float(fields[12])
        shipment_dist_gc = float(fields[13])
        shipment_dist_routed = float(fields[14])
        temp_control_yn = fields[15]
        export_yn = fields[16]
        export_country = fields[17]
        hazmat = fields[18]
        weight_factor = float(fields[19])
    except ValueError:
        # Handle invalid data types
        print(f"Error: Invalid data type in line: {line}")
        return

    # Filter data based on the specified conditions
    if (origin_state == '37' or dest_state == '37') or \
       (origin_cfs_area in ['37-268', '37-172', '37-450', '37-99999'] or dest_cfs_area in ['37-268', '37-172', '37-450', '37-99999']):

        # Additional condition to check SCTG value
        if sctg == '03':
            # Instantiates CommodityExchange Object using input data
            commodity_exchange = CommodityExchange(
                shipment_id, origin_state, origin_ma, origin_cfs_area,
                dest_state, dest_ma, dest_cfs_area, naics, quarter, sctg, mode,
                shipment_value, shipment_weight, shipment_dist_gc, shipment_dist_routed,
                temp_control_yn, export_yn, export_country, hazmat, weight_factor
            )

            # Adds the CommodityExchange Object to a List named cmd_ex_list
            cmd_ex_list.append(commodity_exchange)

# Open the CSV file and process each line
csv_file_path = "C:\\Users\\ayemi\\Desktop\\MetNetwork\\CFS 2017 PUF CSV\\CFS 2017 PUF CSV.csv"
with open(csv_file_path, "r") as csv_file:
    next(csv_file)  # Skip the header line
    for line in csv_file:
        process_csv_line(line)

# Print the number of CommodityExchange objects processed
print(f"Number of CommodityExchange objects created: {len(cmd_ex_list)}")

# Create a directed graph
G = nx.DiGraph()

# Add nodes and edges
for cmd_ex in cmd_ex_list:
    origin_node = (cmd_ex.origin_state, cmd_ex.origin_cfs_area)
    dest_node = (cmd_ex.dest_state, cmd_ex.dest_cfs_area)

    # Adds Nodes with Attributes
    G.add_node(origin_node, fips_state_code=cmd_ex.origin_state, cfs_area=cmd_ex.origin_cfs_area)
    G.add_node(dest_node, fips_state_code=cmd_ex.dest_state, cfs_area=cmd_ex.dest_cfs_area)

    # Edges between the origin and destination nodes
    G.add_edge(origin_node, dest_node)

# Set edge attributes
for u, v, data in G.edges(data=True):
    cmd_ex = next((ex for ex in cmd_ex_list if
                   (ex.origin_state, ex.origin_cfs_area) == u and (ex.dest_state, ex.dest_cfs_area) == v), None)
    if cmd_ex:
        data['shipment_value'] = cmd_ex.shipment_value
        data['shipment_weight'] = cmd_ex.shipment_weight
        data['shipment_dist_gc'] = cmd_ex.shipment_dist_gc
        data['temp_control_yn'] = cmd_ex.temp_control_yn
        data['export_yn'] = cmd_ex.export_yn
        data['hazmat'] = cmd_ex.hazmat
        data['naics'] = cmd_ex.naics
        data['sctg'] = cmd_ex.sctg

# Graphing output
pos = nx.spring_layout(G, k=0.15, iterations=50)  # Adjust spacing with k parameter and iterations
plt.figure(figsize=(15, 10))  # Increase figure size for better visibility
nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', font_size=10, node_size=800)  # Increase node size
plt.axis('off')
plt.show()
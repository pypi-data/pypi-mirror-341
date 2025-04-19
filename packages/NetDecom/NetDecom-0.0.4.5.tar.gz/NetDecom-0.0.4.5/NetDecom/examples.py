import networkx as nx
import pkg_resources

def get_example(file_name):
    """
    Reads the specified example file and returns the corresponding NetworkX graph object.
    
    Available example files:
    - Animal-Network.txt
    - as20000102.txt
    - bio-CE-GN.txt
    - bio-CE-GT.txt
    - bio-DR-CX.txt
    - CA-CondMat.txt
    - CA-HepTh.txt
    - DD6.txt
    - Email-Enron.txt
    - mammalia-voles-rob-trapping-22.txt

    :param file_name: Name of the example file (without the path)
    :return: NetworkX graph object
    """
    
    # List of available files for reference (can be dynamically read if you prefer)
    available_files = [
        "Animal-Network.txt",
        "as20000102.txt",
        "bio-CE-GN.txt",
        "bio-CE-GT.txt",
        "bio-DR-CX.txt",
        "CA-CondMat.txt",
        "CA-HepTh.txt",
        "DD6.txt",
        "Email-Enron.txt",
        "mammalia-voles-rob-trapping-22.txt"
    ]
    
    # Check if the file exists in the available files
    if file_name not in available_files:
        raise ValueError(f"File '{file_name}' not found. Available files: {', '.join(available_files)}")

    # Get the path to the example file
    file_path = pkg_resources.resource_filename(
        __name__, f"examples/{file_name}"
    )

    G = nx.Graph()  # Initialize an empty graph object
    with open(file_path, 'r') as f:
        for line in f:
            elements = line.strip().split()
            if len(elements) == 2:  # Ensure it's in edge format
                G.add_edge(int(elements[0]), int(elements[1]))  # Add the edge
    
    # Output the processed file information
    print(f"Processed {file_name} and saved to ./examples/{file_name}")
    
    return G

import csv
import os

#---------------------------------------------------------------------------------------------------------------------
def open_csv_file(file_path):
    """
    Opens a CSV file and returns its contents as a list of lists.
    Each inner list represents a row in the CSV file.
    """
    with open(file_path, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        csv_data = list(csv_reader)
    return csv_data
#---------------------------------------------------------------------------------------------------------------------
def access_csv_cell(csv_data, row_index, col_index):
    """
    Accesses a cell in the CSV data based on row and column indices.
    Returns the value of the cell.
    """
    if row_index < 0 or row_index >= len(csv_data):
        return None
    if col_index < 0 or col_index >= len(csv_data[row_index]):
        return None
    return csv_data[row_index][col_index]
#---------------------------------------------------------------------------------------------------------------------
def get_csv_files_in_folder(folder_path):
    """
    Retrieves a list of CSV files in the specified folder.
    """
    csv_files = []
    for file in os.listdir(folder_path):
        if file.endswith(".csv"):
            csv_files.append(file)
    return csv_files
#---------------------------------------------------------------------------------------------------------------------
def createNode(id, caption, url, tooltip, img, size=12):
    cap=""
    for c in caption:
        if cap!="":
            cap= cap+" . "+c
        else:
            cap=c

    tool=""
    for t in tooltip:
        if tool!="":
            tool= tool+" . "+t
        else:
            tool=t

    newNode={
        'id': id,
        'url': url.replace('json',''),
        'label': cap[:30] + (cap[30:] and '...'),
        'title': tool[:100]  + (tool[100:] and '...'),
        'shape': 'image',
        'image': img,
        'size':size,
    }
    return newNode
#---------------------------------------------------------------------------------------------------------------------
def createEdge(from_node_id, to_node_id):
    Newedge={'from': from_node_id, 'to': to_node_id, 'title': '' }
    return Newedge
#---------------------------------------------------------------------------------------------------------------------
Course={
    'id': 0,
    'url':'N/A',
    'widthConstraint': { 'maximum': 150,'minimum': 100  },
    'heightConstraint': { 'minimum': 70, 'maximum': 100 },
    'label': '',
    'x': -150,
    'y': -150,
    'shape': "box",
}

def createGraph(courseTitle,csv_data):

    nodes=[]
    edges=[]
    nodes.append(Course)
    id=1
    for row in csv_data:
        #print(row)
        parentID=id
        for cell in row:
            nodes.append(createNode(id,cell,"","","",10))
            edges.append(createEdge(parentID,id))
            id=id+1
    return nodes,edges

#---------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    dataset_nodes={}
    dataset_edges={}
    folder_path=os.getcwd()+".\\CSV\\"
    csv_files = get_csv_files_in_folder(folder_path)

    if not csv_files:
        print("No CSV files found!")
    else:
        print("CSV files:")
        for csv_file in csv_files:
            csv_data = open_csv_file(folder_path+csv_file)
            if not csv_data:
                print("Error: Unable to open the CSV file.")
            else:
               dataset_nodes,dataset_edges = createGraph(csv_file,csv_data)
               print(dataset_edges)
               print(dataset_nodes)



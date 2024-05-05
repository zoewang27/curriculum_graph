from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import csv
import os
import json
from difflib import SequenceMatcher
from sentence_transformers import SentenceTransformer, util
# from sentence_transformers import SentenceTransformer, util
NULL=-10000
#---------------------------------------------------------------------------------------------------------------------

def similar(a, b, threshold=0.75):
    """
    Checks if two strings are similar based on a similarity threshold.
    """
    matcher = SequenceMatcher(None, a, b)
    return matcher.ratio() >= threshold
#---------------------------------------------------------------------------------------------------------------------
def generateSearchSpace(csv_files,folder_path):
    searchSpace={}
    id=0
    for csv_file in csv_files:
        csv_data = open_csv_file(folder_path+csv_file)
        for row in csv_data:
            if 'courseid' not in row:
                searchSpace[id]={'csv_file':csv_file,'row':row}
                id=id+1
    return searchSpace
#---------------------------------------------------------------------------------------------------------------------
def detectSimilarNodes(searchSpace):
    similarNodes={}
    id=0
    for travers1 in searchSpace:
        for travers2 in searchSpace:
            if ((searchSpace[travers1]['csv_file'] != searchSpace[travers2]['csv_file'])) and ("Obj" not in searchSpace[travers1]['row'][6]) and ("Obj" not in searchSpace[travers2]['row'][6]):
                if similar(searchSpace[travers1]['row'][6],searchSpace[travers2]['row'][6]):
                    similarNodes[id]={'node1':searchSpace[travers1],'node2':searchSpace[travers2]}
                    id=id+1
    return similarNodes
#---------------------------------------------------------------------------------------------------------------------

def buildSimilarityGraph(csv_files,folder_path):
    dataset_nodes=[]
    dataset_edges=[]
    searchSpace=generateSearchSpace(csv_files,folder_path)
    similarNodes=detectSimilarNodes(searchSpace)
    #print(similarNodes)
    dataset_nodes,dataset_edges = createSimilarityGraph(similarNodes)

    return dataset_nodes,dataset_edges
#---------------------------------------------------------------------------------------------------------------------

def graph(request):

    try:
        courseTitle = request.GET['courseTitle']
    except:
        courseTitle = ''

    dataset_nodes={}
    dataset_edges={}
    courseTitles=[]
    folder_path = os.path.join(os.getcwd(), 'graphvisualiztion/CSV/')

    # folder_path=os.getcwd()+"\\graphvisualiztion\\CSV\\"
    csv_files = get_csv_files_in_folder(folder_path)

    for csv_file in csv_files:
        courseTitles.append(csv_file[:len(csv_file)-4])

    id=0

    if courseTitle=="Similarity graph":
        dataset_nodes,dataset_edges= buildSimilarityGraph(csv_files,folder_path)
    else:        
        if courseTitle:
            csv_file=courseTitle+".csv"
        else:
            csv_file = csv_files[0]

        if not csv_files:
            print("No CSV files found!")
        else:
            csv_data = open_csv_file(folder_path+csv_file) # extract data from csv file and turn it to a list
            dataset_nodes,dataset_edges,id = createGraph(csv_file,csv_data,id) # csv_file='XX.csv'; csv_data=list; id = 0

               
    return render(request,'graph.html',{
        "dataset_nodes":json.dumps(dataset_nodes),
        "dataset_edges":json.dumps(dataset_edges),
        "courseTitles":courseTitles
    })
#---------------------------------------------------------------------------------------------------------------------
def mergeList(first_list, second_list):
    resulting_list = list(first_list)
    resulting_list.extend(x for x in second_list if x not in resulting_list)
    return resulting_list
#---------------------------------------------------------------------------------------------------------------------

def contentmgmt(request):
       return render(request,'contentmgmt.html') 


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
def createNode(id, cap, url, tooltip, img ,shape='image', size=12,color='white'):

    if len(cap)>30:
        tooltip=cap+"\n"+tooltip

    newNode={
        'id': id,
        'url': url.replace('json',''),
        'label': cap[:30] + (cap[30:] and '...'),
        'title': tooltip[:100]  + (tooltip[100:] and '...'),
        'color':color,
        'shape': shape,
        'image': img,
        'size':size,
    }
    return newNode
#---------------------------------------------------------------------------------------------------------------------
def createEdge(from_node_id, to_node_id):
    Newedge={'from': from_node_id, 'to': to_node_id, 'title': '' }    
    return Newedge
#---------------------------------------------------------------------------------------------------------------------
# only for create course node
def createCourseNode(id,label,tooltip):
    Course={
        'id': id,
        'url':'N/A',
        'widthConstraint': { 'maximum': 150,'minimum': 100  },
        'heightConstraint': { 'minimum': 70, 'maximum': 100 },
        'title': tooltip[:100]  + (tooltip[100:] and '...'),
        'label': label,
        'x': -150,
        'y': -150,
        'shape': "circle",
    }
    return Course
#---------------------------------------------------------------------------------------------------------------------
def createGraph(courseTitle,csv_data,id):
    colors=['BlueViolet','DeepPink','Lime','orange','Indigo','DarkSlateBlue','DarkMagenta',"brown","lightgray"]
    nodes=[]
    edges=[]
    nodes.append(createCourseNode(id,courseTitle[:len(courseTitle)-4],csv_data[1][6])) # id=0, and get courseTitle from file name, and extract the 2-7 columns
    CourseID=id
    id=id+1
    
    Prev_courseid	= NULL
    Prev_chapterid	= NULL
    Prev_sectionid	= NULL
    Prev_unitid	    = NULL
    Prev_subunitid   = NULL
    Prev_topic       = NULL
    Prev_chapter     = NULL
    Prev_CognitiveLevel = NULL
    Prev_description = NULL

    cnt=0
    
    for row in csv_data:
        
        if cnt<2: #ignore the first two rows (title)
            cnt=cnt+1
            continue    
                
        Cur_courseid	= row[0]
        Cur_chapterid	= row[1]
        Cur_sectionid	= row[2]
        Cur_unitid	    = row[3]
        Cur_subunitid   = row[4]
        Cur_topic       = row[6]
        Cur_chapter     = row[8]
        Cur_CognitiveLevel = row[10]
        Cur_description = row[12]

        if not(Prev_courseid): # 检查前一个课程ID是否存在。如果不存在，表示这是第一个课程，则执行创建第一个chapter节点
            parentID=id # 1
            nodes.append(createNode(id,Cur_topic,"",Cur_description,"","box",10,colors[3]))
            edges.append(createEdge(CourseID,id))

        else:   # 非第一个chapter，执行                   
            if (Cur_chapterid != Prev_chapterid): # 判断：如果不是同一个chapter，创建新的chapter
                parentID=id # 赋值 新的父id 2
                nodes.append(createNode(id,Cur_topic,"",Cur_description,"","box",10,colors[3])) 
                edges.append(createEdge(CourseID,id)) # 创建 课程节点 到 chapter 节点 之间的边

            else: # 判断：如果是同一个chapter，创建子节点
                nodes.append(createNode(id,Cur_topic,"",Cur_description,"","image",10,colors[0])) # 创建 子节点
                edges.append(createEdge(parentID,id)) # 创建 chpter节点到 子节点的边
            


        Prev_courseid	= Cur_courseid
        Prev_chapterid	= Cur_chapterid
        Prev_sectionid	= Cur_sectionid
        Prev_unitid	    = Cur_unitid
        Prev_subunitid   = Cur_subunitid
        Prev_topic       = Cur_topic
        Prev_chapter     = Cur_chapter
        Prev_CognitiveLevel = Cur_CognitiveLevel
        Prev_description = Cur_description
        id=id+1


        #print(row)
        #parentID=id 
        #for i in range(6,14):
        #    if  row[i] =="-" or row[i] =="": continue
        #    nodes.append(createNode(id,row[i],"","","",10,colors[i-6]))
        #    if parentID==id:
        #        edges.append(createEdge(CourseID,id))
        #    else:
        #        edges.append(createEdge(parentID,id))
        #    id=id+1
    return nodes,edges,id
#---------------------------------------------------------------------------------------------------------------------
def createSimilarityGraph(similarNodes):
    colors=['BlueViolet','DeepPink','Lime','orange','Indigo','DarkSlateBlue','DarkMagenta',"brown"]
    nodes=[]
    edges=[]
    courses={}
    id=0

    index=[]

    for similarPair in similarNodes:
        #-----------------------------------------------------------------
        node1= similarNodes[similarPair]['node1']
        if node1['csv_file'] not in courses:
            id=id+1          
            nodes.append(createCourseNode(id,node1['csv_file'][:len(node1['csv_file'])-4],""))
            courses[node1['csv_file']]=id

        row1 = node1['row']
        parentID1= courses[node1['csv_file']]

        #-----------------------------------------------------------------
        node2= similarNodes[similarPair]['node2']        
        if node2['csv_file'] not in courses:
            id=id+1
            nodes.append(createCourseNode(id,node2['csv_file'][:len(node2['csv_file'])-4],""))
            courses[node2['csv_file']]=id

        row2 = node2['row']
        parentID2= courses[node2['csv_file']]

        #-----------------------------------------------------------------
        id=id+1
        nodes.append(createNode(id,row1[6]+","+ row2[6],"","","",10,colors[4]))

        edges.append(createEdge(parentID2,id))
        edges.append(createEdge(parentID1,id))

    return nodes,edges
#---------------------------------------------------------------------------------------------------------------------













'''
return all courses name
'''
def SimilarityPage(request):

    courseTitles=[]
    folder_path = os.path.join(os.getcwd(), 'graphvisualiztion/CSV/')

    # folder_path=os.getcwd()+"\\graphvisualiztion\\CSV\\"
    csv_files = get_csv_files_in_folder(folder_path)

    for csv_file in csv_files:
        courseTitles.append(csv_file[:len(csv_file)-4])

    # separate "ACM" courses and "UVA" courses
    acm_courses = [course for course in courseTitles if course.startswith("ACM")]
    uva_courses = [course for course in courseTitles if course.startswith("UVA")]

    return render(request,'similarity.html', {'acm_courses': acm_courses, 'uva_courses': uva_courses}) 





'''
Open the file and extract data into a list
'''
def openfile(csvFile):
    folder_path = os.path.join(os.getcwd(), 'graphvisualiztion/CSV/')
    data = []
    with open(folder_path+csvFile, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data



'''
Extract nodes and edges from a list
'''
def buildNodeEdges(csv_data):
    nodes = []
    edges = []
    courseid = csv_data[1]['courseid']
    shape_mapping = {
    0: "circle",
    1: "box",
    2: "ellipse",
    3: "square",
    4: "diamond"
    }

    cnt = 0
    for row in csv_data:
        if cnt < 0: # 
            cnt += 1
            continue   

        nodeId = ".".join(filter(None, [row["courseid"], row["chapterid"], row["sectionid"], row["unitid"], row["subunitid"]]))
        level = nodeId.count(".")
        shape = shape_mapping.get(level, "square")

        node = {
            "id": nodeId,
            "label": row["topic"],
            "group": courseid,
            "shape": shape,
            "description": row["topic"] + ": " + row["description_of_topic"],
        }
        nodes.append(node)

        parent_id = nodeId[:nodeId.rfind('.')] if '.' in nodeId else None
        if parent_id:
          edge = {
              'from': parent_id,
              'to': nodeId,
              'title': '' 
          }
          edges.append(edge)

    return nodes, edges, courseid





'''
Use a BERT model to check similarity
'''
def bertModel(first_nodes, second_nodes):
    # use the fastest model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    first_nodes_dict =  {node['description']: node['id'] for node in first_nodes if node['id'].count('.') > 0 and not node['label'].startswith('Obj')}
    second_nodes_dict =  {node['description']: node['id'] for node in second_nodes if node['id'].count('.') > 0 and not node['label'].startswith('Obj')}

    first_labels = list(first_nodes_dict.keys())
    second_labels = list(second_nodes_dict.keys())

    first_embeddings = model.encode(first_labels, convert_to_tensor=False)
    second_embeddings = model.encode(second_labels, convert_to_tensor=False)

    # Compute semantic similarity
    cosine_scores = util.cos_sim(first_embeddings, second_embeddings)

    similarEdges = []
    nodeId = []
    for i in range(len(first_labels)):
        for j in range(len(second_labels)):
            if cosine_scores[i][j] > 0.65:
                edge = {
                    'from': first_nodes_dict[first_labels[i]],
                    'to': second_nodes_dict[second_labels[j]],
                    'title': '',
                    'length':900,
                    'color': 'grey',
                    'width': 1,
                    'shadow': False,
                    'dashes': True
                }
                similarEdges.append(edge)
                nodeId.append(first_nodes_dict[first_labels[i]])
                nodeId.append(second_nodes_dict[second_labels[j]])
                              
    return similarEdges, nodeId




'''
build edges for parents of similar nodes
'''
def buildEdgesForParentNode(NodeIds):
    edges = []
    AllNodeIds = []
    for NodeId in NodeIds:
        for i in range(len(NodeId.split('.')) - 1, 0, -1):
            parent_id = '.'.join(NodeId.split('.')[:i])
            child_id = '.'.join(NodeId.split('.')[:i + 1])
            edge = {
                'from': parent_id, 
                'to': child_id, 
                'title': ''}
            if edge not in edges:  # Check if edge already exists
                edges.append(edge)

    for NodeId in NodeIds:
        id_parts = NodeId.split('.')
        for i in range(len(id_parts)):
            parent_id = '.'.join(id_parts[:i + 1])
            if parent_id not in AllNodeIds:  # Check if edge already exists
                AllNodeIds.append(parent_id)

    return edges, sorted(AllNodeIds)




'''
Find all parents nodes
'''
def find_matching_nodes(nodes, nodeIds):
    matching_nodes = []
    for nodeId in nodeIds:
        matching_node = next((node for node in nodes if node['id'] == nodeId), None)
        if matching_node:
            matching_nodes.append(matching_node)
    return matching_nodes




'''
Detect the semantic similarity between two courses and save the result into a json file
'''
def detectSimilarCourse(request):

    if request.method == 'POST':

        courselist_json = request.POST.get('courselist') # get selected courses list
        courselist = json.loads(courselist_json) #Convert JSON

        # build the path
        file_name = courselist[0] + '_' + courselist[1] + '.json'
        file_path = os.path.join(os.getcwd(), 'graphvisualiztion', 'data', file_name)

        # check if the file is exist
        if os.path.exists(file_path):
            with open(file_path, 'r') as json_file:
                response_data = json.load(json_file)
            return JsonResponse(response_data)
        else:
            csv_file_0 = courselist[0] + ".csv"
            csv_file_1 = courselist[1] + ".csv"
            csv_data_0 = openfile(csv_file_0) # extract data from csv file and turn it to a list: [{},{},{}]
            csv_data_1 = openfile(csv_file_1)

            nodes_0,_,courseID_0 = buildNodeEdges(csv_data_0) 
            nodes_1,_,courseID_1= buildNodeEdges(csv_data_1) 

            # compare nodes，and build the edges between similar nodes，get nodeId
            similarEdges, nodeId = bertModel(nodes_0, nodes_1)

            #build edges for parents of similar nodes and find all nodes
            nodeEdges, allId = buildEdgesForParentNode(nodeId)
            matchNode = find_matching_nodes(nodes_0 + nodes_1, allId)

            response = {"nodes": matchNode, "edges": nodeEdges + similarEdges, "courseId": [courseID_0,courseID_1]}

            # save the result to a json file
            folder_path = os.path.join(os.getcwd(), 'graphvisualiztion', 'data')      
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            new_file_path = os.path.join(folder_path, file_name)
            with open(new_file_path, 'w') as json_file:
                json.dump(response, json_file)

            return JsonResponse(response)




def allCourses(request):
    return render(request,'allcourses.html')



'''
Detect the semantic similarity among all courses and save the result into a json file
'''
def detectAllcourses(request):

    if request.method == 'POST':
        curriculum = request.POST.get('curriculumSource') 

        # build the path
        file_name = curriculum + '_all_courses' + '.json'
        file_path = os.path.join(os.getcwd(), 'graphvisualiztion', 'data', file_name)

        # check if the file is exist
        if os.path.exists(file_path):
            with open(file_path, 'r') as json_file:
                response_data = json.load(json_file)
            return JsonResponse(response_data)
        
        else:      
            folder_path = os.path.join(os.getcwd(), 'graphvisualiztion', 'CSV')  
            # get all CSV files with start with "UVA" or "ACM"
            matching_files = [file for file in os.listdir(folder_path) if file.startswith(curriculum)]

            if matching_files:
                matched = 1

            file_list = []  
            for file in matching_files:
                csv_data = openfile(file)  #  # extract data from csv file and turn it to a list: [{},{},{}]
                file_list.append(csv_data)

            # create the course node
            course_nodes = []
            file_node = {}  
            for list in file_list:
                nodes,_,courseId= buildNodeEdges(list) 
                file_node[courseId] = nodes
                if nodes:
                    course_nodes.append(nodes[0])

            # create the similar edges among all courses
            compared_pairs = set()  # save the compared pair, avoid compare again
            edges = []
            for course_id_1, nodes_1 in file_node.items():
                for course_id_2, nodes_2 in file_node.items():
                    if course_id_1 != course_id_2 and (course_id_1, course_id_2) not in compared_pairs:

                        similarEdges, _ = bertModel(nodes_1, nodes_2)
                        compared_pairs.add((course_id_1, course_id_2)) 
                        compared_pairs.add((course_id_2, course_id_1)) 
                        
                        if similarEdges:
                                num_similar_edges = len(similarEdges)  
                                edge = {
                                    'from': course_id_1,
                                    'to': course_id_2,
                                    'title': '',
                                    'value': num_similar_edges
                                }
                                if edge not in edges:  # Check if edge already exists
                                    edges.append(edge)
            
            response = {"nodes": course_nodes, "edges": edges, "matched": curriculum}

            # save the result to the json file
            folder_path = os.path.join(os.getcwd(), 'graphvisualiztion', 'data')      
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            new_file_path = os.path.join(folder_path, file_name)
            with open(new_file_path, 'w') as json_file:
                json.dump(response, json_file)


            return JsonResponse(response)

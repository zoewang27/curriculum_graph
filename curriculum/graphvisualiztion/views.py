from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,Http404
from django.http import JsonResponse
import mimetypes
import csv
import os
import json
import uuid
from difflib import SequenceMatcher
from .models import Trajectory, Course
import google.generativeai as genai


# BERT
from sentence_transformers import SentenceTransformer, util



# NULL=-10000
# #---------------------------------------------------------------------------------------------------------------------

# def similar(a, b, threshold=0.75):
#     """
#     Checks if two strings are similar based on a similarity threshold.
#     """
#     matcher = SequenceMatcher(None, a, b)
#     return matcher.ratio() >= threshold
# #---------------------------------------------------------------------------------------------------------------------
# def generateSearchSpace(csv_files,folder_path):
#     searchSpace={}
#     id=0
#     for csv_file in csv_files:
#         csv_data = open_csv_file(folder_path+csv_file)
#         for row in csv_data:
#             if 'courseid' not in row:
#                 searchSpace[id]={'csv_file':csv_file,'row':row}
#                 id=id+1
#     return searchSpace
# #---------------------------------------------------------------------------------------------------------------------
# def detectSimilarNodes(searchSpace):
#     similarNodes={}
#     id=0
#     for travers1 in searchSpace:
#         for travers2 in searchSpace:
#             if ((searchSpace[travers1]['csv_file'] != searchSpace[travers2]['csv_file'])) and ("Obj" not in searchSpace[travers1]['row'][6]) and ("Obj" not in searchSpace[travers2]['row'][6]):
#                 if similar(searchSpace[travers1]['row'][6],searchSpace[travers2]['row'][6]):
#                     similarNodes[id]={'node1':searchSpace[travers1],'node2':searchSpace[travers2]}
#                     id=id+1
#     return similarNodes
# #---------------------------------------------------------------------------------------------------------------------

# def buildSimilarityGraph(csv_files,folder_path):
#     dataset_nodes=[]
#     dataset_edges=[]
#     searchSpace=generateSearchSpace(csv_files,folder_path)
#     similarNodes=detectSimilarNodes(searchSpace)
#     #print(similarNodes)
#     dataset_nodes,dataset_edges = createSimilarityGraph(similarNodes)

#     return dataset_nodes,dataset_edges
# #---------------------------------------------------------------------------------------------------------------------

# def graph(request):

#     try:
#         courseTitle = request.GET['courseTitle']
#     except:
#         courseTitle = ''

#     dataset_nodes={}
#     dataset_edges={}
#     courseTitles=[]
#     folder_path = os.path.join(os.getcwd(), 'graphvisualiztion/CSV/')

#     # folder_path=os.getcwd()+"\\graphvisualiztion\\CSV\\"
#     csv_files = get_csv_files_in_folder(folder_path)

#     for csv_file in csv_files:
#         courseTitles.append(csv_file[:len(csv_file)-4])

#     id=0

#     if courseTitle=="Similarity graph":
#         dataset_nodes,dataset_edges= buildSimilarityGraph(csv_files,folder_path)
#     else:        
#         if courseTitle:
#             csv_file=courseTitle+".csv"
#         else:
#             csv_file = csv_files[0]

#         if not csv_files:
#             print("No CSV files found!")
#         else:
#             csv_data = open_csv_file(folder_path+csv_file) # extract data from csv file and turn it to a list
#             dataset_nodes,dataset_edges,id = createGraph(csv_file,csv_data,id) # csv_file='XX.csv'; csv_data=list; id = 0

               
#     return render(request,'graph.html',{
#         "dataset_nodes":json.dumps(dataset_nodes),
#         "dataset_edges":json.dumps(dataset_edges),
#         "courseTitles":courseTitles
#     })
# #---------------------------------------------------------------------------------------------------------------------
# def mergeList(first_list, second_list):
#     resulting_list = list(first_list)
#     resulting_list.extend(x for x in second_list if x not in resulting_list)
#     return resulting_list
# #---------------------------------------------------------------------------------------------------------------------

# def contentmgmt(request):
#        return render(request,'contentmgmt.html') 


# #---------------------------------------------------------------------------------------------------------------------
# def open_csv_file(file_path):
#     """
#     Opens a CSV file and returns its contents as a list of lists.
#     Each inner list represents a row in the CSV file.
#     """
#     with open(file_path, 'r', newline='') as file:
#         csv_reader = csv.reader(file)
#         csv_data = list(csv_reader)
#     return csv_data
# #---------------------------------------------------------------------------------------------------------------------
# def access_csv_cell(csv_data, row_index, col_index):
#     """
#     Accesses a cell in the CSV data based on row and column indices.
#     Returns the value of the cell.
#     """
#     if row_index < 0 or row_index >= len(csv_data):
#         return None
#     if col_index < 0 or col_index >= len(csv_data[row_index]):
#         return None
#     return csv_data[row_index][col_index]
# #---------------------------------------------------------------------------------------------------------------------
# def get_csv_files_in_folder(folder_path):
#     """
#     Retrieves a list of CSV files in the specified folder.
#     """
#     csv_files = []
#     for file in os.listdir(folder_path):
#         if file.endswith(".csv"):
#             csv_files.append(file)
#     return csv_files
# #---------------------------------------------------------------------------------------------------------------------
# def createNode(id, cap, url, tooltip, img ,shape='image', size=12,color='white'):

#     if len(cap)>30:
#         tooltip=cap+"\n"+tooltip

#     newNode={
#         'id': id,
#         'url': url.replace('json',''),
#         'label': cap[:30] + (cap[30:] and '...'),
#         'title': tooltip[:100]  + (tooltip[100:] and '...'),
#         'color':color,
#         'shape': shape,
#         'image': img,
#         'size':size,
#     }
#     return newNode
# #---------------------------------------------------------------------------------------------------------------------
# def createEdge(from_node_id, to_node_id):
#     Newedge={'from': from_node_id, 'to': to_node_id, 'title': '' }    
#     return Newedge
# #---------------------------------------------------------------------------------------------------------------------
# # only for create course node
# def createCourseNode(id,label,tooltip):
#     Course={
#         'id': id,
#         'url':'N/A',
#         'widthConstraint': { 'maximum': 150,'minimum': 100  },
#         'heightConstraint': { 'minimum': 70, 'maximum': 100 },
#         'title': tooltip[:100]  + (tooltip[100:] and '...'),
#         'label': label,
#         'x': -150,
#         'y': -150,
#         'shape': "circle",
#     }
#     return Course
# #---------------------------------------------------------------------------------------------------------------------
# def createGraph(courseTitle,csv_data,id):
#     colors=['BlueViolet','DeepPink','Lime','orange','Indigo','DarkSlateBlue','DarkMagenta',"brown","lightgray"]
#     nodes=[]
#     edges=[]
#     nodes.append(createCourseNode(id,courseTitle[:len(courseTitle)-4],csv_data[1][6])) # id=0, and get courseTitle from file name, and extract the 2-7 columns
#     CourseID=id
#     id=id+1
    
#     Prev_courseid	= NULL
#     Prev_chapterid	= NULL
#     Prev_sectionid	= NULL
#     Prev_unitid	    = NULL
#     Prev_subunitid   = NULL
#     Prev_topic       = NULL
#     Prev_chapter     = NULL
#     Prev_CognitiveLevel = NULL
#     Prev_description = NULL

#     cnt=0
    
#     for row in csv_data:
        
#         if cnt<2: #ignore the first two rows (title)
#             cnt=cnt+1
#             continue    
                
#         Cur_courseid	= row[0]
#         Cur_chapterid	= row[1]
#         Cur_sectionid	= row[2]
#         Cur_unitid	    = row[3]
#         Cur_subunitid   = row[4]
#         Cur_topic       = row[6]
#         Cur_chapter     = row[8]
#         Cur_CognitiveLevel = row[10]
#         Cur_description = row[12]

#         if not(Prev_courseid): 
#             parentID=id 
#             nodes.append(createNode(id,Cur_topic,"",Cur_description,"","box",10,colors[3]))
#             edges.append(createEdge(CourseID,id))

#         else:                    
#             if (Cur_chapterid != Prev_chapterid):
#                 parentID=id 
#                 nodes.append(createNode(id,Cur_topic,"",Cur_description,"","box",10,colors[3])) 
#                 edges.append(createEdge(CourseID,id)) 

#             else: 
#                 nodes.append(createNode(id,Cur_topic,"",Cur_description,"","image",10,colors[0])) 
#                 edges.append(createEdge(parentID,id)) 
            


#         Prev_courseid	= Cur_courseid
#         Prev_chapterid	= Cur_chapterid
#         Prev_sectionid	= Cur_sectionid
#         Prev_unitid	    = Cur_unitid
#         Prev_subunitid   = Cur_subunitid
#         Prev_topic       = Cur_topic
#         Prev_chapter     = Cur_chapter
#         Prev_CognitiveLevel = Cur_CognitiveLevel
#         Prev_description = Cur_description
#         id=id+1


#         #print(row)
#         #parentID=id 
#         #for i in range(6,14):
#         #    if  row[i] =="-" or row[i] =="": continue
#         #    nodes.append(createNode(id,row[i],"","","",10,colors[i-6]))
#         #    if parentID==id:
#         #        edges.append(createEdge(CourseID,id))
#         #    else:
#         #        edges.append(createEdge(parentID,id))
#         #    id=id+1
#     return nodes,edges,id
# #---------------------------------------------------------------------------------------------------------------------
# def createSimilarityGraph(similarNodes):
#     colors=['BlueViolet','DeepPink','Lime','orange','Indigo','DarkSlateBlue','DarkMagenta',"brown"]
#     nodes=[]
#     edges=[]
#     courses={}
#     id=0

#     index=[]

#     for similarPair in similarNodes:
#         #-----------------------------------------------------------------
#         node1= similarNodes[similarPair]['node1']
#         if node1['csv_file'] not in courses:
#             id=id+1          
#             nodes.append(createCourseNode(id,node1['csv_file'][:len(node1['csv_file'])-4],""))
#             courses[node1['csv_file']]=id

#         row1 = node1['row']
#         parentID1= courses[node1['csv_file']]

#         #-----------------------------------------------------------------
#         node2= similarNodes[similarPair]['node2']        
#         if node2['csv_file'] not in courses:
#             id=id+1
#             nodes.append(createCourseNode(id,node2['csv_file'][:len(node2['csv_file'])-4],""))
#             courses[node2['csv_file']]=id

#         row2 = node2['row']
#         parentID2= courses[node2['csv_file']]

#         #-----------------------------------------------------------------
#         id=id+1
#         nodes.append(createNode(id,row1[6]+","+ row2[6],"","","",10,colors[4]))

#         edges.append(createEdge(parentID2,id))
#         edges.append(createEdge(parentID1,id))

#     return nodes,edges
# #---------------------------------------------------------------------------------------------------------------------
















'''
return all courses with an uploaded CSV file.
'''
def getAllcourses():
    acm_courses = Course.objects.filter(source='ACM').exclude(csv_file__isnull=True).exclude(csv_file='').order_by('course_number').values('course_id', 'course_name')
    uva_courses = Course.objects.filter(source='UvA').exclude(csv_file__isnull=True).exclude(csv_file='').order_by('course_number').values('course_id', 'course_name')
    return acm_courses, uva_courses
    



'''
return singlecourse.html
'''
def singleCourse(request):
    acm_courses,uva_courses = getAllcourses()
    uva_courses_json =  json.dumps(list((uva_courses))) # Convert the queryset to JSON format.
    acm_courses_json = json.dumps(list((acm_courses)))
    return render(request,'singlecourse.html', {'acm_courses': acm_courses_json, 'uva_courses': uva_courses_json})




'''
return Similarity.html
'''
def SimilarityPage(request):
    acm_courses,uva_courses = getAllcourses()
    return render(request,'similarity.html', {'acm_courses': acm_courses, 'uva_courses': uva_courses}) 




'''
Open the file and extract data into a list
'''
def openfile(csvFile, folder_path=None):
    if folder_path is None:
        folder_path = os.path.join(os.getcwd(), 'graphvisualiztion/CSV/')
    else:
        folder_path = os.path.join(os.getcwd(), folder_path)

    data = []
    file_path = os.path.join(folder_path, csvFile)
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data



'''
Extract nodes and edges from a list
'''
def buildNodeEdges(csv_data,course_id=None):
    nodes = []
    edges = []
    if course_id is None:
        courseId = csv_data[1]['courseid']
    else:
        courseId = str(course_id)
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
        
        if row["topic"].startswith('Obj'): # 
            cnt += 1
            continue   

        nodeId = ".".join(filter(None, [courseId, row["chapterid"], row["sectionid"], row["unitid"], row["subunitid"]]))
        layer = nodeId.count(".")
        shape = shape_mapping.get(layer, "square")

        node = {
            "id": nodeId,
            "label": row["topic"],
            "group": courseId,
            "shape": shape,
            "cog_level": row["Cognitive level"].strip(),
            "title": row["topic"] + ": " + row["description_of_topic"],
            "layer": layer
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

    return nodes, edges, courseId



'''
Show single course graph
'''
def showCourseGraph(request):
    if request.method == 'POST':
        selected_courseID = request.POST.get('course') 
        selected_course = Course.objects.filter(course_id = selected_courseID)
        csv_data = openfile(str(selected_course[0].csv_file), 'media/')
        nodes,edges,courseID = buildNodeEdges(csv_data,selected_course[0].course_id)
        response = {"nodes": nodes, "edges": edges, "courseId": courseID}
        return JsonResponse(response)



'''
Save result(nodes and edges) to a json file
'''
def saveToJSON(folder_path,file_path,result):

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    with open(file_path, 'w') as json_file:
        json.dump(result, json_file, indent=2)


'''
Use a BERT model to check semantic similarity
'''
def bertModel(first_nodes, second_nodes):
    # use the fastest model
    model = SentenceTransformer('all-mpnet-base-v2')

    first_nodes_dict =  {
        node['title']: node['id'] for node in first_nodes if not node['label'].startswith('Obj')
        }
    second_nodes_dict =  {
        node['title']: node['id'] for node in second_nodes if not node['label'].startswith('Obj')
        }
    
#     first_nodes_dict =  {
#     node['title']: node['id'] for node in first_nodes if node['id'].count('.') > 0 and not node['label'].startswith('Obj')
#     }
# second_nodes_dict =  {
#     node['title']: node['id'] for node in second_nodes if node['id'].count('.') > 0 and not node['label'].startswith('Obj')
#     }


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
            if cosine_scores[i][j] > 0.6:
                score = str(round(float(cosine_scores[i][j]), 4))
                edge = {
                    'from': first_nodes_dict[first_labels[i]],
                    'to': second_nodes_dict[second_labels[j]],
                    'title': score,
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
            if parent_id not in AllNodeIds:  # Check if nodeid already exists
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
        selected_courses = Course.objects.filter(course_id__in=courselist)

        # build the path
        file_name = selected_courses[0].course_name.replace("/", "_") + '_' + selected_courses[1].course_name.replace("/", "_") + '.json'
        folder_path = os.path.join(os.getcwd(), 'media', 'JSON', 'courseSimilarity')   
        file_path = os.path.join(os.getcwd(), folder_path, file_name)

        # check if the file is exist
        if os.path.exists(file_path):
            with open(file_path, 'r') as json_file:
                response_data = json.load(json_file)
            return JsonResponse(response_data)
        else:
            csv_data_0 = openfile(str(selected_courses[0].csv_file), 'media/') # extract data from csv file and turn it to a list: [{},{},{}]
            csv_data_1 = openfile(str(selected_courses[1].csv_file), 'media/')

            nodes_0,_,courseID_0 = buildNodeEdges(csv_data_0, str(selected_courses[0].course_id)) 
            nodes_1,_,courseID_1= buildNodeEdges(csv_data_1, str(selected_courses[1].course_id)) 

            # compare nodes，and build the edges between similar nodes，get nodeId
            similarEdges, nodeId = bertModel(nodes_0, nodes_1)

            # build edges for parents of similar nodes and find all nodes
            nodeEdges, allId = buildEdgesForParentNode(nodeId)
            matchNode = find_matching_nodes(nodes_0 + nodes_1, allId)

            response = {"nodes": matchNode, "edges": nodeEdges + similarEdges, "courseId": [courseID_0,courseID_1]}
            saveToJSON(folder_path,file_path,response)

            return JsonResponse(response)




def allCourses(request):
    return render(request,'allcourses.html')



'''
Detect the semantic similarity among all courses and save the result into a json file
'''
def detectAllcourses(request):

    if request.method == 'POST':
        curricula = request.POST.get('curriculumSource') 

        # build the path
        file_name = curricula + '_all_courses' + '.json'
        folder_path = os.path.join(os.getcwd(),'media', 'JSON', 'curriculaSimilarity')  
        file_path = os.path.join(os.getcwd(), folder_path, file_name)

        # check if the file is exist
        if os.path.exists(file_path):
            with open(file_path, 'r') as json_file:
                response_data = json.load(json_file)
            return JsonResponse(response_data)
        
        else:      
            selected_courses = Course.objects.filter(source = curricula).exclude(csv_file__isnull=True).exclude(csv_file='')
            course_nodes = []
            file_node = {}
            for course in selected_courses:
                csv_data = openfile(str(course.csv_file), 'media/') 
                nodes,_,courseId= buildNodeEdges(csv_data,course.course_id) 
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
                                if num_similar_edges > 3:
                                    edge = {
                                        'from': course_id_1,
                                        'to': course_id_2,
                                        'title': num_similar_edges,
                                        'value': num_similar_edges
                                    }
                                    if edge not in edges:  # Check if edge already exists
                                        edges.append(edge)
            
            response = {"nodes": course_nodes, "edges": edges, "matched": curricula}
            saveToJSON(folder_path,file_path,response)
            return JsonResponse(response)
        








'''
return filesmgmt.html
'''
def filesManagement(request):
    acm_courses = Course.objects.filter(source='ACM').order_by('course_number')
    uva_courses = Course.objects.filter(source='UvA').order_by('course_number')
    context = {
        'acm_courses': acm_courses,
        'uva_courses': uva_courses
    }
    
    return render(request,'filesmgmt.html', context)




'''
Upload csv files
'''
def uploadfile(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        csv_file = request.FILES.get('files')
        
        if course_id and csv_file:
            course = get_object_or_404(Course, course_id=course_id)
            course.csv_file = csv_file
            course.save()

            # 转为json文件存储
            csv_data = openfile(str(course.csv_file), 'media/')
            nodes, edges, _ = buildNodeEdgesVersion2(csv_data, course.course_id)
            json_data = {
                'nodes': nodes,
                'edges': edges
            }

            # build the path
            file_name = course_id + '.json'
            folder_path = os.path.join(os.getcwd(), 'media', 'JSON', 'UvA_courses')   
            file_path = os.path.join(os.getcwd(), folder_path, file_name)

            if json_data:
                saveToJSON(folder_path,file_path,json_data)


            return JsonResponse({'message': 'File uploaded successfully!'})
        else:
            return JsonResponse({'message': 'Failed to upload file.'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method.'}, status=405)



'''
Delete csv files
'''
def deleteCSVfile(request):
    if request.method == 'POST':
        select_course = request.POST.get('courseID')
        if select_course:
            course = Course.objects.filter(course_id=select_course).first()
            if course:
                if course.csv_file:
                    file_path = course.csv_file.path
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    course.csv_file = None  
                    course.save() 
                    return JsonResponse({'message': 'File deleted successfully.'})
        return JsonResponse({'message': 'Failed to delete file.'})
    else:
        return JsonResponse({'message': 'Invalid request method.'})
    



'''
download csv files
'''
def download_csv_file (request, course_id):
    course = get_object_or_404(Course, course_id=course_id)
    if course.csv_file:
        file_path = course.csv_file.path
        file_name = course.csv_file.name.split('/')[-1]
        mime_type, _ = mimetypes.guess_type(file_path)
        response = HttpResponse(open(file_path, 'rb'), content_type=mime_type)
        response['Content-Disposition'] = f'attachment; filename={file_name}'
        return response
    else:
        raise Http404("No CSV file associated with this course.")




'''
Delete temporary json files( this function is needed after uploading new csv files)
'''
def deleteJSONfile(request):
    if request.method == 'POST':
        directories = ['media/JSON/courseSimilarity', 'media/JSON/curriculaSimilarity', 'media/JSON/trajectory']
        success = True
        
        for directory in directories:
            file_dir = os.path.join(os.getcwd(), directory)
            if os.path.exists(file_dir):
                for file_name in os.listdir(file_dir):
                    file_path = os.path.join(file_dir, file_name)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
            else:
                success = False
                break

        if success:
            return JsonResponse({'message': 'All temporary JSON files are cleared successfully!'})
        else:
            return JsonResponse({'message': 'Failed to delete files.'})
    else:
        return JsonResponse({'message': 'Invalid request method.'})
    




'''
Return trajectory.html
'''
def trajectory(request):
    return render(request,'trajectory.html') 



'''
show the trajectory graph
'''
def showTrajectory(request):
    if request.method == 'POST':
        selected_trajectory = request.POST.get('trajectory') 
        # build the path
        file_name = selected_trajectory + '.json'
        folder_path = os.path.join(os.getcwd(),'media', 'JSON', 'trajectory') 
        file_path = os.path.join(os.getcwd(), folder_path, file_name)

        # check if the file is exist
        if os.path.exists(file_path):
            with open(file_path, 'r') as json_file:
                response_data = json.load(json_file)
            return JsonResponse(response_data)
        
        else:    

            # Find all records where trajectory_name is the value of the selected trajectory
            trajectory_records = Trajectory.objects.filter(trajectory_name=selected_trajectory)

            nodes = []
            edges = []  
            color_mapping = {
                "create": "#b8bceb",      # purple
                "evaluate": "#a3ddf5",    # blue
                "analyze": "#b0e3bf",     # green
                "apply": "#fefaa3",       # yellow
                "understand": "#ffd2af",  # orange
                "remember": "#faadb0"     # red
            }

            for i, trajectory_record in enumerate(trajectory_records):
                # add objective nodes and edges of the trajectory
                trajectory_objective_node_id  = str(trajectory_record.trajectory_id)
                objective_label = f"{i + 1}. {trajectory_record.objective}" 
                level_color = color_mapping.get(trajectory_record.level.lower(), "#000000") 
                nodes.append({'id': trajectory_objective_node_id, 'label': objective_label, "cog_level": trajectory_record.level, "shape": "box", "color": level_color,  "font": {"align": "left" }})

                if i != len(trajectory_records) - 1:
                    next_node = str(trajectory_records[i + 1].trajectory_id)
                    edges.append({'from': trajectory_objective_node_id, 'to': next_node, 'arrows': "to", 'width': "2", "color": {"color": '#363a44'} })
    
                related_objectives = trajectory_record.related_course_objectives.all() # return all Course.Objective instances
                added_courses = set()

                for objective in related_objectives:

                    # Add course nodes and edges
                    related_course_name = objective.course.course_name
                    course_node_id = trajectory_objective_node_id + '.' + str(objective.course.course_id)
                    objective_node_id = course_node_id + '.' + str(objective.objective_id)

                    if related_course_name not in added_courses:
                        nodes.append({'id': course_node_id, 'label': related_course_name,  "shape": "ellipse"}) 
                        edges.append({'from': trajectory_objective_node_id, 'to': course_node_id}) 
                        added_courses.add(related_course_name)
                        
                    # Add objective nodes and edges of the course
                    level_color = color_mapping.get(objective.level.lower(), "#000000") 
                    if objective.course.csv_file:
                        similarity_level = compareObjectiveAndTopic(objective.course.csv_file, objective.content)
                    else:
                        similarity_level = "[N/A]"

                    if similarity_level == "[0]":
                        nodes.append({'id': objective_node_id, 'label': similarity_level + "--" + objective.content, "shape": "square", "cog_level": objective.level, "shape": "box", "font": {"align": "left", "color": "#ffffff", "background": "#404040" } , "color": level_color})
                    else:
                        nodes.append({'id': objective_node_id, 'label': similarity_level + "--" + objective.content, "shape": "square", "cog_level": objective.level, "shape": "box", "font": {"align": "left" } , "color": level_color})
                    edges.append({'from': course_node_id, 'to': objective_node_id})
            
            response = {"nodes": nodes, "edges": edges}
            saveToJSON(folder_path,file_path,response)
            return JsonResponse(response)







'''
detect how many topics cover this course's objective
'''
def compareObjectiveAndTopic(csv_file_name,objective):
    
    path = 'media/'
    csv_data = openfile(str(csv_file_name), path)
    nodes,_,_ = buildNodeEdges(csv_data) 
    topics = [node['label'] for node in nodes if node['id'].count('.') > 0 and not node['label'].startswith('Obj')]

    # use BERT model to calculate the semilarity between objective and course topics
    model = SentenceTransformer('all-mpnet-base-v2')
    first_embedding = model.encode(objective, convert_to_tensor=True)
    second_embeddings = model.encode(topics, convert_to_tensor=True)

    cosine_scores = util.cos_sim(first_embedding, second_embeddings)
    threshold = 0.4
    counter = 0
    for score in cosine_scores[0]: 
        if score > threshold:
            counter += 1 

    str_counter = "[" + str(counter)+ "]"
    return str_counter













def editGraph(request, course_id):

    course = get_object_or_404(Course, pk=course_id)
    objectives = course.objectives.all()

    nodes, edges = courseNodesEdgesFromJSON(course.course_id, course.course_name)


    if not nodes and not edges:
      
        if course.csv_file:
            csv_data = openfile(str(course.csv_file), 'media/')
            nodes, edges,_ = buildNodeEdgesVersion2(csv_data, course.course_id)

    if not nodes and not edges:
        nodes = [{
            'id': course.course_id,  
            'label': course.course_name,  
            'shape': "circle"
        }]
        edges = []

    related_courses = findRelatedCourse2(course_id)

    response = {
        "nodes": nodes, 
        "edges": edges, 
        "courseId": course_id, 
        "course": course, 
        "objectives": objectives,
        "related_courses":related_courses
    }
    
    return render(request, 'editGraph.html', response)





# 从 JSON 获取单个课程的内容
def courseNodesEdgesFromJSON(course_id, course_name):
    file_name = str(course_id) + '.json'
    folder_path = os.path.join(os.getcwd(), 'media', 'JSON', 'UvA_courses')
    file_path = os.path.join(folder_path, file_name)
    nodes = []
    edges = []

    if os.path.exists(file_path) and os.path.isfile(file_path):
        try:
            with open(file_path, 'r') as json_file:
                # Read JSON file data
                json_data = json.load(json_file)
                if json_data and "nodes" in json_data and "edges" in json_data:
                    nodes = json_data["nodes"]
                    edges = json_data["edges"]
        except Exception as e:
            print(f"Error reading JSON file: {e}")

    return nodes, edges





'''
Extract nodes and edges from a list(version 2)
'''
def buildNodeEdgesVersion2(csv_data,course_id=None):
    nodes = []
    edges = []
    if course_id is None:
        courseId = csv_data[1]['courseid']
    else:
        courseId = str(course_id)
    shape_mapping = {
    0: "circle",
    1: "ellipse",
    2: "box",
    3: "box",
    4: "box"
    }

    original_to_uuid = {}  # Mapping from original ID to UUID
    node_map = {}  # To keep track of nodes by UUID

    cnt = 0
    for row in csv_data:
        if cnt < 0: # 
            cnt += 1
            continue   
        
        if row["topic"].startswith('Obj'): # 
            cnt += 1
            continue   

        nodeId = str(uuid.uuid4())
        original_id = ".".join(filter(None, [courseId, row["chapterid"], row["sectionid"], row["unitid"], row["subunitid"]]))
        layer = original_id.count(".")
        shape = shape_mapping.get(layer, "square")

        node = {
            "id": nodeId,
            "label": row["topic"],
            "shape": shape,
            "cog_level": row["Cognitive level"].strip(),
            "title": row["topic"],
            "description":row["topic"] + ": " + row["description_of_topic"],
            "layer": layer
        }
        nodes.append(node)

        node_map[nodeId] = original_id
        original_to_uuid[original_id] = nodeId

        # Set up parent-child relationships based on original IDs
        parent_original_id = original_id[:original_id.rfind('.')] if '.' in original_id else None
        if parent_original_id and parent_original_id in original_to_uuid:
            parent_uuid = original_to_uuid[parent_original_id]
            edge = {
                'from': parent_uuid,
                'to': nodeId,
                'title': ''
            }
            edges.append(edge)

    return nodes, edges, courseId


def explainByAI(request):
    if request.method == 'POST':
        nodeInfo = request.POST.get('nodeInfo')
        
        # 配置 Google Generative AI
        genai.configure(api_key=os.environ.get("API_KEY"))
        model = genai.GenerativeModel("gemini-pro")
        content = "Write a short description about '" + nodeInfo + "'"
        response_obj = model.generate_content(content)
        
        # 从 GenerateContentResponse 对象中提取文本内容
        response_text = response_obj.text  # 假设返回对象有一个 text 属性
        
        # 将响应包装在字典中
        response = {
            'description': response_text
        }
        
        return JsonResponse(response, safe=False)


def overview(request):
    # 获取所有课程
    courses = Course.objects.all().filter(source="UvA")

    trajectories = Trajectory.objects.values('trajectory_name').distinct().order_by('trajectory_name')

    selected_trajectory_name = request.GET.get('trajectory')

    selected_objectives = []
    
    if selected_trajectory_name:
        selected_trajectories = Trajectory.objects.filter(trajectory_name=selected_trajectory_name)
        selected_objectives = selected_trajectories.values_list('objective', flat=True)


    if selected_trajectory_name:

        selected_trajectories = Trajectory.objects.filter(trajectory_name=selected_trajectory_name)
        related_objectives = Course.Objective.objects.filter(trajectory__in=selected_trajectories)
        courses = Course.objects.filter(objectives__in=related_objectives).distinct()
    else:
        courses = Course.objects.all()

    context = {
        'courses': courses,
        'trajectories': trajectories,
        'selected_trajectory_name': selected_trajectory_name,
        'selected_objectives': selected_objectives,
    }


    return render(request,'overview.html',context)



def saveJson(request):
    if request.method == 'POST':
        try:
            course_id = request.POST.get('courseId')
            json_data = request.POST.get('data')

            # build the path
            file_name = course_id + '.json'
            folder_path = os.path.join(os.getcwd(), 'media', 'JSON', 'UvA_courses')   
            file_path = os.path.join(os.getcwd(), folder_path, file_name)

            if json_data:
                # 将JSON字符串解析为Python字典
                data = json.loads(json_data)
            saveToJSON(folder_path,file_path,data)

            return JsonResponse({'status': 'success', 'message': 'File saved successfully.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)






# def findRelatedCourse(course_id):
#     file_name = str(course_id) + '.json'
#     folder_path = os.path.join(os.getcwd(), 'media', 'JSON', 'UvA_courses')
#     file_path = os.path.join(folder_path, file_name)

#     if os.path.exists(file_path) and os.path.isfile(file_path):
#         with open(file_path, 'r') as json_file:
#             # 读取 JSON 文件数据
#             json_data = json.load(json_file)
#             target_labels = [node["label"] for node in json_data["nodes"]]
#             target_course = ",".join(target_labels)

#             target_labels_1 = {node["label"] for node in json_data["nodes"]}
#     else:
#         return []
    
#     other_courses = []
#     for file in os.listdir(folder_path):
#         if file.endswith('.json') and file != file_name:
#             other_file_path = os.path.join(folder_path, file)
#             with open(other_file_path, 'r') as other_json_file:
#                 other_json_data = json.load(other_json_file)
#                 other_labels = [node["label"] for node in other_json_data["nodes"]]
#                 other_course_str = ",".join(other_labels)
#                 other_courses.append((file, other_course_str))  # 保存文件名和拼接后的字符串

#                 other_labels_1 = {node["label"] for node in other_json_data["nodes"]}
#                 common_labels =  target_labels_1.intersection(other_labels_1)
#                 print(common_labels)
    

#     model = SentenceTransformer("all-MiniLM-L6-v2")
#     target_embedding = model.encode(target_course)
    
#     similar_courses = []

#     for file, other_course_str in other_courses:
#         other_embedding = model.encode(other_course_str)  # 计算每个课程的嵌入
#         similarity = util.cos_sim(target_embedding, other_embedding).item()  # 计算相似度
        
#         if similarity > 0.45: 
#             print(similarity)
#             course_id_from_file = file.replace('.json', '')  # 获取课程 ID (去掉 .json 扩展名)
#             similar_courses.append((course_id_from_file, similarity))

#     # Step 4: 返回相似度大于 0.5 的课程的 Course 对象
#     if similar_courses:
#         similar_courses.sort(key=lambda x: x[1], reverse=True)  # 按相似度排序
        
#         # 获取相似课程的 Course 对象
#         course_ids = [course_id for course_id, _ in similar_courses]
#         related_courses = Course.objects.filter(course_id__in=course_ids)  # 根据课程 ID 查询 Course 对象
        
#         return related_courses
#     else:
#         return []



'''
打开文件名为UvA_all_courses的json文件
搜索edges里面的from 或者 to 里面有该course_id的边
然后或者该边的另一个course id 收集起来 

'''

def findRelatedCourse2(course_id):
    # Initialize an empty set to collect course IDs
    course_ids = set()

    # Construct the file path
    file_name = 'UvA_all_courses.json'
    folder_path = os.path.join(os.getcwd(), 'media', 'JSON', 'curriculaSimilarity')
    file_path = os.path.join(folder_path, file_name)

    # Check if the file exists and is valid
    if os.path.exists(file_path) and os.path.isfile(file_path):
        try:
            # Open and load the JSON data
            with open(file_path, 'r') as json_file:
                json_data = json.load(json_file)

                # Iterate over the edges and find related courses
                for edge in json_data["edges"]:
                    # Convert edge["from"] and edge["to"] to string to ensure type match
                    if str(edge["from"]) == str(course_id):
                        course_ids.add(edge["to"])
                    elif str(edge["to"]) == str(course_id):
                        course_ids.add(edge["from"])

            # Query the Course model for the related courses
            related_courses = Course.objects.filter(course_id__in=list(course_ids))

            return related_courses

        except json.JSONDecodeError:
            print("Error: Failed to decode the JSON file.")
        except Exception as e:
            print(f"Error: {e}")

    else:
        print("Error: File not found or inaccessible.")

    return []

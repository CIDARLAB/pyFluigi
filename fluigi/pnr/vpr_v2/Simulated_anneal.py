# # def simulated_annealing (cells: List[Cell], nets: List[Net], temperature: float, cooling_rate: float, iterations: int) -> List[Cell]:
# # # """Simulated annealing algorithm.

# # # Args:
# # # cells (List[Cell]): List of cells to be placed.
# # # nets (List[Net]): List of nets to be routed.
# # # temperature (float): Initial temperature.
# # # cooling_rate (float): Cooling rate.
# # # iterations (int): Number of iterations.

# # # Returns:
# # # List[Cell]: List of cells placed.
# # # """
# # # Initialize the best solution

# # best_solution = cells
# # best_solution_cost = calculate_cost(cells, nets)

# # # Initialize the current solution
# # current_solution = cells
# # current_solution_cost = best_solution_cost

# # # Loop until the system has cooled
# # while temperature > 1:
# # # Loop until the system has reached equilibrium
# # for i in range(iterations):
# # # Create a new solution
# # new_solution = create_new_solution(current_solution)
# # new_solution_cost = calculate_cost(new_solution, nets)

# # # Check if the new solution is better
# # if new_solution_cost < current_solution_cost:
# # current_solution = new_solution
# # current_solution_cost = new_solution_cost

# # # Check if the new solution is the best solution
# # if current_solution_cost < best_solution_cost:
# # best_solution = current_solution
# # best_solution_cost = current_solution_cost
# # else:
# # # Calculate the probability of accepting the new solution
# # probability = math.exp(
# # (current_solution_cost - new_solution_cost) / temperature)

# # # Check if the new solution should be accepted
# # if probability > random.random():
# # current_solution = new_solution
# # current_solution_cost = new_solution_cost

# # # Cool the system
# # temperature *= 1 - cooling_rate

# # return best_solution

# import json
# import random
# import math
# import matplotlib.pyplot as plt
# import matplotlib.patches as mpatches
# from matplotlib.patches import Rectangle
# import itertools


# def overlap_area( data, init_place):

#    ROUTE_SPACE = 100
#    COMP_SPACE = 1000
#    x = []
#    y = []     
#    for i in init_place:
#      x.append(round(((init_place[i][0]))))
#      y.append(round(((init_place[i][1]))))

#    overlap_param = {}

# #    vi_left = []
# #    vi_right = []
# #    vi_bottom = []
# #    vi_top = []

#    for i in range(0,len(init_place)-1):
#         overlap_param[i] ={}
#         overlap_param[i]['vi_left'] = (x[i] - COMP_SPACE - ROUTE_SPACE)
#         overlap_param[i]['vi_right'] = (x[i] + data['components'][i]['x-span'] + ROUTE_SPACE + COMP_SPACE)
#         overlap_param[i]['vi_top'] = (y[i] - COMP_SPACE - ROUTE_SPACE)
#         overlap_param[i]['vi_bottom'] =(y[i] + data['components'][i]['y-span'] + ROUTE_SPACE + COMP_SPACE)
  
   
#    #Area = (max(vi_right) - min(vi_left))*(max(vi_bottom)-min(vi_top))
  
#    overlap = [] 

#    for i in range(0,len(init_place)-1):
#       for j in range (i+1, len(init_place)-1): 
#          if ((overlap_param[i]['vi_left'] <= overlap_param[j]['vi_right']) and (overlap_param[i]['vi_right'] >= overlap_param[j]['vi_left']) and (overlap_param[i]['vi_bottom'] <= overlap_param[j]['vi_top']) and (overlap_param[i]['vi_top']>=overlap_param[j]['vi_bottom'])):
#             overlap_x = min(overlap_param[i]['vi_right'], overlap_param[j]['vi_right']) - max(overlap_param[i]['vi_left'], overlap_param[j]['vi_left'])
#             overlap_y = min(overlap_param[i]['vi_bottom'], overlap_param[j]['vi_bottom']) - max(overlap_param[i]['vi_top'], overlap_param[j]['vi_top'])
#             overlap.append(overlap_x * overlap_y)

#    tot_Overlap = sum(overlap)
#    #print(tot_Overlap)
#    return tot_Overlap


# def initial_random_place (data):

#     j = 0
#     # maxDeviceWidth = 150000     #micron
#     # maxDeviceLength = 150000     #micron  

#     maxDeviceWidth = 76800     #micron
#     maxDeviceLength = 76800     #micron 


#     place_init = {}
#     for comp in data['components']:
#         x = round((random.random())*maxDeviceWidth, 2)
#         y = round((random.random())*maxDeviceLength, 2)
#         place_init[data['components'][j]['name']] = [x,y]
#         #print(data['components'][j]['name'])
#         j=j+1
        
#     return place_init

# def initial_cost(data, init_place, overlap_ar):
#     #print(len(data['connections']))
#     j=0
#     dist = []
#     for conn in data['connections']:
#         sink = data['connections'][j]['sinks'][0]['component']
#         src = data['connections'][j]['source']['component']

#         if sink in init_place:
#             sink_coord = init_place[sink]

#         if src in init_place:
#             src_coord = init_place[src]
       
#         #print(sink_coord, src_coord)
#         #distance = math.sqrt(pow((sink_coord[0] - src_coord[0]),2) + pow((sink_coord[1] - src_coord[1]),2))
#         distance = abs(sink_coord[0] - src_coord[0]) + abs(sink_coord[1] - src_coord[1])
#         dist.append(round(distance, 2))
#         j=j+1

#     print(dist)
#     cost_init = (2*sum(dist)) + (overlap_ar*10000)
#     return cost_init


# def calc_cost(data, init_place, overlap_ar):
#     #print(len(data['connections']))
#     j=0
#     dist = []
#     for conn in data['connections']:
#         sink = data['connections'][j]['sinks'][0]['component']
#         src = data['connections'][j]['source']['component']

#         if sink in init_place:
#             sink_coord = init_place[sink]

#         if src in init_place:
#             src_coord = init_place[src]
       
#         #print(sink, src)
#         #distance = math.sqrt(pow((sink_coord[0] - src_coord[0]),2) + pow((sink_coord[1] - src_coord[1]),2))

#         distance = abs(sink_coord[0] - src_coord[0]) + abs(sink_coord[1] - src_coord[1])
#         dist.append(round(distance, 2))
#         j=j+1

#     #print(dist)
#     cost_init = (2*sum(dist)) + (overlap_ar*10000)
#     return cost_init


# def initial_temp(init_cost):
#     return (init_cost*20)


# maxDeviceWidth = 76800     #micron
# maxDeviceLength = 76800     #micron 


# with open('dx10_ref.json', 'r') as f:
#     data = json.load(f)   


# init_place = initial_random_place(data)
# overlap_ar = overlap_area(data, init_place)
# init_cost = initial_cost(data, init_place, overlap_ar)
# print("Initial Cost:" + str(init_cost))
# init_temp = initial_temp(init_cost)
# #init_temp = 100
# print("Initial Temp:" + str(init_temp))
# print("Initial Placement:")
# print(init_place)

# rangeX = maxDeviceWidth
# rangeY = maxDeviceLength
# temp = init_temp    
# cost = init_cost
# Numcomp = len(data['components'])
# numMovesperTemppermodule = int(10 * pow(Numcomp, 0.33))
# accept = 0
# totalmoves = 0


# while ((temp > (0.005 * cost/Numcomp)) and (temp >2)):
#     #print("In here")
#     for i in range(Numcomp * numMovesperTemppermodule):
#         #print("Iteration no." + str(i))

#         init_place_orig = {}
#         init_place_orig = init_place
#         add_x = 0
#         add_y = 0

#         random_node = random.choice(list(init_place))

#         #init_place[random_node] = [c_x, c_y]

#         if random.randint(-1,1) > 0:

#             add_x = (random.randint(-1,1))*rangeX  
#             #add_x = 0.5      
#             init_place[random_node][0] = init_place[random_node][0] + add_x        
            

#         else:

#             add_y = (random.randint(-1,1))*rangeY
#             init_place[random_node][1] = init_place[random_node][1] + add_y        
        
#         overlap_ar = overlap_area(data, init_place)
#         new_cost = calc_cost(data, init_place, overlap_ar)
#         totalmoves = totalmoves + 1
#         #print("New cost: " + str(new_cost) + " Old Cost: " + str(cost))


#         if new_cost < cost:
#             #print("Move accepted")
#             accept = accept + 1
#             cost = new_cost

#         if new_cost > cost:
#             if random.randint(0,1) < pow((math.e), (cost - new_cost)/temp):        
#                 #print("Move accepted")
#                 accept = accept + 1
#                 cost = new_cost

#             else:
#                 init_place = init_place_orig 
#                 #print("Undo move")
    
#     acceptrate = accept / totalmoves

#     if acceptrate > 0.96:
#         temp = temp * 0.5

#     if acceptrate > 0.8 and acceptrate <= 0.96:
#         temp = temp * 0.9

#     if acceptrate > 0.15 and acceptrate <= 0.8:
#         temp = temp * 0.95

#     if acceptrate <= 0.15:
#         temp = temp * 0.8

#     rangeX = rangeX * (1 - 0.44 + acceptrate)

#     rangeY = rangeY * (1 - 0.44 + acceptrate)
   
# #print("Overlap area:")
# #print(overlap_area(data, init_place))
# print("Final placement:")
# print(init_place)
# x = []
# y = []     
# for i in init_place:
#    x.append(round(((init_place[i][0]))))
#    y.append(round(((init_place[i][1]))))

# print("Total acceptanced moves: " + str(accept))
# print("Acceptance rate: " + str(acceptrate))


# def plot_render(init_place):

#     x=[]
#     y=[]
#     for i in init_place:
#         x.append(round(((init_place[i][0])/pow(10,7)),2))
#         y.append(round(((init_place[i][1])/pow(10,7)),2))

    
#     plt.plot(x, y, 'bo')

#     x=[]
#     y=[]
#     for i in init_place:
#         x.append(round(((init_place[i][0])/pow(10,7))))
#         y.append(round(((init_place[i][1])/pow(10,7))))

    
#     plt.axis([-10, 10, -10, 10])

#     print('min x, y')
#     print(min(x), min(y))
    
#     left, bottom, width, height = (min(x)-2, min(y)-2, 10, 10)
#     rect=mpatches.Rectangle((left,bottom),width,height, 
#                             fill=False,
#                             color="black",
#                         linewidth=1)
#                         #facecolor="red")
#     plt.gca().add_patch(rect)


#     # for i_x, i_y in zip(x, y):
#     #     plt.text(i_x, i_y, '({}, {})'.format(i_x, i_y))

#     plt.show()


# plot_render(init_place)

import json
import random
import math
import math
import cairo
from typing import Tuple, Dict


def initial_random_place (data) -> Dict[str, Tuple[float, float]]: 

    
    maxDeviceWidth = 76200     #micron
    maxDeviceLength = 76200     #micron 

    place_init = {}

    for comp in data['components']:
        x = round((random.random())*maxDeviceWidth, 2)
        y = round((random.random())*maxDeviceLength, 2)
        place_init[comp['name']] = [x,y]
        
        
    return place_init


def calc_area_overlap_penalty(data, place_array) -> float:

    v_left = []
    v_right = []
    v_top = []
    v_bottom = []

    for k,v in place_array.items():
        x = round(v[0])
        y = round(v[1])
        for comp in data['components']:
            if comp['name'] == k:
                x_span = comp['x-span']
                y_span = comp['y-span']


        v_left.append(x - 1000 - 100)
        v_right.append(x + x_span + 1000 + 100)
        v_top.append(y - 1000 - 100)
        v_bottom.append(y + y_span + 1000 + 100)

    area = (max(v_right) - min(v_left))*(max(v_bottom) - min(v_top))

    overlap = [] 

    for i in range(0,len(place_array)-1):
        for j in range (i+1, len(place_array)-1): 
            if ((v_left[i] <= v_right[j]) and (v_right[i] >= v_left[j]) and (v_bottom[i] <= v_top[j]) and (v_top[i]>= v_bottom[j])):
                overlap_x = min(v_right[i], v_right[j]) - max(v_left[i], v_left[j])
                overlap_y = min(v_bottom[i], v_bottom[j]) - max(v_top[i], v_top[j])
                overlap.append(overlap_x * overlap_y)

    
    OverlapArea = sum(overlap)
    #print(OverlapArea)
    overlapPenalty = OverlapArea * 10000
    #print(overlapPenalty)
    areaPenalty = area * 0

    return overlapPenalty + areaPenalty
    
    
def find_port_coord(data, comp_name, port_no) -> Tuple[float, float]:
   
    
    for comp in data['components']:
        if comp['name'] == comp_name:
            for k in comp['ports']:
                if k['label']['label'] == port_no:
                    x = k['label']['x']
                    y = k['label']['y']
                    return(x,y)
            


def calc_chan_penalty(data, init_place):

    dist = []
    spenalty = 0
    tpenalty = 0
    numpenalty = 0

    for conn in data['connections']:
        sink = conn['sinks'][0]['component']
        src = conn['source']['component']

        try:
            sink_port_x =conn['sinks'][0]['port']['x']
            sink_port_y =conn['sinks'][0]['port']['y']
        except:
            port_no = conn['sinks'][0]['port']
            sink_port_x, sink_port_y = find_port_coord(data, sink, port_no)

        try:
            src_port_x = conn['source']['port']['x']
            src_port_y = conn['source']['port']['y']
        except:
            port_no = conn['source']['port']
            src_port_x, src_port_y = find_port_coord(data, src, port_no)


        if sink in init_place:
            sink_coord = init_place[sink]

        sink_coord_x = sink_coord[0] + sink_port_x
        sink_coord_y = sink_coord[1] + sink_port_y

        if src in init_place:
            src_coord = init_place[src]
                 
        src_coord_x = src_coord[0] + src_port_x
        src_coord_y = src_coord[1] + src_port_y
      
        ch_length = abs( src_coord_x - sink_coord_x) + abs(src_coord_y - sink_coord_y)
        dist.append(round(ch_length, 2))

        #Overlap source

        if src_coord_y < sink_coord_y:
            spenalty = 1
            

        elif src_coord_y > sink_coord_y:
            spenalty = 1
            

        elif src_coord_x > sink_coord_x:
            spenalty =  1
            

        if src_coord_x < sink_coord_x:
            spenalty = 1
            
        #Overlap target

        if sink_coord_y < src_coord_y:
            tpenalty = 1
            

        elif sink_coord_y > src_coord_y:
            tpenalty = 1
            

        elif sink_coord_x < src_coord_x:
            tpenalty =  1
            

        if sink_coord_x < src_coord_x:
            tpenalty = 1

        numpenalty = numpenalty + spenalty + tpenalty
        
    #print('numpenalty'+str(numpenalty))    
    channel_penalty = (2*sum(dist)) #+ (numpenalty*10000)
    #print('channel penalty'+str(channel_penalty))
    return channel_penalty
    


def initial_temp(init_cost: float) -> float:
    return (init_cost*20)
    #return 1000


def get_x_y_span(data, component: str) -> Tuple[int, int]:
    
    for comp in data['components']:
        if comp['name'] == component:
            x_span = comp['x-span']
            y_span = comp['y-span']
            return (x_span, y_span)
            
def get_port_radius(data, port_name: str) -> int:

    for comp in data['components']:
        if comp['name'] == port_name:
            return comp['params']['portRadius'] 

def make_render(final_place, data, rangeX: int, rangeY: int) -> None:
    
    WIDTH = int(76200/350)
    HEIGHT = int(76200/350)

    # WIDTH = int(rangeX/1000)
    # HEIGHT = int(rangeY/1000)

    
    surface = cairo.ImageSurface(cairo.FORMAT_RGB24, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)
    ctx.set_source_rgba(0.0, 0.0, 0.0, 1.0)
    ctx.scale(1/350, 1/350)

    for k,v in final_place.items():

        x_coord = round(v[0])
        y_coord = round(v[1])

        if is_port(data, k):
            
            ctx.arc(x_coord, y_coord, (get_port_radius(data, k)), 0, 2*math.pi)
            ctx.set_source_rgb(0.6, 0.6, 0.6)
            ctx.fill()

        else:
            x_span, y_span = get_x_y_span(data, k)
            ctx.rectangle(x_coord, y_coord, x_span, y_span)
            ctx.set_source_rgb(0.6, 0.6, 0.6)
            ctx.fill()

    surface.write_to_png("example.png")  # Output to PNG


def is_port(data, component_id: str) -> bool:

    for comp in data['components']:
        if comp['name'] == component_id:
            return True if comp['entity'] == "PORT" else False

def sim_anneal() -> None:

    maxDeviceWidth = 76200     #micron
    maxDeviceLength = 76200     #micron 

    with open('dx6_ref.json', 'r') as f:
        data = json.load(f)   


    init_place = initial_random_place(data)
    init_cost  = round(calc_chan_penalty(data, init_place) + calc_area_overlap_penalty(data, init_place), 2)
    init_temp = initial_temp(init_cost)
    print("Initial Cost:" + str(init_cost))
    print("Initial Temp:" + str(init_temp))
    print("Initial Placement:")
    print(init_place)

    rangeX = maxDeviceWidth
    rangeY = maxDeviceLength
    placed_arr = init_place
    temp = init_temp    
    cost = init_cost
    Numcomp = len(data['components'])
    numMovesperTemppermodule = int(10 * pow(Numcomp, 0.33))
    accept = 0
    totalmoves = 0


    while ((temp > (0.005 * cost/Numcomp)) and (cost >2)):
        
        for i in range(Numcomp * numMovesperTemppermodule):

            new_cost = 0
            placement_new = {}
            placement_new = placed_arr
            add_x = 0
            add_y = 0

            random_node = random.choice(list(placement_new))

            x_span, y_span = get_x_y_span(data, str(random_node))


            add_x = rangeX/20*random.random() if random.random() > 0.5 else -rangeX/20*random.random()
            add_y = rangeY/20*random.random() if random.random() > 0.5 else -rangeY/20*random.random()
            
            
            if random.random()> 0.5:
                add_x = 0

            else:
                add_y = 0
            
            if add_x + x_span + placement_new[random_node][0]> maxDeviceWidth:
                add_x = 0

            elif placement_new[random_node][0] + add_x < 0:
                add_x = 0

            if add_y + y_span + placement_new[random_node][1]> maxDeviceLength:
                add_y = 0

            elif placement_new[random_node][1] + add_y < 0:
                add_y = 0
                

            placement_new[random_node][0] = round (placement_new[random_node][0] + add_x, 2)        
            placement_new[random_node][1] = round(placement_new[random_node][1] + add_y, 2)        
            #print('placement_new[random_node][x]')
            #print(placement_new[random_node][0])

            new_cost = calc_chan_penalty(data, placement_new) + calc_area_overlap_penalty(data, placement_new)
            #print('New cost'+str(new_cost))
            totalmoves = totalmoves + 1
            


            if new_cost < cost:
                #print("Move accepted")
                accept = accept + 1
                cost = new_cost
                placed_arr = placement_new


            if new_cost > cost:
                if random.random() < pow((math.e), -(cost - new_cost)/temp):        
                    #print("Move accepted")
                    accept = accept + 1
                    cost = new_cost
                    placed_arr = placement_new

                else:
                    placed_arr = placed_arr 
                    #print("Undo move")
    
        acceptrate = accept / (totalmoves * numMovesperTemppermodule)

        rangeX = rangeX * (1 - 0.44 + acceptrate)

        rangeY = rangeY * (1 - 0.44 + acceptrate)

        if rangeX >= maxDeviceWidth:
            rangeX = maxDeviceWidth
            
        if rangeY >= maxDeviceLength:
            rangeY = maxDeviceLength
            

        if acceptrate > 0.96:
            temp = temp * 0.5

        if acceptrate > 0.8 and acceptrate <= 0.96:
            temp = temp * 0.9

        if acceptrate > 0.15 and acceptrate <= 0.8:
            temp = temp * 0.95

        if acceptrate <= 0.15:
            temp = temp * 0.8

        
   
    print("Final placement:")
    print(placed_arr)

    #print('Final Dimensions')
    #print(round(rangeX, 2), round(rangeY, 2))
    

    print("Total accepted moves: " + str(accept))
    print("Acceptance rate: " + str(round(acceptrate*100, 2)) +"%")

    make_render(placed_arr, data, rangeX, rangeY)


sim_anneal()

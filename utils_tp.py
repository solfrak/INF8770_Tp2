# from asyncio.windows_events import NULL
import numpy as np
import cv2

def extract_sequence(cap, frame_init = 0):
    frame_sequence = []

    for i in range(15):
        cap.set(1, frame_init + i)
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_sequence.append(gray)
        # plt.imshow(gray, cmap='gray')
        # plt.show()

    return frame_sequence

def decoupe(frame, dim_bloc = 16):
    n,m = frame.shape
    n_block = int(n/dim_bloc)
    m_block = int(m/dim_bloc)

    list_of_zone = []
    coords_of_zone = []

    for i in range(n_block):
        for j in range(m_block):
            zone = frame[i*dim_bloc:(i+1)*dim_bloc,j*dim_bloc:(j+1)*dim_bloc]
            list_of_zone.append(zone)
            coords_of_zone.append([i*dim_bloc,j*dim_bloc])
    
    return list_of_zone, coords_of_zone



def macroblock(frame, type_frame='I'):
    list_of_block, coords_of_block = decoupe(frame)

    list_of_macrobloc = []

    for k in range(len(list_of_block)):
        bloc = list_of_block[k]
        coords = coords_of_block[k]
        B,_ = decoupe(bloc,dim_bloc=8)
        macroblock = {
                        "ADDR": coords,
                        "TYPE": type_frame,
                        "VECT": [0,0],
                        "BCP": 0b0000,
                        "B0": B[0],
                        "B1": B[1],
                        "B2": B[2],
                        "B3": B[3],   
                    }
        list_of_macrobloc.append(macroblock)
    
    return list_of_macrobloc

def compute_D(Vx,Vy, macrobloc, frame, prev_frame, dim_bloc = 16):
    D = 0
    n,m = macrobloc["ADDR"]
    for i in range(dim_bloc):
        for j in range(dim_bloc):
            if (n+Vx+i>=0)&(m+Vy+j>=0)&(n+Vx+i<frame.shape[0])&(m+Vy+j<frame.shape[1]):
                D += (frame[n+Vx+i, m+Vy+j]-prev_frame[n+i,m+j])**2
    return D

def update_vect_mouvement(list_of_macrobloc, frame, prev_frame,dim_bloc = 16, epsilon=0.01):
    for n in range(len(list_of_macrobloc)):
        macrobloc = list_of_macrobloc[n]
        # Calcul du vecteur de mouvement
        D = []
        V = []
        for Vx in range(-dim_bloc, dim_bloc):
            for Vy in range(-dim_bloc, dim_bloc):
                D.append(compute_D(Vx,Vy,macrobloc,frame,prev_frame))
                V.append([Vx,Vy])
        dmin = np.argmin(D)

        if D[dmin]<epsilon:
            V = V[dmin]
            # Update du macrobloc lorsqu'on l'a trouvé
            list_of_macrobloc[n]['TYPE']='P'
            list_of_macrobloc[n]['VECT']=V
        else:
            # Si le minimum trouvé n'est pas nul, on encode le bloc comme une trame I
            list_of_macrobloc[n]['TYPE']='I'
            list_of_macrobloc[n]['VECT']=[0,0]

    return(list_of_macrobloc)


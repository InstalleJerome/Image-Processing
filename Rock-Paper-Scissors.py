import cv2
import numpy as np
import imutils
import time
import random

last_count = time.perf_counter_ns()
cap = cv2.VideoCapture(0)

def winner(player1, player2): #fonction pour définir le résultat
    if (player1 == "rock" and player2 == "scissors") or (player1 == "paper" and player2 == "rock") or (player1 == "scissors" and player2 == "paper"):
        winner = player1
    elif (player2 == "rock" and player1 == "scissors") or (player2 == "paper" and player1 == "rock") or (player2 == "scissors" and player1 == "paper"):
        winner = player2
    else : 
        winner = "Tie"
    return winner
    
red = (0,0,255)
green = (0,255,0)
blue = (255,0,0)

color = green
status = "None"
while True: #début de la boucle de capture vidéo
    count = time.perf_counter_ns()
    ret, frame = cap.read() #capture l'image de la caméra
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #transforme les couleurs de l'image du format BGR au format HSV

    #création du masque de couleur de peau
    lower_hand = np.array([100,50,50])
    upper_hand = np.array([140,255,255])
    mask = cv2.inRange(hsv, lower_hand, upper_hand)

    cnts = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #détection des contours dans la range du mask
    cnts = imutils.grab_contours(cnts) #permet de récupérer juste les contours de la ligne précédente
    cnts = sorted(cnts, key = cv2.contourArea, reverse=True) #trie la liste des contours par ordre décroissant de taille
    shapes = ["rock", "paper", "scissors"]

    if count - last_count >  100000000: #FPS
        for i, c in enumerate(cnts) : 
            area = cv2.contourArea(c) #renvoie l'aire du contour détecté, en pixels

            #Une forme en rouge, l'autre en vert
            if i%2 == 0 : 
                color = green
            elif i%2 != 0 :
                color = red
            
            if area > 5000 : #permet de faire un tri sur l'affichage et ne pas dessiner les petits contours
                cv2.drawContours(frame, [c], -1, color, 2) #dessine les contours

                #Calcule les moments d'inertie en x et en y du contours pour en trouver le centre (optionnel)
                M = cv2.moments(c)
                cx = int(M["m10"]/M["m00"])
                cy = int(M["m01"]/M["m00"])
                cv2.circle(frame,(cx,cy),7,(255,255,255),-1)

                #Conditions pour déterminer la forme réalisée par la main, à adapter en fonction de la distance de celle-ci par rapport à la caméra
                if area < 33000 : 
                    if color == red :
                        player2 = "rock"
                    if color == green:
                        player = "rock"
                elif 33000< area <37000:
                    if color == red:    
                        player2 = "scissors"
                    if color == green:
                        player = "scissors"
                else :
                    if color == red :
                        player2 = "paper"
                    if color == green:
                        player = "paper"
                

                print("area is...",area, "shape is ...", player)
                last_count = count

        if cv2.waitKey(1) == ord('q'): #menu de démarage
            color = blue
            status = "Ready"
        if cv2.waitKey(1) == ord('r'): #lancer une partie contre l'ordi
            ordi = random.choice(shapes)
            color = (200,150,100)
            if winner(player, ordi) == player:
                status = "WON"
            elif winner(player, ordi) == ordi:
                status = "LOST"
            else:
                status = "TIE"
        if cv2.waitKey(1) == ord('m'): #lancer une partie à 2 joueurs
            if winner(player, player2) == player:
                status = "P1"
            elif winner(player, player2) == player2:
                status = "P2"
            else : 
                status = "TIE"
                
        #affichage du résultat
        if status == "Ready":
            cv2.putText(frame, "SOLO : PRESS R", (200, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2, cv2.LINE_AA)

            cv2.putText(frame, " 2 PLAYERS : PRESS M", (200, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2, cv2.LINE_AA)

            cv2.putText(frame, "READY ?", (200,200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2, cv2.LINE_AA)
        elif status == "WON":
            cv2.putText(frame, "YOU WON", (200,60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 2, cv2.LINE_AA)
            cv2.putText(frame, "Ordi :" + str(ordi), (200,150), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 2, cv2.LINE_AA)
        elif status == "LOST":
            cv2.putText(frame, "YOU LOST", (200,60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 2, cv2.LINE_AA)
            cv2.putText(frame, "Ordi :" + str(ordi), (200,150), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 2, cv2.LINE_AA)
        elif status == "TIE":
            cv2.putText(frame, "TIE", (200,60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 2, cv2.LINE_AA)
            cv2.putText(frame, "Ordi :" + str(ordi), (200,150), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 2, cv2.LINE_AA)
        elif status == "P1":
            cv2.putText(frame, "Player1 Won", (200,60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 2, cv2.LINE_AA)
        elif status == "P2":
            cv2.putText(frame, "Player2 Won", (200,60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 2, cv2.LINE_AA)

        cv2.imshow("frame", frame)
    if cv2.waitKey(1) == 27:
        break
cap.release()
cv2.destroyAllWindows()
import cv2
import mediapipe as mp
import numpy as np
import math

# Inicializar o módulo Pose do MediaPipe
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils  # Para desenhar landmarks

# Definir as conexões que deseja desenhar (ombros e orelhas)
pose_connections = [(mp_pose.PoseLandmark.LEFT_EAR, mp_pose.PoseLandmark.LEFT_SHOULDER),
                    (mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.LEFT_HIP)
                    ]


# Inicializar a captura de vídeo usando a webcam (0 para webcam integrada)
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Converter o frame BGR para RGB (necessário para o MediaPipe)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Processar o frame para estimar poses
    results = pose.process(rgb_frame)

    if results.pose_landmarks:
        torso_coords = [(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x,
                         results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y),
                        (results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].x,
                         results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].y)]



        # Coordenada do quadril
        left_hip_coords = (results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].x,
                            results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].y)

        # Coordenada do ombro

        left_shoulder_coords = (results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x,
                                results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y)

        # Coordenadas das orelhas
        left_ear_coords = (results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EAR].x,
                           results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EAR].y)
        right_ear_coords = (results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_EAR].x,
                            results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_EAR].y)

        # Desenhar as landmarks (marcadores) das poses no frame, excluindo os braços
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, connections=pose_connections,
                                  landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 0, 255), circle_radius=0),
                                  connection_drawing_spec=mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2))
        #verde => 0, 255, 0
        #vermelho => 0, 0, 255

        """ponto_a = [left_shoulder_coords[0],left_ear_coords[1]]
        ponto_b = [hip_left_coords[0], hip_left_coords[1]]
        ponto_c = [knee_left_coords[0], knee_left_coords[1]]"""

       # angle = calculate_angle(ponto_a, ponto_b, ponto_c)



      #  print(angle)

        # Calcular a inclinação da linha do tronco
        trunk_slope = (left_hip_coords[1] - left_shoulder_coords[1]) / (left_hip_coords[0] - left_shoulder_coords[0])

        # Calcular a inclinação da linha perpendicular (inversa e negativa)
        perpendicular_slope = -1 / trunk_slope

        # Ponto inicial da linha perpendicular é o mesmo que o ponto do ombro esquerdo
        start_point_perpendicular = left_shoulder_coords

        # Calcular o ponto final da linha perpendicular a 180 graus
        length_perpendicular = 50  # Ajuste para o tamanho da linha
        end_point_perpendicular = (start_point_perpendicular[0] + length_perpendicular,
                                   start_point_perpendicular[1] + length_perpendicular * perpendicular_slope)


        # Calcular a inclinação da linha do tronco (angulo entre ombro e quadril)
        trunk_angle = math.degrees(math.atan2(left_hip_coords[1] - left_shoulder_coords[1],
                                              left_hip_coords[0] - left_shoulder_coords[0]))

        print(trunk_angle)

        if trunk_angle < 90:
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, connections=pose_connections,
                                      landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 0, 255), circle_radius=0),
                                      connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 0, 255),
                                                                                     thickness=2))

            cv2.putText(frame, "Postura errada", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2, cv2.LINE_AA)

        elif trunk_angle >= 90 or trunk_angle < 140:
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, connections=pose_connections,
                                      landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), circle_radius=0),
                                      connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0),
                                                                                     thickness=2))


            cv2.putText(frame, "Postura correta", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2, cv2.LINE_AA)

        else:
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, connections=pose_connections,
                                      landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255, 255, 255), circle_radius=0),
                                      connection_drawing_spec=mp_drawing.DrawingSpec(color=(255, 55, 255),
                                                                                     thickness=2))



    cv2.imshow("Pose Estimation", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

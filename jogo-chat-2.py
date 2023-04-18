import cv2
from cvzone.HandTrackingModule import HandDetector

detector = HandDetector(detectionCon=0.5, maxHands=2)

# Carregue a imagem da câmera ou do vídeo
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    hands, image = detector.findHands(image, draw=True)

    if hands and len(hands) == 2:
        for hand in hands:
            # Obter os pontos das mãos
            landmarks = hand["lmList"]

            # Inicializar a lista de pontos dos dedos
            finger_tip_points = []

            # Percorrer os pontos das mãos e adicionar os pontos dos dedos à lista
            for point in landmarks:
                finger_tip_points.append((point[1], point[2]))

            # Verificar se o dedo está levantado ou dobrado
            finger_status = [0, 0, 0, 0, 0]
            print(finger_tip_points)
            print(finger_tip_points[4][1])
            print(finger_tip_points[3][1])
            if finger_tip_points:
                # Polegar
                if finger_tip_points[4][0] < finger_tip_points[3][0]:
                    finger_status[0] = 1

                # Indicador
                if finger_tip_points[8][1] < finger_tip_points[6][1]:
                    finger_status[1] = 1

                # Médio
                if finger_tip_points[12][1] < finger_tip_points[10][1]:
                    finger_status[2] = 1

                # Anelar
                if finger_tip_points[16][1] < finger_tip_points[14][1]:
                    finger_status[3] = 1

                # Mínimo
                if finger_tip_points[20][1] < finger_tip_points[18][1]:
                    finger_status[4] = 1

            # Contar o número de dedos levantados
            num_fingers_raised = sum(finger_status)

            # Exibir o número de dedos levantados
            cv2.putText(image, f"Number of fingers raised: {num_fingers_raised}", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    else:
        print("Detectadas menos de duas mãos.")
    
    # Exibir a imagem
    cv2.imshow('Hand Tracking', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

# Liberar os recursos
hands.close()
cap.release()
cv2.destroyAllWindows()





import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

# Carregue a imagem da câmera ou do vídeo
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    # Converta a imagem em RGB
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Processar a imagem para detectar as mãos
    results = hands.process(image)

    # Desenhar os pontos das mãos na imagem
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Exibir a imagem
    cv2.imshow('Hand Tracking', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

# Liberar os recursos
hands.close()
cap.release()
cv2.destroyAllWindows()

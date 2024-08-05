# Importer la bibliothèque OpenCV
import cv2
import random

# Créer une liste de mots à mimer avec la main
mots = ["pouce", "index", "majeur", "annulaire", "auriculaire", "poing", "paume", "main ouverte",
        "main fermée",
        "victoire", "ok", "rock",
        "coeur", "salut", "au revoir"]

# Choisir un mot au hasard dans la liste

mot = random.choice(mots)

# Afficher le mot à mimer
print("Le mot à mimer est :", mot)

# Capturer la vidéo de la webcam
cap = cv2.VideoCapture(0)


# Définir une fonction pour détecter la main dans l'image

def detect_hand(image):
    # Convertir l'image en niveaux de gris

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Appliquer un seuil adaptatif pour isoler la main du fond
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 5)
    # Trouver les contours de la main
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Retourner le plus grand contour, qui correspond à la main
    max_area = 0
    hand_contour = None
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            hand_contour = cnt
    return hand_contour


# Définir une fonction pour décrire le mouvement de la main
def describe_hand(contour):
    # Calculer le centre de gravité de la main
    m = cv2.moments(contour)
    cx = int(m["m10"] / m["m00"])
    cy = int(m["m01"] / m["m00"])
    # Calculer le point le plus éloigné du centre, qui correspond au bout du doigt
    max_dist = 0
    finger_point = None
    for point in contour:
        x = point[0][0]
        y = point[0][1]
        dist = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
        if dist > max_dist:
            max_dist = dist
            finger_point = (x, y)
    # Calculer l'angle entre le centre, le bout du doigt et l'horizontale
    import math
    angle = math.degrees(math.atan2(cy - finger_point[1], finger_point[0] - cx))
    # Définir des seuils pour déterminer la direction du doigt
    if angle < -67.5 or angle > 67.5:
        direction = "haut"
    elif -22.5 < angle < 22.5:
        direction = "droite"
    elif -67.5 < angle < -22.5:
        direction = "diagonale haut droite"
    elif 22.5 < angle < 67.5:
        direction = "diagonale haut gauche"
    else:
        direction = "inconnue"
    # Retourner la description du mouvement de la main
    descript: str = "Le doigt pointe vers le " + direction
    return descript


# Boucle principale du jeu
while True:
    # Lire une image de la vidéo
    ret, frame = cap.read()
    # Vérifier que la lecture a réussi
    if not ret:
        break
    # Détecter la main dans l'image
    hand = detect_hand(frame)
    # Vérifier que la main a été détectée
    if hand is not None:
        # Dessiner le contour de la main sur l'image
        cv2.drawContours(frame, [hand], -1, (0, 255, 0), 2)
        # Décrire le mouvement de la main
        description = describe_hand(hand)
        # Afficher la description sur l'image
        cv2.putText(frame, description, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    # Afficher l'image
    cv2.imshow("Jeu de mime", frame)
    # Attendre que l'utilisateur appuie sur la touche Q pour quitter
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

# Libérer les ressources
cap.release()
cv2.destroyAllWindows()

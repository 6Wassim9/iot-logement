#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

// Configuration du Wi-Fi
const char* ssid = "wassim";           // Remplacez par le nom de votre réseau Wi-Fi
const char* password = "wassim123"; // Remplacez par le mot de passe de votre réseau Wi-Fi

// Adresse du serveur Flask
const char* flaskServer = "http://192.168.43.137:5000/capteur";

// Objet WiFiClient partagé pour les requêtes HTTP
WiFiClient client;

// Fonction pour envoyer une requête de test à un serveur public
void testPublicServer() {
    if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        http.begin(client, "http://httpbin.org/get"); // URL pour tester la connectivité Internet
        int httpCode = http.GET(); // Envoie une requête GET
        Serial.print("Code HTTP (Public): ");
        Serial.println(httpCode);

        if (httpCode > 0) {
            String payload = http.getString();
            Serial.println("Réponse :");
            Serial.println(payload);
        } else {
            Serial.println("Erreur dans la requête vers le serveur public");
        }

        http.end();
    } else {
        Serial.println("Wi-Fi non connecté !");
    }
}

// Fonction pour envoyer des données au serveur Flask
void sendDataToFlask() {
    if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;

        // Construction des données à envoyer
        String postData = "{\"temperature\":23.5, \"humidite\":45.3, \"timestamp\":\"2024-12-23 15:00:00\"}";
        http.begin(client, flaskServer); // Adresse du serveur Flask
        http.addHeader("Content-Type", "application/json"); // Définir le type de contenu

        // Envoie de la requête POST
        int httpCode = http.POST(postData);
        Serial.print("Code HTTP (Flask): ");
        Serial.println(httpCode);

        // Lire la réponse du serveur Flask
        if (httpCode > 0) {
            String payload = http.getString();
            Serial.println("Réponse Flask :");
            Serial.println(payload);
        } else {
            Serial.println("Erreur dans la requête vers le serveur Flask");
        }

        http.end();
    } else {
        Serial.println("Wi-Fi non connecté !");
    }
}

void setup() {
    Serial.begin(115200); // Initialiser la communication série
    delay(1000);

    // Connexion au réseau Wi-Fi
    Serial.print("Connexion au Wi-Fi : ");
    Serial.println(ssid);
    WiFi.begin(ssid, password);

    // Attendre la connexion
    int retries = 0;
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.print(".");
        retries++;
        if (retries > 20) {
            Serial.println("Impossible de se connecter au Wi-Fi !");
            return;
        }
    }
    Serial.println("\nConnecté au Wi-Fi !");
    Serial.print("Adresse IP : ");
    Serial.println(WiFi.localIP());
}

void loop() {
    // Tester la connexion à un serveur public
    Serial.println("\n=== Test avec un serveur public ===");
    testPublicServer();

    // Tester la connexion au serveur Flask
    Serial.println("\n=== Test avec le serveur Flask ===");
    sendDataToFlask();

    // Pause de 10 secondes avant le prochain test
    delay(10000);
}

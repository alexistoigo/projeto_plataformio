#define BLYNK_TEMPLATE_ID "TMPL27MaDhXaz"
#define BLYNK_TEMPLATE_NAME "Quickstart Template"
#define BLYNK_AUTH_TOKEN "JAJ3rn4XIiQkhY-yycGRXHP7gKG7QVvL"

#define DHTPIN 21
#define DHTTYPE DHT22

#define BLYNK_PRINT Serial

#include <WiFi.h>
#include <WiFiClient.h>
#include <BlynkSimpleEsp32.h>
#include <DHT.h>

#include <iostream>
#include <string>
#include <cstring>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <random>

char ssid[] = "LCI01";
char pass[] = "up3@wz01";

std::string caminaoId = "DEF9012";

BlynkTimer timer;

DHT dht(DHTPIN, DHTTYPE);

float h = dht.readHumidity();
float t = dht.readTemperature();

BLYNK_WRITE(V0)
{
  int value = param.asInt();
  Blynk.virtualWrite(V1, value);
}

void myTimerEvent()
{
  Blynk.virtualWrite(V6, t);
  Blynk.virtualWrite(V7, h);
}

std::string getSensoresCamaraFria()
{
  std::string binaryString;
  std::random_device rd;
  std::mt19937 gen(rd());
  std::uniform_int_distribution<> dis(0, 1);
  for (int i = 0; i < 4; ++i)
  {
    int bit = dis(gen);
    binaryString += std::to_string(bit);
  }

  return binaryString;
}

void enviaMensagem()
{
  int sock = 0;
  struct sockaddr_in serv_addr;
  std::string temperatura = std::to_string(t);
  std::string umidade = std::to_string(h);
  std::string localizacao = "Brasilia";

  std::string tmp = caminaoId + " " + temperatura + " " + umidade + " " + localizacao + " " + getSensoresCamaraFria();

  const char *msg = tmp.c_str();

  if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0)
  {
    std::cerr << "Erro ao criar socket" << std::endl;
    return;
  }

  serv_addr.sin_family = AF_INET;
  serv_addr.sin_port = htons(65432);

  if (inet_pton(AF_INET, "192.168.90.108", &serv_addr.sin_addr) <= 0)
  {
    std::cerr << "Endereço inválido ou não suportado" << std::endl;
    return;
  }

  if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
  {
    std::cerr << "Conexão falhou" << std::endl;
    return;
  }

  send(sock, msg, strlen(msg), 0);
  std::cout << "Mensagem enviada" << std::endl;

  close(sock);

  //delay(900000);  // Pausa de 15 minutos (900.000 milissegundos)
}

void setup()
{
  Serial.begin(9600);

  Blynk.begin(BLYNK_AUTH_TOKEN, ssid, pass);
  timer.setInterval(2000L, myTimerEvent);
  dht.begin();
}

void loop()
{
  Blynk.run();
  timer.run();

  h = dht.readHumidity();

  t = dht.readTemperature();
  if (t > 15.)
  {
    enviaMensagem();
  }
}

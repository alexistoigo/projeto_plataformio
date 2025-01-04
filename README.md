# Projeto de Controle de Temperatura para Caminhão Frigorífico

Este projeto foi desenvolvido como parte da disciplina de Internet das Coisas (IoT) no meu mestrado. Ele utiliza a plataforma ESP32 para monitorar e controlar a temperatura de uma câmara fria em um caminhão. Caso a temperatura esteja fora dos parâmetros estabelecidos, o sistema envia uma mensagem via Telegram para o gestor da frota, informando dados como localização, temperatura, entre outros.

## Funcionalidades

- Monitoramento contínuo da temperatura da câmara fria.
- Envio de alertas via Telegram quando a temperatura está fora do intervalo permitido.
- Inclusão de dados adicionais na mensagem, como localização do caminhão e temperatura atual.

## Componentes Utilizados

- ESP32
- Sensor de temperatura
- Conexão com a API do Telegram

## Instalação e Configuração

1. Clone este repositório:
    ```sh
    git clone https://github.com/seu-usuario/projeto_plataformio.git
    ```
2. Navegue até o diretório do projeto:
    ```sh
    cd projeto_plataformio
    ```
3. Configure as credenciais do Telegram e outros parâmetros no arquivo `config.h`.

4. Compile e carregue o código no ESP32 utilizando o PlatformIO.

## Uso

Após a instalação e configuração, o sistema começará a monitorar a temperatura da câmara fria automaticamente. Em caso de anomalias, o gestor da frota receberá uma mensagem no Telegram com as informações necessárias para tomar as devidas providências.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

## Contato

Para mais informações, entre em contato pelo email: alexistoigo@gmail.com

# Teste amo promo

Para executar o código siga os passo:

1. Clone este repositorio;
2. Monte a imagem do container;

`docker build . -t teste_amo_promo`

3. Execute o container

`docker run -p 8000:8000 teste_amo_promo`

A aplicacao ira rodar no endereço:

`127.0.0.1:8000`

## Endpoints

Voos somente ida:

`http://127.0.0.1:8000/api/search/<IATA ORIGEM>/<IATA DESTINO>/<DATA IDA>`

Voos ida e volta:

`http://127.0.0.1:8000/api/search/<IATA ORIGEM>/<IATA DESTINO>/<DATA IDA>/<DATA VOLTA>`

### Como alterar a api_key?

modifique a variavel de ambiente no Dockerfile e monte novamente a imagem do container
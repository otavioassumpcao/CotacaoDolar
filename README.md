# Aplicação Cotação Dólar

Este projeto é uma aplicação web que permite aos usuários consultar a cotação do dólar americano para uma data específica. Se a cotação não estiver disponível no banco de dados local, a aplicação buscará automaticamente as informações na API do Banco Central, salvará no banco de dados e apresentará os resultados ao usuário. Além da cotação, o usuário também recebrá como informação a variação da cotação em relação ao último dia útil, bem como o p-valor referente a essa varição.

## Características

- Consulta de cotação do dólar em uma data específica;
- Cálculo da variação da cotação e análise de significância estatística;
- Frontend simples com HTML e CSS;
- Backend implementado em Python com Flask;
- Persistência dos dados com SQLite3 e SQLAlchemy.

## Base de dados

A base de dados foi construída através dos dos dados disponibilizados pelo Banco Central através do Ipeadata (http://www.ipeadata.gov.br/ExibeSerie.aspx?serid=38590&module=M). A partir dela foi construída a base inicial ```Cotacao_Dolar_Serie_Histprica.csv```, que captura o valor de compra diário do dólar comercial desde 02/01/1985. Foi adicionado também, uma coluna com a variação da cotação em relação ao último dia útil. O cálculo para essa variação segue o seguinte modelo:

```math
\text{Variação}_t=\frac{\text{Cotação}_t - \text{Cotação}_{t-1}}{{Cotação}_{t-1}} \times 100
```

A partir dessa base inicial, foi construída uma base em SQL utilizando o SQLite, o código de construção dessa base pode ser visto no arquivo ```base.ipynb```

Em relação ao input de novas informações na base a partir da API do Banco Central é importante ressaltar que, essa API gera informações sobre cotação de compra e venda na data e hora solicitada. Para que houvesse uma compatibilidade entre as informações já existentes na base e as informações novas inseridas, foi tirada a média entre o valor de venda e o valor de compra da cotação, o resultado é o valor que é utilizado para os cálculos.

## Instalação e Configuração

Para rodar o projeto localmente, siga os passos abaixo:

1. Clone o repositório para sua máquina local:
```bash
git clone [URL do repositório]
```

2. Instale as dependências necessárias:
```bash
pip install -r requirements.txt
```

3. Execute o aplicativo em seu terminal:
```bash
app.py
```

**Atenção:** o arquivo ```base.ipynb``` não deve ser rodado, ele está presente no código apenas por motivos de elucidação da construção da base, caso seja rodado, toda informação inserida na base após o início da aplicação será perdida.

## Uso
Para consultar a cotação do dólar, siga as etapas abaixo:

1. Abra o seu navegador e vá para http://127.0.0.1:5000/.
2. No campo fornecido, insira a data desejada no formato (DD/MM/AAAA).
3. Submeta o formulário para receber a cotação e as demais informações.

## Significância Estatística

A aplicação também calcula a variação da cotação do dólar em relação ao último dia útil e avalia a significância estatística dessa variação. A análise estatística é um aspecto fundamental da aplicação, pois ela determina se as flutuações na cotação do dólar são normais ou se indicam uma mudança significativa no mercado.

### Teste de Hipótese

Para avaliar a significância da variação do dólar, um teste de hipóteses é realizado utilizando o teste t, que é uma ferramenta estatística que permite comparar a média de uma amostra com uma média de população conhecida ou com as médias de duas amostras independentes. Neste caso, usamos o teste t para comparar a variação atual do dólar com as variações históricas.

A escolha de utilizar a distribuição normal para modelar as variações da cotação do dólar é respaldada por observações gráficas dos dados históricos, que aparentam seguir essa distribuição. Esta suposição é consistente com muitos modelos econômicos e financeiros que pressupõem a normalidade dos retornos ou variações de preços devido à variedade de fatores pequenos e independentes que afetam o mercado cambial. A normalidade das variações de cotação é uma característica esperada, pois reflete um mercado eficiente onde a informação é rapidamente absorvida e refletida nos preços.

<p align="center">
  <img src="https://github.com/otavioassumpcao/CotacaoDolar/assets/83320033/74fd80fa-7b98-4512-820c-16c7d111374a">
</p>


O teste de hipótese é estruturado da seguinte forma:

- **Hipótese Nula (H0)**: A variação atual da cotação do dólar não é significativamente diferente das variações anteriores.
- **Hipótese Alternativa (H1)**: A variação atual da cotação do dólar é significativamente diferente das variações anteriores.

### Fórmula do Teste t

O valor t é calculado pela seguinte fórmula:

```math
t = \frac{ \bar X - \mu_t }{ \frac{S}{\sqrt{n}} }
```
onde:

- $\bar X:$ média das 500 últimas varições em relação à data consultada;
- $\mu_t:$ variação na data $t$ consultada;
- $S:$ desvio-padrão da amostra;
- $n:$ tamanho da amostra (500).

### Interpretação do p-valor

O p-valor resultante do teste t nos informa a probabilidade de observarmos uma variação tão extrema quanto a variação atual, assumindo que a hipótese nula é verdadeira. Se o p-valor for menor que o nível de significância estabelecido (geralmente 0.05), rejeitamos a hipótese nula. Isso indica que há menos de 5% de probabilidade de que a variação seja parte das flutuações normais do mercado, e portanto, é considerada estatisticamente significativa.

### Significância a 95%

Um p-valor abaixo de 0.05 sugere que a variação observada não é um resultado aleatório e pode ser considerada significativa com 95% de confiança. Isso significa que há evidências suficientes para afirmar que a variação do dólar na data em questão é atípica em comparação ao comportamento usual da moeda. 
Para exemplificar a utilidade da análise de significância estatística em um contexto real, podemos considerar o evento que ficou conhecido como "Joesley Day". Em 17 de maio de 2017, o Brasil foi sacudido por um escândalo político após a divulgação de uma conversa entre o então presidente Michel Temer e o empresário Joesley Batista. A conversa indicava que Temer havia dado aval para comprar o silêncio do ex-presidente da Câmara dos Deputados, Eduardo Cunha, o que gerou turbulência política e incertezas quanto à estabilidade do governo.

Os eventos desse dia foram tão impactantes que levantaram questionamentos sobre um possível impeachment do presidente Temer, afetando diretamente a confiança na aprovação da reforma da previdência, considerada crucial para a economia do país. Como resultado direto dessa instabilidade, no dia seguinte, 18 de maio de 2017, o mercado financeiro reagiu de forma dramática.

Nesse cenário, a cotação do dólar apresentou uma variação de 8.645%, uma mudança abrupta que foi capturada pela aplicação. O p-valor associado a essa variação foi de 3.58e-05, muito abaixo do limiar de significância de 0.05. Este valor baixo do p-valor nos permite rejeitar a hipótese nula de que a variação foi uma oscilação ordinária, confirmando que o evento político teve um efeito anômalo e significativo no mercado de câmbio.

Este exemplo demonstra o poder da aplicação em detectar e quantificar o impacto de eventos políticos e econômicos significativos na cotação do dólar. A capacidade de identificar tais variações não apenas oferece insights sobre o comportamento do mercado, mas também pode servir como uma ferramenta valiosa para analistas e investidores que buscam entender as forças que influenciam as taxas de câmbio.

<p align="center">
  <img src="https://github.com/otavioassumpcao/CotacaoDolar/assets/83320033/1c03594f-4420-4f61-8eb9-9944d56244c1">
</p>

## Limitações e Considerações finais
Este projeto é minha primeira aplicação do tipo, portando, existem algumas questões que ainda precisam ser revisadas, cito a seguir as que consegui identificar:

1. Cálculo do p-valor:
   Existe um problema amostral no cálculo do p-valor. Como essa estatística é calculada a partir das 500 últimas observações, é possível que, dependendo da data que o usuário está consultado, o p-valor seja calculado a partir de datas mais anteriores do que as precisamente 500 últimas. Isso acontece pelo fato de o programa adicionar as informações na base de dados, quando não consta nela, a partir da API do Banco Central apenas para a data consultada e a do dia anterior. Isso no curto prazo pode não ser um problema tão grande mas, por exemplo, se o usuário estiver no ano de 2030 e as últimas cotações registradas são do ano de 2023, o cálculo do p-valor será feito a partir do valor das varições de 2023, o que gera uma inconsistência no resultado obtido.

2. Base de comparação:
   A série histórica da cotação do dólar tem dados a partir de 02/01/1985 o que pode gerar inconsistências nos resultados apresentados pela aplicação, já que o Real foi implementado no Brasil apenas em 1994, ou seja, as informações apresentadas anteriomente a essa data podem não estar ajustadas para o Real (não encontrei informações a respeito no site do Banco Central).

3. Frontend:
   Como esse é minha primeira aplicação onde utilizo html e css, acredito que as informações não estão sendo apresentadas da melhor maneira possível. Por exemplo, no frontend da aplicação não há uma explicação acerca do p-valor, ele simplesmente aparece como um número solto. Além disso, a parte visual e maneira de fazer o input da data de consulta poderiam ser mais elegantes.

4. Distribuição normal:
   Assumi que a distribuição de probabilidade da serie histórica da variação da cotação do dólar é uma Normal principalmente pela análise gráfica, testes mais robustos devem ser feitos para verificar com mais precisão o tipo da distribuição.

3. Valores da cotação e USO da API
   A  base inicial utiliza a taxa de câmbio comercial para compra, já as informações coletadas da API são uma média da entre os valores de compra e venda, que são os dados disponibilizados pela API, o correto seria utilizar somente os de compra.

## Licença 

Este projeto está licenciado sob a Licença MIT - veja o arquivo ```LICENSE.md``` para detalhes.

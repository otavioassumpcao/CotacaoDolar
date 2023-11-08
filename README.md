# Aplicação - Cotação do Dólar

Este projeto é uma aplicação que permite aos usuários consultar a cotação do dólar americano para uma data específica. Caso a cotação não esteja disponível no banco de dados local, a aplicação buscará automaticamente as informações na API do Banco Central, salvará no banco de dados e apresentará os resultados ao usuário. Além da cotação, o usuário receberá informações sobre a variação da cotação em relação ao último dia útil, assim como o p-valor correspondente a essa variação.

## Características

- Consulta de cotação do dólar para datas específicas;
- Cálculo da variação da cotação e análise de sua significância estatística;
- Interface de usuário simples com HTML e CSS;
- Backend implementado em Python utilizando Flask;
- Persistência de dados com SQLite3 e SQLAlchemy.

## Base de Dados

A base de dados foi construída a partir dos dados disponibilizados pelo Banco Central via Ipeadata (http://www.ipeadata.gov.br/ExibeSerie.aspx?serid=38590&module=M). Com esses dados, foi criada a base inicial `Cotacao_Dolar_Serie_Historica.csv`, que registra o valor de compra diário do dólar comercial desde 02/01/1985. Também foi adicionada uma coluna que mostra a variação percentual da cotação em relação ao último dia útil, calculada pela fórmula:

```math
\text{Variação}_t = \frac{\text{Cotação}_t - \text{Cotação}_{t-1}}{\text{Cotação}_{t-1}} \times 100
```

A base inicial foi então expandida para uma base de dados SQL utilizando SQLite. O script utilizado para a construção dessa base está disponível no arquivo `base.ipynb`.

É importante salientar que, ao adicionar novas informações à base de dados a partir da API do Banco Central, a API fornece cotações de compra e venda para a data e hora especificadas. Para garantir a compatibilidade entre os dados históricos existentes e as novas informações inseridas, optei por calcular a média entre os valores de venda e de compra. Este valor médio é então utilizado nos cálculos de variação da cotação.

## Instalação e Configuração

Para rodar o projeto localmente, siga os passos abaixo:

1. Clone o repositório para sua máquina local:
```bash
git clone https://github.com/otavioassumpcao/CotacaoDolar/tree/main
```

2. Instale as dependências necessárias:
```bash
pip install -r requirements.txt
```

3. Execute a aplicação utilizando o comando:
```bash
python app.py
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

1. **Cálculo do p-valor**:

   A metodologia atual para o cálculo do p-valor pode apresentar um viés amostral. O p-valor é derivado das últimas 500 observações disponíveis; no entanto, se a data consultada pelo usuário for significativamente posterior à última cotação registrada, o p-valor seria calculado com base em um período anterior não contíguo. Por exemplo, se estivermos em 2030 e as últimas cotações disponíveis forem de 2023, o cálculo do p-valor utilizará as variações de 2023, introduzindo uma potencial distorção nos resultados. Embora no curto prazo isso possa não representar um problema significativo, é uma limitação que precisa ser considerada para análises em longo prazo e poderia ser abordada com uma atualização mais frequente da base de dados ou ajustes na lógica de cálculo.

2. **Base de Comparação:**

   A série histórica utilizada neste projeto começa em 02/01/1985, período em que o Brasil ainda não havia adotado o Real como moeda. Isso pode acarretar discrepâncias nos resultados apresentados pela aplicação, visto que os dados anteriores à adoção do Real em 1994 podem não estar devidamente ajustados para a nova moeda (não encontrei informações a respeito no site do Banco Central).

3. **Frontend:**

   Como esse é minha primeira aplicação onde utilizo HTML e CSS, acredito que as informações não estão sendo apresentadas da melhor maneira possível. Por exemplo, no frontend da aplicação não há uma explicação acerca do p-valor, ele simplesmente aparece como um número solto. Além disso, a estética da interface e a funcionalidade de inserção da data podem ser aprimoradas para proporcionar uma experiência de usuário mais intuitiva e visualmente agradável.

4. **Distribuição normal:**

   A suposição de que a série histórica das variações da cotação do dólar segue uma distribuição normal foi baseada principalmente em uma análise gráfica. Reconheço que testes estatísticos mais robustos são necessários para confirmar essa suposição com maior precisão. O tipo de distribuição tem um impacto significativo na análise de significância estatística e, portanto, é crucial que essa suposição seja verificada de forma mais rigorosa.

5. **Valores da cotação e USO da API:**

   A base de dados inicial contém taxas de câmbio comerciais referentes à compra, enquanto as informações adicionadas a partir da API do Banco Central representam uma média entre as taxas de compra e venda. Idealmente, para manter a consistência, deveríamos utilizar apenas os dados de compra. Esta discrepância metodológica pode levar a pequenas variações nos resultados finais e deve ser ajustada para garantir a integridade e a comparabilidade dos dados ao longo do tempo.

## Licença 

Este projeto está licenciado sob a Licença MIT - veja o arquivo ```LICENSE.md``` para maiores detalhes.

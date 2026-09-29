# 🪄 Tech Challenge - Fase 05

**🎓 FIAP + Alura**  
**📊 Pós-Tech Data Analytics - Turma 12DTAT**

## 👨‍💻 Autor

**Rodrigo Santiago Silva**  
**🆔 RM:** 369341

---

# 📊 Associação Passos Mágicos — Efetividade Socioeducacional e Preditivo de Risco
## 🔗 Links do Projeto

* 🌐 **Aplicação Interativa (Streamlit):** [Clique aqui para acessar a aplicação na nuvem](https://seu-link-no-streamlit.streamlit.app/)

## 📖 Descrição

Este projeto foi desenvolvido como parte do **Tech Challenge - Fase 05** (Projeto Final) da **Pós-Tech em Data Analytics**, promovida pela **FIAP** em parceria com a **Alura**.

O objetivo é realizar uma análise analítica e preditiva completa sobre a jornada socioeducacional dos alunos assistidos pela **Associação Passos Mágicos**, utilizando técnicas de **Ciência de Dados**, **Análise Exploratória de Dados (EDA)** e **Machine Learning** para compreender os fatores de desenvolvimento, engajamento, desempenho e risco de evasão/desengajamento.

Ao longo do projeto são executadas diversas etapas, incluindo:

- 📥 Coleta, higienização e preparação dos dados históricos e multidimensionais;
- 🧹 Limpeza e tratamento da base de dados com exportação otimizada (`.parquet`);
- 📊 Análise exploratória dos dados (EDA) estruturada em perguntas de negócio;
- ⚙️ Engenharia de atributos (*Feature Engineering*) e cálculo do viés de autoavaliação;
- 🤖 Treinamento e avaliação do modelo preditivo de risco de desengajamento;
- 📈 Avaliação de resultados e impacto longitudinal do programa pelas fases (**Quartzo ➔ Ágata ➔ Ametista ➔ Topázio**);
- 💡 Geração de insights para apoiar a tomada de decisão pedagógica e psicossocial.

Além da construção do modelo preditivo, a solução entrega um **Dashboard Interativo em Streamlit** para apoiar gestores e educadores na identificação precoce de vulnerabilidades.

---

> **Objetivo:** Prever a probabilidade de risco de desengajamento/desempenho crítico dos estudantes e avaliar a efetividade de longo prazo das dimensões socioeducacionais do programa Passos Mágicos.

# 📌 Introdução

A **Associação Passos Mágicos** atua há mais de 30 anos transformando a vida de crianças e jovens em situação de vulnerabilidade social por meio da educação de qualidade, apoio psicossocial e desenvolvimento pessoal.

Para mensurar o desenvolvimento multidimensional dos estudantes, a associação utiliza o **INDE (Índice de Desenvolvimento Educacional)**, composto por diversos pilares:
* **IAN:** Indicador de Adequação ao Nível (nivelamento e defasagem)
* **IDA:** Indicador de Desempenho Acadêmico (notas)
* **IEG:** Indicador de Engajamento (presença e tarefas)
* **IAA:** Indicador de Autoavaliação (percepção própria)
* **IPS:** Indicador Psicossocial (suporte familiar e emocional)
* **IPP:** Indicador Psicopedagógico (avaliação de aprendizagem)
* **IPV:** Indicador de Ponto de Virada (autonomia e transformação)

Neste contexto, o uso de **Data Analytics** e **Machine Learning** oferece uma abordagem preditiva para mapear antecipadamente alunos que necessitam de intervenção pedagógica preventiva, validando o impacto transformador do programa ao longo dos anos.

---

# ❓ Análise Guiada pelas 10 Perguntas dos Indicadores

Em substituição a análises genéricas, a exploração dos dados foi estruturada para responder às **questões centrais** sobre o desenvolvimento multidimensional dos alunos:

---

### 1️⃣ Adequação do Nível (IAN)
**Pergunta:** *Qual o perfil geral de defasagem e nivelamento dos alunos ao ingressar e evoluir no programa?*  
**Achado:** Permite identificar a proporção de alunos que iniciam com defasagem escolar e como o suporte educacional reduz o hiato de aprendizado ao longo das fases.

---

### 2️⃣ Desempenho Acadêmico (IDA)
**Pergunta:** *Como evoluem as notas acadêmicas médias por ano de exercício e por classificação de Pedra?*  
**Achado:** Demonstra uma trajetória ascendente consistente do IDA à medida que o aluno progride do estágio Quartzo até o Topázio.

---

### 3️⃣ Engajamento nas Atividades (IEG)
**Pergunta:** *Qual a relação entre o engajamento (IEG) com o desempenho acadêmico (IDA) e o Ponto de Virada (IPV)?*  
**Achado:** O engajamento é a variável de maior impacto direto: alunos com alto IEG apresentam desempenho acadêmico superior e maior alcance do Ponto de Virada.

---

### 4️⃣ Autoavaliação do Aluno (IAA)
**Pergunta:** *Existe discrepância entre a percepção própria do aluno (IAA) e o seu desempenho real (IDA)?*  
**Achado:** A análise do viés de autoavaliação ($IAA - IDA$) revela que alunos em fases iniciais tendem a superestimar seu desempenho, enquanto fases avançadas apresentam autoavaliação mais alinhada à realidade.

---

### 5️⃣ Aspectos Psicossociais (IPS)
**Pergunta:** *Quais padrões psicossociais influenciam diretamente o rendimento do estudante?*  
**Achado:** O suporte familiar e a estabilidade emocional mensurados pelo IPS funcionam como uma base sustentadora para o aproveitamento acadêmico.

---

### 6️⃣ Aspectos Psicopedagógicos (IPP)
**Pergunta:** *Como a avaliação psicopedagógica (IPP) se relaciona com o nível de adequação (IAN)?*  
**Achado:** A matriz de densidade demonstra que dificuldades psicopedagógicas diagnosticadas no IPP coincidem com níveis mais baixos de adequação acadêmica.

---

### 7️⃣ Ponto de Virada (IPV)
**Pergunta:** *Quais fatores possuem maior correlação com o alcance do Ponto de Virada pelo estudante?*  
**Achado:** O IEG (Engajamento) e o IDA (Desempenho) são os principais impulsionadores para que o aluno atinja a autonomia e a transformação de vida representadas pelo IPV.

---

### 8️⃣ Multidimensionalidade (Composição do INDE)
**Pergunta:** *Como a combinação dos pilares (IDA + IEG + IPS + IPP) estrutura a nota global (INDE)?*  
**Achado:** Através do gráfico de coordenadas paralelas, comprova-se que o equilíbrio entre desempenho, engajamento e aspecto emocional é indispensável para altas notas do INDE.

---

### 9️⃣ Análise Preditiva de Risco
**Pergunta:** *É possível prever com antecedência quais alunos possuem alta probabilidade de desengajamento ou desempenho crítico?*  
**Achado:** O modelo treinado classifica os estudantes em faixas de risco (🚨 Alto, ⚠️ Médio, ✅ Baixo), viabilizando planos de ação preventivos antes do término do ano letivo.

---

### 🔟 Efetividade do Programa e Impacto de Longo Prazo
**Pergunta:** *A jornada longitudinal do aluno pelas Pedras (Quartzo ➔ Ágata ➔ Ametista ➔ Topázio) comprova a efetividade da instituição?*  
**Achado:** A análise longitudinal confirma a elevação progressiva de todos os indicadores conforme o tempo de permanência e avanço de fase, atestando o sucesso do impacto socioeducacional.

---

## 🤖 Resumo dos Modelos e Metodologia

### 🔄 Pipeline de Machine Learning
1. **Tratamento e Persistência:** Limpeza e estruturação de dados em formato de alta performance (`.parquet`).
2. **Engenharia de Atributos:** Criação de variáveis agregadas e normalização das dimensões do INDE.
3. **Divisão e Validação:** Separação estratificada entre conjuntos de treino e teste.
4. **Treinamento do Modelo:** Implementação de algoritmo de classificação otimizado via `scikit-learn`.
5. **Exportação do Artefato:** Salvamento do modelo e pré-processadores em arquivo `.pkl` para inferência em tempo real no Streamlit.

---

### 📊 Modelo Escolhido
O **Random Forest Classifier** foi selecionado para a predição da probabilidade de risco dos alunos pelas seguintes razões:

1. **Robustez contra Overfitting:** A combinação de múltiplas árvores de decisão garante boa generalização para novos dados de alunos.
2. **Capacidade de Capturar Relações Multidimensionais:** O algoritmo lida com perfeição com a interação complexa entre os pilares (como a relação não-linear entre engajamento, aspecto psicossocial e nota final).
3. **Interpretabilidade via Feature Importance:** Permite identificar com clareza quais indicadores (ex: IEG ou IPP) mais contribuem para o risco do estudante.

---

### 🛠️ Tecnologias e Bibliotecas Utilizadas
* **Manipulação e Análise de Dados:** `Pandas`, `NumPy`, `PyArrow`
* **Visualização:** `Plotly Express`, `Seaborn`, `Matplotlib`
* **Machine Learning & Pipeling:** `scikit-learn`
* **Dashboard e Interface:** `Streamlit`

---

## 🏁 Conclusão

A realização deste estudo consolidou a aplicação de **Data Analytics** e **Machine Learning** voltada ao impacto social real. A combinação das **10 perguntas analíticas** com o modelo preditivo integrado ao **Streamlit** fornece à **Associação Passos Mágicos** uma ferramenta de gestão pedagógica preventiva e baseada em evidências.

Como principais aprendizados e impactos, destacam-se:
- A comprovação estatística da efetividade da jornada do aluno através das Pedras;
- A identificação do **Engajamento (IEG)** como o principal catalisador do sucesso do estudante;
- O fornecimento de um painel interativo de apoio à decisão para a equipe psicopedagógica.

---

### 🚀 Próximos Passos

1. **Monitoramento Continuo:** Integração automatizada da base do Streamlit com novos ciclos de avaliação.
2. **Alertas Automáticos:** Envio prévio de relatórios para a equipe pedagógica sobre alunos sinalizados em **🚨 Alto Risco**.
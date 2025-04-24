# Ensuring ESG Integrity in Carbon Markets through Llama 3 and Apache Spark

## Team 1

**Members:** Anne Hackman, Apurva Baru, Fnu Aastha, Sameeksha Mohan, Shang-Chien Wang, and Qirui Zheng

> This project repository is created in partial fulfillment of the requirements for the Big Data Analytics course offered by the Master of Science in Business Analytics program at the Carlson School of Management, University of Minnesota.

## Executive Summary

This project focuses on detecting greenwashing and other potentially fraudulent activities in carbon credit transactions through the AI-driven analysis of both structured and unstructured carbon credit and offset data. As carbon credits are increasingly traded in global markets, the prevalence of fraudulent practices poses significant risks to market integrity. By leveraging Llama 3 for natural language processing-based fraud flagging and Apache Spark for high-performance anomaly detection, with insights summarized in a lightweight dashboard, this project contributes directly to the evolution of trustworthy, data-driven ESG frameworks. The resulting business insights can be utilized by a broad set of stakeholders dedicated to upholding transparency and accountability in carbon markets, including regulatory authorities, businesses concerned with their environmental impact, and environmental NGOs and advocacy organizations.

## Business Value

The Gartner Hype Cycle for Sustainability identifies Carbon Accounting and Management Software as a key emerging technology, expected to mature within the next 5–10 years. This reflects an urgent need for tools that not only track carbon flows but also ensure compliance and prevent fraud.

<img width="651" alt="Hype cycle" src="https://github.com/user-attachments/assets/7525f2a8-98b2-48d5-b77e-0adbd38d624c" />

## Target Audience

This project is tailored for a broad set of stakeholders dedicated to upholding transparency and accountability in carbon markets.
* **Regulatory authorities** tasked with ensuring the integrity of carbon credit systems, who can leverage these tools for early detection of fraudulent activities.
* **Businesses engaged in carbon credit trading**, including corporations pursuing net-zero goals, stand to benefit significantly—as ensuring ESG integrity is increasingly becoming a top strategic priority for companies across industries. The ability to validate carbon transactions and avoid reputational or regulatory risks is essential in today’s sustainability-driven landscape.
* **Environmental NGOs and advocacy organizations** will find value in the project’s potential to promote responsible climate action.
* **Data and technology teams** building sustainability analytics solutions can draw on this work to enhance the scalability and reliability of their ESG data infrastructure.

## Data Sources

[Voluntary Registry Offsets Database](https://gspp.berkeley.edu/research-and-impact/centers/cepp/projects/berkeley-carbon-trading-project/offsets-database)

This structured dataset was compiled by researchers at the Berkeley Carbon Trading Project, located at the University of California,   Berkeley, and is licensed for use under a Creative Commons Attribution ([CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)) license. Each record represents a carbon offset project and its related credit issuances and credit retirements as collected from four voluntary offset project registries: the American Carbon Registry (ACR), Climate Action Reserve (CAR), Gold Standard, and Verra (VCS). The dataset contains 10,145 records measured across 152 variables, including both numerical and categorical information on each carbon offset project.

[Verra Registry](https://registry.verra.org/)

We used a web scraping tool to extract project description data from downloadable, publicly available carbon credit project PDF reports on the Verra Registry, a globally recognized voluntary carbon registry. This textual data was sent to our LLM to semantically score project descriptions and highlight vague claims.

## Tools Required

* Apache Spark
*  Web scraper API
*  Azure Storage
*  PySpark ML
*  OpenAI
*  Llama
*  Streamlit

## Project Workflow

<img width="594" alt="Project workflow" src="https://github.com/user-attachments/assets/f5c10d61-6255-421f-8f5d-4872ab66b1bd" />

## Project Documents

[Project Flier](https://www.canva.com/design/DAGlgt5IFps/XJnwYmskxM8jsDW_ghUNLg/edit)

Dashboard Prototype (link TBD)

Instructions (document TBD)

[Annotated Bibliography](https://docs.google.com/document/d/1REVrUjHongVOkwz-I0pRcb2i8T3ePSUY-lCRz3s1-EU/edit?usp=sharing)

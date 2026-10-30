# First Call

First Call helps a South Australian family get ready for their first call to My Aged Care
when an older person they love needs help at home. It turns a worried, messy paragraph into a
plain-English plan, using real numbers for the family's own region.

## What it does

A family member (a son, daughter, partner or neighbour) picks one of South Australia's
11 aged care planning regions and describes, in their own words, what is going on.

Each time, Python looks up that region's real figures (services, people living alone, people
needing help with core activities) and sends them to Gemma together with a short block of
verified Support at Home facts. Gemma only writes: it turns the family's words into aged-care
terms, explains their region's numbers, lists what usually happens next, and gives a checklist
and three questions to ask the assessor. It is told never to invent numbers, costs, waiting
times or eligibility rules.

Two safety checks run in plain Python, whatever Gemma says: emergency phrases such as
"can't get up" or "chest pain" show a red "call 000" box, and mentions of the NDIS or
disability show a pointer to ndis.gov.au. The plan can be downloaded as a Markdown file.

## The model

- **Model:** Gemma 4, `gemma-4-26b-a4b-it`, through the Gemini API
- **Licence:** [Apache 2.0](https://ai.google.dev/gemma/apache_2)

## Data

| Dataset | Source | Licence | Credit line |
| --- | --- | --- | --- |
| A3 My aged care region (ACPR) supplementary tables 2024-25 | [Australian Institute of Health and Welfare, GEN Aged Care Data](https://github.com/klimhawk/h4h-adelaide-2026/tree/main/data/1_health/A3_my-aged-care-region-tables) | CC BY 4.0 | Source: Australian Institute of Health and Welfare, GEN Aged Care Data, My aged care region supplementary tables 2024-25 (CC BY 4.0). We filtered and summarised this data. |
| Support at Home program facts (summarised by hand in `src/prompts.py`) | Australian Government Department of Health, Support at Home guidance, October 2025 | © Commonwealth of Australia | Source: Australian Government Department of Health, Support at Home guidance, October 2025. |

We use Table 1 (population characteristics) and Table 2.1 (number of services) for the 11 SA
regions only. The figures are from 2024-25, before Support at Home began on 1 November 2025.

## AI tools we used

- **Claude Code:** checked the repo against the organiser template, downloaded the data,
  wrote the data preparation script, the Gemma call, the Streamlit app, the test cases and
  this README, and ran the tests. The team wrote the brief, the prompt text and the facts.
- **Gemma 4:** writes each family's plan inside the app.

## How to run it

1. Install: `pip install -r requirements.txt`
2. Get a free Gemini API key from [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
   and put it in a file called `.env` in this folder (it is already in `.gitignore`):
   `GEMINI_API_KEY=your-key`
3. Build the region data: `python src/data_prep.py`
4. Start the app: `streamlit run app.py`

Optional: `python tests/run_cases.py` runs four example families through Gemma, and
the sidebar's offline mode uses a local Gemma through [Ollama](https://ollama.com)
(`ollama pull gemma4`).

## Team

[Your names, if you want them here.]

## Licence

MIT: see [LICENSE](LICENSE).

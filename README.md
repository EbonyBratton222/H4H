<!--
README template for your Hack for Humanity Adelaide project.

How to use it: open your own repo's README.md, click the pencil, paste this in, and replace
the text in [square brackets]. These notes in arrows do not show on the page.

Sections marked "Checked for a challenge" are what the organisers check before the demos.
Everything else is advice: keep what helps your team, cut what does not.
-->

# H4H

[One or two sentences: what your app does and who it helps.]

<!-- Reference only (do not copy its code): https://github.com/klimhawk/h4h-adelaide-2026/blob/main/worked-example/README.md -->

## What it does

[What a person does in your app, and what Gemma does for them each time.]

## The model

<!-- Checked for a challenge: Best Use of Gemma 4 and both open-source challenges. -->

- **Model:** Gemma 4, `gemma-4-26b-a4b-it`, through the Gemini API
- **Licence:** [Apache 2.0](https://ai.google.dev/gemma/apache_2)

## Data

<!-- The data licences ask you to credit the source. Our data guide has a credit line
     for every dataset: put it here and on your final slide. -->

| Dataset | Source | Licence | Credit line |
| --- | --- | --- | --- |
| [name] | [publisher, with a link] | [for example CC BY 4.0] | [from the data guide] |

## How CoCo helped

<!-- Checked for the Snowflake challenge. Delete this section if you are not entering it. -->

- **Snowflake Marketplace dataset:** [its name]
- **What CoCo did:** [for example: found the dataset, explained it, wrote the queries]
- **CoCo's answers and our queries:** [link to the folder in this repo], with account names removed

## AI tools we used

[The AI coding tools you used and what each one did.]

## How to run it

1. Install: `pip install -r requirements.txt`
2. Get a free Gemini API key from [aistudio.google.com/apikey](https://aistudio.google.com/apikey),
   paste it into `sample.env`, then rename that file to `.env`:
   `GEMINI_API_KEY=your-key`
3. Check the key works: `python hello_gemma.py`

## Team

[Your names, if you want them here.]

## Licence

<!-- Checked for a challenge: both open-source challenges. -->

MIT: see [LICENSE](LICENSE).

# Terminal commands

### 1. Pre-requisites

- `mkdir yle_scraper`

- `cd yle_scraper`

- `python3 -m venv venv`

- `source venv/bin/activate`

- `pip install openai pandas selenium matplotlib numpy scipy wordcloud`

- `export OPENAI_API_KEY="YOUR_API_KEY"`

### 2. Scrape Yle

- `python yle_scraper.py`

### 3. Manually add missing data (e.g. date, content, header)

### 4. Analyse sentiment and theme

- `python analyse.py`

### 5. Analyse word counts

- `python wordcounts.py`

### 6. Manually delete redundant articles

### 7. Perform logistic linear regression (lra)

- `python cleaned_data_lra.py`
- `python logistic_regression.py`

### 8. Visualise results

**Relative graph**
- `data_for_relative_graph.py`
- `python stackedarea.py`
- image

**Absolute graph**
- `python absolutegraph.py`
- image
 
**Wordcloud**
- `python extract_wordcloud.py`
- `python create_wordcloud.py`
- image

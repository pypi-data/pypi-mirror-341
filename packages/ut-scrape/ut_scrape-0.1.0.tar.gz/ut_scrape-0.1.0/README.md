# ut-scrape

`ut-scrape` is a lightweight REST API built using [Reflex](https://reflex.dev/) that leverages the functionality of the [`untappd-scraper`](https://gitlab.com/wardy-mini-projects/portfolio/untappd-scraper) library. It enables users to scrape data from Untappd and access it via a simple API interface.

## Features

- **Data Scraping**: Utilizes `untappd-scraper` to fetch and parse data from Untappd.
- **REST API**: Exposes the scraped data through a Reflex-powered REST API.

## Requirements

- Python >= 3.13
- `untappd-scraper` >= 0.6.2
- `reflex` >= 0.7.6

## Installation

```bash
pip install ut-scrape
```

## Usage

Run the API server:

```bash
python -m ut_scrape
```

Access the API endpoints to retrieve data scraped from Untappd.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

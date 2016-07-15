# Machine Enrichments

This repository is an implementation of the [Enrichment API](https://github.com/beeldengeluid/labs-enrichment-api). It provides machine based capabilities for data enrichment (as opposed to crowd based data enrichment provided by [CrowdTruth](https://github.com/CrowdTruth/CrowdTruth).

## Currently implemented enrichment services
 - [NERD](http://nerd.eurecom.fr/)

## How to run it
From the src/ folder, install required Python dependencies:

```
$ pip install -r requirements.txt
```

Create and edit `settings.py` configuration file (you can use `settings-example.py` as a starting point. Provide your relevant API keys in this file.

Now you are ready to run your Machine Enrichments service:

```
$ python app.py -p 8081
```

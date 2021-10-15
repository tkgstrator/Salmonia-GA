# Salmonia for GitHub Actions

## Requirement

- iksm_session
- api_token

### How to get tokens

#### iksm_session

[Salmonia](https://github.com/tkgstrator/Salmonia) generate a setting configuration file as `config.json` including `iksm_session` and `api_token`.

#### api_token

Register in [Salmon Stats](https://salmon-stats.yuki.games/) by twitter account and get api_token in settings.

## Installation

Fork this repository and set environment variables as known as `Secrets`.

### Secrets

| Key            | Value   | Description                | 
| :------------: | :-----: | :------------------------: | 
| IKSM_SESSION   | String  | iksm_session               | 
| API_TOKEN      | String  | api_token for Salmon Stats | 
| EMAIL          | String  | GitHub Account's           | 
| USERNAME       | String  | GitHub Account's           | 
| LATEST_JOB_NUM | Integer | 0                          | 

### Enable GitHub Actions

In forked repository, GitHub Actions are disalbed by default, so you should enable it in the settings.

# juntagrico-crowdfunding

[![.github/workflows/juntagrico-ci.yml](https://github.com/juntagrico/juntagrico-crowdfunding/actions/workflows/juntagrico-ci.yml/badge.svg?branch=main&event=push)](https://github.com/juntagrico/juntagrico-crowdfunding/actions/workflows/juntagrico-ci.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/f72b9766dceba7c8bee4/maintainability)](https://codeclimate.com/github/juntagrico/juntagrico-crowdfunding/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/f72b9766dceba7c8bee4/test_coverage)](https://codeclimate.com/github/juntagrico/juntagrico-crowdfunding/test_coverage)
[![image](https://img.shields.io/github/last-commit/juntagrico/juntagrico-crowdfunding.svg)](https://github.com/juntagrico/juntagrico-crowdfunding)
[![image](https://img.shields.io/github/commit-activity/y/juntagrico/juntagrico-crowdfunding)](https://github.com/juntagrico/juntagrico-crowdfunding)


Create crowdfunding campaigns in juntagrico.

This is an extension for juntagrico. You can find more information about juntagrico here
(https://github.com/juntagrico/juntagrico).


## Installation

Install juntagrico-crowdfunding via pip
`pip install juntagrico-crowdfunding`

or add it to your django project's `requirements.txt`:
`juntagrico-crowdfunding`

In your `juntagrico.settings.py` add `juntagrico_crowdfunding` somewhere **above** `juntagrico`:
```python
INSTALLED_APPS = (
    'juntagrico_crowdfunding',
    'juntagrico',
    ...
```

And add this middleware:

```python
MIDDLEWARE = [
    ...
    'juntagrico_crowdfunding.middleware.FunderAccess'
]
```

In your urls.py you also need to add the new pattern:
```python
urlpatterns = [
    ...
    path('',include('juntagrico_crowdfunding.urls')),
]
```

Run `python manage.py migrate` to create the required databases.

## Configuration

Set these in your `settings.py` to modify `juntagrico-crowdfunding`

### VOCABULARY

(added keys to the existing juntagrico setting)

default value:

```python
{
    'funding_project': 'Unterstützungs-Projekt',
    'funding_project_pl': 'Unterstützungs-Projekte'
}
```

### EMAILS

Sets the email templates
(added keys to the existing juntagrico setting)

default value:
  
```python
{
    'fund_confirmation_mail': 'cf/mails/fund_confirmation_mail.txt',
}
```

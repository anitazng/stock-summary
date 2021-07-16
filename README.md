# Stock Email Summary

## Description

A simple program that sends you an email summary of your investment portfolio performance. Provides current profit/loss percentage of each position in your portfolio, the daily P&L, and your total P&L for the day.

Uses Outlook and Questrade account.

## Usage

Install Questrade API Wrapper.

```
pip install questrade-api
```

Register a personal app in your Questrade account and generate a new token for manual authorization. Copy this token and replace

```
q = Questrade()
```

with

```
q = Questrade(refresh_token='your_refresh_token_here')
```

on your first run of the program. For subsequent executions, the refresh token will not be required again.

Schedule the program to run daily using Task Scheduler for Windows or CRON on Mac OS.



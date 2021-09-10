# Solana Cord

[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://img.shields.io/github/license/jaloo555/solana-cord)
[![Version](https://badge.fury.io/gh/tterb%2FHyde.svg)](https://badge.fury.io/gh/tterb%2FHyde)
[![PR's Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat)](http://makeapullrequest.com)  

## Overview

Solana Cord is an implementation of Solana's JSON RPC API, wrapped for discord bots - meaning all features can be customized to your liking. Currently, this bot supports Solana Epoch tracking and custom settings for epoch updates. This project is meant to be a _self-hosted bot_, but you can contact me and we can work together to set it up.

Currently, the RPC wrapper supports multiple API methods that are useful for discord bots/members. However, the wrapper is _modular_ by nature and easily expandable. Feel free to build on top of it. There's also an additional sample discord bot code that allow you to customize for your own server. The bot currently supports epoch tracking and notification updates when a staking cycle is about to end.

#### Features - JSON RPC API Wrapper

- getBlock
- getBlockHeight
- getBlockTime
- getEpochInfo
- getEpochSchedule
- getLeaderSchedule
- getInflationRate

#### Features - Sample bot

- Epoch Tracking Information
- Notification when an epoch is about to end (1 hour)

## Demo

![epoch_demo](https://imgur.com/a/Itcj89B)

## Installation

Installation is **very easy**. Simply follow the procedures listed below:

```bash
git clone https://github.com/jaloo555/solana-cord.git
pip install -r requirements.txt
```
Configuration:
> The bot extracts configuration information from /config/options.ini, add a discord bot account token under credentials to get started.

To run:
```bash
python3 run.py
```


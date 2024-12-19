# A Data-Driven Assessment of Political Messaging: Experimental Evidence from the 2024 US Elections

This is a preliminary release of the code and data associated with the research paper **"A Data-Driven Assessment of Political Messaging: Experimental Evidence from the 2024 US Elections"**.

**Authors**: Yi-Yun Chu, Uttara M Ananthakrishnan, Ramayya Krishnan, and Ananya Sen

**Website**: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5057627

---

## Overview

This repository contains the code and methodologies used to sign up for and interact with political campaigns during the 2024 U.S. election cycle. It provides researchers with tools to investigate how political candidates personalize email content. The repository is organized into the following components:

- **`email-signup/`**: Contains tools and scripts for automating email list signups from political campaign websites.
  - **`signup_multithread.py`**: Executes multithreaded email signups to collect emails from various campaign websites.
  - **`driver_setup.py`**: Configures the Chrome WebDriver environment for automating browser actions during the signup process.
  - **`vpn_automate.py`**: Automates VPN connectivity using Private Internet Access (PIA) to ensure privacy and location diversity during email signups.  

- **`email-interact/`**: Provides scripts to automate engagement and interactions with campaign emails
  - **`interaction_open.py`**: Simulates user behavior by opening email messages.  
  - **`interaction_open_click.py`**: Simulates user interactions by clicking links or buttons in the emails.  

---

## Dataset

The dataset includes over 1.2M emails collected during the 2024 U.S. election cycle. These emails were collected through automated sign-ups and manual curation of political campaign mailing lists. The dataset includes key metadata (e.g., sender, recipient demographics, engagement behaivors, subject, and timestamps) and the full content of email messages.

The dataset is available upon request [here](https://forms.gle/QREVy9qG8G34x8X1A).

---

## Citation

If you use this code or data in your research, please cite:

> Yi-Yun Chu, Uttara M Ananthakrishnan, Ramayya Krishnan, and Ananya Sen. A Data-Driven Assessment of Political Messaging: Experimental Evidence from the 2024 US Elections. Available at SSRN 5057627 (2024).
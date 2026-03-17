#!/usr/bin/env bash
# exit on error
set -o errexit

# ૧. પાયથોન લાઈબ્રેરી ઇન્સ્ટોલ કરો
pip install -r requirements.txt

# ૨. Playwright અને તેના માટે જરૂરી સિસ્ટમ ફાઈલો ઇન્સ્ટોલ કરો
playwright install --with-deps chromium

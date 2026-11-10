# Templates for statur-lead-gen-ads

Part of Lead generation ads: the Meta and TikTok playbook (https://statur.co/lead-generation-ads/), recipe 07.

## lead-sheet-template.csv

One row per lead. Import it in Google Sheets (File > Import > Upload, "Replace spreadsheet"), rename the tab `leads`, delete the TEST row. Columns A to T: name, email, phone, company, the three form answers (qualify, pitch, play), owner, status, next step, notes, created, first call, source, organic, campaign, ad set, ad, consent, platform lead ID. The row number is the lead's ID everywhere (contact name, alert, calls: "call row 83").

## make-lead-router.blueprint.json

A Make scenario for Facebook Lead Ads (swap the trigger for TikTok Lead Forms "Watch Leads" or a webhook):

1. Trigger: Facebook Lead Ads, new lead.
2. Clean the name, the email (lower case) and the phone (digits only).
3. Search the sheet by email, then by the last 9 digits of the phone.
4. Router: absent, add a row; present, add nothing.
5. Search again to read the row number, then search Google Contacts.
6. Create the contact "83 Jane Doe" or tag the existing contact with its row number.
7. Internal alert email with the row number and a link to the row.

Import: in Make, create a scenario, open the three-dot menu, Import Blueprint, pick the file. Then reconnect each module to your own accounts, replace YOUR_SPREADSHEET_ID and YOUR_ALERT_EMAIL, and map the MAP_* placeholders to your form questions. Test with Meta's Lead Ads Testing Tool before spending. Lessons from real runs: a Google Sheets search with no result still returns a bundle, so test `first(map(array; "row"))` with exist / notexist; always pass `organization {name}` to Google Contacts; run the scenario in non-sequential mode so one failed run does not block the next leads.

The welcome email and the follow-up sequence are better in your email tool or CRM; the skill drafts them (recipe 08).

---
name: statur-trades-admin
description: Write one-page processes for the paperwork of a trades business (quote request, quote follow-up, invoicing, late payment) by interviewing the owner one question at a time, then prepare the handover to a reliable human assistant who follows them and makes reminders by phone. Use when an electrician, plumber, installer or builder asks to organize quotes, invoices and payment reminders, write an admin procedure, or hire someone for the paperwork.
license: MIT
metadata:
  author: Dr. Louis Korczowski
  version: "2.0.0"
  playbook: https://statur.co/tradespeople-video-handbook/
  repository: https://github.com/lkorczowski/content-strategist-AI-cookbook
---

# Trades admin process

Part of The One-Hour Video Handbook for Tradespeople (https://statur.co/tradespeople-video-handbook/). Read https://statur.co/tradespeople-video-handbook.md for the full method and its sources when you can open links.

The job: get the paperwork out of the tradesperson's head and onto four one-page processes that a reliable person can follow. Paperwork needs reliability more than speed, so a human runs it with a written process and the assistant helps write and improve the pages. Customers accept a payment reminder from a person better than from a machine, and an assistant who picks up the phone closes the loop.

## What to ask for

If the workspace has a company context file (kb/01_BRAND.md from the blueprint, or .agents/product-marketing.md), read it first and ask only for what is missing.

Interview the user one question at a time, in short plain words. Stop when a process is complete enough to be followed by someone new, then move to the next one.
- How quote requests arrive today (phone, email, website form, messages) and who answers.
- What a quote needs before it can be sent (visit, photos, measurements, prices from suppliers), and how long it takes.
- When and how the user follows up a quote that got no answer.
- How invoices are made and sent, and with which tool (software, template, accountant).
- When an invoice counts as late, and what happens then.
- Which of these steps the user wants to keep, and which an assistant could do.

## The four processes

Each one fits on one page and follows the same shape: trigger, steps with who does what, the delay for each step, the message to use, when to call the owner, and where it is logged.
1. Quote request. From the first contact to a scheduled visit or a clear "not for us". Collect the same information every time: name, town, job, photos, urgency, best time to call.
2. Quote follow-up. From the quote sent to a yes or a no. Fixed reminder dates, one call before the last reminder, and a clear end: the quote is closed and logged.
3. Invoicing. From the job finished to the invoice sent the same day or the next. Checklist of what each invoice must contain, checked with the accountant for the user's country.
4. Late payment. From the due date to payment. Friendly reminder, phone call by the assistant in their own name, written reminder, then the step the owner decides (accountant, lawyer or formal notice). Every step dated and logged.

## Method

1. Interview for one process at a time, starting with the one that loses the most money today (often quote follow-up or late payment).
2. Write the page in the shape above. Use the user's own words and real delays. Missing information: write [to decide] and ask.
3. Write the ready-to-use messages for each step: email, text message and a short phone script. Polite, short, with one clear next step.
4. Read the page back to the user as if you were the new assistant, and list every point where you would have to guess. Fix them.
5. Prepare the handover:
   - The profile to hire: someone who likes clear, repetitive admin work.
   - The working rule: the collaboration continues as long as the process is followed.
   - A first-week plan: read the four pages, shadow one quote and one invoice, then run them alone with a weekly review.
   - The assistant makes customer reminders by phone, in their own name.
6. Improve monthly: ask the assistant and the owner what broke, update the page and date the change.

## Pitfalls to flag

- A process that lives in the owner's head.
- Reminders with no fixed dates.
- An invoice sent days after the job.
- Legal mentions or late-payment penalties copied from the internet without checking with the accountant.
- An assistant hired before the pages exist.

## Output

```
PROCESS · <quote request | quote follow-up | invoicing | late payment> · <business> · version <date>
Trigger: <what starts it>
Owner of the process: <assistant | owner>
Steps:
1. <action> | who: <role> | delay: <from the user> | message: <name of template>
2. ...
Call the owner when: <cases>
Logged in: <tool or sheet the user named>
Messages:
- <template name>: <email, text or phone script>
To decide: <open points marked [to decide]>
To check with the accountant: <legal mentions, penalties, deadlines>
```

## Rules

- Drafts only. Never send an email, a text message, an invoice or a reminder for the user, and never call anyone. The user or their assistant sends.
- Never ask for a password, bank details or customer payment data, and never sign in for the user. Respect the terms of use of each tool.
- No promised results. No invented numbers: never invent a delay, a price, a penalty rate or a legal rule. Every figure comes from the user or a source the user can open.
- Legal, tax and payment-collection points are information only. Ask the user to confirm them with their accountant or a lawyer for their country.
- Flag confidential information (customer names, amounts owed, disputes) and keep it out of shared templates.
- Companion skills: statur-trades-video, statur-trades-setup, statur-trades-morning-routine.

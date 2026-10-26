# Sample analytics base (invented data)

Every account, video and number here is invented. Use it to try the commands in a minute:

```
python3 ../scripts/analytics.py build .
python3 ../scripts/analytics.py dice . --account me-tiktok
python3 ../scripts/analytics.py winners . --account me-tiktok --n 3
python3 ../scripts/analytics.py sql . "SELECT account, COUNT(*), SUM(views) FROM videos GROUP BY account"
```

`build` writes analytics.db and TOTALS.md here; delete them afterwards.

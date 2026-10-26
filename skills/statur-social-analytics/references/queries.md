# Questions to ask your analytics base

Run any of these with `python3 scripts/analytics.py sql <dir> "<query>"`, or let your AI write its own SQL on the views described in references/schema.md. Mature data only for verdicts: at least 7 days live and 1,000 views, unless the account is smaller.

Which videos crossed 100k views in their first 7 days?
```sql
SELECT account, video_id, posted, views_d7, views, caption FROM videos
WHERE views_d7 >= 100000 ORDER BY views_d7 DESC;
```

How did each month of publishing do, per account?
```sql
SELECT account, substr(posted, 1, 7) AS month, COUNT(*) AS videos, SUM(views) AS views,
       SUM(views >= 100000) AS over_100k
FROM videos GROUP BY account, month ORDER BY account, month;
```

How many views did the account earn in each calendar month (all videos, old ones included)?
```sql
SELECT account, substr(date, 1, 7) AS month, SUM(views) AS views, MAX(followers) AS followers_end
FROM daily GROUP BY account, month ORDER BY account, month;
```

Which formats keep people at 3 seconds, and do they also get saved?
```sql
SELECT f.format, COUNT(*) n, ROUND(AVG(v.ret_3s_pct), 1) ret_3s, ROUND(1000.0 * SUM(v.saves) / SUM(v.views), 1) saves_per_1k
FROM videos v JOIN formats f USING (video_id)
WHERE v.days_live >= 7 AND v.views >= 1000 GROUP BY f.format ORDER BY ret_3s DESC;
```

Does length help or hurt, per format?
```sql
SELECT f.format, CASE WHEN length_s < 30 THEN 'a <30s' WHEN length_s < 60 THEN 'b 30-60s' WHEN length_s < 120 THEN 'c 1-2min' ELSE 'd 2min+' END AS length,
       COUNT(*) n, CAST(AVG(views) AS INTEGER) avg_views
FROM videos v JOIN formats f USING (video_id) WHERE days_live >= 7 GROUP BY 1, 2 ORDER BY 1, 2;
```

Where do viewers drop on my last viral video (second by second)?
```sql
SELECT second, pct_remaining FROM retention WHERE video_id = '<id>' ORDER BY second;
```

How does a watched account compare with mine this month?
```sql
SELECT a.relation, v.account, COUNT(*) videos, CAST(AVG(v.views) AS INTEGER) avg_views, MAX(v.views) top
FROM videos v JOIN accounts a ON a.key = v.account
WHERE v.posted >= date('now', '-30 day') GROUP BY v.account ORDER BY avg_views DESC;
```

Which videos did a competitor post that beat their own median by 3x (formats worth studying)?
```sql
WITH m AS (SELECT account, AVG(views) avg_v FROM videos GROUP BY account)
SELECT v.account, v.video_id, v.posted, v.views, ROUND(v.views / m.avg_v, 1) x_avg, v.caption
FROM videos v JOIN m USING (account) JOIN accounts a ON a.key = v.account
WHERE a.relation = 'watch' AND v.views >= 3 * m.avg_v ORDER BY x_avg DESC;
```

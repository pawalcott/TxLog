# Tx Field Log

Phone app for the transmitter crew: for each transmission, the pole station plus the start and end time (UTC, from the
phone clock), and optionally the current and a note. It works offline and keeps the log on the phone until you start a
new day.

## Files

| File | What |
|---|---|
| `txlog_app.html` | the app (edit this one) |
| `build.py` | makes `app/` from it: `python TxLog/build.py` |
| `app/` | the installable copy: `index.html`, `manifest.webmanifest`, `sw.js` (offline), icons |

## On the phone (Android and iPhone)

1. Put the `app` folder on any HTTPS web host (company site, GitHub Pages, ...), or copy it to the phone.
2. Open `index.html` in Chrome (Android) or Safari (iPhone).
3. Add it to the home screen (Chrome menu > Add to Home screen; Safari > Share > Add to Home Screen).
   From an HTTPS host it then runs offline.

## In the field

Set the line, the step between poles and the direction. Tap **Start Tx** when the transmitter comes on at the pole and
**Stop Tx** when it goes off; the station then moves one step. Tap a reading to correct its station, times or current.
**Save / share CSV** sends the day's file, for example by email or to a drive.

## The file

`TxLog_L<line>_<date>.csv`:

```
line,station,start_utc,end_utc,current_a,note
1000,3250,2023-09-30 17:22:00,2023-09-30 17:23:30,1.41,
```

The Inline IP program reads it under **1 Inputs > Tx field log(s)** (several files at once are fine), or on the command
line with `--tx-log`.

# Tx Field Log

Phone app for the transmitter crew: for each transmission, the pole station plus the start and end time (UTC, from the
phone clock), and optionally the current and a note. It works offline and keeps the log on the phone until you start a
new day.

## Files

| File | What |
|---|---|
| `txlog_app.html` | the app (edit this one) |
| `build.py` | makes `app/` and `index.html` from it: `python TxLog/build.py` |
| `app/` | the installable copy: `index.html`, `manifest.webmanifest`, `sw.js` (offline), icons |
| `index.html` | opens `app/`, so the site's own address shows the app |

## On the phone (Android and iPhone)

1. Open **https://pawalcott.github.io/TxLog/** in Chrome (Android) or Safari (iPhone). Any other HTTPS host with
   these files works too.
2. Add it to the home screen (Chrome menu > Add to Home screen; Safari > Share > Add to Home Screen). It then runs
   offline.

## Updating

Edit `txlog_app.html`, run `python TxLog/build.py`, and upload `index.html` and the `app` folder. Phones get the new
build the next time they open the app with a connection (open it twice for a phone that has the first version). The
build date and code show at the bottom of the app.

## In the field

Set the line, the step between poles and the direction, and the **current logger**: the gDAS unit (s/n and channel)
the current clamp is plugged into. It stays set until you change it, so change it when the clamp moves to another unit.
The Inline IP program uses that unit and channel as each reading's transmitter reference. Tap **Start Tx** when the transmitter comes on at the pole and
**Stop Tx** when it goes off; the station then moves one step. Tap a reading to correct its station, times or current.
**Save / share CSV** sends the day's file, for example by email or to a drive.

## The file

`TxLog_L<line>_<date>.csv`:

```
line,station,start_utc,end_utc,current_a,note,logger_sn,logger_ch
1000,3250,2023-09-30 17:22:00,2023-09-30 17:23:30,1.41,,212,1
```

For testing, the program also accepts an existing links workbook with a `Transmitters` sheet (for example a
hand-made `1000Links.xlsx`) instead of the CSV.

The Inline IP program reads it under **1 Inputs > Tx field log(s)** (several files at once are fine), or on the command
line with `--tx-log`.

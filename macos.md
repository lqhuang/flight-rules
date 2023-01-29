---
created: 2023-01-29
updated: 2023-01-29
---

## Configure repeat scheduled power events (`sleep`/`wakeup`/`shutdown`) in macOS 13 Ventura

Ventura (macOS 13) has removed scheduled `sleep`/`wakeup`/`shutdown`, but CLI
interface to set **repeat** scheduled power events is still supported for now.

The usage is

```shell
# man pmset
sudo pmset repeat type weekdays HH:mm:ss
# type - one of sleep, wake, poweron, shutdown, wakeorpoweron
# weekdays - a subset of MTWRFSU ("M" and "MTWRF" are valid strings)
```

For example, if you want your Mac to sleep at 11:30 a.m every weekday, change
the command to:

```sh
sudo pmset repeat sleep MTWRF 11:30:00.
```

Here,

- M: Monday
- T: Tuesday
- W: Wednesday
- R: Thursday
- F: Friday
- S: Saturday
- U: Sunday

Another example for combination of `wakeorpoweron`/`sleep`

```
sudo pmset repeat wakeorpoweron T 12:00:00 sleep MTWRFSU 20:00:00
```

Cancel "repeat" schedules

```sh
sudo pmset repeat cancel
```

Check current scheduled events from cli

```sh
pmset -g sched
```

Or you could find the same info in the app System Information (tab: Hardware ->
Power)

Refs:

- [How to Change macOS Sleep Settings? (Ventura Updated)](https://iboysoft.com/news/how-to-change-macos-sleep-settings.html)
- [Schedule Mac To Shutdown, Sleep, Wake in Ventura (Examples)](https://www.howtoisolve.com/how-to-schedule-mac-turn-on-off-and-sleep-wake/)

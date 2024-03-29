# attendx

Developed for UNC's Comp 411 with Montek Singh.

[![This project is considered stable](https://img.shields.io/badge/status-stable-success.svg)](https://benknoble.github.io/status/stable/)

## What

Track time-stamped attendance

## Why

Any reason you want (like, thwarting cheating)

## How

1. Download and prepare your student data
   - For ease of use, it needs to be semi-colon separated (see [format](#roster-format))
   - If you use Sakai, you can export your roster as CSV and use
     `./bin/sak_to_gen` to put it in the required format
1. Generate your attendx survey `./bin/generate -t "Event title" students.csv > event.html`
   - you can use your own template instead of [template.html](./template.html)
     with the `-i` flag
1. Share `event.html` with all the instructors who need to take attendance
1. Have your instructors tick student names in the HTML
1. Download the CSVs from any instructors who issued the attendx survey
1. Merge your results `./bin/merge_csv result*.csv > final.csv`
1. Suss out those cheaters

### Roster format

```
Name;Student ID
"foobar";123
"bar, foo";456
```

### Tips 'n' tricks

- Use `<final.csv ./bin/stats` to see all the recorded IDs
- Use `<final.csv ./bin/stats dupes` to find duplicates in the merge result,
  indicating someone checked themselves off in two locations (suspicious...)
- Use `<final.csv ./bin/stats count` to count the number of unique students who
  attended
- [`./bin/stats`](./bin/stats) takes `--all` to produce every statistic it knows
  about in one run! (Does not output recorded ids at this time.)
- Sakai users can download assessment data and do `./bin/sakai_stat.py sakai.xls
  merged.csv` for even more information (may need to `pip3 install -r
  ./bin/requirements.txt`)
- **New**: [`./bin/full-report`](./bin/full-report) can be used for a full
  report, combining stats and sakai parsing.

### Generating sheets for a single class

The following script is helpful as a starting point to generate sheets for a
class:

```bash
#! /usr/bin/env bash

set -euo pipefail
current_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

log() {
  printf '%s\n' "$@"
} >&2

usage() {
  cat <<DOG
usage: $0 date
DOG
}

die() {
  local ex="${1:-1}"
  exit "$ex"
}

usage_and_die() { usage && die; }

main() {
  if (($# != 1)) ; then
    usage_and_die
  fi

  local dir=./quizzes/quiz_"$1"
  mkdir "$current_dir"/"$dir"
  "$current_dir"/../bin/generate -t "Quiz $1" "$current_dir"/../data/411-students.csv > "$dir"/quiz.html
}

main "$@"
```

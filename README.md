# attendx

Developed for UNC's Comp 411 with Montek Singh.

[![This project is considered stable](https://img.shields.io/badge/status-stable-success.svg)](https://benknoble.github.io/status/stable/)

## What

Track time-stamped attendance

## Why

Any reason you want (like, thwarting cheating)

## How

1. Download and prepare your student data
  - For ease of use, it needs to be semi-colon separated in the format
```
Name;Student ID
"foobar";123
"bar, foo";456
```
  - If you use Sakai, you can export your roster as CSV and use
    `./contrib/sak_to_gen` to put it in this format
1. Generate your attendx survey `./bin/generate -t "Event title" students.csv > event.html`
  - you can use your own template instead of [template.html](./template.html)
    with the `-i` flag
1. Share `event.html` with all the instructors who need to take attendance
1. Have your instructors tick student names in the HTML
1. Download the CSVs from any instructors who issued the attendx survey
1. Merge your results `$ ./bin/merge_csv result*.csv > final.csv`
1. Suss out those cheaters

### Tips 'n' tricks

- Use `<final.csv ./contrib/stat` to see all the recorded IDs
- Use `<final.csv ./contrib/stat dupes` to find duplicates in the merge
  result, indicating someone checked themselves off in two locations
  (suspicious...)
- Use `<final.csv ./contrib/stat count` to count the number of unique students
  who attended
- `./contrib/stat` takes `--all` to produce every statistic it knows about in
  one run! (Does not output recorded ids at this time.)
- Sakai users can download assessment data and do `./contrib/sakai_stat.py sakai.xls merged.csv`
  for even more information (may need to `pip3 install -r ./contrib/requirements.txt`)
- **New**: `./contrib/full-report` can be used for a full report, combining
  stats and sakai parsing. It makes use of `./contrib/convert_tz`, since some
  browsers output EST as Eastern Standard Time in the time-stamps (??)

### Generating sheets for a single class

The following script is helpful as a starting point to generate sheets for a
class:

```bash
#! /usr/bin/env bash

set -euo pipefail

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

  local top
  local dir=./quizzes/quiz_"$1"
  top="$(git rev-parse --show-toplevel || printf .)"
  mkdir "$top"/"$dir"
  "$top"/bin/generate -t "Quiz $1" "$top"/data/411-students.csv > "$dir"/quiz.html
}

main "$@"
```

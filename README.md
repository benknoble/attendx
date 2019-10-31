# attendx

Developed for UNC's Comp 411 with Montek Singh.

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
1. Generate your attendx survey `$ ./scripts/generate -t "Event title" students.csv > event.html`
1. Share `event.html` with all the instructors who need to take attendance
1. Have your students tick their names in the HTML
1. Download the CSVs from any instructors who issued the attendx survey
1. Merge your results `$ ./scripts/merge_csv result*.csv > final.csv`
1. Suss out those cheaters

### Tips 'n' tricks

- Use `$ <final.csv ./contrib/stat` to see all the recorded PIDs
- Use `$ <final.csv ./contrib/stat dupes` to find duplicates in the merge
  result, indicating someone checked themselves off in two locations
  (suspicious...)
- Use `$ <final.csv ./contrib/stat count` to count the number of unique students
  who attended

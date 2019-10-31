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
2. `$ ./scripts/generate -t "Event title" students.csv > event.html`
3. Have your students tick their names in the HTML
4. Download the CSVs from any instructors who issued the attendx survey
5. `$ ./scripts/merge_csv result*.csv > final.csv`
6. Suss out those cheaters

### Tips 'n' tricks

- Use `$ <final.csv uniq -c | awk '$1 > 1'` to find duplicates in the merge
  result, indicating someone checked themselves off in two locations
  (suspicious...)

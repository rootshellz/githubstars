# githubstars

Quick and dirty scripts for managing started repos.
Born from a need to quickly cleanup a massive numbe of given stars accumulated
over the years.

## Authentication

Each script expects a valid and properly scoped GitHub token to be saved at `.token`.

## Scripts

### get_all_given_stars.py

This script enumerates all repos the user has starred and writes them to `given_stars.json`.

### remove_all_stars.py

This script enumerates all repos the user has starred and removes the star from
each, unless the repo's full name (i.e. `owner/repo`) appears in a
`keep_stars.txt` file (which has one repo fullname per line).

### remove_specified_stars.py

This script reads in a `remove_stars.txt` file, which has one repo fullname
(i.e. `owner/repo`) per line, and removes the user's star from each.

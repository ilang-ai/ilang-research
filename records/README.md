# Records

Verbatim records written by the intake gate (`gate/`), one file per issue.

- `counterexamples/` — reproducible cases against a clause of the canon, SOUL or the Source Book. A counterexample is recorded; it does not change a clause by itself (SPEC-v5.0 MODULE::AMENDMENT, RULE:counterexample).
- `amendments/` — proposed changes with a fix, with the output of every gate and the `::JUDGE{v5.0}` block the judgment layer wrote for the action "merge this".

Nothing in this directory is merged into the canon by a machine. The owner reads it on their own schedule and merges by hand into `ilang-ai/ilang-spec`, where every change goes through that repository's CI and a version DOI.

Files are named `YYYY-MM-DD-issue-N.md`. Logs inside them are not edited.

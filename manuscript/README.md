# Weighted extensions and Mathar's A084261 recurrence

The note resolves Mathar's conjecture in OEIS A084261, FORMULA,
30 November 2012, for every integer n >= 3:

    a(n,t) = sum(binomial(n,2k) k! t^(n-2k), k=0,...,floor(n/2)),
    2a(n,1)-4a(n-1,1)+(2-n)a(n-2,1)+(n-2)a(n-3,1) = 0.

It gives an alternative proof of Jovovic's 2003 exponential generating
function. The weighted factorization is credited to Fang, Hamaker and
Troyka (2020; journal version 2022). Its explicit polynomial recurrence is

    2a(n,t)-4t a(n-1,t)+(2t^2-n)a(n-2,t)+t(n-2)a(n-3,t) = 0.

The moment representation also proves the recorded A161556 row sums,
Hanna's continued fraction, the A137704 Hankel product, and Rousseau's
asymptotic equivalent. The determinant is independent of real t. The
asymptotic formula extends to each fixed real t > 0; at t=0 the exact even
and odd values require a separate formula. The continued fraction is a
formal power series identity, not an analytic convergence assertion.

## Files and build

- `note.tex`: mathematical text with embedded bibliography.
- `note.pdf`: typeset note.
- `verify.py`: dependency-free Python 3 exact finite checker.
- `check-results.json`: expected checker output.
- `metadata.json`: creators, license, problem identity and coverage.
- `LICENSE.txt`: CC BY 4.0 notice.
- `MANIFEST.sha256`: exact file digests.

Build with Tectonic 0.17.0:

```sh
tectonic note.tex
```

Alternatively, run a standard LaTeX installation twice:

```sh
pdflatex -interaction=nonstopmode -halt-on-error note.tex
pdflatex -interaction=nonstopmode -halt-on-error note.tex
```

No BibTeX step is needed because the bibliography is embedded.

## Verification scope

```sh
python3 verify.py --to 880
```

The output equals `check-results.json`. It compares 881 values of the
defining sum and the recurrence, checks 590 weighted integer instances,
118 full polynomial recurrence identities, 120 Appell identities, 305 row
evaluations, 305 continued-fraction moment coefficients and 70 Hankel
determinants. The parity and differential-equation coefficients have
additional exact controls. These checks are finite; universal statements
have the written proofs in `note.tex`, including the asymptotic formula.

For comparison with the public OEIS table, download
https://oeis.org/A084261/b084261.txt and run:

```sh
python3 verify.py --to 880 --oeis-table b084261.txt
```

The declaration `D5.S1.Recurrence.MatharA084261.result` proves the
unweighted recurrence for all natural n >= 3, with the literal inclusive
even-index factorial sum, in this pinned Lean file:
https://github.com/the-omega-institute/trureturing/blob/b0f7c01b01511ea00428c1b6edad5dd2b372eaf8/D5/S1/Recurrence/MatharA084261.lean

The weighted recurrence, generating functions, moment consequences and
asymptotics have written proofs, distinct from that declaration. The
coverage table identifies the additional source items outside the note.

## Creators and license

Haobo Ma (ChronoAI Pte Ltd, Singapore), followed by Wenlin Zhang
(National University of Singapore; ChronoAI Pte Ltd, Singapore).
CC BY 4.0; see `LICENSE.txt`.

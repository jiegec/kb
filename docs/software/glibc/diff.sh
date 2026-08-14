#!/bin/sh
git -C ~/glibc diff glibc-2.31 glibc-2.32 -- malloc/malloc.c > glibc-2.32.diff
git -C ~/glibc diff glibc-2.32 glibc-2.33 -- malloc/malloc.c > glibc-2.33.diff
git -C ~/glibc diff glibc-2.33 glibc-2.34 -- malloc/malloc.c > glibc-2.34.diff
git -C ~/glibc diff glibc-2.34 glibc-2.35 -- malloc/malloc.c > glibc-2.35.diff
git -C ~/glibc diff glibc-2.35 glibc-2.36 -- malloc/malloc.c > glibc-2.36.diff
git -C ~/glibc diff glibc-2.36 glibc-2.37 -- malloc/malloc.c > glibc-2.37.diff
git -C ~/glibc diff glibc-2.37 glibc-2.38 -- malloc/malloc.c > glibc-2.38.diff
git -C ~/glibc diff glibc-2.38 glibc-2.39 -- malloc/malloc.c > glibc-2.39.diff
git -C ~/glibc diff glibc-2.39 glibc-2.40 -- malloc/malloc.c > glibc-2.40.diff
git -C ~/glibc diff glibc-2.40 glibc-2.41 -- malloc/malloc.c > glibc-2.41.diff
git -C ~/glibc diff glibc-2.41 glibc-2.42 -- malloc/malloc.c > glibc-2.42.diff
git -C ~/glibc diff glibc-2.42 glibc-2.43 -- malloc/malloc.c > glibc-2.43.diff
git -C ~/glibc diff glibc-2.43 glibc-2.44 -- malloc/malloc.c > glibc-2.44.diff

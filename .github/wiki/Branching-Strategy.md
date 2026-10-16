## `main`
Should always be in a stable place with passing CI. `develop` branch will occasionally merge to `main` branch. Never push directly to `main`.

## `develop`
A working space. Can be broken at times, but that's fine. Developers will create branches off of `develop` and make pull requests onto `develop`.

## Strategy
1. Pick an issue
2. Assign the issue to yourself
3. Create a branch from the issue. Make sure you base your branch off of `develop` instead of `main`.
4. Do your work on your branch.
5. When ready, create a PR. Ensure you merge to `develop` instead of `main`.
6. Once merged, delete your branch both locally and on origin (more importantly on origin).

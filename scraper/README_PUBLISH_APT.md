# Publishing the fortune-swahili .deb as an APT repository

This workspace includes a helper script `make_apt_repo.sh` which builds a
minimal static apt repository directory (pool + Packages.gz + Release) that
can be uploaded to any static file host (GitHub Pages, S3, etc.) and then
used as an apt source by clients.

## Steps

1) Build the .deb (already present in the workspace):

   ```bash
   ./build_deb.sh "$(pwd)/../data"
   ```

2) Create the apt repo directory:

   ```bash
   ./make_apt_repo.sh ./fortune-swahili_0.1_all.deb ./apt-repo
   ```

3) Upload the contents of `apt-repo/` to a static web host (e.g., https://example.com/fortune-repo/)

4) On client machines add the apt source (example using a private, trusted host):

   ```bash
   echo "deb [trusted=yes] https://example.com/fortune-repo stable main" | sudo tee /etc/apt/sources.list.d/fortune-swahili.list
   sudo apt update
   sudo apt install fortune-swahili
   ```

## Notes

- The `trusted=yes` option avoids needing to sign the repository; for production
  you should sign the Release file and distribute the GPG key to clients.
- If you prefer not to use `trusted=yes`, follow standard apt repo signing steps
  (apt-ftparchive, gpg --detach-sign, etc.).

## Publishing to GitHub Pages

You can publish the `apt-repo/` directory to GitHub Pages by pushing it to the
`gh-pages` branch of a repository. A helper script `publish_to_github_pages.sh`
is included. Example:

```bash
# set the target GitHub repo and push gh-pages branch
./publish_to_github_pages.sh --repo git@github.com:USERNAME/REPO.git --branch gh-pages --dir ./apt-repo
```

Notes:

- The script requires you to have push access and an SSH key or HTTPS auth
  configured for the repo.
- The script force-pushes the branch (safe for a dedicated `gh-pages` branch).
- After publishing, the apt repository will be available at:
  https://USERNAME.github.io/REPO/   (if using GitHub Pages for the repo root)
Publishing the fortune-swahili .deb as an APT repository

This workspace includes a helper script `make_apt_repo.sh` which builds a
minimal static apt repository directory (pool + Packages.gz + Release) that
can be uploaded to any static file host (GitHub Pages, S3, etc.) and then
used as an apt source by clients.

Steps:

1) Build the .deb (already present in the workspace):

   ./build_deb.sh "$(pwd)/../data"

2) Create the apt repo directory:

   ./make_apt_repo.sh ./fortune-swahili_0.1_all.deb ./apt-repo

3) Upload the contents of `apt-repo/` to a static web host (e.g., https://example.com/fortune-repo/)

4) On client machines add the apt source (example using a private, trusted host):

   echo "deb [trusted=yes] https://example.com/fortune-repo stable main" | sudo tee /etc/apt/sources.list.d/fortune-swahili.list
   sudo apt update
   sudo apt install fortune-swahili

Notes:
- The `trusted=yes` option avoids needing to sign the repository; for production
  you should sign the Release file and distribute the GPG key to clients.
- If you prefer not to use `trusted=yes`, follow standard apt repo signing steps
  (apt-ftparchive, gpg --detach-sign, etc.).

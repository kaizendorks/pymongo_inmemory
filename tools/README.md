# Updating download URLs

Run URL check tool from the root:

```sh
python ./tools/check_urls
```

It will expand the URL tree and check all the URLs by sending `HEAD` requests.

The check is done concurrently, but in order to reduce server-sode throttling, there is a random
sleep between 1 to 4 seconds for each check.

In the end of the check it will report all the URLs that has some problem. Update the patterns
accordingly.

Note that URL checker will not generate new URLs. For instance if there is a new MongoDB version,
it won't be checked.

The URLs are collected from:

- [Releases](https://www.mongodb.com/download-center/community/releases) page
- [Release archive](https://www.mongodb.com/download-center/community/releases/archive) page

The last addition is MongoDB version 8.0.5.

Best way to keep track of the new version is to subscribe to [MongoDB release alerts](https://www.mongodb.com/lp/newsletter/enterprise-release-announcements).

Result of the URL checking should be reflected on the [download patterns](_patterns.py)
and the main [README](../../README.md)

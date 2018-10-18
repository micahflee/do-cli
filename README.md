# DigitalOcean CLI tool

A simple command line tool for listing, creating, and deleting DigitalOcean
droplets.

## Getting started

You need to store a DigitalOcean API key in the `DO_API_KEY` environment
variable, like this:

```
export DO_API_KEY=[your_api_key_here]
```

You can run that line to set the environment variable. But, if you want,
you can also copy that line into your `~/.bashrc` file so it always gets
automatically set. Be careful to protect your API key though. Anyone who
has it can create/delete DigitalOcean VPSes in your account.

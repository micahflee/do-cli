# DigitalOcean CLI tool

A simple command line tool for listing, creating, and deleting DigitalOcean
droplets.

## Getting started

Install `do` with pip3, like:

```sh
pip3 install do-cli
```

You need to store a DigitalOcean API key in the `DO_API_KEY` environment
variable, like this:

```
export DO_API_KEY=[your_api_key_here]
```

You can run that line to set the environment variable. But, if you want,
you can also copy that line into your `~/.bashrc` file so it always gets
automatically set. Be careful to protect your API key though. Anyone who
has it can create/delete DigitalOcean VPSes in your account.

## Usage

First, choose a sub-command, either `list`, `create`, or `delete`:

```
$ do -h
usage: do [-h] {list,create,delete} ...

positional arguments:
  {list,create,delete}
    list                List droplets
    create              Create a new droplet
    delete              Delete a droplet

optional arguments:
  -h, --help            show this help message and exit
```

Listing doesn't require any extra arguments.

Creating requires a name, and you can optionally choose size, image, and
region for the droplet that you'll be creating. Note that `do` will
automatically upload the SSH public key it finds in `~/.ssh/id_rsa.pub`
to your account if it's not already there, and add it to the new droplet
that gets created.

```
$ do create -h
usage: do create [-h] [--size SIZE] [--image IMAGE] [--region REGION] name

positional arguments:
  name             Name of droplet

optional arguments:
  -h, --help       show this help message and exit
  --size SIZE      Size (in RAM) of the droplet (default: 512mb)
  --image IMAGE    Base image of the droplet (default: ubuntu-18-10-x64)
  --region REGION  Region of the droplet (default: sfo2)
```

Deleting requires a droplet id, which you can get by running list. When
deleting a droplet, you *must* include the optional flag `--force` or
else it won't delete it.

```
$ do delete -h
usage: do delete [-h] [--force] id

positional arguments:
  id          Id of droplet

optional arguments:
  -h, --help  show this help message and exit
  --force     Required to actually delete the droplet
```

# Example

My DigitalOcean account doesn't have any droplets yet, so I'll create one:

```
$ do create test1
Added your SSH key, 'user@dev' to DigitalOcean
Droplet    IP address           id    Memory    Disk  Region
---------  ------------  ---------  --------  ------  --------
test1                    115661631       512      20  sfo2
```

Notice that `do` added my SSH key to DigitalOcean. The IP address of the
new droplet isn't shown yet because it was just created, but I can run
list to see it:

```
$ do list
Droplet    IP address              id    Memory    Disk  Region
---------  ---------------  ---------  --------  ------  --------
test1      138.68.12.60     115661631       512      20  sfo2
```

Great, now I'll add a second droplet, but this time in New York instead
of San Francisco, and with 1GB of RAM instead of 512MB.

```
$ do create test2 --size 1gb --region nyc1
Droplet    IP address           id    Memory    Disk  Region
---------  ------------  ---------  --------  ------  --------
test2                    115661894      1024      30  nyc1
```

Now I'm going to look at my list of droplets:

```
$ ./do list
Droplet    IP address              id    Memory    Disk  Region
---------  ---------------  ---------  --------  ------  --------
test1      138.68.12.60     115661631       512      20  sfo2
test2      159.65.229.223   115661894      1024      30  nyc1
```

Now I'm going to delete my test1 droplet:

```
$ do delete test1
The resource you were accessing could not be found.
```

This doesn't work because I was supposed to supply the id of the droplet,
not the name. (This is important because ids are unique and names aren't.
You can have multiple droplets with the same name.) Let's try again, but
this time with the id "115661631".

```
$ do delete 115661631
To delete the following droplet, run again with --force.

Droplet    IP address           id    Memory    Disk  Region
---------  ------------  ---------  --------  ------  --------
test1      138.68.12.60  115661631       512      20  sfo2
```

Almost. To avoid accidentally permanently deleting the wrong droplet, you have to pass `--force` into `do`.

```
$ do delete 115661631 --force
The following droplet has been deleted.

Droplet    IP address           id    Memory    Disk  Region
---------  ------------  ---------  --------  ------  --------
test1      138.68.12.60  115661631       512      20  sfo2
```

It's been deleted. Let's list droplets now.

```
$ ./do list
Droplet    IP address              id    Memory    Disk  Region
---------  ---------------  ---------  --------  ------  --------
test2      159.65.229.223   115661894      1024      30  nyc1
```

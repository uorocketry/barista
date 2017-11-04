# Barista
## Background
Barista is application responsible for flight control of the uOttawa 2019 Rocket.

## Usage
 1. Ensure you have pip and python2.7 installed
 2. use `app.py` to launch the application command line

### Command Line Functions
```
>>> help
```
lists available commands

**NOT IMPLEMENTED YET**
```
>>> run
```
launches the main application thread

```
>>> stop
```
stops main application thread

```
>>> state [state_name]
```
forces main application thread to state

```
>>> update
```
fetches latest master from github

```
>>> compile
```
compiles all DLLs

```
>>> test [test_path]
```
runs all unit tests, optionally runs [test_path]

# Rawnald Newton Gregory

Rawnald Newton Gregory, AKA Random Name Generator, is a tool for generating random names that hopefully provide comedic value.

## Usage

### Setup

Generate the linguistics dictionary you need to generate names:

```
git submodule update --recursive
python3 -m rng compile
```

### Generating Names

Generation requires a source name. The simplest way to generate a name is:

```
python3 -m rng gen Barack Obama
```

Generation takes several parameters. Use the `-h` param to get more info.

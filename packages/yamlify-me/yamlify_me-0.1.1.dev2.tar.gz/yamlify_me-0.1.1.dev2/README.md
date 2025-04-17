# Yamlify

Yamlify is a document generation tool and python library, which combines yaml and
Jinja2.

It includes:

* Read data from multiple files in a folder.
* Read data recursively from subfolders.
* Manipulate data after reading and before rendering.
* Render data with a jinja template file to generate a document.
* Render data with multiple jinja template files to generate multiple documents

## Usage

```bash
> datify --help
```

## I a nutshell

Define data in a file data/cars/00001.yaml:

``` yaml
make: Toyota
model: Corolla
year: 2020
owner: persons/john
```

Define a template file templates/template_multi.j2:

```
{{ make }} {{ model }} {{ year }} {{ filename }}
```

The command ```datify data/cars/ templates/template_multi.j2 -f {make}.txt```
generates the file Toyota.txt:

```txt
Toyota Corolla 2020 00001.yaml
```

If you define more that one data files, multiple output files are generated
accordingly (see tests).

## License

MIT - see LICENSE file

### cQuery

cQuery is a Content Object Model traversal library, built to  solve the issue of quickly searching, finding and filtering content in a file-system.

The Content Object Model (COM) is based on the Document Object Model (DOM) of HTML/Javascript in that each folder in a file-system is the equivalent of a Node in a DOM tree and may be selected and manipulated via similar facilities; namely via the use of CSS selectors - like jQuery (hence the name). For the purposes of this prototypical implementation, you may consider the COM identical in every way to the DOM and cQuery identical in functionality and use to the CSS selector facilities of jQuery (although other jQuery features are in the pipeline too, such as events and modifications to the DOM).

See also

 - [RFC](http://rfc.abstractfactory.io/spec/73/)

### Usage

cQuery works in conjunction with [Open Metadata][]. The process is as follows:

1. One of more directories are tagged with either `class` or `id` entries.
2. cQuery then operates within a hierarchy containing these tags.

cQuery supports three selectors; class, ID and name.
To search for a class, prefix your selector with a dot
(.). To do the equivalent but for an ID, use hash (#).
To search by name, do not include a prefix.

```bash
# To return all matches of class "Asset":
$ cquery .Asset
# c:\studio\content\jobs\spiderman\Ben
# c:\studio\content\jobs\spiderman\HarryOsborn
# c:\studio\content\jobs\spiderman\Norman
# c:\studio\content\jobs\spiderman\Peter

# To return all matches of ID "MyBen":
$ cquery "#MyBen"
# c:\studio\content\jobs\spiderman\Ben

# To return all matches of name "System.custom":
$ cquery System.custom
# c:\studio\content\jobs\spiderman\util\dump
# c:\studio\content\jobs\spiderman\system\crash

# When searching by name, matches are returned via a
# user-defined suffix, as opposed to the built-in class
# and ID (.class and .id respectively). For example, these
# two queries are identical
$ cquery .Female
$ cquery Female.class

# This facilitates the creation of custom selectors. For
# example, let's return all known passwords of the
# user "Marcus":
$ cquery Marcus.password

```

### Architecture

cQuery works upon directories tagged with metadata to indicate its class, ID or name. The tagged directories may then be queried, either from outside a hierarchy looking in or from within a hierarchy looking out in order to find either all matches or best-match.

For tagging, cQuery uses the semantics of Open Metadata; the process is quite simple - for each subdirectory within a directory, recursively look for a file by name stored within the Open Metadata container. If a match is found, return the absolute path to said directory. The name of this file is the "selector" argument of your query.

E.g. cquery .Asset  # Search for the file "Asset.class"

### Performance

cQuery operates on the hard-drive and is a seek-only algorithm and as such doesn't perform any reads. Despite this however, disk-access is the prime bottle-neck. cQuery has been implemented in both Python and Go for performance comparisons, here are some results:

**Python**

```python
# Scanning a hierarchy of 3601 items
# 1 queries, 7 matches in 1.494072 seconds
# 1 queries, 7 matches in 1.480471 seconds
# 1 queries, 7 matches in 1.477589 seconds
#   Average time/query: 1.484044 seconds

# Scanning a hierarchy of 47715 items
# 1 queries, 14 matches in 19.888399 seconds
# 1 queries, 14 matches in 20.078811 seconds
# 1 queries, 14 matches in 19.879660 seconds
#   Average time/query: 19.948957 seconds

```

**Go**

```python
# Scanning a hierarchy of 3601 items
# 1 queries, 7 matches in 1.425702 seconds
# 1 queries, 7 matches in 1.420373 seconds
# 1 queries, 7 matches in 1.419541 seconds
#   Average time/query: 1.421872 seconds

# Scanning a hierarchy of 47715 items
# 1 queries, 14 matches in 18.015012 seconds
# 1 queries, 14 matches in 17.951607 seconds
# 1 queries, 14 matches in 17.994924 seconds
#   Average time/query: 17.987181 seconds
```

As you can see, the differences are marginal and of little concern. A benefit of Go however is the standalone executables it produces which may prove useful in certain circumstances.

Benchmarks can be found under /benchmark


[Open Metadata]: https://github.com/abstractfactory/openmetadata
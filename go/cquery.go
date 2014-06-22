// cQuery - Content Object Model traversal with Open Metadata
//
// cQuery supports three selectors; class, ID and name.
// To search for a class, prefix your selector with a dot
// (.). To to the equivalent but for an ID, use hash (#).
// To search by name, simply do not prefix with anything.
//
// When searching by name, matches are returned via a
// user-defined suffix, as opposed to the built-in class
// and ID (.class and .id respectively).
//
// For example, these two queries are identical
// $ cquery .Female
// $ cquery Female.class
//
// Usage:
//  To return all matches of class "Asset":
// 		$ cquery .Asset
//
//  To return all matches of ID "MyFolder":
// 		$ cquery #MyFolder
//
//  To return all matches of name "SomeFolder":
// 		$ cquery MyProperty.string
//

package main

import "os"
import "fmt"
import "strings"
import "flag"
import "path/filepath"

func walk(root string,
		  selector string,
		  direction string,
		  verbose bool) {

	// Recursively walk through `root` in search for `selector`
	var scan = func(root string, info os.FileInfo, err error) error {
		if err != nil {
			if verbose == true {
				fmt.Println(err)
			}
			return nil
		}

		if !info.IsDir() {
			return nil
		}

		// Skip hidden folders
		if strings.HasPrefix(info.Name(), ".") {
			return filepath.SkipDir
		}

		// Look for `selector` within `root`
		var filename string = filepath.Join(root, selector)
		if _, err := os.Stat(filename); err == nil {
			os.Stdout.Write([]byte(root + "\n"))
		}

		return nil
	}

	filepath.Walk(root, scan)
}

func main() {
	CONTAINER := ".meta"
	root, _ := os.Getwd()

	// Parse arguments
	selectorPtr := flag.String("selector", "", "Selector")
	rootPtr := flag.String("root", "", "Absolute root from which to start looking (defaults to working directory)")
	directionPtr := flag.String("direction", "down", "Query below or above hierarchy")
	verbosePtr := flag.Bool("verbose", false, "Include debug information?")

	flag.Parse()

	selector := flag.Arg(0)
	if *selectorPtr != "" {
		selector = *selectorPtr
	}
	if *rootPtr != "" {
		root = *rootPtr
	}

	// Append Open Metadata container to selector.
	// This is where metadata of this sort is stored.
	if strings.HasPrefix(selector, ".") {
		selector = filepath.Join(CONTAINER, selector[1:]+".class")
	} else if strings.HasPrefix(selector, "#") {
		selector = filepath.Join(CONTAINER, selector[1:]+".id")
	} else {
		selector = filepath.Join(CONTAINER, selector)
	}

	// Commence query
	walk(root, selector, *directionPtr, *verbosePtr)
}

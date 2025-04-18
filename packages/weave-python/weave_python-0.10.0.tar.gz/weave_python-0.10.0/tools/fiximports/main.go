package main

import (
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"regexp"
)

// Regular expressions for replacing import statements
var (
	importRegex   = regexp.MustCompile(`from datamanagement`)
	dbImportRegex = regexp.MustCompile(`from db import models`)
)

func main() {
	// Parse command line arguments
	var directory string
	flag.StringVar(&directory, "directory", "weave/gen", "Directory containing generated files to fix")
	flag.Parse()

	// If a positional argument is provided, use it as the directory
	if flag.NArg() > 0 {
		directory = flag.Arg(0)
	}

	fmt.Printf("Fixing imports in %s\n", directory)

	// Walk through all Python files in the directory
	err := filepath.Walk(directory, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}

		// Skip directories
		if info.IsDir() {
			return nil
		}

		// Only process Python files
		if filepath.Ext(path) != ".py" {
			return nil
		}

		return fixFileImports(path)
	})

	if err != nil {
		fmt.Printf("Error walking directory: %v\n", err)
		os.Exit(1)
	}

	fmt.Println("Import fixing completed")
}

// fixFileImports fixes imports in a single file
func fixFileImports(filePath string) error {
	// Read file content
	content, err := os.ReadFile(filePath)
	if err != nil {
		return fmt.Errorf("error reading file %s: %v", filePath, err)
	}

	// Convert to string for regex operations
	contentStr := string(content)

	// Fix import statements
	// Pattern: from datamanagement... import ...
	modifiedContent := importRegex.ReplaceAllString(contentStr, "from weave.gen.datamanagement")

	// Fix BuildTopDescriptorsAndMessages calls
	// Pattern: _builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'datamanagement...', _globals)
	modifiedContent = dbImportRegex.ReplaceAllString(modifiedContent, "from weave.gen.datamanagement.db import models")

	// Only write back if changes were made
	if contentStr != modifiedContent {
		fmt.Printf("Fixing imports in %s\n", filePath)
		err = os.WriteFile(filePath, []byte(modifiedContent), 0644)
		if err != nil {
			return fmt.Errorf("error writing file %s: %v", filePath, err)
		}
	}

	return nil
}

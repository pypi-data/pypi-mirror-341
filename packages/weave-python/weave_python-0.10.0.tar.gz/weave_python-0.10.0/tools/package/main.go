package main

import (
	"flag"
	"fmt"
	"os"
	"path/filepath"
)

const (
	initFileName = "__init__.py"
)

func main() {
	var targetDir string
	flag.StringVar(&targetDir, "target-dir", "", "Target directory for the generated Python package")
	flag.Parse()

	if targetDir == "" {
		flag.Usage()
		return
	}

	if err := os.MkdirAll(targetDir, 0o755); err != nil {
		fmt.Printf("Error creating directory %s: %v\n", targetDir, err)
		os.Exit(1)
	}

	if err := createInitFiles(targetDir); err != nil {
		fmt.Printf("Error creating init files: %v\n", err)
		os.Exit(1)
	}

	fmt.Println("successfully packaged Python dependencies")
}

// createInitFiles recursively checks directories and creates __init__.py files where needed
func createInitFiles(rootDir string) error {
	return filepath.Walk(rootDir, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}

		if !info.IsDir() {
			return nil
		}

		initPath := filepath.Join(path, initFileName)
		if _, err := os.Stat(initPath); !os.IsNotExist(err) {
			return nil
		}

		file, err := os.Create(initPath)
		if err != nil {
			return err
		}
		defer file.Close()

		return nil
	})
}

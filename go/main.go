package main

import (
	"bufio"
	"encoding/csv"
	"fmt"
	"os"
	"strings"
	"time"
)

func main() {
	reader := bufio.NewReader(os.Stdin)

	// Get input and output file paths from user
	inputFile := getInput(reader, "Enter input CSV file path (default: input.csv): ", "input.csv")
	outputFile := getInput(reader, "Enter output CSV file path (default: output.csv): ", "output.csv")

	// Get delimiter choice
	delimiter := getInput(reader, "Choose delimiter - Comma (C) or Tab (T) [default: Comma]: ", "C")
	csvDelimiter := ','
	if strings.ToUpper(strings.TrimSpace(delimiter)) == "T" {
		csvDelimiter = '\t'
	}

	// Get interval choice
	intervalChoice := getInput(reader, "Choose time interval - Hourly (H) or Minutes (M) [default: Hourly]: ", "H")
	var interval int
	if strings.ToUpper(strings.TrimSpace(intervalChoice)) == "H" {
		interval = 60
	} else {
		intervalStr := getInput(reader, "Enter the number of minutes for interval: ", "60")
		fmt.Sscanf(intervalStr, "%d", &interval)
	}

	// Get first or last entry choice
	firstOrLast := getInput(reader, "Choose First (F) or Last (L) entry for each interval [default: First]: ", "F")

	// Process CSV
	processCSV(inputFile, outputFile, csvDelimiter, interval, firstOrLast)
}

func getInput(reader *bufio.Reader, prompt, defaultValue string) string {
	fmt.Print(prompt)
	input, _ := reader.ReadString('\n')
	input = strings.TrimSpace(input)
	if input == "" {
		return defaultValue
	}
	return input
}

func processCSV(inputFile, outputFile string, delimiter rune, interval int, firstOrLast string) {
	file, err := os.Open(inputFile)
	if err != nil {
		panic(err)
	}
	defer file.Close()

	reader := csv.NewReader(file)
	reader.Comma = delimiter

	records, err := reader.ReadAll()
	if err != nil {
		panic(err)
	}

	processedRecords := make(map[string][]string)
	for _, record := range records {
		if len(record) < 3 {
			continue // Skip if record does not have enough fields
		}
		datetimeStr := record[1] + " " + record[2]
		datetime, err := time.Parse("2006-01-02 15:04:05", datetimeStr)
		if err != nil {
			fmt.Printf("Skipping record with invalid date: %s\n", datetimeStr)
			continue
		}

		roundedDatetime := roundDownTime(datetime, interval)
		key := roundedDatetime.Format("2006-01-02 15:04:05")

		if _, exists := processedRecords[key]; !exists || strings.ToUpper(firstOrLast) == "L" {
			processedRecords[key] = record
		}
	}

	writeCSV(outputFile, processedRecords)
}

func roundDownTime(t time.Time, interval int) time.Time {
	if interval == 60 {
		return t.Truncate(time.Hour)
	}
	return t.Truncate(time.Duration(interval) * time.Minute)
}

func writeCSV(outputFile string, records map[string][]string) {
	file, err := os.Create(outputFile)
	if err != nil {
		panic(err)
	}
	defer file.Close()

	writer := csv.NewWriter(file)
	for _, record := range records {
		if err := writer.Write(record); err != nil {
			panic(err)
		}
	}
	writer.Flush()
}